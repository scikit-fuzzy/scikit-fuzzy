"""
antecedent_consequent.py : Contains Antecedent and Consequent classes.
"""
import numpy as np
import networkx as nx

from .state import StatefulProperty
from .fuzzyvariable import FuzzyVariable


def accumulation_max(*args):
    """
    Take the maximum of input values/arrays.

    This is the default OR aggregation method for a fuzzy Rule.
    """
    return np.fmax(*args)


def accumulation_mult(*args):
    """
    Multiply input values/arrays.

    This may be used as an alternate AND aggregation method for a fuzzy Rule.
    """
    return np.multiply(*args)


class Antecedent(FuzzyVariable):
    """
    Antecedent (input/sensor) variable for a fuzzy control system.

    Parameters
    ----------
    universe : array-like
        Universe variable. Must be 1-dimensional and convertible to a NumPy
        array.
    label : string
        Name of the universe variable.
    """

    # Customized subclass of `FuzzyVariable`
    input = StatefulProperty(None)

    def __init__(self, universe, label):
        """""" + Antecedent.__doc__
        super(Antecedent, self).__init__(universe, label)
        self.__name__ = 'Antecedent'

    @property
    def graph(self):
        """
        NetworkX graph which connects this Antecedent with its Term(s).
        """
        g = nx.DiGraph()
        for t in self.terms.values():
            g.add_edge(self, t)
        return g


class Consequent(FuzzyVariable):
    """
    Consequent (output/control) variable for a fuzzy control system.

    Parameters
    ----------
    universe : array-like
        Universe variable. Must be 1-dimensional and convertible to a NumPy
        array.
    label : string
        Name of the universe variable.
    defuzzify_method : string
        name of method used for defuzzification, defaults to 'centroid'

    Notes
    -----
    The ``label`` string chosen must be unique among Antecedents and
    Consequents in the ``ControlSystem``.
    """

    # Customized subclass of `FuzzyVariable`
    output = StatefulProperty(None)

    def __init__(self, universe, label, defuzzify_method='centroid'):
        """""" + Consequent.__doc__
        super(Consequent, self).__init__(universe, label, defuzzify_method)
        self.__name__ = 'Consequent'

        # Default accumulation method is to take the max of any cut
        self.accumulation_method = accumulation_max

    @property
    def graph(self):
        """
        NetworkX graph which connects this Consequent with its Term(s).
        """
        g = nx.DiGraph()
        for t in self.terms.values():
            g.add_edge(t, self)
        return g
