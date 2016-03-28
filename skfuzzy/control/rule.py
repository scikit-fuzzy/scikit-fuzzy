"""
rule.py : Contains structure to create fuzzy rules.

Most notably, contains the `Rule` object which is used to connect atecedents
with conqeuents in a `ControlSystem`.
"""
from __future__ import print_function, division

import networkx as nx
from .fuzzyvariable import (FuzzyAggregationMethod, Term,
                            TermAggregate, TermPrimitive)
from .visualization import ControlSystemVisualizer
from .state import StatefulProperty


class WeightedTerm(object):
    """
    A `Term`, with a weight assigned.

    All consequents become `WeightedTerm`s in calculation; if a weight
    was not assigned, they default to a weight of 1.0.
    """

    activation = StatefulProperty(None)

    def __init__(self, term, weight=1.0):
        """
        Initialize the weighted consequent.

        Parameters
        ----------
        term : Term
            A fuzzy variable with specified mebership function.
        weight : float
            Weight to assign this Term
        """
        assert isinstance(term, Term)
        self.term = term
        self.weight = weight

    def __repr__(self):
        """
        String representation of the `WeightedTerm`.
        """
        if self.weight == 1.:
            return self.term.full_label
        else:
            return "%s@%0.2f%%" % (self.term.full_label, self.weight)


class Rule(object):
    """
    Rule in a fuzzy control system, connecting antecedent(s) to consequent(s).

    Parameters
    ----------
    antecedent : Antecedent term(s) or logical combination thereof, optional
        Antecedent terms serving as inputs to this rule. Multiple terms may
        be combined using operators `|` (OR), `&` (AND), `~` (NOT), and
        parentheticals to group terms.
    consequent : Consequent term(s) or logical combination thereof, optional
        Consequent terms serving as outputs from this rule. Multiple terms may
        be combined using operators `|` (OR), `&` (AND), `~` (NOT), and
        parentheticals to group terms.
    label : string, optional
        Label to reference the meaning of this rule. Optional, but recommended.

    Notes
    -----
    Fuzzy Rules can be completely built on instantatiation or one can begin
    with an empty Rule and construct interactively by setting `.antecedent`,
    `.consequent`, and `.label` variables.
    """

    aggregate_firing = StatefulProperty(None)

    def __init__(self, antecedent=None, consequent=None, label=None):
        """
        Rule in a fuzzy system, connecting antecedent(s) to consequent(s).

        Parameters
        ----------
        antecedent : Antecedent term(s) or combination thereof, optional
            Antecedent terms serving as inputs to this rule. Multiple terms may
            be combined using operators `|` (OR), `&` (AND), `~` (NOT), and
            parentheticals to group terms.
        consequent : Consequent term(s) or combination thereof, optional
            Consequent terms serving as outputs from this rule. Multiple terms
            may be combined using operators `|` (OR), `&` (AND), `~` (NOT), and
            parentheticals to group terms.
        label : string, optional
        Label to reference the meaning of this rule. Optional, but recommended.
        """
        self.label = label
        self.aggregation_method = FuzzyAggregationMethod()

        self._antecedent = None
        self._consequent = None
        if antecedent is not None:
            self.antecedent = antecedent
        if consequent is not None:
            self.consequent = consequent

    def __repr__(self):
        """
        Concise, readable summary of the fuzzy rule.
        """
        if self.label is not None:
            return self.label
        if len(self.consequent) == 1:
            cons = self.consequent[0]
        else:
            cons = self.consequent
        return "IF %s THEN %s" % (self.antecedent, cons)

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
            raise ValueError("Consquent not set")
        return self._consequent

    @consequent.setter
    def consequent(self, value):
        """
        Accepts consequents in four formats:
         a) Unweighted single output.
            eg: output['term']
         b) Weighted single output
            eg: (output['term']%0.5)
         c) Unweighted multiple output
            eg: (output1['term1'], output2['term2'])
         d) Weighted multiple output
            eg: ( (output1['term1']%1.0), (output2['term2']%0.5) )
        """
        if isinstance(value, Term):
            self._consequent = [WeightedTerm(value, 1.)]

        elif isinstance(value, WeightedTerm):
            self._consequent = [value]

        elif not hasattr(value, '__iter__'):
            raise ValueError("Unexpected consequent type")

        else:

            # Must be one of formats b) to d)
            self._consequent = []
            for i in value:
                if isinstance(i, Term):
                    self._consequent.append(WeightedTerm(i, 1.))
                elif isinstance(i, WeightedTerm):
                    self._consequent.append(i)
                else:
                    raise ValueError("Unexpected consequent type")

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
            graph.add_path([t, self])
            graph = nx.compose(graph, t.parent_variable.graph)

        # Link all consequents from me
        for c in self.consequent:
            assert isinstance(c, WeightedTerm)
            graph.add_path([self, c.term])
            graph = nx.compose(graph, c.term.parent_variable.graph)
        return graph

    def view(self):
        """
        Show a visual representation of this Rule.
        """
        ControlSystemVisualizer(self).view().show()
