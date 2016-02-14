"""
visualization.py : Contains classes to help with visualizing a control system
"""
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

from .. import defuzz, interp_membership


class FuzzyVariableVisualizer(object):

    def __init__(self, fuzzy_var):
        """

        Parameters
        ----------
        fuzzy_var : FuzzyVariable to plot

        Returns
        -------

        """
        from .fuzzyvariable import FuzzyVariable
        assert isinstance(fuzzy_var, FuzzyVariable)
        self.fuzzy_var = fuzzy_var
        self.fig, self.ax = plt.subplots()
        self.plots = {}

    def view(self, sim=None, *args, **kwargs):
        """
        Visualize this variable and its membership functions with Matplotlib.
        Additionally, show the current output membership functions.
        """
        from .controlsystem import (CrispValueCalculator, ControlSystem,
                                    ControlSystemSimulation)
        if sim is None:
            # Create an empty simulation so we can view with default values
            sim = ControlSystemSimulation(ControlSystem())

        self._init_plot()

        crispy = CrispValueCalculator(self.fuzzy_var, sim)
        output_mf, cut_mfs = crispy.find_memberships()

        # Plot the output membership functions
        cut_plots = {}
        zeros = np.zeros_like(self.fuzzy_var.universe, dtype=np.float64)

        for label, mf_plot in self.plots.items():
            # Only attempt to plot those with cuts
            if label in cut_mfs:
                # Harmonize color between mf plots and filled overlays
                color = mf_plot[0].get_color()
                cut_plots[label] = self.ax.fill_between(
                    self.fuzzy_var.universe, zeros, cut_mfs[label],
                    facecolor=color, alpha=0.4)

        # Plot defuzzified output if available
        if len(cut_mfs) > 0 and not all(output_mf == 0):
            crip_value = defuzz(self.fuzzy_var.universe, output_mf,
                                self.fuzzy_var.defuzzify_method)
            if crip_value is not None:
                y = interp_membership(self.fuzzy_var.universe,
                                      output_mf, crip_value)
                if y < 0.1:
                    y = 1.
                self.ax.plot([crip_value] * 2, [0, y],
                              color='k', lw=3, label='crisp value')

        return self.fig

    def _init_plot(self):
        # Formatting: limits
        self.ax.set_ylim([0, 1])
        self.ax.set_xlim([self.fuzzy_var.universe.min(),
                     self.fuzzy_var.universe.max()])

        # Make the plots
        for key, term in self.fuzzy_var.terms.items():
            self.plots[key] = self.ax.plot(self.fuzzy_var.universe,
                                             term.mf,
                                             label=key,
                                             lw=1)

        # Place legend in upper left
        self.ax.legend(framealpha=0.5)

        # Turn off top/right axes
        self.ax.spines['top'].set_visible(False)
        self.ax.spines['right'].set_visible(False)
        self.ax.get_xaxis().tick_bottom()
        self.ax.get_yaxis().tick_left()

        # Ticks outside the axes
        self.ax.tick_params(direction='out')

        # Label the axes
        self.ax.set_ylabel('Membership')
        self.ax.set_xlabel(self.fuzzy_var.label)


class ControlSystemVisualizer(object):

    def __init__(self, control_system):
        """

        Parameters
        ----------
        control_system : ControlSystem

        Returns
        -------

        """
        self.ctrl = control_system


        self.fig = plt.figure()
        self.ax = self.fig.add_axes((0,0,1,1))

    def view(self):
        nx.draw(self.ctrl.graph, ax=self.ax)
        return self.fig