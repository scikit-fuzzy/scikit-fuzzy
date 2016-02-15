"""
rule.py : Contains `Rule` object which is used to connected
atecedents with conqeuents in a `ControlSystem`.
"""

import numpy as np
import networkx as nx
from weakref import WeakKeyDictionary
from .antecedent_consequent import Antecedent, Consequent
from .fuzzyvariable import (FuzzyVariable, FuzzyVariableTerm,
                            FuzzyAggregationMethod,
                            FuzzyVariableTermAggregate, TermPrimitive)
from .visualization import ControlSystemVisualizer
from .state import StatefulProperty, StatefulProperty

try:
    from collections import OrderedDict
except ImportError:
    from .ordereddict import OrderedDict


class WeightedConsequent(object):

    activation = StatefulProperty(None)

    def __init__(self, term, weight):
        assert isinstance(term, FuzzyVariableTerm)
        self.term = term
        self.weight = weight

    def __repr__(self):
        if self.weight == 1.:
            return self.term.full_label
        else:
            return "%s@%0.2f%%" % (self.term.full_label, self.weight)


class Rule(object):

    aggregate_firing = StatefulProperty(None)

    def __init__(self, antecedent=None, consequent=None, label=None):
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
        Print a concise, readable summary of the fuzzy rule.
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
        if self._antecedent is None:
            raise ValueError("Antecedent not set")
        return self._antecedent
    @antecedent.setter
    def antecedent(self, value):
        if not isinstance(value, TermPrimitive):
            raise ValueError("Unexpected antecedent type")
        # Should be either FuzzyVariableTerm or FuzzyVariableTermAggregate
        self._antecedent = value



    @property
    def antecedent_terms(self):
        # Grab all the terms that make up my antecedent clause
        terms = []
        def _find_terms(obj):
            if isinstance(obj, FuzzyVariableTerm):
                terms.append(obj)
            elif obj is None:
                pass
            else:
                assert isinstance(obj, FuzzyVariableTermAggregate)
                _find_terms(obj.term1)
                _find_terms(obj.term2)
        _find_terms(self.antecedent)
        return terms

    @property
    def consequent(self):
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
        if isinstance(value, FuzzyVariableTerm):
            self._consequent = [WeightedConsequent(value, 1.)]

        elif isinstance(value, WeightedConsequent):
            self._consequent = [value]

        elif not hasattr(value, '__iter__'):
            raise ValueError("Unexpected consequent type")

        else:

            # Must be one of formats b) to d)
            self._consequent = []
            for i in value:
                if isinstance(i, FuzzyVariableTerm):
                    self._consequent.append(WeightedConsequent(i, 1.))
                elif isinstance(i, WeightedConsequent):
                    self._consequent.append(i)
                else:
                    raise ValueError("Unexpected consequent type")

    @property
    def graph(self):
        graph = nx.DiGraph()
        # Link all antecedents to me by decomposing
        #  FuzzyVariableTermAggregate down to just FuzzyVariableTerms
        for t in self.antecedent_terms:
            assert isinstance(t, FuzzyVariableTerm)
            graph.add_path([t, self])
            graph = nx.compose(graph, t.parent_variable.graph)

        # Link all consequents from me
        for c in self.consequent:
            assert isinstance(c, WeightedConsequent)
            graph.add_path([self, c.term])
            graph = nx.compose(graph, c.term.parent_variable.graph)
        return graph


    def view(self):
        ControlSystemVisualizer(self).view().show()