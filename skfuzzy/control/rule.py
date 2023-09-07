"""
rule.py : Contains structure to create fuzzy rules.

Most notably, contains the `Rule` class which is used to connect antecedents
with consequents in a `ControlSystem`.
"""
import networkx as nx
import numpy as np

from .state import StatefulProperty
from .term import (FuzzyAggregationMethods, Term, TermAggregate, TermPrimitive,
                   WeightedTerm)
from .visualization import ControlSystemVisualizer


class Rule(object):
    """
    Rule in a fuzzy control system, connecting antecedent(s) to consequent(s).

    Parameters
    ----------
    antecedent : Antecedent term(s) or logical combination thereof, optional
        Antecedent terms serving as inputs to this rule. Multiple terms may
        be combined using operators `|` (OR), `&` (AND), `~` (NOT), and
        parentheticals to group terms.
    consequent : Consequent term(s), optional
        Consequent terms serving as outputs from this rule. Multiple terms may
        be accepted in four formats:

        Unweighted single output.
            output['term']
        Weighted single output
            (output['term'] % 0.5)
        Unweighted multiple output
            (output1['term1'], output2['term2'])
        Weighted multiple output
            ((output1['term1'] % 1.0), (output2['term2'] % 0.5))
    label : string, optional
        Label to reference the meaning of this rule. Optional, but recommended.
        If provided, the label must be unique among rules in any particular
        `ControlSystem`.

    Notes
    -----
    Fuzzy Rules can be completely built on instantiation or one can begin
    with an empty Rule and construct interactively by setting `.antecedent`,
    `.consequent`, and `.label` variables.
    """

    aggregate_firing = StatefulProperty(None)

    def __init__(self, antecedent=None, consequent=None, label=None,
                 and_func=np.fmin, or_func=np.fmax):
        """
        Rule in a fuzzy system, connecting antecedent(s) to consequent(s).

        Parameters
        ----------
        antecedent : Antecedent term(s) or combination thereof, optional
            Antecedent terms serving as inputs to this rule. Multiple terms may
            be combined using operators `|` (OR), `&` (AND), `~` (NOT), and
            parentheticals to group terms.
        consequent : Consequent term(s) or combination thereof, optional
            Consequent terms serving as outputs from this rule.
            Accept consequents in four formats:

             a) Unweighted single output.
                e.g.: output['term']
             b) Weighted single output
                e.g.: (output['term'] % 0.5)
             c) Unweighted multiple output
                e.g.: (output1['term1'], output2['term2'])
             d) Weighted multiple output
                e.g.: ((output1['term1'] % 1.0), (output2['term2'] % 0.5))
        label : string, optional
            Label to reference the meaning of this rule. Optional, but
            recommended.
        and_func : function, optional
            Function which accepts multiple floating-point arguments and
            returns a single value. Defaults to NumPy function `fmin`, to
            support both single values and arrays. For multiplication,
            substitute `fuzz.control.mult` or `np.multiply`.
        or_func : function, optional
            Function which accepts multiple floating-point arguments and
            returns a single value. Defaults to NumPy function `fmax`, to
            support both single values and arrays.
        """
        self._aggregation_methods = FuzzyAggregationMethods()
        self.and_func = and_func
        self.or_func = or_func

        self._antecedent = None
        self._consequent = None
        if antecedent is not None:
            self.antecedent = antecedent
        if consequent is not None:
            self.consequent = consequent

        if label is not None:
            self.label = label
        else:
            self.label = id(self)

    def __repr__(self):
        """
        Concise, readable summary of the fuzzy rule.
        """
        if len(self.consequent) == 1:
            cons = self.consequent[0]
        else:
            cons = self.consequent

        return ("IF {0} THEN {1}"
                "\n\tAND aggregation function : {2}"
                "\n\tOR aggregation function  : {3}").format(
                    self.antecedent, cons,
                    self.and_func.__name__,
                    self.or_func.__name__)

    @property
    def and_func(self):
        """
        Aggregation function for AND relationships. Default is `min`.
        """
        return self._aggregation_methods.and_func

    @and_func.setter
    def and_func(self, newfunc):
        """
        Method to interactively set the AND aggregation function.
        """
        try:
            newfunc(0.3, 0.96)
        except Exception:
            raise ValueError("The provided function does not support "
                             "floating-point arguments.")
        self._aggregation_methods.and_func = newfunc

    @property
    def or_func(self):
        """
        Aggregation function for OR relationships. Default is `max`.
        """
        return self._aggregation_methods.or_func

    @or_func.setter
    def or_func(self, newfunc):
        """
        Method to interactively set the OR aggregation function.
        """
        try:
            newfunc(0.3, 0.96)
        except Exception:
            raise ValueError("The provided function does not support "
                             "floating-point arguments.")
        self._aggregation_methods.or_func = newfunc

    @property
    def antecedent(self):
        """
        Antecedent clause, consisting of multiple term(s) in this fuzzy Rule.
        """
        if self._antecedent is None:
            raise ValueError("Antecedent not set")
        return self._antecedent

    @antecedent.setter
    def antecedent(self, value):
        """
        Method to interactively set Antecedent term(s).
        """
        if not isinstance(value, TermPrimitive):
            raise ValueError("Unexpected antecedent type")
        # Should be either Term or TermAggregate
        self._antecedent = value

    @property
    def antecedent_terms(self):
        """
        Utility function to list all Antecedent terms present in this clause.
        """
        # Grab all the terms that make up my antecedent clause
        terms = []

        def _find_terms(obj):
            if isinstance(obj, Term):
                terms.append(obj)
            elif obj is None:
                pass
            else:
                assert isinstance(obj, TermAggregate)
                _find_terms(obj.term1)
                _find_terms(obj.term2)
        _find_terms(self.antecedent)
        return terms

    @property
    def consequent(self):
        """
        Consequent clause, consisting of multiple term(s) in this fuzzy Rule.
        """
        if self._consequent is None:
            raise ValueError("Consequent not set")
        return self._consequent

    @consequent.setter
    def consequent(self, value):
        """
        Accept consequents in four formats:

         a) Unweighted single output.
            e.g.: output['term']
         b) Weighted single output
            e.g.: (output['term'] % 0.5)
         c) Unweighted multiple output
            e.g.: (output1['term1'], output2['term2'])
         d) Weighted multiple output
            e.g.: ((output1['term1'] % 1.0), (output2['term2'] % 0.5))
        """
        if isinstance(value, Term):
            self._consequent = [WeightedTerm(value, 1.)]

        elif isinstance(value, WeightedTerm):
            self._consequent = [value]

        elif not hasattr(value, '__iter__'):
            raise ValueError("Unexpected consequent type")

        else:
            # Must be one of formats c) or d)
            self._consequent = []
            for i in value:
                if isinstance(i, Term):
                    self._consequent.append(WeightedTerm(i, 1.))
                elif isinstance(i, WeightedTerm):
                    self._consequent.append(i)
                else:
                    raise ValueError("Unexpected consequent type")

    @property
    def graph_n(self):
        graph = nx.DiGraph()
        # Link all antecedents to me by decomposing
        # TermAggregate down to just Terms
        nodes = []
        structure = []
        colors = []
        antecedent_attr = [getattr(self.antecedent, attr) for attr in
                           dir(self.antecedent) if
                           not attr.startswith("__")]
        for method in antecedent_attr:
            if isinstance(method, Term):
                active_label = method.label
                nodes.append(method.parent.label)
                colors.append([method.parent.label, 'green'])
                for key in method.parent.terms.keys():
                    nodes.append(str(key))
                    structure.append([key, method.parent.label])
                    if str(key) == active_label:
                        colors.append([str(key), 'green'])
                    else:
                        colors.append([str(key), 'red'])
                for j in range(len(self.consequent)):
                    structure.append([method.parent.label,
                                      self.consequent[j].term.parent.label])
                    nodes.append(self.consequent[j].term.parent.label)
                    colors.append(
                        [self.consequent[j].term.parent.label, 'green'])
        if len(nodes) == 0:
            active_label = self.antecedent.label
            nodes.append(self.antecedent.parent.label)
            colors.append([self.antecedent.parent.label, 'green'])
            for key in self.antecedent.parent.terms.keys():
                nodes.append(str(key))
                structure.append([key, self.antecedent.parent.label])
                if str(key) == active_label:
                    colors.append([str(key), 'green'])
                else:
                    colors.append([str(key), 'red'])
            for j in range(len(self.consequent)):
                structure.append([self.antecedent.parent.label,
                                  self.consequent[j].term.parent.label])
                nodes.append(self.consequent[j].term.parent.label)
                colors.append([self.consequent[j].term.parent.label, 'green'])
        graph.add_nodes_from(nodes)
        graph.add_edges_from(structure)
        return graph, colors

    @property
    def graph(self):
        """
        NetworkX directed graph representing this Rule's connectivity.
        """
        graph = nx.DiGraph()
        # Link all antecedents to me by decomposing
        #  TermAggregate down to just Terms
        for t in self.antecedent_terms:
            assert isinstance(t, Term)
            graph.add_edge(t, self)
            graph = nx.compose(graph, t.parent.graph)

        # Link all consequents from me
        for c in self.consequent:
            assert isinstance(c, WeightedTerm)
            graph.add_edge(self, c.term)
            graph = nx.compose(graph, c.term.parent.graph)
        return graph

    def view(self):
        """
        Show a visual representation of this Rule.
        """
        return ControlSystemVisualizer(self).view()

    def view_n(self):
        """
        Show a visual network representation of this Rule.
        To run this all names of the Membership functions needs to unique.
        """
        return ControlSystemVisualizer(self).view_n()
