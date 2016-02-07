"""
controlsystem.py : Contains framework for fuzzy logic control systems.

"""
import numpy as np
import networkx as nx
from .antecedent_consequent import Antecedent, Consequent
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
                 modifiers={}):
        self._chk_kind(kind)
        self.kind = kind.lower()
        self.antecedents = self._chk_obj(antecedents, Antecedent)
        self.consequents = self._chk_obj(consequents, Consequent)
        self.modifiers = modifiers
        self.graph = nx.DiGraph()
        self.graph.add_node(self)
        self.graph.node[self]['kind'] = kind
        self.inputs = OrderedDict()
        self._id = id(self)

        if antecedents is None or consequents is None:
            self.connections = None
        else:
            self._connect(antecedents, consequents, kind, modifiers)

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
            if not isinstance(adj, FuzzyVariableAdjective):
                raise ValueError("All elements must be adjectives")
            if adj.parent_variable is None:
                raise ValueError("All adjectives must have a parent")
            if not isinstance(adj.parent_variable, obj):
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
        assert isinstance(antecedent, Antecedent)

        variable_id = antecedent._id
        unique_id = ' {0}'.format(variable_id)
        for label, adj in antecedent.adjectives.items():
            unique_label = label + unique_id
            self.graph.add_path([antecedent, unique_label])
            self.graph.node[unique_label]['mf'] = adj.mf
            self.graph.node[unique_label]['shortlabel'] = label
            self.graph.node[unique_label]['parent'] = antecedent.label


        self.graph.add_path([antecedent_adj.label + unique_id, self])
        antecedent.connections[antecedent_adj.label] = self

    def add_consequent(self, consequent_adj):
        """
        Populate the graph with a new consequent, connecting it to this rule.
        """
        assert isinstance(consequent_adj, FuzzyVariableAdjective)
        consequent = consequent_adj.parent_variable
        assert isinstance(consequent, Consequent)

        variable_id = consequent._id
        unique_id = ' {0}'.format(variable_id)
        for label, adj in consequent.adjectives.items():
            unique_label = label + unique_id
            self.graph.add_path([unique_label, consequent])
            self.graph.node[unique_label]['mf'] = adj.mf
            self.graph.node[unique_label]['shortlabel'] = label
            self.graph.node[unique_label]['parent'] = consequent.label

        self.graph.add_path([self, consequent_adj.label + unique_id])
        consequent.connections[consequent_adj.label] = self


    def _connect(self, antecedents=None, consequents=None, kind='or',
                 modifiers={}):
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
        # Calculate firing for all connected antecedents if needed
        for antecedent in self.antecedents:
            if antecedent.parent_variable.output is None:
                antecedent.parent_variable.compute()

        # Collect the firing of all input membership functions
        collected_firing = []
        for mf in self.graph.predecessors(self):
            mf_label = self.graph.node[mf]['shortlabel']
            collected_firing.append(
                self.graph.predecessors(mf)[0].output[mf_label])

        # Combine membership function firing as appropriate for this rule
        if self.kind == 'or':
            final_firing = np.asarray(collected_firing).max()
        else:
            final_firing = np.asarray(collected_firing).min()

        # Cap output membership function(s) in consequents
        for mf in self.graph.successors(self):
            self.graph.successors(mf)[0].set_patch(
                self.graph.node[mf]['shortlabel'], final_firing)


class ControlSystem(object):
    """
    Fuzzy Control System
    """
    def __init__(self, rules=None):
        self.antecedents = OrderedDict()
        self.consequents = OrderedDict()
        self.graph = nx.DiGraph()
        self.rules = OrderedDict()
        self._mapping = OrderedDict()
        self.input = self._InputAcceptor(self)
        self._changed = set()
        self._cached = set()
        self.output = OrderedDict()

        # Construct a system from provided rules, if given
        if rules is not None:
            try:
                for rule in rules:
                    self.addrule(rule)
            except AttributeError or TypeError:
                try:
                    self.addrule(rules)
                except:
                    raise ValueError("Optional argument `rules` must be a "
                                     "FuzzyRule or iterable of FuzzyRules.")

    class _InputAcceptor(object):
        def __init__(self, system):
            self.system = system

        def __setitem__(self, key, value):
            uid = self.system._mapping[key]
            self.system.antecedents[uid].input = value
            self.system._changed.add(uid)
            try:
                self.system._cached.remove(uid)
            except KeyError:
                # This wasn't previously cached, that's OK
                pass

    def addrule(self, rule):
        """
        Add a new rule to the graph.
        """
        # Add rule to self.rules, extract and track other needed info
        self.rules[id(rule)] = (rule)

        # Track antecedents connected to rule, deduplicate
        for antecedent_adj in rule.antecedents:
            antecedent = antecedent_adj.parent_variable
            if id(antecedent) not in self.antecedents:
                self.antecedents[id(antecedent)] = antecedent
                self._mapping[antecedent.label] = id(antecedent)

        # Track consequents connected to rule, deduplicate
        for consequent_adj in rule.consequents:
            consequent = consequent_adj.parent_variable
            if id(consequent) not in self.consequents:
                self.consequents[id(consequent)] = consequent
                self._mapping[consequent.label] = id(consequent)

        # Combine the two graphs, which may not be disjoint
        self.graph = nx.compose(self.graph, rule.graph)

    def compute(self):
        """
        Compute the fuzzy system.
        """
        # Check if any fuzzy variables lack input values
        for antecedent in self.antecedents.values():
            if antecedent.input is None:
                raise ValueError("All antecedents must have input values!")

        # Compute antecedents if not already computed
        # This will usually only happen once
        for antecedent in self.antecedents.values():
            if antecedent._id not in self._cached:
                antecedent.compute()
                self._cached.add(antecedent._id)

        # Figure out which values changed, and what rules they affected
        changed_rules = OrderedDict()
        for changed in self._changed:

            # Find connected rules
            changed_antecedent = self.antecedents[changed]
            connected_mfs = self.graph.successors(changed_antecedent)
            connected_rules = set()
            for mf in connected_mfs:
                # Pass by unconnected membership functions
                if len(self.graph.successors(mf)) != 0:
                    for succesor in self.graph.successors(mf):
                        connected_rules.add(succesor)

            for rule in connected_rules:
                if rule not in changed_rules:
                    changed_rules[rule] = rule

        # Reset the hidden tracker for changed rules
        self._changed = set()

        # (Re)calculate only changed rules, taking inputs and capping outputs
        for changed_rule in changed_rules.values():
            changed_rule.compute()

        # Collect the results and present them as a dict
        for consequent in self.consequents.values():
            consequent.compute()
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
