"""
controlsystem.py : Contains framework for fuzzy logic control systems.

"""
import numpy as np
import networkx as nx
import matplotlib.pylab as plt
from .antecedent_consequent import Antecedent, Consequent, Intermediary
from .fuzzyvariable import FuzzyVariable, FuzzyVariableAdjective

try:
    from collections import OrderedDict
except ImportError:
    from .ordereddict import OrderedDict


class Rule(object):
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
        self.inputs = OrderedDict()
        self._id = id(self)

        if self.label is None:
            self.label = "Rule %d" % self._id

        if antecedents is None or consequents is None:
            self.connections = None
        else:
            self._connect(antecedents, consequents, kind)

    def __repr__(self):
        """
        Print a concise, readable summary of the fuzzy rule.
        """
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
        for adj in temp:
            parent = adj.parent_variable
            if not isinstance(adj, FuzzyVariableAdjective):
                raise ValueError("All elements must be adjectives")
            if parent is None:
                raise ValueError("All adjectives must have a parent")
            if not isinstance(parent, obj) and \
               not isinstance(parent, Intermediary):
                raise ValueError("All adjective's variables must be of type "
                                 "{0}".format(obj))
        return temp

    def _iter(self, var):
        """
        Ensure a variable is iterable; wrap in a list if necessary.
        """
        if issubclass(var.__class__, FuzzyVariableAdjective):
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

    def add_antecedent(self, antecedent_adj):
        """
        Populate the graph with a new antecedent, connecting it to this rule.
        """
        assert isinstance(antecedent_adj, FuzzyVariableAdjective)
        antecedent = antecedent_adj.parent_variable
        assert isinstance(antecedent, Antecedent) or isinstance(antecedent, Intermediary)

        # Antecedent -> Antecedent_Adj -> Rule
        self.graph.add_path([antecedent, antecedent_adj])
        self.graph.add_path([antecedent_adj, self])


    def add_consequent(self, consequent_adj):
        """
        Populate the graph with a new consequent, connecting it to this rule.
        """
        assert isinstance(consequent_adj, FuzzyVariableAdjective)
        consequent = consequent_adj.parent_variable
        assert isinstance(consequent, Consequent) or isinstance(consequent, Intermediary)

        # Rule -> Consequent_Adjective -> Consequent
        self.graph.add_path([self, consequent_adj])
        self.graph.add_path([consequent_adj, consequent])



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
        collected_firing = []
        for antecedent_adj in self.graph.predecessors(self):
            mv = antecedent_adj.membership_value
            if mv is None:
                raise Exception("Membership value missing for " +
                                antecedent_adj.full_label)
            collected_firing.append(mv)

        # Combine membership function firing as appropriate for this rule
        if self.kind == 'or':
            final_firing = np.asarray(collected_firing).max()
        elif self.kind == 'and':
            final_firing = np.asarray(collected_firing).min()
        else:
            raise NotImplementedError("Unexpected kind: " + self.kind)

        # Cap output membership function(s) in consequents
        for consequent_adj in self.graph.successors(self):
            consequent_adj.parent_variable.set_patch(
                consequent_adj.label, final_firing)

    def view(self):
        plt.figure()
        nx.draw(self.graph)
        plt.show()

class ControlSystem(object):
    """
    Fuzzy Control System
    """
    def __init__(self, rules=None):
        self.graph = nx.DiGraph()
        self.input = self._InputAcceptor(self)
        self.output = OrderedDict()

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

    class _InputAcceptor(object):
        def __init__(self, system):
            assert isinstance(system, ControlSystem)
            self.system = system

        def __setitem__(self, key, value):
            # Find the antecedent we should set the input for
            matches = [n for n in self.system.graph.nodes()
                               if isinstance(n, Antecedent) and n.label == key]
            if len(matches) == 0:
                raise ValueError("Unexpected input: " + key)
            assert len(matches) == 1
            matches[0].input = value

    @property
    def rules(self):
        # We have to expose the rules in the order from antecedents to
        #  consequences.  For example if we have:
        #  Antecedent -> rule1 -> Intermediary -> rule2 -> Consequence
        #  if we expose rule2 before rule1, we won't calculate correctly
        exposed_intermediaries = [] # Could also contain consequences
        
        def _process_rules(rules):
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
                    print "*** moving %s to end of list" % rule
                else:
                    yield rule
                    exposed_intermediaries.extend(self.graph.successors(rule))

            if len(skipped_rules) > 0:
                if len(skipped_rules) == len_rules:
                    raise Exception("Unable to resolve rule execution order")
                else:
                    _process_rules(skipped_rules)
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
    def fuzzy_variables(self):
        for node in self.graph.nodes():
            if isinstance(node, FuzzyVariable):
                yield node

    def addrule(self, rule):
        """
        Add a new rule to the graph.
        """
        # Combine the two graphs, which may not be disjoint
        self.graph = nx.compose(self.graph, rule.graph)

    def compute(self):
        """
        Compute the fuzzy system.
        """
        # TODO: Tracking and caching

        # Check if any fuzzy variables lack input values and fuzzyfy inputs
        for antecedent in self.antecedents:
            if antecedent.input is None:
                raise ValueError("All antecedents must have input values!")

        # Calculate rules, taking inputs and accumulating outputs
        for rule in self.rules:
            print "computing rule %s" % rule
            rule.compute()

        # Collect the results and present them as a dict
        for consequent in self.consequents:
            self.output[consequent.label] = consequent.output

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

    def view(self):
        plt.figure()
        nx.draw(self.graph)
        plt.show()

    def print_state(self):
        for v in self.fuzzy_variables:
            print "{0:<25} = {1}".format(v, v.crisp_value)
            for adj in v.adjectives.values():
                print "  - {0:<15}:{1}".format(adj.label, adj.membership_value)