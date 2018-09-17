'''
    A scanner for the Fuzzy Control Language (FCL).
    This is written using PLY (Python Lex-Yacc: http://www.dabeaz.com/ply)

    I'm working from the *draft* IEC 61131-7 standard..
    References: https://en.wikipedia.org/wiki/Fuzzy_Control_Language

    @author: james.power@mu.ie, Created on Tue Aug 14 09:58:10 2018
'''


import sys
import os
import codecs

from .local_ply import lex    # Saves installing PLY to run this.


class FCLLexer(object):
    '''
    A scanner for the FCL language.
    Call scan_text() on a string, or scan_file() with a filename.
    '''

    def __init__(self, strict=False):
        '''Set up the lexer, ready to accept some input'''
        # Load reserved words: default is upper case
        self.reserved = {a.upper(): a.upper() for a in FCLLexer.reserved_words}
        if not strict:  # Allow lower-case reserved words too:
            self.reserved.update({a.lower(): a.upper()
                                  for a in FCLLexer.reserved_words})
        # Get PLY to do its magic and build the lexer:
        self.lexer = lex.lex(module=self)
        # Initialise context information:
        self.line_start = 1   # char position of most recent line-start
        self.error_count = 0  # no. of errors seen in this file
        self.reset_lineno()
        self.next_token = None

    def lexical_error(self, tok, msg):
        '''Report an error, print the position and next token.'''
        print('>>> {} {}'.format(self.get_pos(tok), msg))
        self.error_count += 1

    def reset_lineno(self, filename=None):
        ''' Resets the internal line-number counter of the lexer. '''
        self.lexer.lineno = 1
        self.line_start = 1  # char position of most recent line-start
        self.filename = filename
        self.error_count = 0
        self.clear_lookahead()

    def get_pos(self, token):
        '''Return a string with the token's position: filename, line, column'''
        pstr = ''
        if self.filename:
            pstr = self.filename
        if token:
            colno = 1+(token.lexpos - self.line_start)
            pstr += '[%d,%d]' % (token.lineno, colno)
        else:
            pstr += '[EOF]'
        return pstr

    def input(self, text):
        '''Load the given text into the scanner, and prepare to scan'''
        self.lexer.input(text)

    def clear_lookahead(self):
        '''Throw away the current lookahead token (e.g. after an error)'''
        self.next_token = None

    def token(self):
        '''Read the next word from the input and return its token'''
        tok = self.next_token if self.next_token else self.lexer.token()
        self.next_token = None
        return tok

    def lookahead(self):
        '''Have a look at the next token, but don't consume it'''
        if not self.next_token:
            self.next_token = self.lexer.token()
        return self.next_token

    def scan_text(self, data, filename=None, silent=False):
        '''
        Run the lexer with the given string as input.
        Can specify the filename (it's only used for error messages).
        If not silent then print each token as it is scanned.
        '''
        self.reset_lineno(filename)
        self.lexer.input(data)
        for tok in self.lexer:
            if not silent:
                print(tok)

    def scan_file(self, filename, silent=False):
        '''Run the lexer with the contents of filename as input.'''
        with codecs.open(filename, 'r',
                         encoding='utf-8', errors='ignore') as fileh:
            self.scan_text(fileh.read(), filename, silent)

    # #################################### #
    # ### FCL LEXICAL RULES START HERE ### #
    # See PLY for info on lex rule formats #
    # #################################### #

    states = (
        ('incomment', 'exclusive'),
    )

    reserved_words = '''
        fuzzify defuzzify ruleblock function_block
        end_fuzzify end_defuzzify end_ruleblock end_function_block
        var_input var_output var end_var option end_option
        accu act default method range term  nan nc
        rule if then with and or not is
        lock enabled
    '''.split()

    tokens = '''
        INT_CONST FLOAT_CONST IDENTIFIER
        COMMA DOTDOT SEMICOLON COLON ASSIGN
        LPAREN RPAREN
        '''.split() + [a.upper() for a in reserved_words]

    # Token patterns:
    t_COMMA = r','
    t_DOTDOT = r'\.\.'
    t_SEMICOLON = r';'
    t_COLON = r':'
    t_ASSIGN = r':='
    t_LPAREN = r'\('
    t_RPAREN = r'\)'

    def t_ANY_newline(self, t):
        r'\n+'
        t.lexer.lineno += t.value.count("\n")
        self.line_start = t.lexpos

    def t_OPEN_COMMENT(self, t):
        r'/\*'
        t.lexer.begin('incomment')

    def t_incomment_CLOSE_COMMENT(self, t):
        r'\*/'
        t.lexer.begin('INITIAL')

    def t_incomment_ignore_stuff(self, t):
        r'[^\*\n]'

    t_incomment_ignore = ' \t'

    def t_incomment_error(self, t):
        self.lexical_error(t, 'Discarding "{}"'.format(t.value[:3]))
        t.lexer.skip(1)

    # Note that newline below is enabled for any state (including incomment)

    # Floats: borrowed and adapted from pycparser/c_lexer.py
    exponent_part = r"""([eE][-+]?[0-9]+)"""
    fractional_constant = r"""([0-9]*\.[0-9]+)|([0-9]+\.)"""
    floating_constant = '[-+]?((((' + fractional_constant + ')' \
                        + exponent_part + '?)'\
                        + '|([0-9]+' + exponent_part + '))[FfLl]?)'

    @lex.TOKEN(floating_constant)
    def t_FLOAT_CONST(self, t):
        try:
            t.value = float(t.value)
        except ValueError:
            self.lexical_error(t, 'Float value "{}" is not valid'
                                  .format(t.value))
            t.value = 0.0
        return t

    def t_INT_CONST(self, t):
        r'[-+]?\d+'
        try:
            t.value = int(t.value)
        except ValueError:
            self.lexical_error(t, 'Integer value "{}" is too large'
                                  .format(t.value))
            t.value = 0
        return t

    def t_IDENTIFIER(self, t):
        r'[a-zA-Z_][a-zA-Z_0-9\-]*'
        t.type = self.reserved.get(t.value, 'IDENTIFIER')
        return t

    # Ignore whitespace:
    t_ignore = ' \t'
    # Ignore single-line comments (C++/Java or Python style):
    t_ignore_PY_COMMENT = r'\#.*'
    t_ignore_CPP_COMMENT = r'//.*'

    def t_error(self, t):
        '''Only get here if the current char was unrecognised'''
        self.lexical_error(t, 'Illegal character "{}"'.format(t.value[0]))
        t.lexer.skip(1)

    # ################################## #
    # ### FCL LEXICAL RULES END HERE ### #
    # ################################## #


class BufferedFCLLexer(FCLLexer):
    '''
    A wrapper for the FCLLexer to support look-ahead for parsing.
    Mainly a bunch of routines of the form: "what token is next?"
    The peek_* functions look at the next token but don't consume it.
    The recognise_* functions consume a token, maybe throw an error.
    '''

    def __init__(self, error_handler):
        '''
        Bind the scanner's error-handling function to the one given.
        '''
        FCLLexer.__init__(self)
        self.error_handler = error_handler

    def lexical_error(self, tok, msg):
        '''
        Raise a lexical error at the given token position.
        Redirect handling this to the supplied error handler.
        We supply the pos, so we don't call token() (again) to get it.
        '''
        self.error_handler(msg, 'lexical error', self.get_pos(tok))

    def maybe_set_input(self, input_string):
        '''
        Set the input to be the given string, if there is a given string.
        '''
        if input_string:
            self.reset_lineno()
            self.input(input_string)

    def peek_type(self):
        '''
        Return the type of the next token, or None if EOF
        '''
        next_tok = self.lookahead()
        if next_tok:
            return next_tok.type
        return None

    def peek(self, toktype):
        '''
        Return true iff the next token has type toktype.
        Does not consume the token.
        '''
        return self.peek_some([toktype])

    def peek_some(self, toktypes):
        '''
        Return true iff the next token has one of the types toktypes.
        Does not consume token.  Returns False if next token is EOF.
        i.e. *check* if a toktype token is next.
        '''
        next_tok = self.lookahead()
        if next_tok and next_tok.type in toktypes:
            return next_tok
        return None

    def peek_not(self, toktypes):
        '''
        Return true iff the next token has a type other than toktypes.
        Does not consume token.  N.B. returns False if next token is EOF.
        i.e. *check* that the next token isn't of type toktype.
        Used mostly in loops, so that's why we return False on EOF.
        '''
        next_tok = self.lookahead()
        if next_tok and next_tok.type not in toktypes:
            return True
        return False

    def recognise(self, toktype):
        '''
        If the next token is of the type toktype, then read it
        and return its value.  Else signal a syntax error.
        '''
        return self.recognise_some([toktype])

    def recognise_some(self, toktypes):
        '''
        If the next token has one of the types toktypes, then read it
        and return its value.  Else signal a syntax error.
        i.e. *demand* that a toktype token is next.
        '''
        next_tok = self.lookahead()
        if next_tok and next_tok.type in toktypes:
            return self.token().value
        self.error_handler('expected {}'.format(toktypes))

    def recognise_if_there(self, toktype):
        '''
        If the next token has one of the types toktypes, then read it
        and return its value.  Else return False (don't signal an error).
        i.e. *optionally* recognise a toktype token, if it is next.
        '''
        next_tok = self.lookahead()
        if next_tok and next_tok.type == toktype:
            return self.token().value
        return None

    def recognise_anything(self):
        '''Read the next token, whatever it is.'''
        return self.token()


_FCL_SUFFIX = '.fcl'


def scan_dir(lexer, rootdir, silent=False):
    '''
    Scan all the .fcl files in root and its subdirs.
    Default is to print out each token as it is recognised.
    '''
    files_tot, files_err = 0, 0
    for rootpath, _, files in os.walk(rootdir):
        for filename in files:
            if filename.endswith(_FCL_SUFFIX):
                filepath = os.path.join(rootpath, filename)
                print('===', filepath)
                files_tot += 1
                lexer.scan_file(filepath, silent)
                if lexer.error_count > 0:
                    files_err += 1
    print('Scanned %d files (%d had errors).' % (files_tot, files_err))


if __name__ == '__main__':
    _LEXER = FCLLexer()
    if len(sys.argv) == 1:  # No args, scan all examples
        scan_dir(_LEXER, 'Examples')
    else:  # Parse the given files:
        for fcl_filename in sys.argv[1:]:
            _LEXER.scan_file(fcl_filename)
