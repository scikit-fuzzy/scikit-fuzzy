"""
term.py : Framework to create fuzzy terms.

Most notably, contains the `Term` and `WeightedTerm` objects which are used to
identify specific membership functions attached to Antecedents or
Consequents when constructing fuzzy Rules.

Terms have redefined logical operators which enable the simple and elegant
combination of several during Rule creation.
"""
import numpy as np

from .state import StatefulProperty
from .visualization import FuzzyVariableVisualizer


class TermPrimitive(object):
    """
    Marker class for type checking when a term or term aggregate is expected.
    """

    def membership_value(self):
        raise NotImplementedError("Implement in concrete class")

    def __and__(self, other):
        if not isinstance(other, TermPrimitive):
            raise ValueError("Can only construct 'AND' from the term "
                             "of a fuzzy variable")

        return TermAggregate(self, other, 'and')

    def __or__(self, other):
        if not isinstance(other, TermPrimitive):
            raise ValueError("Can only construct 'OR' from the term "
                             "of a fuzzy variable")

        return TermAggregate(self, other, 'or')

    def __invert__(self):
        return TermAggregate(self, None, 'not')


class Term(TermPrimitive):
    """
    A Term is a universe and associated specific membership function.

    For example, if one were creating a FuzzyVariable with a simple three-
    point Likert scale, three `Terms` would be created named 'poor', 'average',
    and 'good'.
    """

    # State variables
    membership_value = StatefulProperty(None)
    cuts = StatefulProperty({})

    def __init__(self, label, membership_function):
        super(Term, self).__init__()
        self.label = label
        self.parent = None
        self.mf = membership_function

    @property
    def full_label(self):
        """Term with parent.  Ex: velocity['fast']"""
        if self.parent is None:
            raise ValueError("This term must be bound to a parent first")
        return self.parent.label + "[" + self.label + "]"

    def view(self, *args, **kwargs):
        """""" + FuzzyVariableVisualizer.view.__doc__
        fig, ax = FuzzyVariableVisualizer(self).view(*args, **kwargs)
        fig.show()

    def __repr__(self):
        return self.full_label

    def __mod__(self, other):
        from .rule import WeightedTerm
        if isinstance(other, int):
            other = float(other)
        else:
            assert isinstance(other, float)
        return WeightedTerm(self, other)


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
            return "{}@{:0.2f}%".format(self.term.full_label, self.weight)


class FuzzyAggregationMethods(object):
    def __init__(self, and_func=np.fmin, or_func=np.fmax):
        # Default and to OR = max and AND = min
        self.and_func = and_func
        self.or_func = or_func


class _MembershipValueAccessor(object):

    def __init__(self, agg):
        assert isinstance(agg, TermAggregate)
        self.agg = agg

    def __getitem__(self, key):
        from .controlsystem import ControlSystemSimulation
        assert isinstance(key, ControlSystemSimulation)

        # Perform aggregation to determine membership
        term1 = self.agg.term1.membership_value[key]
        if self.agg.term2 is not None:
            term2 = self.agg.term2.membership_value[key]

        if self.agg.kind == 'and':
            return self.agg.agg_methods.and_func(term1, term2)
        elif self.agg.kind == 'or':
            return self.agg.agg_methods.or_func(term1, term2)
        elif self.agg.kind == 'not':
            return 1. - self.agg.term1.membership_value[key]
        else:
            raise NotImplementedError()


class TermAggregate(TermPrimitive):
    """
    Used to track the creation of AND and OR clauses used when building
    the antecedent of a rule.
    """

    def __init__(self, term1, term2, kind):
        assert isinstance(term1, TermPrimitive)
        if kind in ('and', 'or'):
            assert isinstance(term2, TermPrimitive)
        elif kind == 'not':
            assert term2 is None, "NOT (~) operates on a single Term, not two."
        else:
            raise ValueError("Unexpected kind")

        self.term1 = term1
        self.term2 = term2
        self.kind = kind
        self._agg_methods = FuzzyAggregationMethods()
        self.membership_value = _MembershipValueAccessor(self)

    def __repr__(self):
        def _term_to_str(term):
            if isinstance(term, Term):
                return term.full_label
            elif isinstance(term, TermAggregate):
                return "({!s})".format(term)

        if self.kind == 'not':
            return "NOT-{}".format(_term_to_str(self.term1))

        return "{} {} {}".format(_term_to_str(self.term1),
                                 self.kind.upper(),
                                 _term_to_str(self.term2))

    @property
    def agg_methods(self):
        return self._agg_methods

    @agg_methods.setter
    def agg_methods(self, agg_methods):
        if not isinstance(agg_methods, FuzzyAggregationMethods):
            raise ValueError("Expected FuzzyAggregationMethods")
        self._agg_methods = agg_methods

        # Propegate agg method down to all agg terms below me
        for term in (self.term1, self.term2):
            if isinstance(term, TermAggregate):
                term.agg_methods = agg_methods
