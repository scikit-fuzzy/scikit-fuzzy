# -*- coding: utf-8 -*-
'''
    Read and run an FLC file over some given data, taken from an FLD file.
    This can be used used to test one system against another,
    e.g. generate data using jFuzzyLogic and test it using skfuzzy.
    Typically we generate random inputs and compare outputs and rules.
    @author: james.power@mu.ie Created on Tue Aug  7 15:06:34 2018
'''

from __future__ import print_function

import sys
import os.path
import codecs
from datetime import datetime
from collections import OrderedDict

import numpy as np

from skfuzzy import control as ctrl
from skfuzzy.control import ControlSystemSimulation
from skfuzzy.control.controlsystem import CrispValueCalculator

from skfuzzy.fcl import FCLParser

_COMMENT_CHAR = '#'
_FCL_SUFFIX = '.fcl'
_FLD_SUFFIX = '.fld'

_DEFAULT_PERCENT_ACCURACY = 2  # Percentage error that's OK in outputs

_DEC_PLACES = 2  # number of decimal places to print


# This function was robbed from controlsystem.py, and tidied up
def _print_simulator_state(testnum, simulator):
    """
    Print info about the inner workings of a ControlSystemSimulation.
    """
#    if next(simulator.ctrl.consequents).output[simulator] is None:
#        raise ValueError("Call compute method first.")
    print('-'*70)
    print('* Run', testnum, ': Antecedents')
    for var in simulator.ctrl.antecedents:
        print("  * {0} = {1}".format(var, var.input[simulator]))
        for term in var.terms.values():
            print("  - {0}: {1}"
                  .format(term.label, term.membership_value[simulator]))
    print("")
    print('* Run', testnum, ': Rules ')
    sorted_rules = sorted(simulator.ctrl.rules, key=lambda r: r.label)
    rule_number = {}
    for rn, rule in enumerate(sorted_rules):
        rule_number[rule] = "RULE #%d" % rn
        print("  * RULE %s (#%d): %s" % (rule.label, rn, rule))

        print("  = Aggregation (IF-clause):")
        for term in rule.antecedent_terms:
            print("    Input: {0} = {1}"
                  .format(term.full_label, term.membership_value[simulator]))
        print("    Total: {0} = {1}"
              .format(rule.antecedent, rule.aggregate_firing[simulator]))

        print("  = Activation (THEN-clause):")
        for conseq in rule.consequent:
            print("    {0} : {1}"
                  .format(conseq, conseq.activation[simulator]))
        print("")

    print('* Run', testnum, ': Intermediaries and Consequents ')
    for conseq in simulator.ctrl.consequents:
        cvc = CrispValueCalculator(conseq, simulator)
        try:
            print("  * {0} = {1}".format(conseq, cvc.defuzz()))
        except Exception as exc:
            print('\t- {}'.format(exc))
        # If you want to drill into the output mfs, print these:
        ups_universe, output_mf, cut_mfs = cvc.find_memberships()
        # print(ups_universe, output_mf, cut_mfs)
        for term in conseq.terms.values():
            print("  - %s:" % term.label)
            for cut_rule, cut_value in term.cuts[simulator].items():
                print("    {0} : {1}".format(cut_rule, cut_value))
            accu = "Accumulate using %s" % conseq.accumulation_method.__name__
            print("    ({0} : {1})"
                  .format(accu, term.membership_value[simulator]))
        print("")


def _print_memberships(var):
    '''
    Tabulate the values in each of the membership functions for a variable.
    For each universe value, print the corresponding mf value.
    '''
    print('-', 'Variable', var)
    # Print the names of the terms:
    print('{:8}'.format(''), ['{:>8}'.format(v.label)
                              for v in var.terms.values()])
    # Then print each unverse value and the corresponding term values:
    for i, x in enumerate(var.universe):
        print('{:8.3}'.format(x),
              ['{:8.3}'.format(v.mf[i]) for v in var.terms.values()])


class TestData(object):
    '''
    Just a container for var/rule names and corresponding test data.
    A list of names, and then an array with one column per name.
    '''
    def __init__(self, names, num_tests):
        '''One row per test case, one col per name, initialise to zero'''
        self.names = list(names)  # Order is important here!
        self.value = np.zeros((num_tests, len(self.names)))
        self.message = {}  # Hold error messages (if any)

    @property
    def num_tests(self):
        '''The number of test cases is the number of rows'''
        return self.value.shape[0]


class SimulationHarness(object):
    '''
    A class to handle reading FLD files and running simulations.
    '''
    def __init__(self, verbose=False):
        # N.B. the following are stored in lists since the order is important
        self.antecedents = OrderedDict()  # Maps names to variable objects
        self.consequents = OrderedDict()  # Maps names to variable objects
        self.all_rules = OrderedDict()    # Maps names to rule objects
        self.control_system = None
        self.percent_accuracy = _DEFAULT_PERCENT_ACCURACY
        self.verbose = verbose

    def set_verbose(self):
        '''Will set flag to print detailed simulation results'''
        self.verbose = True

    def make_fld_filename(self, fclfile):
        '''
        How to get the FLD file corresponding to a FCL file.
        At the moment this just looks in the same directory,
        but you may wish to change this.
        '''
        return fclfile.replace(_FCL_SUFFIX, _FLD_SUFFIX)

    def read_fcl_file(self, fclfile):
        '''
        Read an FCL file and initialise the variable/rule lists.
        '''
        assert os.path.isfile(fclfile),\
            'Can\'t find specified FCL file "{}"'.format(fclfile)
        parser = FCLParser().read_fcl_file(fclfile)
        if self.verbose:
            print(parser)
        self.antecedents = {var.label: var for var in parser.antecedents}
        self.consequents = {var.label: var for var in parser.consequents}
        self.all_rules = OrderedDict(parser.all_rules)
        self.control_system = ctrl.ControlSystem(self.all_rules.values())

    def simulate_one(self, input_dict):
        '''
        A utility routine to run a simluation with a given set of data.
        Supply the data as a dict of var-name:value pairs.
        Handy for testing; not used elsewhere here.
        '''
        simulator = ControlSystemSimulation(self.control_system)
        for k, v in input_dict.items():
            simulator.input[k] = v
        simulator.compute()
        print('-'*70)
        _print_simulator_state(simulator)

    @staticmethod
    def _get_fs(simulator, rule, weighted=True):
        '''
        Return the fire-strength for a rule (after a simulation run).
        With no weighting this is the accumulation for the rule,
        with weighting it's the activation (we pick the first consequent)
        '''
        if not weighted:  # want the fire strength before weighting
            return rule.aggregate_firing[simulator]
        else:  # want the activation i.e. *after* weighting
            first_conseq = rule.consequent[0]  # Pick the first one
            # I'm assuming activation is the same for other consequents.
            return first_conseq.activation[simulator]

    def simulate(self, input_data):
        '''
        Supply the inputs, run the system, collect the outputs,
        return the results (outputs, rules), once row for each test.
        '''
        simulator = ControlSystemSimulation(self.control_system)
        num_tests = input_data.num_tests
        output_data = TestData(self.consequents.keys(), num_tests)
        rule_data = TestData(self.all_rules.keys(), num_tests)
        if self.verbose:
            print('-'*70)
            for var in (list(self.antecedents.values()) +
                        list(self.consequents.values())):
                _print_memberships(var)
            print('-'*70)
        # For each test case (row of input values):
        for row in range(num_tests):
            # Load up the inputs and run:
            for j, vname in enumerate(input_data.names):
                simulator.input[vname] = input_data.value[row][j]
            try:
                simulator.compute()
                if self.verbose:
                    _print_simulator_state(row, simulator)
            except Exception as exc:
                if self.verbose:
                    _print_simulator_state(row, simulator)
                output_data.message[row] = '\t- {}'.format(exc)
                continue
            # Collect the output values:
            for j, vname in enumerate(output_data.names):
                output_data.value[row][j] = simulator.output[vname]
            # Collect the rule fire-strengths:
            for rule in simulator.ctrl.rules:
                if rule.label in rule_data.names:  # and it should be
                    col = rule_data.names.index(rule.label)
                    rule_data.value[row][col] = self._get_fs(simulator, rule)
        return output_data, rule_data

    def read_fld_file(self, fldfile):
        '''
        Read an FLD file, which has space-separated data values.
        Ensure order of variable-names is synched to what we're expecting.
        Return three arrays, one each for: inputs, outputs, rules.
        Each row in an array corresponds to one test case.
        '''
        assert os.path.isfile(fldfile),\
            'Can\'t find data file "{}"'.format(fldfile)
        with codecs.open(fldfile, 'r') as fileh:
            # First line is the variable names:
            varnames = fileh.readline().strip().split()
            # Remaining lines are the space-separated values
            data = np.loadtxt(fileh)
        # One row per test, no. of columns is the number of variables:
        num_tests = data.shape[0]
        assert len(varnames) == data.shape[1],\
            'Got {} data values for {} variables {}'\
            .format(data.shape[1], len(varnames), varnames)
        # Let's check that the variables were the ones we were expecting:
        input_data = TestData(self.antecedents.keys(), num_tests)
        output_data = TestData(self.consequents.keys(), num_tests)
        rule_data = TestData(self.all_rules.keys(), num_tests)
        wanted_vars = input_data.names + output_data.names
        fld_has_rules = len(varnames) > len(wanted_vars)
        if fld_has_rules:
            wanted_vars += rule_data.names
        s_want, s_have = set(wanted_vars), set(varnames)
        missing = s_want - s_have
        assert len(missing) == 0,\
            '{} is missing data for variables {}'.format(fldfile, missing)
        extra = s_have - s_want
        assert len(extra) == 0,\
            '{} has data for unknown variables {}'.format(fldfile, extra)
        # Now synch the order of variables to be the one we want
        wanted_order = [varnames.index(v) for v in wanted_vars]
        data = data[:, wanted_order]  # numpy trickery for rearranging columns
        # Finally, split the array into (input, output) and return it
        inum = len(input_data.names)
        onum = inum + len(output_data.names)
        if fld_has_rules:
            input_data.value, output_data.value, rule_data.value \
                = np.hsplit(data, (inum, onum))
        else:  # ... second arg to hsplit must be a tuple:
            input_data.value, output_data.value \
                = np.hsplit(data, (inum, ))
            rule_data = None
        return input_data, output_data, rule_data

    def gen_sample_inputs(self, num_tests):
        '''
        Generate a set of random values for the input variables.
        '''
        input_data = TestData(self.antecedents.keys(), num_tests)
        # Generate the data one variable (row) at a time:
        for i, var_name in enumerate(input_data.names):
            var = self.antecedents[var_name]
            lo, hi = np.min(var.universe), np.max(var.universe)
            input_data.value[:, i] = np.random.uniform(lo, hi, num_tests)
        return input_data

    @staticmethod
    def _calc_error(want, got):
        '''
        Calculate the absolute percentage error, rounded to 1%
        '''
        # We're working in whole-percentage values:
        if want != 0:
            error = np.round(100*(got-want) / want, 0)
        else:
            error = np.round(got, 0)
        return np.abs(error)

    def _check_outputs(self, row, output_want, output_got):
        '''
        Check each output value for this test case;
        return true iff they all were within the desired accuracy.
        '''
        print('Output variables:')
        if row in output_got.message:
            print('Error running test case no. {}:'.format(row))
            print(output_got.message[row])
        all_outputs_ok = True
        for col, vname in enumerate(output_want.names):
            want = output_want.value[row][col]
            got = output_got.value[row][col]
            error_perc = self._calc_error(want, got)
            if error_perc < self.percent_accuracy:
                msg = 'CORRECT'
            else:
                all_outputs_ok = False
                msg = 'FAIL (wanted {1:.{0}f})'.format(_DEC_PLACES, want)
            print('  {1}={2:.{0}f}  {3}, ERROR={4:03.0f}%'
                  .format(_DEC_PLACES, vname, got, msg, error_perc))
        return all_outputs_ok

    def _check_rule_fs(self, row, rule_want, rule_got):
        '''
        Check the fire-strength for each rule for this test case;
        return true iff they all were within the desired accuracy.
        '''
        print('Rule fire-strengths for test case {}:'.format(row))
        rules_failed = 0
        for col, rname in enumerate(rule_got.names):
            got = rule_got.value[row][col]
            rstr = '  RULE {1} = {2:.{0}f}'.format(_DEC_PLACES, rname, got)
            # If we have desired rule fire-strenghts, then compare:
            if rule_want:
                want = rule_want.value[row][col]
                # Ruel fire strengths are between 0 and 1 anyway:
                error_perc = self._calc_error(want, got)
                if error_perc/100.0 < self.percent_accuracy:
                    rstr += ' (CORRECT)'
                else:
                    rules_failed += 1
                    rstr += ' (wanted {1:.{0}f})'.format(_DEC_PLACES, got)
            print(rstr)
        return rules_failed == 0

    def simulate_and_check(self, input_data, output_want, rule_want=None):
        '''
        Run the system with the given input data;
        then check the results against the given outputs.
        We are given target ouput values and (maybe) rule fire-strengths
        '''
        output_got, rule_got = self.simulate(input_data)
        failed_cases = 0
        # Each row is a test case:
        for row in range(input_data.num_tests):
            print('-' * 70)
            print('Run', row, end=': ')
            for col, vname in enumerate(input_data.names):
                print('{1}={2:.{0}f}'.format(_DEC_PLACES, vname,
                      input_data.value[row][col]), end=' ')
            print()
            # Check outputs, rules:
            out_fail = not self._check_outputs(row, output_want, output_got)
            rule_fail = not self._check_rule_fs(row, rule_want, rule_got)
            if out_fail or rule_fail:
                failed_cases += 1
        print('-' * 70)
        print('Failed {} of {} test cases (within {}%)'
              .format(failed_cases, input_data.num_tests,
                      self.percent_accuracy))
        return (failed_cases, input_data.num_tests)

    def simulate_from_file(self, fclfile, data_filename=None):
        '''
        Read and test the given FCL file with the given data file.
        Can find a corresponding data filename if non given.
        '''
        self.read_fcl_file(fclfile)
        if not data_filename:
            data_filename = self.make_fld_filename(fclfile)
        input_data, output_data, rule_data = self.read_fld_file(data_filename)
        print('=' * 70)
        print('=', fclfile, 'on', datetime.now().strftime("%d %b %Y at %H:%M"))
        print('=' * 70)
        return self.simulate_and_check(input_data, output_data, rule_data)

    def simulate_to_file(self, fclfile, num_tests, rules_too=False):
        '''
        Simulate the system (generating some sample inputs),
        and then write the results to a file in the given dir.
        '''
        self.read_fcl_file(fclfile)
        # Get an array of input values:
        input_data = self.gen_sample_inputs(num_tests)
        # And generate corresponding results for outputs and rules:
        output_data, rule_data = self.simulate(input_data)
        # Last, write these to a file:
        data_filename = self.make_fld_filename(fclfile)
        file_name_comment = 'Generated using {} on {}'\
            .format(fclfile, datetime.now())
        all_names = input_data.names + output_data.names
        all_vals = (input_data.value, output_data.value)
        if rules_too:
            all_names += rule_data.names
            all_vals = (input_data.value, output_data.value, rule_data.value)
        with codecs.open(data_filename, 'w') as fileh:
            fileh.write(' '.join(all_names) + '\n')
            np.savetxt(fileh,
                       np.concatenate(all_vals, axis=1),
                       comments=_COMMENT_CHAR, header=file_name_comment)

    def simulate_from_dir(self, datadir):
        '''
        Read and test all the FCL files in root and its subdirs.
        Uses the data from the corresponding FLD file.
        '''
        for dirpath, _, files in os.walk(datadir):
            for filename in files:
                if not filename.endswith(_FCL_SUFFIX):
                    continue
                filepath = os.path.join(dirpath, filename)
                print('===', filepath)
                self.simulate_from_file(filepath)

    def simulate_to_dir(self, fclrootdir, num_tests):
        '''
        Read and test all the .fcl files in root and its subdirs.
        Generate random data for num_tests test cases for the inputs,
        and these values, along with the outputs are written to a file.
        One data file is written for each input fcl file.
        '''
        for dirpath, _, files in os.walk(fclrootdir):
            for filename in files:
                if not filename.endswith(_FCL_SUFFIX):
                    continue
                filepath = os.path.join(dirpath, filename)
                print('===', filepath)
                self.simulate_to_file(filepath, num_tests)

if __name__ == '__main__':
    harness = SimulationHarness(True)
    if len(sys.argv) == 1:  # No args, test all examples
        harness.simulate_from_dir('../Examples')
    else:  # Test with the given FCL files:
        for fcl_filename in sys.argv[1:]:
            harness.simulate_from_file(fcl_filename)
