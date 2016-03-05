"""
antecedent_consequent.py : Contains Antecedent and Consequent classes.
"""
import numpy as np
import networkx as nx

from .state import StatefulProperty
from ..fuzzymath import interp_membership
from .fuzzyvariable import FuzzyVariable
from ..defuzzify import defuzz

try:
    from collections import OrderedDict
except ImportError:
    from .ordereddict import OrderedDict



def accu_max(*args):
    return np.max(args)


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
        g = nx.DiGraph()
        for t in self.terms.values():
            g.add_path([self, t])
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

    Notes
    -----
    The ``label`` string chosen must be unique among Antecedents and
    Consequents in the ``ControlSystem``.
    """
    # Customized subclass of `FuzzyVariable`

    output = StatefulProperty(None)

    def __init__(self, universe, label):
        """""" + Consequent.__doc__
        super(Consequent, self).__init__(universe, label)
        self.__name__ = 'Consequent'

        # Default accumulation method is to take the max of any cut
        self.accumulation_method = accu_max

    @property
    def graph(self):
        g = nx.DiGraph()
        for t in self.terms.values():
            g.add_path([t, self])
        return g
