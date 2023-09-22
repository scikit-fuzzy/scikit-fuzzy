# -*- coding: utf-8 -*-
'''
    Top-down recursive descent parser for the Fuzzy Control Language (FCL).
    This is a bare-bones parser that just collects things as it goes through,
    building lists of variables and rules (which are skfuzzy objects).

    I'm working from the draft IEC 61131-7 standard, but I have widened
    the grammar slightly in places, as usage seems to be more liberal.
    In particular, in blocks (variables, rules) I'm not fussy about
    the order of decls where it doesn't matter.  Also, I've made the
    terminating semi-colon optional in most places (again reflecting usage).

    References: https://en.wikipedia.org/wiki/Fuzzy_Control_Language

    @author: james.power@mu.ie, Created on Tue Aug 14 09:58:10 2018
'''

import os
import sys
import codecs

import numpy as np

import skfuzzy.control as ctrl
import skfuzzy.control.term as fuzzterm

from .fcl_scanner import BufferedFCLLexer
from .fcl_symbols import NameMapper, SymbolTable

# A universe is given this no. of points unless specified:
_DEFAULT_UNIVERSE_SIZE = 1000


class ParsingError(Exception):
    '''The parser raises this to flag an error while parsing an FCL file.'''
    def __init__(self, pos, error_kind, msg):
        Exception.__init__(self, '{} {}: {}'.format(pos, error_kind, msg))
        self.pos = pos    # filename[line,col]
        self.error_kind = error_kind  # e.g. 'lexical error', 'syntax error'


class FCLParser(NameMapper, SymbolTable):
    '''
    A top-down parser for the Fuzzy Control Language (FCL).
    The main entry point is to call fcl_file() with a filename,
    or you can call any non-terminal with a string.

    The relationship with NameMapper and SymbolTable should
    really be "has-a" rather than "is-a", but it's simpler this way.
    '''

    def __init__(self, vars=None):
        '''
        Set up parser by initialising symbol table and lexer
        Optionally supply an initial list of variables (or add them later)
        '''
        NameMapper.__init__(self)
        self.load_ieee_names()
        self.load_fcl_names_too()
        self.load_jfl_names()
        SymbolTable.__init__(self, vars)
        self.lex = BufferedFCLLexer(self._report_error)

    def _report_error(self, msg, error_kind='syntax error', pos=None):
        '''
        Raise an error; report the current position if no pos is given.
        All error kinds (lexical, syntax, scope) go through this method.
        '''
        if not pos:  # No user-supplied position, get it from lexer:
            tok = self.lex.token()
            pos = self.lex.get_pos(tok)
            got = tok.value if tok else '[EOF]'
            msg += ' while reading token "{}"'.format(got)
        raise ParsingError(pos, error_kind, msg)

    def _calc_universe(self, start, stop, step=None):
        '''
        Return an np array corresponding to the given RANGE bounds.
        Optionally specify the step, otherwise we guess.
        '''
        if start >= stop:
            self._report_error('invalid range bounds ({}, {})'
                               .format(start, stop))
        if not step:  # Guess some "reasonable" step:
            urange = 1 + (stop - start)
            scale_by = urange / _DEFAULT_UNIVERSE_SIZE
            step = np.power(10, np.round(np.log10(scale_by), 0))
        universe = np.arange(start, stop, step)
        return universe

    def _make_mf(self, universe, mfunc, params):
        '''
        Given a function name and parameters, make a membership function.
        '''
        assert len(universe) > 0,\
            'No current universe has been set for this mf'
        skfunc, split_params = self.translate_mf(mfunc)
        if split_params:
            return skfunc(universe, *params)
        else:  # Takes parameters as an array
            return skfunc(universe, params)

    def _finalise_ante_var(self, universe, varname):
        '''
        Have just finished an input var definition, so add it to the list.
        '''
        fuzzyvar = ctrl.Antecedent(universe, varname)
        self.add_vars([fuzzyvar])
        return fuzzyvar

    def _finalise_cons_var(self, universe, varname, options):
        '''
        Have just finished an output var definition, so add it to the list.
        Make sure any declared options (e.g. defuzz method) are registered.
        Default values are ignored at the moment.
        '''
        fuzzyvar = ctrl.Consequent(universe, varname)
        for key, val in options.items():
            key = key.upper()
            if key == 'METHOD':
                fuzzyvar.defuzzify_method = self.translate_defuzz(val)
            elif key == 'ACCU':
                fuzzyvar.accumulation_method = self.translate_accu(val)
            elif key == 'DEFAULT':
                pass
        self.add_vars([fuzzyvar])
        return fuzzyvar

    def _finalise_terms(self, fuzzyvar, termlist):
        '''
        Have just finished a var definition, collected terms and a universe.
        Propagate universe values to any terms declared before the universe.
        That is, make sure all term definitions are skfuzzy Term objects.
        '''
        universe = fuzzyvar.universe
        for term in termlist:
            if not isinstance(term, fuzzterm.Term):
                # Myst have seen this TERM definition before we saw the RANGE
                (term_name, fname, params) = term
                mf_def = self._make_mf(universe, fname, params)
                term = fuzzterm.Term(term_name, mf_def)
            self.add_term_to_var(fuzzyvar, term)

    def _add_hedges(self, fvar, hedges, orig_term):
        '''
        Apply one or more hedge functions to the given (term) member function.
        Create a new mf for the result, and add it as a term to the variable.
        Return the Term object corresponding to this new membership function.
        '''
        if len(hedges) == 0:
            return orig_term
        mf_name = '{}__{}'.format('_'.join(hedges), orig_term.label)
        if mf_name in fvar.terms:  # Already done it (some previous rule)
            return fvar[mf_name]
        mf_vals = orig_term.mf
        # Now apply each hedge in turn, starting at the last one:
        for hedge_name in hedges[::-1]:
            hedge_func = self.translate_hedge(hedge_name)
            mf_vals = hedge_func(mf_vals)
        # All the hedges processed, so add this as a new mf to the variable:
        new_term = fuzzterm.Term(mf_name, mf_vals)
        self.add_term_to_var(fvar, new_term)
        return new_term

    def _finalise_rules(self, rbname, rulelist, options):
        '''
        Prefix the rule labels by the ruleblock name (if any).
        Propagate any ruleblock AND/OR option-values to individual rules.
        Ignoring any ACCU option here, since skfuzzy does this at the
        variable level and could have same variable in different rule-blocks.
        '''
        and_key = options.get('AND', None)
        or_key = options.get('OR', None)
        fam = self.translate_and_or(and_key, or_key)
        for rule in rulelist:
            if rbname:
                self.set_rule_label(rule, '{}.{}'.format(rbname, rule.label))
            rule.and_func = fam.and_func
            rule.or_func = fam.or_func
        return rulelist

    def read_fcl_file(self, filename):
        '''
        Read the given FCL file and parse it.
        Returns the parser object (on success), to facilitate create-and-call.
        '''
        self.lex.reset_lineno(filename)
        self.flag_error_on_redefine()
        with codecs.open(filename, 'r',
                         encoding='utf-8', errors='ignore') as fileh:
            try:
                self.lex.input(fileh.read())
                self.function_block()
                return self
            except ParsingError as parsing_error:
                raise parsing_error
            except Exception as other_error:
                # Show all errors as parser errors so we get line,col ref:
                self._report_error(str(other_error), 'internal error')

    # ########################################## #
    # ### FCL grammar definition starts here ### #
    # ########################################## #

    # All of these parsing routines correspond to a grammar non-terminal,
    # all can be called with a string (and will parse that string)
    # and (nearly) all return an corresponding skfuzzy object.

    # ################################# #
    # 1. Overall FCL program structure: #
    # ################################# #

    def function_block(self, input_string=None):
        '''
        This is the grammar's start symbol; parse an entire function block.
        Returns:
        --------
            Nothing.  Get any results (vars, rules) from the symbol table.
        Grammar Rule:
        -------------
            function_block_declaration ::=
                'FUNCTION_BLOCK' function_block_name
                    {fb_io_var_declarations}
                    {fuzzify_block}
                    {defuzzify_block}
                    {rule_block}
                    {option_block}
                'END_FUNCTION_BLOCK'
        Notes:
        ------
            Actually, I take these contents in any order.
        '''
        self.lex.maybe_set_input(input_string)
        self.lex.recognise('FUNCTION_BLOCK')
        self.fb_name = self.lex.recognise_if_there('IDENTIFIER')
        while self.lex.peek_not(['END_FUNCTION_BLOCK']):
            if self.lex.peek_some(['VAR_INPUT', 'VAR_OUTPUT']):
                self.var_decls()
            elif self.lex.peek('FUZZIFY'):
                self.fuzzify_block()
            elif self.lex.peek('DEFUZZIFY'):
                self.defuzzify_block()
            elif self.lex.peek('RULEBLOCK'):
                self.rule_block()
            elif self.lex.peek('OPTION'):
                self.option_block()
            else:
                self._report_error('Unknown element in function block')
        self.lex.recognise('END_FUNCTION_BLOCK')
        return None

    def var_decls(self, input_string=None):
        '''
        Process a list of variable name-type declarations (not definitions).
        Returns:
        --------
            A list of variable (name,type) pairs
        Grammar Rule:
        -------------
            fb_io_var_declarations ::=
                  'VAR_INPUT' {IDENTIFIER ':' IDENTIFIER ';'} 'END_VAR'
                | 'VAR_OUTPUT' {IDENTIFIER ':' IDENTIFIER ';'} 'END_VAR'
        '''
        self.lex.maybe_set_input(input_string)
        self.lex.recognise_some(['VAR_INPUT', 'VAR_OUTPUT'])
        decls = []
        while self.lex.peek_not(['END_VAR']):
            vname = self.lex.recognise('IDENTIFIER')
            self.lex.recognise('COLON')
            vtype = self.lex.recognise('IDENTIFIER')
            self.lex.recognise_if_there('SEMICOLON')
            decls.append((vname, vtype))
        self.lex.recognise('END_VAR')
        return decls

    def option_block(self, input_string=None):
        '''
        Process (and throw away) a list of option declarations.
        Returns:
        --------
            Nothing.
        Grammar Rule:
        -------------
            option_block ::= 'OPTION' any-old-stuff 'END_OPTION'
        '''
        self.lex.maybe_set_input(input_string)
        self.lex.recognise('OPTION')
        while self.lex.peek_not(['END_OPTION']):
            self.lex.recognise_anything()  # Chuck away any contents...
        self.lex.recognise('END_OPTION')
        return None  # Just for emphasis

    # ################### #
    # 2. Fuzzy variables: #
    # ################### #

    def _option_def(self, keyword):
        '''
        A single option in variable or rule-block definitions.
        Returns:
        --------
            A single key:value pair for this option.
        Grammar Rule:
        -------------
            an_option ::= keyword ':' IDENTIFIER ';'
        '''
        key = self.lex.recognise(keyword)
        self.lex.recognise('COLON')
        value = self.lex.recognise('IDENTIFIER')
        self.lex.recognise_if_there('SEMICOLON')
        return {key: value}

    def fuzzify_block(self, input_string=None):
        '''
        Parse an input ('fuzzify') variable definition.
        Returns:
        --------
            An skfuzzy Antecedent (variable) object.
        Grammar Rule:
        -------------
            fuzzify_block ::=
                'FUZZIFY' variable_name
                    {linguistic_term}
                    [range]
                'END_FUZZIFY'
        Notes:
        ------
            The range can occur at beginning or end (or anywhere in between).
            Don't add the terms until you have the range.
        '''
        self.lex.maybe_set_input(input_string)
        self.lex.recognise('FUZZIFY')
        varname = self.lex.recognise('IDENTIFIER')
        termlist = []
        universe = ()
        while self.lex.peek_not(['END_FUZZIFY']):
            if self.lex.peek('TERM'):
                termlist.append(self.term_def())
            elif self.lex.peek('RANGE'):
                universe = self.range_def()
            else:
                self._report_error('Unknown element in fuzzify block')
        self.lex.recognise('END_FUZZIFY')
        if len(universe) == 0:
            self._report_error('No universe for variable "{}"'
                               .format(varname), 'range error')
        fuzzyvar = self._finalise_ante_var(universe, varname)
        self._finalise_terms(fuzzyvar, termlist)
        return fuzzyvar

    def defuzzify_block(self, input_string=None):
        '''
        Parse an output ('defuzzify') variable definition.
        Returns:
        --------
            An skfuzzy Consequent (variable) object.
        Grammar Rule:
        -------------
            defuzzify_block ::=
                'DEFUZZIFY' variable_name
                    {linguistic_term}
                    'ACCU' ':' accumulation_method ';'
                    'METHOD' ':' defuzzification_method ';'
                    default_value
                    [range]
                'END_FUZZIFY'
            defuzzification_method ::= IDENTIFIER
            accumulation_method ::= IDENTIFIER
            default_value ::= 'DEFAULT' ':=' numeric_literal | 'NC' ';'
        Notes:
        ------
            I'm not fussy about the order of the block contents, and I accept
            any identifier as a defuzz/accu method, and worry about it later.
        '''
        self.lex.maybe_set_input(input_string)
        self.lex.recognise('DEFUZZIFY')
        varname = self.lex.recognise('IDENTIFIER')
        options = {}
        termlist = []
        universe = ()
        while self.lex.peek_not(['END_DEFUZZIFY']):
            toktype = self.lex.peek_type()

            if toktype == 'TERM':
                termlist.append(self.term_def())
            elif toktype == 'RANGE':
                universe = self.range_def()
            elif toktype in ['METHOD', 'ACCU']:
                options.update(self._option_def(toktype))
            elif self.lex.recognise_if_there('DEFAULT'):
                self.lex.recognise_some(['ASSIGN', 'COLON'])
                if self.lex.recognise_if_there('NC'):
                    default_val = 'NC'
                if self.lex.recognise_if_there('NAN'):
                    default_val = 'NAN'
                else:
                    default_val = self.number()
                self.lex.recognise_if_there('SEMICOLON')
                options['DEFAULT'] = default_val
            else:
                self._report_error('Unknown element in defuzzify block')
        self.lex.recognise('END_DEFUZZIFY')
        if len(universe) == 0:
            self._report_error('No universe for variable "{}"'
                               .format(varname), 'range error')
        fuzzyvar = self._finalise_cons_var(universe, varname, options)
        self._finalise_terms(fuzzyvar, termlist)
        return fuzzyvar

    def range_def(self, input_string=None):
        '''
        Parse a RANGE (universe) definition for a variable.
        Returns:
        --------
            A NumPy array that corresponds to the universe.
        Grammar Rule:
        -------------
            range ::= 'RANGE ':=' '(' numeric_literal '..' numeric_literal ')'
                      [WITH numeric_literal]
                      ';'
        Notes:
        ------
            I've extended the grammar here to allow a 'step' to be specified.
            - I reused the 'WITH' keyword for this.
        '''
        self.lex.maybe_set_input(input_string)
        self.lex.recognise('RANGE')
        self.lex.recognise('ASSIGN')
        self.lex.recognise('LPAREN')
        rmin = self.number()  # originally ident_or_number()
        self.lex.recognise('DOTDOT')
        rmax = self.number()
        self.lex.recognise('RPAREN')
        numpoints = None
        if self.lex.recognise_if_there('WITH'):
            numpoints = self.number()
        self.lex.recognise_if_there('SEMICOLON')
        return self._calc_universe(rmin, rmax, numpoints)

    # ###################################### #
    # 3. Fuzzy terms (membership functions): #
    # ###################################### #

    def term_def(self, input_string=None):
        '''
        Parse the definition of a term.
        Returns:
        --------
            A Term object.
        Grammar Rule:
        -------------
            linguistic_term ::= term_header membership_function ';'
        '''
        self.lex.maybe_set_input(input_string)
        name = self.term_header()
        body = self.mf()
        self.lex.recognise_if_there('SEMICOLON')
        if body[0] == 'MF':  # No universe defined yet
            body[0] = name
            return body
        else:  # Have a universe so make a term:
            return fuzzterm.Term(name, body)

    def term_header(self, input_string=None):
        '''
        Returns:
        --------
            The name of the term.
        Grammar Rule:
        -------------
            term_header ::= 'TERM' term_name ':='
        '''
        self.lex.maybe_set_input(input_string)
        self.lex.recognise('TERM')
        name = self.lex.recognise('IDENTIFIER')
        self.lex.recognise('ASSIGN')
        return str(name)

    def mf(self, input_string=None, universe=[]):
        '''
        Parse a definition of a member function.
        Returns:
        --------
            Either a mf (list of y-values) if we've seen a universe,
            else a triple: (mf-kind, mf-name, mf-parameters).
        Grammar Rule:
        -------------
            membership_function ::= singleton | points | funcall
            singleton ::= numeric_literal
            funcall ::= 'IDENTIFIER' {'IDENTIFIER'}
        '''
        self.lex.maybe_set_input(input_string)
        if self.lex.peek('LPAREN'):
            fname, params = 'pointlist', self.point_list()
        elif self.lex.peek('IDENTIFIER'):
            fname = self.lex.recognise('IDENTIFIER')
            # Possible list of parameter values now follows:
            params = []
            while self.lex.peek_some(['INT_CONST', 'FLOAT_CONST']):
                params.append(self.number())
        else:  # Must be a singleton value
            fname, params = 'singleton', [self.number()]
        # Make a term if we have a universe:
        if len(universe) > 0:
            mf_def = self._make_mf(universe, fname, params)
        else:  # No universe defined yet, return items for the moment:
            mf_def = ['MF', fname, params]
        return mf_def

    def point_list(self, input_string=None):
        '''
        Parse a mf definition that's just a list of points.
        Returns:
        --------
            A list of (x,y) points.
        Grammar Rule:
        -------------
            points ::= {'(' numeric_literal ',' numeric_literal ')'}
        Notes:
        ------
            The original allowed an ident for first point; not sure why.
        '''
        self.lex.maybe_set_input(input_string)
        plist = []
        while self.lex.recognise_if_there('LPAREN'):
            x_val = self.number()
            self.lex.recognise('COMMA')
            y_val = self.number()
            self.lex.recognise('RPAREN')
            plist.append((x_val, y_val))
        return plist

    # ####################### #
    # ### 4. Fuzzy rules: ### #
    # ####################### #

    def rule_block(self, input_string=None):
        '''
        Parse a single rule block (rules plus options, maybe named).
        Returns:
        --------
            A list of Rule objects.
        Grammar Rule:
        -------------
            rule_block ::=
                'RULEBLOCK' [rule_block_name]
                    'AND'  ':' operator_definition ';'
                    'OR'   ':' operator_definition ';'
                    'ACT'  ':' activation_method ';'
                    'ACCU' ':' accumulation_method ';'
                    {rule}
                'END_RULEBLOCK'
            operator_definition ::= IDENTIFER
            activation_method ::= IDENTIFER
            accumulation_method ::= IDENTIFER
        Notes:
        ------
            I'm not fussy about the order of the block contents,
            and I've made its name optional.
        '''
        self.lex.maybe_set_input(input_string)
        self.lex.recognise('RULEBLOCK')
        rbname = self.lex.recognise_if_there('IDENTIFIER')
        rules = []
        options = {}
        while self.lex.peek_not(['END_RULEBLOCK']):
            toktype = self.lex.peek_type()
            if toktype == 'RULE':
                rules.append(self.rule_def())
            elif toktype in ['AND', 'OR', 'ACT', 'ACCU']:
                options.update(self._option_def(toktype))
            else:
                self._report_error('Unknown element in rule block')
        self.lex.recognise('END_RULEBLOCK')
        return self._finalise_rules(rbname, rules, options)

    def rule_def(self, input_string=None):
        '''
        Parse a rule definition (i.e. rule name and IF-THEN rule-body).
        Returns:
        --------
            A Rule object.
        Grammar Rule:
        -------------
            rule ::= rule_header rule 'SEMICOLON'
        '''
        self.lex.maybe_set_input(input_string)
        name = self.rule_header()
        body = self.rule()
        self.lex.recognise_if_there('SEMICOLON')
        self.set_rule_label(body, name)
        return body

    def rule_header(self, input_string=None):
        '''
        Returns:
        --------
            The name of the rule as a string (even if it was a number).
        Grammar Rule:
        -------------
            rule_header ::= 'RULE' integer_literal ':'
        Notes:
        ------
            I allow an identifier (or a number) as a rule name.
        '''
        self.lex.maybe_set_input(input_string)
        self.lex.recognise('RULE')
        name = self.ident_or_number()
        self.lex.recognise('COLON')
        return str(name)

    def rule(self, input_string=None):
        '''
        Parse an IF-THEN rule (with optional weighting).
        Returns:
        --------
            A Rule object.  All its Conseqeuents will be weighted if specified.
        Grammar Rule:
        -------------
            rule ::= 'IF' antecedent 'THEN' consequent [WITH weighting_factor]
            weighting_factor ::= variable | numeric_literal
        '''
        self.lex.maybe_set_input(input_string)
        self.lex.recognise('IF')
        ant = self.antecedent()
        self.lex.recognise('THEN')
        con = self.consequent()
        # Recognise a weighting_factor if there is one:
        if self.lex.recognise_if_there('WITH'):
            weight = self.ident_or_number()
            con = [fuzzterm.WeightedTerm(c, weight) for c in con]
        return self.add_rule(ctrl.Rule(ant, con))

    def antecedent(self, input_string=None):
        '''
        One or more antecedecents (possibly) OR-ed together.
        Returns:
        --------
            A Term or TermAggregate object.
        Grammar Rule:
        -------------
            condition ::= clause {('AND' | 'OR') clause}
        Notes:
        ------
            I need to do enforce precedence, so this is actually:
                condition ::= _condition_and {'OR' _condition_and}
        '''
        self.lex.maybe_set_input(input_string)
        left = self._antecedent_and()
        while self.lex.recognise_if_there('OR'):
            right = self._antecedent_and()
            left = fuzzterm.TermAggregate(left, right, 'or')
        return left

    def _antecedent_and(self):
        '''
        One or more antecedecents (possibly) AND-ed together.
        Returns:
        --------
            A Term or TermAggregate object.
        Grammar Rule:
        -------------
            condition_and ::= clause {('COMMA' | 'AND') clause}
        Notes:
        ------
            Assuming 'COMMA' is just another way of saying 'AND'
        '''
        left = self.clause(parent_rule=self.antecedent)
        while self.lex.peek_some(['COMMA', 'AND']):
            self.lex.recognise_some(['COMMA', 'AND'])
            right = self.clause(parent_rule=self.antecedent)
            left = fuzzterm.TermAggregate(left, right, 'and')
        return left

    def consequent(self, input_string=None):
        '''
        One or more consequents (possibly) AND-ed together.
        Returns:
        --------
            Return a list of Term objects.
        Grammar Rule:
        -------------
            condition ::= clause {'AND' clause}
        '''
        self.lex.maybe_set_input(input_string)
        clist = [self.clause(parent_rule=self.consequent)]
        while self.lex.peek_some(['COMMA', 'AND']):
            self.lex.recognise_some(['COMMA', 'AND'])
            clist.append(self.clause(parent_rule=self.consequent))
        return clist

    def clause(self, input_string=None, parent_rule=None):
        '''
        Parse a variable reference in a rule, maybe with negation.
        Returns:
        --------
            A Term object
        Grammar Rule:
        -------------
            clause ::=
                | 'NOT' condition()
                | '(' condition() ')'   # Allow extra parentheses
                | atomic_clause
        Notes:
        ------
            The syntax has been loosened to permit more flexible expressions;
            These are the same: 'NOT v IS t', 'v IS NOT t', 'NOT(v IS t')
        '''
        # Note that the parent (caller) might be antecedent or consequent
        # We pass it as a parameter so we can call it for sub-clauses.
        self.lex.maybe_set_input(input_string)
        if self.lex.recognise_if_there('NOT'):
            subclause = self.clause(parent_rule=parent_rule)
            return fuzzterm.TermAggregate(subclause, None, 'not')
        elif self.lex.recognise_if_there('LPAREN'):
            subclause = parent_rule() if parent_rule else self.clause()
            self.lex.recognise('RPAREN')
            return subclause
        else:
            in_consequent = (parent_rule == self.consequent)
            return self.atomic_clause(in_consequent=in_consequent)

    def atomic_clause(self, input_string=None, in_consequent=False):
        '''
        An in-rule reference to a single variable's term, possibly hedged.
        Returns:
        --------
            A Term object
        Grammar Rule:
        -------------
            atomic_clause ::=
                | variable_name   # Not doing this!
                | variable_name 'IS' {hedge} term_name
        Notes:
        ------
            The optional hedges are: any identifier or 'NOT'.
        '''
        varname = self.lex.recognise('IDENTIFIER')
        hedges = []
        self.lex.recognise('IS')
        while self.lex.peek_some(['IDENTIFIER', 'NOT']):
            hedges.append(self.lex.recognise_some(['IDENTIFIER', 'NOT']))
        # Actually, the last one was the member function name:
        membfun = hedges.pop()
        fvar = self.get_var_defn(varname)
        this_clause = fvar[membfun]
        # Special case when the only hedge is 'not':
        if len(hedges) == 1 and hedges[0] == 'NOT':
            this_clause = fuzzterm.TermAggregate(this_clause, None, 'not')
        # Otherwise apply the hedge functions, if there are any:
        elif len(hedges) > 0:
            this_clause = self._add_hedges(fvar, hedges, this_clause)
        return this_clause

    def ident_or_number(self, input_string=None):
        '''
        Parse an identifier or a numeric constant.
        Returns:
        --------
            An int, float or string.
        Grammar Rule:
        -------------
            ident_or_number ::= identifier | integer_literal | real_literal
        '''
        self.lex.maybe_set_input(input_string)
        if self.lex.peek('IDENTIFIER'):
            return self.lex.recognise('IDENTIFIER')
        if self.lex.peek('INT_CONST'):
            return int(self.lex.recognise('INT_CONST'))
        if self.lex.peek('FLOAT_CONST'):
            return float(self.lex.recognise('FLOAT_CONST'))
        self._report_error('expected ident/num')

    def number(self, input_string=None):
        '''
        Parse an intefer or float ('REAL') constant.
        Returns:
        --------
            An int or float.
        Grammar Rule:
        -------------
            numeric_literal ::= integer_literal | real_literal
        '''
        self.lex.maybe_set_input(input_string)
        if self.lex.peek('INT_CONST'):
            return int(self.lex.recognise('INT_CONST'))
        if self.lex.peek('FLOAT_CONST'):
            return float(self.lex.recognise('FLOAT_CONST'))
        self._report_error('expected numeric literal')

    # ######################################### #
    # ### FCL grammar definition ends here ### #
    # ######################################### #


_FCL_SUFFIX = '.fcl'


def parse_dir(parser, rootdir, want_output=False):
    '''
    Scan all the .fcl files in rootdir and its subdirs.
    Print any errors and the number of files parsed.
    '''
    files_tot, files_err = 0, 0
    for rootpath, _, files in os.walk(rootdir):
        for filename in files:
            if filename.endswith(_FCL_SUFFIX):
                filepath = os.path.join(rootpath, filename)
                print('===', filepath)
                try:
                    files_tot += 1
                    parser.clear()
                    parser.read_fcl_file(filepath)
                    if want_output:
                        print(parser)
                except Exception as exc:
                    files_err += 1
                    print(exc)
    print('Parsed %d files (%d had errors).' % (files_tot, files_err))


if __name__ == '__main__':
    _parser = FCLParser()
    if len(sys.argv) == 1:  # No args, scan all examples
        parse_dir(_parser, 'Examples')
    else:  # Parse the given files:
        for fcl_filename in sys.argv[1:]:
            _parser.read_fcl_file(fcl_filename)
            print(_parser)
