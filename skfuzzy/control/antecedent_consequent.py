"""
antecedent_consequent.py : Contains Antecedent and Consequent classes.
"""
import numpy as np
from ..fuzzymath import interp_membership
from .fuzzyvariable import FuzzyVariable
from ..defuzzify import defuzz

try:
    from collections import OrderedDict
except ImportError:
    from .ordereddict import OrderedDict


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
    def __init__(self, universe, label):
        """""" + Antecedent.__doc__
        super(Antecedent, self).__init__(universe, label)
        self.input = None
        self.output = OrderedDict()
        self.__name__ = 'Antecedent'

    def _chk(self):
        """
        Guarantee a compute operation can be attempted.
        """
        if (len(self.mf.keys()) is 0 or
                self.input is None):

            raise ValueError("Membership function(s) and an input must be "
                             "set before computing.")

    def set_input(self, variable):
        self.input = variable

    def compute(self, active=None):
        """
        Computes the activity of each membership function at the current input.

        Parameters
        ----------
        active : str, optional
            If provided, the firing for specific membership function
            ``'active'`` will be calculated and returned.

        Notes
        -----
        If ``active`` is None or not provided, this method calculates the
        firing for every membership function in the ``FuzzyVariable``,
        storing results in dictionary form as ``FuzzyVariable.output``.
        Nothing is returned.
        """
        self._chk()
        if active is None:
            for label, value in self.mf.iteritems():
                self.output[label] = (
                    interp_membership(self.universe, value, self.input))
            return None

        else:
            return interp_membership(self.universe,
                                     self.mf[active], self.input)

    def view(self, *args, **kwargs):
        """
        Visualize this antecedent and its membership functions with Matplotlib.
        """
        self._variable_figure_generator(self, *args, **kwargs)

        # If input is available, draw the input as well
        if self.input is not None:
            if self.output is None:
                self.compute()

            max_activity = 0
            for label, activity in self.output.iteritems():
                if activity > max_activity:
                    max_activity = activity

            self._ax.plot([self.input] * 2, [0, max_activity],
                          color='k', lw=3, label='input')
        self._fig.show()


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
    def __init__(self, universe, label):
        """""" + Consequent.__doc__
        super(Consequent, self).__init__(universe, label)
        self.cuts = OrderedDict()
        self.cut_mfs = OrderedDict()
        self.output_mf = np.zeros_like(universe, dtype=np.float64)
        self.output = None
        self.__name__ = 'Consequent'

    def _chk(self):
        """
        Guarantee a compute operation can be attempted.
        """
        if (len(self.mf.keys()) is 0 or
                len(self.cuts) is 0):

            raise ValueError("Membership function(s) and results from at "
                             "least one rule must be set before computing.")

    def set_patch(self, label, cut):
        """
        Input method from a fuzzy rule on a consequent membership function.

        Parameters
        ----------
        label : string
            Memebership function the rule is associated with.
        cut : float
            Floating-point value from 0 to 1 calculated from current inputs
            via a fuzzy rule.
        """
        # Add a new cut if none related exist
        if label not in self.cuts:
            self.cuts[label] = cut

        # Update existing cut if new one is greater
        else:
            if self.cuts[label] < cut:
                self.cuts[label] = cut

    def compute(self, mode='centroid'):
        """
        Calculates the output of the system for this consequent variable.

        Parameters
        ----------
        mode : string, optional
            Defuzzification method to be used. Default: 'centroid'.
            See ``skfuzzy.defuzz`` for additional defuzzification methods.

        Notes
        -----
        Result is stored in the ``.output`` variable.

        See Also
        --------
        SKFUZZY.DEFUZZ
        """
        self._chk()

        # Build the cut output membership functions
        self.update()

        # Defuzzify
        self.output = defuzz(self.universe, self.output_mf, mode)

    def update(self):
        self._chk()

        # Clear prior output, if any
        self.output_mf = np.zeros_like(self.universe, dtype=np.float64)

        # Build output membership function
        for label, cut in self.cuts.iteritems():
            self.cut_mfs[label] = np.minimum(cut, self.mf[label])
            np.maximum(self.output_mf, self.cut_mfs[label], self.output_mf)

    def view(self, *args, **kwargs):
        """
        Visualize this consequent and its membership functions with Matplotlib.
        Additionally, show the current output membership functions.
        """
        self._variable_figure_generator(self, *args, **kwargs)

        # Plot the output membership functions
        self._cut_plots = {}
        zeros = np.zeros_like(self.universe, dtype=np.float64)

        for label, mf_plot in self._plots.iteritems():
            # Only attempt to plot those with cuts
            if label in self.cuts and label in self.cut_mfs:
                # Harmonize color between mf plots and filled overlays
                color = mf_plot[0].get_color()
                self._cut_plots[label] = self._ax.fill_between(
                    self.universe, zeros, self.cut_mfs[label],
                    facecolor=color, alpha=0.4)

        # Plot defuzzified output if available
        if self.output is not None:
            y = interp_membership(self.universe, self.output_mf, self.output)
            self._ax.plot([self.output] * 2, [0, y],
                          color='k', lw=3, label='output')

        self._fig.show()
