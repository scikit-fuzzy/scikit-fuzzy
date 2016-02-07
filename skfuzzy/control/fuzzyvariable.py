"""
fuzzyvariable.py : Contains base fuzzy variable class.
"""
import numpy as np
import matplotlib.pyplot as plt
from ..membership import trimf

try:
    from collections import OrderedDict
except ImportError:
    from .ordereddict import OrderedDict


class FuzzyVariableAdjective(object):
    """
    An adjective and associated member function for a fuzzy varaible.
    For example, if one were creating a FuzzyVariable with a simple three-point
    liker scale, three `FuzzyVariableAdjective` would be created: poor, average,
    and good.
    """

    def __init__(self, label, membership_function):
        self.label = label
        self.mf = membership_function

        self.parent_variable = None
        self.membership_value = 0

    @property
    def not_(self):
        """
        Complement of this adjective.

        Returns
        -------
        not self
        """
        result = FuzzyVariableAdjective("NOT-" + self.label, 1. - self.mf)
        result.parent_variable = self.parent_variable
        result.membership_value = 1. - self.membership_value
        return result

    @property
    def full_label(self):
        """Adjective with parent.  Ex: velocity['fast']"""
        if self.parent_variable is None:
            raise ValueError("This adjective must be bound to a parent first")
        return self.parent_variable.label + "['" + self.label + "']"

    def __repr__(self):
        return self.full_label

    def view(self, *args, **kwargs):
        raise NotImplementedError()
        # TODO: Implement this aspect of the code that was in FuzzyVariable
        # Plot the active membership function (if any) heavier
        if key == self.active:
            lw = 2
        else:
            lw = 1


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

    Methods
    -------

    Notes
    -----
    This class is designed as the base class underlying the Antecedent and
    Consequent classes, not for individual use.
    """
    def __init__(self, universe, label):
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
        self.adjectives = OrderedDict()
        self._id = id(self)
        self.output = None

    def __repr__(self):
        return "{0}: {1}".format(self.__name__, self.label)

    def __len__(self):
        return self.universe.size

    def __getitem__(self, key):
        """
        Calling variable['label'] will activate 'label' membership function.
        """
        if key in self.adjectives.keys():
            return self.adjectives[key]
        else:
            # Build a pretty list of available mf labels and raise an
            # informative error message
            options = ''
            i0 = len(self.adjectives) - 1
            i1 = len(self.adjectives) - 2
            for i, available_key in enumerate(self.adjectives.keys()):
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
        Enables new membership functions or adjectives to be added with the
        syntax::

          variable['new_label'] = new_mf
        """
        if isinstance(item, FuzzyVariableAdjective):
            if item.label != key:
                raise ValueError("Adjective's label must match new key")
            if item.parent_variable is not None:
                raise ValueError("Adjective must not already have a parent")
        else:
            # Try to create an adjective
            item = FuzzyVariableAdjective(key, np.asarray(item))

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
        item.parent_variable = self
        self.adjectives[key] = item

    def _variable_figure_generator(self, *args, **kwargs):
        """
        Creates a base figure representation of this fuzzy variable.
        """
        # Assign plot to hidden attributes for bookkeeping in child classes
        self._fig, self._ax = plt.subplots()
        self._plots = {}

        # Formatting: limits
        self._ax.set_ylim([0, 1])
        self._ax.set_xlim([self.universe.min(), self.universe.max()])

        # Make the plots
        for key, adj in self.adjectives.items():
            self._plots[key] = self._ax.plot(self.universe,
                                             adj.mf,
                                             label=key,
                                             lw=1)

        # Place legend in upper left
        self._ax.legend(framealpha=0.5)

        # Ticks outside the axes
        self._ax.tick_params(direction='out')

        # Label the axes
        self._ax.set_ylabel('Membership')
        self._ax.set_xlabel(self.label)

        # Not returned - child classes use these attributes in .view() methods
        return None

    def automf(self, number=5, variable_type='quality', invert=False):
        """
        Automatically populates the universe with membership functions.

        Parameters
        ----------
        number : [3, 5, 7]
            Number of membership functions to create. Must be an odd integer.
            At present, only 3, 5, or 7 are supported.
        variable_type : string
            Type of variable this is. Accepted arguments are
            * 'quality' : Continuous variable, higher values are better.
            * 'quant' : Quantitative variable, no value judgements.
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

        if number not in [3, 5, 7]:
            raise ValueError("Only number = 3, 5, or 7 supported.")

        limits = [self.universe.min(), self.universe.max()]
        universe_range = limits[1] - limits[0]
        widths = [universe_range / ((number - 1) / 2.)] * int(number)
        centers = np.linspace(limits[0], limits[1], number)

        abcs = [[c - w / 2, c, c + w / 2] for c, w in zip(centers, widths)]

        # Clear existing adjectives, if any
        self.adjectives = OrderedDict()
        if self.__name__ == 'Antecedent':
            self.output = OrderedDict()
        else:
            self.output = None

        # Repopulate
        for name, abc in zip(names, abcs):
            self[name] = trimf(self.universe, abc)
