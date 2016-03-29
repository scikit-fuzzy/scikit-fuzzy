"""
controlsystem.py : Framework for the new fuzzy logic control system API.
"""
from __future__ import print_function, division

import numpy as np
import networkx as nx
import matplotlib.pylab as plt

from skfuzzy import interp_membership, defuzz
from .antecedent_consequent import Antecedent, Consequent
from .fuzzyvariable import FuzzyVariable, Term, TermAggregate
from .visualization import ControlSystemVisualizer
from .rule import Rule, WeightedTerm

try:
    from collections import OrderedDict
except ImportError:
    from .ordereddict import OrderedDict


class ControlSystem(object):
    """
    Fuzzy Control System
    """
    def __init__(self, rules=None):
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
        # We have to expose the rules in the order from antecedents to
        #  consequences.  For example if we have:
        #  Antecedent -> rule1 -> Intermediary -> rule2 -> Consequence
        #  if we expose rule1 before rule2, we won't calculate correctly
        return self._rule_generator

    @property
    def antecedents(self):
        """
        Generator which yields Antecedents in the system.
        """
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

    def view(self):
        """
        View a representation of the system NetworkX graph.
        """
        fig = ControlSystemVisualizer(self).view()
        fig.show()


class _InputAcceptor(object):
    """
    Set a single input value to an Antecedent in this ControlSystemSimulation.
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

        if value > var.universe.max():
            if self.sim.clip_to_bounds:
                value = var.universe.max()
            else:
                raise ValueError("Input value out of bounds.  Max is %s" %
                                 max(var.universe))
        if value < var.universe.min():
            if self.sim.clip_to_bounds:
                value = var.universe.min()
            else:
                raise ValueError("Input value is out of bounds.  Min is %s" %
                                 min(var.universe))

        var.input[self.sim] = value

    def __repr__(self):
        """
        Print a convenient string representation of all current input data.
        """
        current_inputs = self.get_inputs()
        out = ""
        for key, val in current_inputs.iteritems():
            out += "{0} : {1}\n".format(key, val)
        return out

    def get_inputs(self):
        """
        Find and return all antecedent inputs available.
        """
        antecedents = [n for n in self.sim.ctrl.graph.nodes()
                       if isinstance(n, Antecedent)]

        inputs = OrderedDict()
        for antecedent in antecedents:
            try:
                inputs[antecedent.label] = antecedent.input[self.sim]
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
    """

    def __init__(self, control_system, clip_to_bounds=True):
        assert isinstance(control_system, ControlSystem)
        self.ctrl = control_system

        self.input = _InputAcceptor(self)
        self.output = OrderedDict()
        self.unique_id = self._update_unique_id()

        self.clip_to_bounds = clip_to_bounds

    def _update_unique_id(self):
        """
        Unique hash of this control system including a specific set of inputs.

        Generated at runtime from the system state. Used as key to access data
        from `StatePerSimulation` objects, enabling multiple runs.
        """
        # The string to be hashed is the concatenation of:
        #  * the control system ID, which is independent of inputs
        #  * hash of the current input dictionary

        # Simple hashes and Python ids are fast and serve our purposes.
        self.unique_id = (str(id(self.ctrl)) +
                          str(hash(self.get_inputs().__repr__())))

    def get_inputs(self):
        return self.input.get_inputs()

    def inputs(self, input_dict):
        """
        Convenience method to accept multiple inputs to antecedents.

        Parameters
        ----------
        input_dict : dict
            Contains key:value pairs where the key is the label for a
            connected Antecedent and the value is the input.
        """
        for label, value in input_dict.items():
            self.input[label] = value
        self._update_unique_id()

    def compute(self):
        """
        Compute the fuzzy system.
        """
        # Lazy updating of system ID - only when computing
        temp = self.get_inputs()
        self._update_unique_id()
        self.inputs(temp)

        # Check if any fuzzy variables lack input values and fuzzify inputs
        for antecedent in self.ctrl.antecedents:
            if antecedent.input[self] is None:
                raise ValueError("All antecedents must have input values!")
            if list(antecedent.terms.values())[0].membership_value[self] is not None:
                # Clear all previously existing membership values
                pass
            CrispValueCalculator(antecedent, self).fuzz(antecedent.input[self])

        # Calculate rules, taking inputs and accumulating outputs
        for rule in self.ctrl.rules:
            self.compute_rule(rule)

        # Collect the results and present them as a dict
        for consequent in self.ctrl.consequents:
            consequent.output[self] = \
                CrispValueCalculator(consequent, self).defuzz()
            self.output[consequent.label] = consequent.output[self]

    def compute_rule(self, rule):
        """
        Implements rule according to the three step method of
        Mamdani inference: Aggregation, activation, and accumulation
        """
        # Step 1: Aggregation.  This finds the net accomplishment of the
        #  antecedent by AND-ing or OR-ing together all the membership values
        #  of the terms that make up the accomplishment condition.
        #  The process of actually aggregating everything is delegated to the
        #  TermAggregation class, but we can tell that class
        #  what aggregation style this rule mandates

        if isinstance(rule.antecedent, TermAggregate):
            rule.antecedent.agg_method = rule.aggregation_method
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
                assert len(term.cuts[self]) == 0, "Membership value already set"
                term.membership_value[self] = value
            else:
                # Use the accumulation method of variable to determine
                #  how to to handle multiple cuts
                accu = term.parent_variable.accumulation_method
                term.membership_value[self] = accu(value,
                                                   term.membership_value[self])

            term.cuts[self][rule] = value

    def print_state(self):
        if self.ctrl.consequents.next().output[self] is None:
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

    def __init__(self, fuzzy_var, sim):
        assert isinstance(fuzzy_var, FuzzyVariable)
        assert isinstance(sim, ControlSystemSimulation)
        self.var = fuzzy_var
        self.sim = sim

    def defuzz(self):
        """Derive crisp value based on membership of adjective(s)."""
        output_mf, cut_mfs = self.find_memberships()
        if len(cut_mfs) == 0:
            raise ValueError("No terms have memberships.  Make sure you "
                             "have at least one rule connected to this "
                             "variable and have run the rules calculation.")
        return defuzz(self.var.universe, output_mf, self.var.defuzzify_method)

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
        # Check we have some adjectives
        if len(self.var.terms.keys()) == 0:
            raise ValueError("Set term membership function(s) first")

        # Initilize membership
        output_mf = np.zeros_like(self.var.universe, dtype=np.float64)

        # Build output membership function
        term_mfs = {}
        for label, term in self.var.terms.items():
            cut = term.membership_value[self.sim]
            if cut is None:
                continue  # No membership defined for this adjective
            term_mfs[label] = np.minimum(cut, term.mf)
            np.maximum(output_mf, term_mfs[label], output_mf)

        return output_mf, term_mfs


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

        Parameters
        ----------
        control_system : ControlSystem
            Fuzzy control system object, instance of `skfuzzy.ControlSystem`.
        """
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
            self.calced_graph.add_star([a, ] + list(a.terms.values()))

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
            raise StopIteration()
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
        for p in self.all_graph.predecessors_iter(rule):
            assert isinstance(p, Term)
            if p not in self.calced_graph:
                return False

            all_degree = len(self.all_graph.predecessors(p))
            calced_degree = len(self.calced_graph.predecessors(p))
            if all_degree != calced_degree:
                return False
        return True
