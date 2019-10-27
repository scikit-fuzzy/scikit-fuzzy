"""
controlsystem.py : Framework for the new fuzzy logic control system API.
"""
from __future__ import print_function, division

import numpy as np
import networkx as nx
from warnings import warn

from ..fuzzymath.fuzzy_ops import _interp_universe_fast
from skfuzzy import interp_membership, defuzz
from .fuzzyvariable import FuzzyVariable
from .antecedent_consequent import Antecedent, Consequent
from .term import Term, WeightedTerm, TermAggregate
from .rule import Rule
from .visualization import ControlSystemVisualizer

try:
    from collections import OrderedDict
except ImportError:
    from .ordereddict import OrderedDict


class ControlSystem(object):
    """
    Base class to contain a Fuzzy Control System.

    Parameters
    ----------
    rules : Rule or iterable of Rules, optional
        If provided, the system is initialized and populated with a set of
        fuzzy Rules (see ``skfuzzy.control.Rule``). This is optional. If
        omitted the ControlSystem can be built interactively.
    """

    def __init__(self, rules=None):
        """
        Initialization method for the fuzzy ControlSystem object.
        """ + '\n'.join(ControlSystem.__doc__.split('\n')[1:])
        self.graph = nx.DiGraph()
        self._rule_generator = RuleOrderGenerator(self)

        # Construct a system from provided rules, if given
        if rules is not None:
            if hasattr(rules, '__iter__'):
                for rule in rules:
                    self.addrule(rule)
            else:
                try:
                    self.addrule(rules)
                except:
                    raise ValueError("Optional argument `rules` must be a "
                                     "FuzzyRule or iterable of FuzzyRules.")

    @property
    def rules(self):
        """
        Generator which yields Rules in the system in calculation order.
        """
        # We have to expose the rules in the order from antecedents to
        #  consequences.  For example if we have:
        #  Antecedent -> rule1 -> Intermediary -> rule2 -> Consequence
        #  if we expose rule1 before rule2, we won't calculate correctly
        return self._rule_generator

    @property
    def antecedents(self):
        """Generator which yields Antecedents in the system."""
        for node in self.graph.nodes():
            if isinstance(node, Antecedent):
                yield node

    @property
    def consequents(self):
        """Generator which yields Consequents in the system."""
        for node in self.graph.nodes():
            if isinstance(node, Consequent):
                yield node

    @property
    def fuzzy_variables(self):
        """
        Generator which yields fuzzy variables in the system.

        This includes Antecedents, Consequents, and Intermediaries.
        """
        for node in self.graph.nodes():
            if isinstance(node, FuzzyVariable):
                yield node

    def addrule(self, rule):
        """
        Add a new rule to the system.
        """
        if not isinstance(rule, Rule):
            raise ValueError("Input rule must be a Rule object!")

        # Ensure no label duplication
        labels = []
        for r in self.rules:
            if r.label in labels:
                raise ValueError("Input rule cannot have same label, '{0}', "
                                 "as any other rule.".format(r.label))
            labels.append(r.label)

        # Combine the two graphs, which may not be disjoint
        self.graph = nx.compose(self.graph, rule.graph)
        try:
            self.add_rule_n(rule)
        except:
            pass

    def add_rule_n(self, rule):
        graph, color = rule.graph_n
        U = nx.Graph()
        if 'graph_n' in dir(self):
            U.add_edges_from(self.graph_n[0].edges())
            U.add_nodes_from(self.graph_n[0].nodes())
        U.add_edges_from(graph.edges())
        U.add_nodes_from(graph.nodes())
        if not 'colors' in dir(self):
            self.colors = []
            self.colors.extend(color)
        else:
            self.colors.extend(color)
        self.graph_n = U, self.colors

    def view(self):
        """
        View a representation of the system NetworkX graph.
        """
        fig, ax = ControlSystemVisualizer(self).view()
        fig.show()

    def view_n(self):
        """
        View a representation of the system NetworkX graph.
        """
        fig, ax = ControlSystemVisualizer(self).view_n()
        fig.show()


def _is_ndarray(object):
    """
    Boolean response if object passed is a NumPy ndarray.
    """
    return isinstance(object, np.ndarray)


class _InputAcceptor(object):
    """
    Set a single input value to an Antecedent in this ControlSystemSimulation.

    Inputs can be singletons or arrays, but all Antecedent inputs must match.
    If they are arrays, all must have the exact same shape.  If they are
    arrays, the output(s) will carry the same shape as the inputs.
    """
    def __init__(self, simulation):
        assert isinstance(simulation, ControlSystemSimulation)
        self.sim = simulation

    def __setitem__(self, key, value):
        # Find the antecedent we should set the input for
        matches = [n for n in self.sim.ctrl.graph.nodes()
                   if isinstance(n, Antecedent) and n.label == key]

        if len(matches) == 0:
            raise ValueError("Unexpected input: " + key)
        assert len(matches) == 1
        var = matches[0]

        # Inform the simulation there is an array input
        if _is_ndarray(value):
            self.sim._array_inputs = True
            # Check if this is the correct array input
            if self.sim._array_shape is not None:
                if self.sim._array_shape != value.shape:
                    warn("Input array is shape {0}, which is different from "
                         "previous array(s) which were {1}.  This may cause "
                         "problems, unless you are replacing all "
                         "inputs.".format(value.shape, self.sim._array_shape))
            self.sim._array_shape = value.shape
        else:
            # Input isn't an array, but we saw arrays before... reset!
            if self.sim._array_inputs is not False:
                warn("This system previously accepted array inputs.  It will "
                     "be reset to operate on the singleton input just passed.")
                self.sim.reset()
                self.sim._array_shape = False

        try:
            maxval = value.max()
            minval = value.min()
        except (SyntaxError, AttributeError):
            maxval = value
            minval = value

        if maxval > var.universe.max():
            if self.sim.clip_to_bounds:
                value = np.fmin(value, var.universe.max())
            else:
                raise IndexError("Input value out of bounds.  Max is %s" %
                                 str(max(var.universe)))
        if minval < var.universe.min():
            if self.sim.clip_to_bounds:
                value = np.fmax(value, var.universe.min())
            else:
                raise IndexError("Input value is out of bounds.  Min is %s" %
                                 str(min(var.universe)))

        var.input['current'] = value
        self.sim._update_unique_id()
        self._update_to_current()

    def __repr__(self):
        """
        Print a convenient string representation of all current input data.
        """
        current_inputs = self._get_inputs()
        out = ""
        for key, val in current_inputs.items():
            out += "{0} : {1}\n".format(key, val)
        return out

    def _update_to_current(self):
        # Private method, used to store the current state of the system in a
        # cache, 'current', accessible before and after the unique_id changes.
        if self.sim.unique_id == 'current':
            return

        # Find all antecedents
        matches = [n for n in self.sim.ctrl.graph.nodes()
                   if isinstance(n, Antecedent)]

        for antecedent in matches:
            antecedent.input[self.sim] = antecedent.input['current']

    def _get_inputs(self):
        """
        Find and return all antecedent inputs available.
        """
        antecedents = [n for n in self.sim.ctrl.graph.nodes()
                       if isinstance(n, Antecedent)]

        inputs = OrderedDict()
        for antecedent in antecedents:
            try:
                inputs[antecedent.label] = antecedent.input['current']
            except AttributeError:
                # No system ID yet, because no assigned values
                inputs[antecedent.label] = None

        return inputs


class ControlSystemSimulation(object):
    """
    Calculate results from a ControlSystem.

    Parameters
    ----------
    control_system : ControlSystem
        A fuzzy ControlSystem object.
    clip_to_bounds : bool, optional
        Controls if input values should be clipped to the consequent universe
        range. Default is True.
    cache : bool, optional
        Controls if results should be stored for reference in fuzzy variable
        objects, allowing fast lookup for repeated runs of `.compute()`.
        Unless you are heavily memory constrained leave this `True` (default).
    flush_after_run : int, optional
        Clears cached results after this many repeated, unique simulations.
        The default of 1000 is appropriate for most hardware, but for small
        embedded systems this can be lowered as appropriate. Higher memory
        systems may see better performance with a higher limit.
    """

    def __init__(self, control_system, clip_to_bounds=True, cache=True,
                 flush_after_run=1000):
        """
        Initialize a new ControlSystemSimulation.
        """ + '\n'.join(ControlSystemSimulation.__doc__.split('\n')[1:])
        assert isinstance(control_system, ControlSystem)
        self.ctrl = control_system

        self.input = _InputAcceptor(self)
        self.output = OrderedDict()
        self.cache = cache
        self._array_inputs = False  # Disable caching if True
        self._array_shape = None    # Tracks input shape, for array inputs
        self.unique_id = self._update_unique_id()

        self.clip_to_bounds = clip_to_bounds
        self._calculated = []

        self._run = 0
        self._flush_after_run = flush_after_run

    def _update_unique_id(self):
        """
        Unique hash of this control system including a specific set of inputs.

        Generated at runtime from the system state. Used as key to access data
        from `StatePerSimulation` objects, enabling multiple runs.
        """
        # The string to be hashed is the concatenation of:
        #  * the control system ID, which is independent of inputs
        #  * hash of the current input OrderedDict

        # Caching only enabled if no array inputs
        if not self._array_inputs:
            # Simple hashes and Python ids are fast and serve our purposes.
            self.unique_id = (str(id(self.ctrl)) +
                              str(hash(self._get_inputs().__repr__())))

    def _get_inputs(self):
        return self.input._get_inputs()

    def inputs(self, input_dict):
        """
        Convenience method to accept multiple inputs to antecedents.

        Parameters
        ----------
        input_dict : dict
            Contains key:value pairs where the key is the label for a
            connected Antecedent and the value is the input.
        """
        # Have to set this twice - first time to get the unique ID,
        #  second time to actually pass them into the correct ID.
        for label, value in input_dict.items():
            self.input[label] = value

    def compute(self):
        """
        Compute the fuzzy system.
        """
        self.input._update_to_current()

        # Must clear downstream calculations for repeated runs
        if self._array_inputs:
            self.cache = False
            self._clear_outputs()

        # Shortcut with lookup if this calculation was done before
        if self.cache is not False and self.unique_id in self._calculated:
            for consequent in self.ctrl.consequents:
                self.output[consequent.label] = consequent.output[self]
            return

        # If we get here, cache is disabled OR the inputs are novel. Compute!

        # Check if any fuzzy variables lack input values and fuzzify inputs
        for antecedent in self.ctrl.antecedents:
            if antecedent.input[self] is None:
                raise ValueError("All antecedents must have input values!")
            CrispValueCalculator(antecedent, self).fuzz(antecedent.input[self])

        # Calculate rules, taking inputs and accumulating outputs
        first = True
        for rule in self.ctrl.rules:
            # Clear results of prior runs from Terms if needed.
            if first:
                for c in rule.consequent:
                    c.term.membership_value[self] = None
                    c.activation[self] = None
                first = False
            self.compute_rule(rule)

        # Collect the results and present them as a dict
        for consequent in self.ctrl.consequents:
            consequent.output[self] = \
                CrispValueCalculator(consequent, self).defuzz()
            self.output[consequent.label] = consequent.output[self]

        # Make note of this run so we can easily find it again
        if self.cache is not False:
            self._calculated.append(self.unique_id)
        else:
            # Reset StatePerSimulations
            self._reset_simulation()

        # Increment run number
        self._run += 1
        if self._run % self._flush_after_run == 0:
            self._reset_simulation()

    def compute_rule(self, rule):
        """
        Implement rule according to Mamdani inference.

        The three step method consists of::
         * Aggregation
         * Activation
         * Accumulation
        """
        # Step 1: Aggregation.  This finds the net accomplishment of the
        #  antecedent by AND-ing or OR-ing together all the membership values
        #  of the terms that make up the accomplishment condition.
        #  The process of actually aggregating everything is delegated to the
        #  TermAggregation class, but we can tell that class
        #  what aggregation style this rule mandates
        if isinstance(rule.antecedent, TermAggregate):
            rule.antecedent.agg_methods = rule._aggregation_methods
        rule.aggregate_firing[self] = rule.antecedent.membership_value[self]

        # Step 2: Activation.  The degree of membership of the consequence
        #  is determined by the degree of accomplishment of the antecedent,
        #  which is what we determined in step 1.  The only difference would
        #  be if the consequent has a weight, which we would apply now.
        for c in rule.consequent:
            assert isinstance(c, WeightedTerm)
            c.activation[self] = rule.aggregate_firing[self] * c.weight

        # Step 3: Accumulation.  Apply the activation to each consequent,
        #   accumulating multiple rule firings into a single membership value.
        #   The process of actual accumulation is delegated to the
        #   Term which uses its parent's accumulation method
        for c in rule.consequent:
            assert isinstance(c, WeightedTerm)
            term = c.term
            value = c.activation[self]

            # Find new membership value
            if term.membership_value[self] is None:
                term.membership_value[self] = value
            else:
                # Use the accumulation method of variable to determine
                #  how to to handle multiple cuts
                accu = term.parent.accumulation_method
                term.membership_value[self] = accu(value,
                                                   term.membership_value[self])

            term.cuts[self][rule.label] = term.membership_value[self]

    def reset(self):
        """
        Reset the simulation.

        Cear memory by removing all inputs, outputs, and intermediate values.
        """
        self._reset_simulation()

    def _reset_simulation(self):
        """
        Clear temporary data from simulation objects.

        Called internally if cache=False (after every run) or after a certain
        number of runs if cache=True according to the `flush_after_run` kwarg.
        """
        def _clear_terms(fuzzy_var):
            for term in fuzzy_var.terms.values():
                term.membership_value.clear()
                term.cuts.clear()

        for rule in self.ctrl.rules:
            rule.aggregate_firing.clear()
            for c in rule.consequent:
                c.activation.clear()

        for consequent in self.ctrl.consequents:
            consequent.output.clear()
            _clear_terms(consequent)

        for antecedent in self.ctrl.antecedents:
            antecedent.input.clear()
            _clear_terms(antecedent)

        self._calculated = []
        self._run = 0

    def _clear_outputs(self):
        """
        Clears all downstream results/firings after Antecedents.
        """
        def _clear_terms(fuzzy_var):
            for term in fuzzy_var.terms.values():
                term.membership_value.clear()
                term.cuts.clear()

        for rule in self.ctrl.rules:
            rule.aggregate_firing.clear()
            for c in rule.consequent:
                c.activation.clear()

        for consequent in self.ctrl.consequents:
            consequent.output.clear()
            _clear_terms(consequent)

        self._calculated = []
        self._run = 0

    def print_state(self):
        """
        Print info about the inner workings of a ControlSystemSimulation.
        """
        if next(self.ctrl.consequents).output[self] is None:
            raise ValueError("Call compute method first.")

        print("=============")
        print(" Antecedents ")
        print("=============")
        for v in self.ctrl.antecedents:
            print("{0:<35} = {1}".format(v, v.input[self]))
            for term in v.terms.values():
                print("  - {0:<32}: {1}".format(term.label,
                                                term.membership_value[self]))
        print("")
        print("=======")
        print(" Rules ")
        print("=======")
        rule_number = {}
        for rn, r in enumerate(self.ctrl.rules):
            assert isinstance(r, Rule)
            rule_number[r] = "RULE #%d" % rn
            print("RULE #%d:\n  %s\n" % (rn, r))

            print("  Aggregation (IF-clause):")
            for term in r.antecedent_terms:
                assert isinstance(term, Term)
                print("  - {0:<55}: {1}".format(term.full_label,
                                                term.membership_value[self]))
            print("    {0:>54} = {1}".format(r.antecedent,
                                             r.aggregate_firing[self]))

            print("  Activation (THEN-clause):")
            for c in r.consequent:
                assert isinstance(c, WeightedTerm)
                print("    {0:>54} : {1}".format(c,
                                                 c.activation[self]))
            print("")
        print("")

        print("==============================")
        print(" Intermediaries and Conquests ")
        print("==============================")
        for c in self.ctrl.consequents:
            print("{0:<36} = {1}".format(
                c, CrispValueCalculator(c, self).defuzz()))

            for term in c.terms.values():
                print("  %s:" % term.label)
                for cut_rule, cut_value in term.cuts[self].items():
                    if cut_rule not in rule_number.keys():
                        continue
                    print("    {0:>32} : {1}".format(rule_number[cut_rule],
                                                     cut_value))
                accu = "Accumulate using %s" % c.accumulation_method.func_name
                print("    {0:>32} : {1}".format(accu,
                                                 term.membership_value[self]))
            print("")


class CrispValueCalculator(object):
    """
    Convert a calculated FuzzyVariable back into a crisp real number.

    Parameters
    ----------
    fuzzy_var : FuzzyVariable
        The fuzzy variable to be defuzzified.
    sim : ControlSystemSimulation
        The simulation which holds all necessary data for this calculation.
    """

    def __init__(self, fuzzy_var, sim):
        """
        Initialization method for CrispValueCalculator.
        """ + '\n'.join(CrispValueCalculator.__doc__.split('\n')[1:])
        assert isinstance(fuzzy_var, FuzzyVariable)
        assert isinstance(sim, ControlSystemSimulation)
        self.var = fuzzy_var
        self.sim = sim

    def defuzz(self):
        """Derive crisp value based on membership of adjective(s)."""
        if not self.sim._array_inputs:
            ups_universe, output_mf, cut_mfs = self.find_memberships()

            if len(cut_mfs) == 0:
                raise ValueError("No terms have memberships.  Make sure you "
                                 "have at least one rule connected to this "
                                 "variable and have run the rules calculation.")

            try:
                return defuzz(ups_universe, output_mf,
                              self.var.defuzzify_method)
            except AssertionError:
                raise ValueError("Crisp output cannot be calculated, likely "
                                 "because the system is too sparse. Check to "
                                 "make sure this set of input values will "
                                 "activate at least one connected Term in each "
                                 "Antecedent via the current set of Rules.")
        else:
            # Calculate using array-aware version, one cut at a time.
            output = np.zeros(self.sim._array_shape, dtype=np.float64)

            it = np.nditer(output, ['multi_index'], [['writeonly', 'allocate']])

            for out in it:
                universe, mf = self.find_memberships_nd(it.multi_index)
                out[...] = defuzz(universe, mf, self.var.defuzzify_method)

            return output

    def fuzz(self, value):
        """
        Propagate crisp value down to adjectives by calculating membership.
        """
        if len(self.var.terms) == 0:
            raise ValueError("Set Term membership function(s) first")

        for label, term in self.var.terms.items():
            term.membership_value[self.sim] = \
                interp_membership(self.var.universe, term.mf, value)

    def find_memberships(self):
        '''
        First we have to upsample the universe of self.var in order to add the
        key points of the membership function based on the activation level
        for this consequent, using the interp_universe function, which
        interpolates the `xx` values in the universe such that its membership
        function value is the activation level.
        '''
        # Find potentially new values
        new_values = []

        for label, term in self.var.terms.items():
            term._cut = term.membership_value[self.sim]
            if term._cut is None:
                continue  # No membership defined for this adjective

            # Faster to aggregate as list w/duplication
            new_values.extend(
                _interp_universe_fast(
                    self.var.universe, term.mf, term._cut).tolist())

        new_universe = np.union1d(self.var.universe, new_values)

        # Initilize membership
        output_mf = np.zeros_like(new_universe, dtype=np.float64)

        # Build output membership function
        term_mfs = {}
        for label, term in self.var.terms.items():
            if term._cut is None:
                continue  # No membership defined for this adjective

            upsampled_mf = interp_membership(
                self.var.universe, term.mf, new_universe)

            term_mfs[label] = np.minimum(term._cut, upsampled_mf)
            np.maximum(output_mf, term_mfs[label], output_mf)

        return new_universe, output_mf, term_mfs

    def find_memberships_nd(self, idx):
        '''
        Index-aware version of find_memberships(), expecting to select a
        particular set of membership values from an array input, given input
        ``idx``.
        '''
        # Find potentially new values
        new_values = []

        for label, term in self.var.terms.items():
            term._cut = term.membership_value[self.sim][idx]
            if term._cut is None:
                continue  # No membership defined for this adjective

            # Faster to aggregate as list w/duplication
            new_values.extend(
                _interp_universe_fast(
                    self.var.universe, term.mf, term._cut).tolist())

        new_universe = np.union1d(self.var.universe, new_values)

        # Initilize membership
        output_mf = np.zeros_like(new_universe, dtype=np.float64)

        # Build output membership function
        term_mfs = {}
        for label, term in self.var.terms.items():
            if term._cut is None:
                continue  # No membership defined for this adjective

            upsampled_mf = interp_membership(
                self.var.universe, term.mf, new_universe)

            term_mfs[label] = np.minimum(term._cut, upsampled_mf)
            np.maximum(output_mf, term_mfs[label], output_mf)

        return new_universe, output_mf


class RuleOrderGenerator(object):
    """
    Generator to yield rules in the correct order for calculation.

    Parameters
    ----------
    control_system : ControlSystem
        Fuzzy control system object, instance of `skfuzzy.ControlSystem`.

    Returns
    -------
    out : Rule
        Fuzzy rules in computation order.
    """

    def __init__(self, control_system):
        """
        Generator to yield rules in the correct order for calculation.
        """ + '\n'.join(RuleOrderGenerator.__doc__.split('\n')[1:6])
        assert isinstance(control_system, ControlSystem)
        self.control_system = control_system
        self._cache = []
        self._cached_graph = None

    def __iter__(self):
        """
        Method to yield the fuzzy rules in order for computation.
        """
        # Determine if we can return the cached version or must calc new
        if self._cached_graph is not self.control_system.graph:
            # The controller is still using a different version of the graph
            #  than we created the rule order for.  Thus, make new cache
            self._init_state()
            self._cache = list(self._process_rules(self.all_rules[:]))
            self._cached_graph = self.control_system.graph

        for n, r in enumerate(self._cache):
            yield r
        else:
            n = 0

        if n == 0:
            pass
        else:
            assert n == len(self.all_rules) - 1, "Not all rules exposed"

    def _init_state(self):
        # This graph will represent what's been calculated so far.  We
        # initialize it to just the antecedents as they, by definition, already
        # have fuzzy values
        self.calced_graph = nx.DiGraph()
        for a in self.control_system.antecedents:
            for t in a.terms.values():
                self.calced_graph.add_edge(a, t)

        self.all_graph = self.control_system.graph

        self.all_rules = []
        for node in self.all_graph.nodes():
            if isinstance(node, Rule):
                self.all_rules.append(node)

    def _process_rules(self, rules):
        # Recursive funcion to process rules in the correct firing order
        len_rules = len(rules)
        skipped_rules = []
        while len(rules) > 0:
            rule = rules.pop(0)
            if self._can_calc_rule(rule):
                yield rule
                # Add rule to calced graph
                self.calced_graph = nx.compose(self.calced_graph, rule.graph)
            else:
                # We have not calculated the predecsors for this rule yet.
                #  Skip it for now
                skipped_rules.append(rule)

        if len(skipped_rules) == 0:
            # All done!
            try:
                return
            except StopIteration:
                return
        else:
            if len(skipped_rules) == len_rules:
                # Avoid being caught in an infinite loop
                raise RuntimeError("Unable to resolve rule execution order. "
                                   "The most likely reason is two or more "
                                   "rules that depend on each other.\n"
                                   "Please check the rule graph for loops.")
            else:
                # Recurse across the skipped rules
                for r in self._process_rules(skipped_rules):
                    yield r

    def _can_calc_rule(self, rule):
        # Check that we've exposed all inputs to this rule by ensuring
        # the predecessor-degree of each predecessor node is the same
        # in both the calculation graph and overall graph

        # NetworkX compatibility
        try:
            # Best practice under 1.x, fails in 2.0
            predecessors = self.all_graph.predecessors_iter(rule)
        except AttributeError:
            predecessors = self.all_graph.predecessors(rule)

        for p in predecessors:
            assert isinstance(p, Term)
            if p not in self.calced_graph:
                return False

            # NetworkX compatibility
            try:
                all_degree = len(self.all_graph.predecessors(p))
                calced_degree = len(self.calced_graph.predecessors(p))
            except TypeError:
                # New iterator doesn't work with len()
                all_degree = self.all_graph.predecessors(p).__sizeof__()
                calced_degree = self.calced_graph.predecessors(p).__sizeof__()

            if all_degree != calced_degree:
                return False
        return True
