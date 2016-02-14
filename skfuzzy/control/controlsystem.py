"""
controlsystem.py : Contains framework for fuzzy logic control systems.

"""
import numpy as np
import networkx as nx
import matplotlib.pylab as plt

from skfuzzy import interp_membership, defuzz
from .antecedent_consequent import Antecedent, Consequent, Intermediary
from .fuzzyvariable import FuzzyVariable, FuzzyVariableTerm, \
    FuzzyVariableTermAggregate
from .visualization import ControlSystemVisualizer
from .rule import Rule, WeightedConsequent

try:
    from collections import OrderedDict
except ImportError:
    from .ordereddict import OrderedDict


class OLD_Rule(object):
    """
    Define a new fuzzzy rule relating universe variables in memory.

    Parameters
    ----------
    antecedents : Antecedent or iterable of Antecedents
        Fuzzy antecedents (input/sensors) as from ``skfuzzy.Antecedent``.
    consequents : Consequent or iterable of Consequents
        Fuzzy consequents (output/control) as from ``skfuzzy.Consequent``.
        Universe variable for the fuzzy consequent.
    kind : string
        Defines the relationship of antecedents. 'or' will combine with a
        maximum operator, while 'and' will combine with a minimum operator.

    Notes
    -----
    Boolean logic order of operations (NOT > AND > OR) is followed.
    """

    def __init__(self, antecedents=None, consequents=None, kind='or',
                 label=None):
        self._chk_kind(kind)
        self.kind = kind.lower()
        self.antecedents = self._chk_obj(antecedents, Antecedent)
        self.consequents = self._chk_obj(consequents, Consequent)
        self.label = label
        self.graph = nx.DiGraph()
        self.graph.add_node(self)
        self.graph.node[self]['kind'] = kind
        self._id = id(self)

        # Debugging state
        self.collected_firing = {}
        self.final_firing = None

        if antecedents is None or consequents is None:
            self.connections = None
        else:
            self._connect(antecedents, consequents, kind)

    def __repr__(self):
        """
        Print a concise, readable summary of the fuzzy rule.
        """
        if self.label is not None:
            return self.label
        # All this for a pretty printed representation of the rule...
        antlen = len(self.antecedents)
        conlen = len(self.consequents)

        ant_str = ''
        con_str = ''

        for antecedent in self.antecedents:
            ant_str += antecedent.full_label + ', '

        for consequent in self.consequents:
            con_str += consequent.full_label + ', '

        ant_str = ant_str[:-2]
        con_str = con_str[:-2]

        if antlen > 1:
            ant_str = '[' + ant_str + ']'

        if conlen > 1:
            con_str = '[' + con_str + ']'

        return "{0}-Rule connecting {1} with {2}".format(
            self.kind.upper(), ant_str, con_str)

    def _chk_obj(self, var, obj):
        """
        Argument checking to ensure every adjective's parent is type ``obj``.
        """
        temp = self._iter(var)
        for term in temp:
            parent = term.parent_variable
            if not isinstance(term, FuzzyVariableTerm):
                raise ValueError("All elements must be terms")
            if parent is None:
                raise ValueError("All terms must have a parent")
            if not isinstance(parent, obj) and \
               not isinstance(parent, Intermediary):
                raise ValueError("All term's variables must be of type "
                                 "{0}".format(obj))
        return temp

    def _iter(self, var):
        """
        Ensure a variable is iterable; wrap in a list if necessary.
        """
        if issubclass(var.__class__, FuzzyVariableTerm):
            return [var, ]
        else:
            return var

    def _chk_kind(self, string):
        """
        The only accepted kinds of fuzzy rules are 'or', or 'and'.
        """
        string = string.lower()
        if string == 'or' or string == 'and':
            return
        else:
            raise ValueError("Incorrect kind. Options are 'or' or 'and'.")

    def add_antecedent(self, antecedent_term):
        """
        Populate the graph with a new antecedent, connecting it to this rule.
        """
        assert isinstance(antecedent_term, FuzzyVariableTerm)
        antecedent = antecedent_term.parent_variable
        assert isinstance(antecedent, Antecedent) or isinstance(antecedent, Intermediary)

        # Antecedent -> Antecedent_Term -> Rule
        self.graph.add_path([antecedent, antecedent_term])
        self.graph.add_path([antecedent_term, self])


    def add_consequent(self, consequent_term):
        """
        Populate the graph with a new consequent, connecting it to this rule.
        """
        assert isinstance(consequent_term, FuzzyVariableTerm)
        consequent = consequent_term.parent_variable
        assert isinstance(consequent, Consequent) or isinstance(consequent, Intermediary)

        # Rule -> Consequent_Term -> Consequent
        self.graph.add_path([self, consequent_term])
        self.graph.add_path([consequent_term, consequent])



    def _connect(self, antecedents=None, consequents=None, kind='or'):
        """
        Private method used when arguments provided on rule instantiation.
        """
        for antecedent in self.antecedents:
            self.add_antecedent(antecedent)

        for consequent in self.consequents:
            self.add_consequent(consequent)

    def compute(self):
        """
        Execute this fuzzy rule.
        """

        # Collect the firing of all input membership functions
        self.collected_firing = {}
        for antecedent_term in self.graph.predecessors(self):
            mv = antecedent_term.membership_value
            if mv is None:
                raise Exception("Membership value missing for " +
                                antecedent_term.full_label)
            self.collected_firing[antecedent_term.full_label] = mv

        # Combine membership function firing as appropriate for this rule
        if self.kind == 'or':
            self.final_firing = np.asarray(self.collected_firing.values()).max()
        elif self.kind == 'and':
            self.final_firing = np.asarray(self.collected_firing.values()).min()
        else:
            raise NotImplementedError("Unexpected kind: " + self.kind)

        # Cap output membership function(s) in consequents
        for consequent_term in self.graph.successors(self):
            consequent_term.parent_variable.set_patch(
                consequent_term.label, self.final_firing)

    def view(self):
        ControlSystemVisualizer(self).view().show()

class ControlSystem(object):
    """
    Fuzzy Control System
    """
    def __init__(self, rules=None):
        self.graph = nx.DiGraph()


        # Construct a system from provided rules, if given
        if rules is not None:
            if hasattr(rules, '__iter__'):
                for rule in rules:
                    self.addrule(rule)
            else:
                try:
                    self.addrule(rules)
                except:
                    raise ValueError("Optional argument `rules` must be a "
                                     "FuzzyRule or iterable of FuzzyRules.")

    @property
    def rules(self):
        # We have to expose the rules in the order from antecedents to
        #  consequences.  For example if we have:
        #  Antecedent -> rule1 -> Intermediary -> rule2 -> Consequence
        #  if we expose rule2 before rule1, we won't calculate correctly
        exposed_intermediaries = [] # Could also contain consequences

        def _process_rules(rules):
            # Recursive funcion to process rules in the correct firing order
            len_rules = len(rules)
            skipped_rules = []
            while len(rules) > 0:
                rule = rules.pop(0)
                # Check that we've exposed all inputs to this rule
                predecesors = self.graph.predecessors(rule)
                p2 = filter(lambda p: isinstance(p.parent_variable,
                                                 Intermediary), predecesors)
                p3 = filter(lambda p: p not in exposed_intermediaries, p2)

                if len(p3) > 0:
                    # We have not calculated the predecsors for this rule yet.
                    #  Skip it for now
                    skipped_rules.append(rule)
                else:
                    yield rule
                    exposed_intermediaries.extend(self.graph.successors(rule))

            if len(skipped_rules) > 0:
                if len(skipped_rules) == len_rules:
                    raise Exception("Unable to resolve rule execution order")
                else:
                    # Recurse across the skipped rules
                    for r in _process_rules(skipped_rules):
                        yield r
            else:
                raise StopIteration()

        rules = []

        for node in self.graph.nodes():
            if isinstance(node, Rule):
                rules.append(node)
        return _process_rules(rules)



    @property
    def antecedents(self):
        for node in self.graph.nodes():
            if isinstance(node, Antecedent):
                yield node
    @property
    def consequents(self):
        for node in self.graph.nodes():
            if isinstance(node, Consequent):
                yield node
    @property
    def intermediaries(self):
        for node in self.graph.nodes():
            if isinstance(node, Intermediary):
                yield node
    @property
    def fuzzy_variables(self):
        for node in self.graph.nodes():
            if isinstance(node, FuzzyVariable):
                yield node

    def addrule(self, rule):
        """
        Add a new rule to the graph.
        """
        if not isinstance(rule, Rule):
            raise ValueError("rule is not a Rule object")

        # Combine the two graphs, which may not be disjoint
        self.graph = nx.compose(self.graph, rule.graph)

    def view(self):
        fig = ControlSystemVisualizer(self).view()
        fig.show()

class _InputAcceptor(object):
    def __init__(self, simulation):
        assert isinstance(simulation, ControlSystemSimulation)
        self.sim = simulation

    def __setitem__(self, key, value):
        # Find the antecedent we should set the input for
        matches = [n for n in self.sim.ctrl.graph.nodes()
                           if isinstance(n, Antecedent) and n.label == key]
        if len(matches) == 0:
            raise ValueError("Unexpected input: " + key)
        assert len(matches) == 1
        matches[0].input[self.sim] = value


class ControlSystemSimulation(object):

    def __init__(self, control_system):
        assert isinstance(control_system, ControlSystem)
        self.ctrl = control_system

        self.input = _InputAcceptor(self)
        self.output = OrderedDict()

    def inputs(self, input_dict):
        """
        Convenience method to accept multiple inputs to antecedents.

        Parameters
        ----------
        input_dict : dict
            Contains key:value pairs where the key is the label for a
            connected Antecedent and the value is the input.
        """
        for label, value in input_dict.items():
            self.input[label] = value

    def compute(self):
        """
        Compute the fuzzy system.
        """
        # TODO: Tracking and caching

        # Check if any fuzzy variables lack input values and fuzzyfy inputs
        for antecedent in self.ctrl.antecedents:
            if antecedent.input[self] is None:
                raise ValueError("All antecedents must have input values!")
            if antecedent.terms.values()[0].membership_value[self] is not None:
                raise RuntimeError("Antecedent already has calculated "
                "membership.  Are you trying to computer a simulation multiple "
                "times?  Create multiple ControlSystemSimulation objects "
                "instead.")
            CrispValueCalculator(antecedent, self).fuzz(antecedent.input[self])

        # Calculate rules, taking inputs and accumulating outputs
        for rule in self.ctrl.rules:
            self.compute_rule(rule)


        # Collect the results and present them as a dict
        for consequent in self.ctrl.consequents:
            consequent.output[self] = \
                CrispValueCalculator(consequent, self).defuzz()
            self.output[consequent.label] = consequent.output[self]

    def compute_rule(self, rule):
        """
        Implements rule according to the three step method of
        Mamdani inference: Aggregation, activation, and accumulation

        """
        # Step 1: Aggregation.  This finds the net accomplishment of the
        #  antecedent by AND-ing or OR-ing together all the membership values
        #  of the terms that make up the accomplishment condition.
        #  The process of actually aggregating everything is delegated to the
        #  FuzzyVariableTermAggregation class, but we can tell that class
        #  what aggregation style this rule mandates

        if isinstance(rule.antecedent, FuzzyVariableTermAggregate):
            rule.antecedent.agg_method = rule.aggregation_method
        rule.aggregate_firing[self] = rule.antecedent.membership_value[self]

        # Step 2: Activation.  The degree of membership of the consequence
        #  is determined by the degree of accomplishment of the antecedent,
        #  which is what we determined in step 1.  The only difference would
        #  be if the consequent has a weight, which we would apply now.
        for c in rule.consequent:
            assert isinstance(c, WeightedConsequent)
            c.activation[self] = rule.aggregate_firing[self] * c.weight

        # Step 3: Accumulation.  Apply the activation to each consequent,
        #   accumulating multiple rule firings into a single membership value.
        #   The process of actual accumulation is delegated to the
        #   FuzzyVariableTerm which uses its parent's accumulation method
        for c in rule.consequent:
            assert isinstance(c, WeightedConsequent)
            term = c.term
            value = c.activation[self]

            # Find new membership value
            if term.membership_value[self] is None:
                assert len(term.cuts[self]) == 0, "Membership value already set"
                term.membership_value[self] = value
            else:
                # Use the accumulation method of variable to determine
                #  how to to handle multiple cuts
                accu = term.parent_variable.accumulation_method
                term.membership_value[self] = accu(value,
                                                   term.membership_value[self])

            term.cuts[self][rule] = value



    def print_state(self):
        if self.ctrl.consequents.next().output[self] is None:
            raise ValueError("Call compute method first.")

        print "============="
        print " Antecedents "
        print "============="
        for v in self.ctrl.antecedents:
            print "{0:<35} = {1}".format(v, v.input[self])
            for term in v.terms.values():
                print "  - {0:<32}: {1}".format(term.label,
                                                term.membership_value[self])
        print ""
        print "======="
        print " Rules "
        print "======="
        rule_number = {}
        for rn, r in enumerate(self.ctrl.rules):
            assert isinstance(r, Rule)
            rule_number[r] = "RULE #%d" % rn
            print "RULE #%d:\n  %s\n" % (rn, r)

            print "  Aggregation (IF-clause):"
            for term in r.antecedent_terms:
                assert isinstance(term, FuzzyVariableTerm)
                print "  - {0:<45}: {1}".format(term.full_label,
                                                term.membership_value[self])
            print "    {0:>44} = {1}".format(r.antecedent,
                                             r.aggregate_firing[self])

            print "  Activation (THEN-clause):"
            for c in r.consequent:
                assert isinstance(c, WeightedConsequent)
                print "    {0:>44} : {1}".format(c,
                                                 c.activation[self])
            print ""
        print ""

        print "=============================="
        print " Intermediaries and Conquests "
        print "=============================="
        both = list(self.ctrl.consequents) + list(self.ctrl.intermediaries)
        for c in both:
            print "{0:<36} = {1}".format(c,
                                         CrispValueCalculator(c, self).defuzz())

            for term in c.terms.values():
                print "  %s:" % term.label
                for cut_rule, cut_value in term.cuts[self].items():
                    if cut_rule not in rule_number.keys(): continue
                    print "    {0:>32} : {1}".format(rule_number[cut_rule],
                                                     cut_value)
                accu = "Accumulate using %s" % c.accumulation_method.func_name
                print "    {0:>32} : {1}".format(accu,
                                                term.membership_value[self])
            print ""


class CrispValueCalculator(object):

    def __init__(self, fuzzy_var, sim):
        assert isinstance(fuzzy_var, FuzzyVariable)
        assert isinstance(sim, ControlSystemSimulation)
        self.var = fuzzy_var
        self.sim = sim

    def defuzz(self):
        """Derive crisp value based on membership of adjectives"""
        output_mf, cut_mfs = self.find_memberships()
        if len(cut_mfs) == 0:
            raise ValueError("No terms have memberships.  Make sure you "
                             "have at least one rule connected to this "
                             "variable and have run the rules calculation.")
        return defuzz(self.var.universe, output_mf, self.var.defuzzify_method)

    def fuzz(self, value):
        """Propagate crisp value down to adjectives by calculating membership"""
        if len(self.var.terms) == 0:
            raise ValueError("Set Term membership function(s) first")

        for label, term in self.var.terms.items():
            term.membership_value[self.sim] = \
                interp_membership(self.var.universe, term.mf, value)


    def find_memberships(self):
        # Check we have some adjectives
        if len(self.var.terms.keys()) == 0:
            raise ValueError("Set term membership function(s) first")

        # Initilize membership
        output_mf = np.zeros_like(self.var.universe, dtype=np.float64)

        # Build output membership function
        term_mfs = {}
        for label, term in self.var.terms.items():
            cut = term.membership_value[self.sim]
            if cut is None:
                continue # No membership defined for this adjective
            term_mfs[label] = np.minimum(cut, term.mf)
            np.maximum(output_mf, term_mfs[label], output_mf)

        return output_mf, term_mfs