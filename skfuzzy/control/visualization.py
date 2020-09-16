"""
visualization.py : Visualize fuzzy control systems.
"""
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np

from ..fuzzymath.fuzzy_ops import interp_membership


class FuzzyVariableVisualizer(object):
    """
    Visualize a fuzzy variable and its membership functions.

    Parameters
    ----------
    fuzzy_var : FuzzyVariable or Term
        Fuzzy variable to be plotted.

    Returns
    -------
    figure : matplotlib Figure
        Figure object containing the visualization.
    """

    def __init__(self, fuzzy_var):
        """
        Initialize the fuzzy variable plot.

        Parameters
        ----------
        fuzzy_var : FuzzyVariable or Term to plot
        """
        from .fuzzyvariable import FuzzyVariable, Term

        # self.term allows us to know if this is a Term quickly, later
        self.term = None
        if isinstance(fuzzy_var, Term):
            self.term = fuzzy_var.label
            self.fuzzy_var = fuzzy_var.parent
        elif isinstance(fuzzy_var, FuzzyVariable):
            self.fuzzy_var = fuzzy_var
        else:
            raise ValueError("`FuzzyVariableVisualizer` can only be called "
                             "with a `FuzzyVariable` or a `Term`.")

        self.fig, self.ax = plt.subplots()
        self.plots = {}

    def view(self, sim=None, *args, **kwargs):
        """
        Visualize this variable and its membership functions with Matplotlib.

        The current output membership function will be shown in bold.

        Returns
        -------
        fig : matplotlib Figure
            The hosting Figure object.
        ax : matplotlib Axis
            The Axis upon which the plot is drawn.

        Notes
        -----
        Matplotlib is used, but ``plt.show()`` is not called. Instead, the
        Figure and Axis are returned, allowing further user customization if
        desired.  In a Jupyter notebook, ``.view()`` will be displayed inline.
        """
        from .controlsystem import (CrispValueCalculator, ControlSystem,
                                    ControlSystemSimulation)

        if sim is None:
            # Create an empty simulation so we can view with default values
            sim = ControlSystemSimulation(ControlSystem())

        self._init_plot()

        crispy = CrispValueCalculator(self.fuzzy_var, sim)
        ups_universe, output_mf, cut_mfs = crispy.find_memberships()

        # Plot the output membership functions
        cut_plots = {}
        zeros = np.zeros_like(ups_universe, dtype=np.float64)

        for label, mf_plot in self.plots.items():
            # Only attempt to plot those with cuts
            if label in cut_mfs:
                # Harmonize color between mf plots and filled overlays
                color = mf_plot[0].get_color()
                cut_plots[label] = self.ax.fill_between(
                    ups_universe, zeros, cut_mfs[label],
                    facecolor=color, alpha=0.4)

        # Plot crisp value if available
        if len(cut_mfs) > 0 and not all(output_mf == 0):
            crisp_value = None
            if hasattr(self.fuzzy_var, 'input'):
                crisp_value = self.fuzzy_var.input[sim]
            elif hasattr(self.fuzzy_var, 'output'):
                crisp_value = self.fuzzy_var.output[sim]

            # Draw the crisp value at the actual cut height
            if crisp_value is not None:
                y = 0.
                for key, term in self.fuzzy_var.terms.items():
                    if key in cut_mfs:
                        y = max(y, interp_membership(self.fuzzy_var.universe,
                                                     term.mf, crisp_value))

                # Small cut values are hard to see, so simply set them to 1
                if y < 0.1:
                    y = 1.

                self.ax.plot([crisp_value] * 2, [0, y],
                             color='k', lw=3, label='crisp value')

        return self.fig, self.ax

    def _init_plot(self):
        # Formatting: limits
        self.ax.set_ylim([0, 1.01])
        self.ax.set_xlim([self.fuzzy_var.universe.min(),
                          self.fuzzy_var.universe.max()])

        # Make the plots
        for key, term in self.fuzzy_var.terms.items():
            # If this is a Term, bold the active mf
            lw = 1
            if self.term == key:
                lw = 3

            self.plots[key] = self.ax.plot(self.fuzzy_var.universe,
                                           term.mf,
                                           label=key,
                                           linewidth=lw)

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
    """
    Visualize a control system with Matplotlib and NetworkX.
    """
    def __init__(self, control_system):
        """
        Initialization method for the ControlSystemVisualizer.

        Parameters
        ----------
        control_system : ControlSystem

        Returns
        -------

        """
        self.ctrl = control_system

        self.fig, self.ax = plt.subplots()

    def view(self):
        """
        View the visualization.

        Returns
        -------
        fig : matplotlib Figure
            The hosting Figure object.
        ax : matplotlib Axis
            The Axis upon which the plot is drawn.

        Notes
        -----
        This method uses the NetworkX ``draw`` command.  If further
        customization is desired, the matplotlib Figure/Axis objects
        are returned.  In a Jupyter notebook, these will be displayed
        inline.
        """
        nx.draw(self.ctrl.graph, ax=self.ax)
        return self.fig, self.ax

    def view_n(self):
        """
        View the network visualization.

        Returns
        -------
        fig : matplotlib Figure
            The hosting Figure object.
        ax : matplotlib Axis
            The Axis upon which the plot is drawn.

        Notes
        -----
        This method uses the NetworkX ``draw_networkx`` command, to check that
        all Mebership Functions, MF, are used (green) among the rules. The plot
        also writes the name of the MF. If further customization is desired,
        the matplotlib Figure/Axis objects are returned.  In a Jupyter
        notebook, these will be displayed inline.
        If the network model fails, it will return the ordenary view.
        """
        try:
            graph, color_list = self.ctrl.graph_n
            colors = []
            c_nodes = []
            c_colors = []
            for c_node, c_color in color_list:
                if c_node in c_nodes:
                    prev_color = c_colors[c_nodes.index(c_node)]
                    if prev_color == 'green':
                        continue
                    elif prev_color == 'red':
                        if c_color == 'green':
                            c_colors[c_nodes.index(c_node)] = 'green'
                else:
                    c_nodes.append(c_node)
                    c_colors.append(c_color)
            for node in graph:
                colors.append(c_colors[c_nodes.index(node)])
            nx.draw_networkx(graph, node_color=colors)
        except ValueError:
            nx.draw(self.ctrl.graph, ax=self.ax)
        return self.fig, self.ax
