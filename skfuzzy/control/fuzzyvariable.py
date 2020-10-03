"""
fuzzyvariable.py : Contains the base fuzzy variable class, FuzzyVariable.
"""
from collections import OrderedDict

import numpy as np

from .term import Term
from .visualization import FuzzyVariableVisualizer
from ..membership import trimf


class FuzzyVariable(object):
    """
    Base class containing universe variable & associated membership functions.

    Parameters
    ----------
    universe : array-like
        Universe variable. Must be 1-dimensional and convertible to a NumPy
        array. Required.
    label : string
        Name of the universe variable. Optional.
    defuzzify_method : string
        name of method used for defuzzification, defaults to 'centroid'
    Methods
    -------

    Notes
    -----
    This class is designed as the base class underlying the Antecedent and
    Consequent classes, not for individual use.
    """

    def __init__(self, universe, label, defuzzify_method='centroid'):
        """
        Initialization of fuzzy variable

        Parameters
        ----------
        universe : array-like
            Universe variable. Must be 1-dimensional and convertible to a NumPy
            array.
        label : string
            Unique name of the universe variable, e.g., 'food' or 'velocity'.
        """
        self.universe = np.asarray(universe)
        self.label = label
        self.defuzzify_method = defuzzify_method
        self.terms = OrderedDict()

        self._id = id(self)

    def __repr__(self):
        return "{0}: {1}".format(self.__name__, self.label)

    def __len__(self):
        return self.universe.size

    def __getitem__(self, key):
        """
        Calling `variable['label']` will return the 'label' term
        """
        if key in self.terms.keys():
            return self.terms[key]
        else:
            # Build a pretty list of available mf labels and raise an
            # informative error message
            options = ''
            i0 = len(self.terms) - 1
            i1 = len(self.terms) - 2
            for i, available_key in enumerate(self.terms.keys()):
                if i == i1:
                    options += "'" + str(available_key) + "', or "
                elif i == i0:
                    options += "'" + str(available_key) + "'."
                else:
                    options += "'" + str(available_key) + "'; "
            raise ValueError("Membership function '{0}' does not exist for "
                             "{1} {2}.\n"
                             "Available options: {3}".format(
                                 key, self.__name__, self.label, options))

    def __setitem__(self, key, item):
        """
        Enable terms to be added with the syntax::

          variable['new_label'] = new_mf
        """
        if isinstance(item, Term):
            if item.label != key:
                raise ValueError("Term's label must match new key")
            if item.parent is not None:
                raise ValueError("Term must not already have a parent")
        else:
            # Try to create a term from item, assuming it is a membership
            # function
            item = Term(key, np.asarray(item))

        mf = item.mf

        if mf.size != self.universe.size:
            raise ValueError("New membership function {0} must be equivalent "
                             "in length to the universe variable.\n"
                             "Expected {1}, got {2}.".format(
                                 key, self.universe.size, mf.size))

        if (mf.max() > 1. + 1e-6) or (mf.min() < 0 - 1e-6):
            raise ValueError("Membership function {0} contains values out of "
                             "range. Allowed range is [0, 1].".format(key))

        # If above pass, add the new membership function
        item.parent = self
        self.terms[key] = item

    def __contains__(self, item):
        return item in self.terms

    def __iter__(self):
        return iter(self.terms)

    def view(self, *args, **kwargs):
        """""" + FuzzyVariableVisualizer.view.__doc__
        fig, ax = FuzzyVariableVisualizer(self).view(*args, **kwargs)
        fig.show()

    def automf(self, number=5, variable_type='quality', names=None,
               invert=False):
        """
        Automatically populate the universe with membership functions.

        Parameters
        ----------
        number : integer or list of names
            Number of membership functions to create. For fully automated use,
            supply 3, 5, or 7.  Any number may be generated, if you provide
            an appropriately sized list of `names`.  If names are provided,
            they are used in lieu of the default names below.
        variable_type : string
            Type of variable this is. Accepted arguments are
            * 'quality' : Continuous variable, higher values are better.
            * 'quant' : Quantitative variable, no value judgements.
        names : list
            List of names to use when creating membership functions if you wish
            to override the default. Naming proceeds from lowest to highest,
            unless invert is True.
        invert : bool
            Reverses the naming order if True. Membership function peaks still
            march from lowest to highest.

        Notes
        -----
        This convenience function allows quick construction of fuzzy variables
        with overlapping, triangular membership functions.

        It uses a standard naming convention defined for ``'quality'`` as::

        * dismal
        * poor
        * mediocre
        * average (always middle)
        * decent
        * good
        * excellent

        and for ``'quant'`` as::

        * lowest
        * lower
        * low
        * average (always middle)
        * high
        * higher
        * highest

        where the names on either side of ``'average'`` are used as needed to
        create 3, 5, or 7 membership functions.
        """
        if names is not None:
            # set number based on names passed
            number = len(names)
        else:
            if number not in [3, 5, 7]:
                raise ValueError("If number is not 3, 5, or 7, "
                                 "you must pass a list of names "
                                 "equal in length to number.")

            if variable_type.lower() == 'quality':
                names = ['dismal',
                         'poor',
                         'mediocre',
                         'average',
                         'decent',
                         'good',
                         'excellent']
            else:
                names = ['lowest',
                         'lower',
                         'low',
                         'average',
                         'high',
                         'higher',
                         'highest']

            if number == 3:
                if variable_type.lower() == 'quality':
                    names = names[1:6:2]
                else:
                    names = names[2:5]
            if number == 5:
                names = names[1:6]

        if invert is True:
            names = names[::-1]

        limits = [self.universe.min(), self.universe.max()]
        universe_range = limits[1] - limits[0]
        widths = [universe_range / ((number - 1) / 2.)] * int(number)
        centers = np.linspace(limits[0], limits[1], number)

        abcs = [[c - w / 2, c, c + w / 2] for c, w in zip(centers, widths)]

        # Clear existing adjectives, if any
        self.terms = OrderedDict()

        # Repopulate
        for name, abc in zip(names, abcs):
            self[name] = trimf(self.universe, abc)
