# -*- coding: utf-8 -*-
'''
    This started as a copy of skfuzzy/control/tests/test_controlsystem.py
    I've hacked it a bit to partially use the FCL parser.
    @hacker: james.power@mu.ie Created on Tue Aug 21 10:11:04 2018
'''

from __future__ import division
import os

import numpy as np
import numpy.testing as tst
import nose

import skfuzzy.control as ctrl

from skfuzzy.fcl import FCLParser


def test_tipping_problem():
    '''
        Define the variables as usual,
        but use FCL for some membership functions and for all the rules.
    '''

    # First we set up the variables in the usual way:
    food = ctrl.Antecedent(np.linspace(0, 10, 11), 'quality')
    service = ctrl.Antecedent(np.linspace(0, 10, 11), 'service')
    tip = ctrl.Consequent(np.linspace(0, 25, 26), 'tip')

    # Auto-generate the membership functions for the inputs:
    food.automf(3)
    service.automf(3)

    # Define a FCL parser-object:
    p = FCLParser()
    # Use FCL to define membership functions for the output:
    tip['bad'] = p.mf('Triangle 0 0 13', tip.universe)
    tip['middling'] = p.mf('Triangle 0 13 25', tip.universe)
    tip['lots'] = p.mf('Triangle 13 25 25', tip.universe)

    # We need to tell the parser about the variables before we parse the rules:
    p.add_vars([food, service, tip])

    # Now use FCL to define three rules:
    rule1 = p.rule('IF quality IS poor OR service IS poor THEN tip IS bad')
    rule2 = p.rule('IF service is average THEN tip is middling')
    rule3 = p.rule('if service is good or quality is good then tip is lots')

    # To get the control system, just add the rules (from the parser):
    tipping = ctrl.ControlSystem(p.rules)

    # From here on it's just the same as the original:
    tipping2 = ctrl.ControlSystem(rule1)
    tipping2.addrule(rule2)
    tipping2.addrule(rule3)

    tip_sim = ctrl.ControlSystemSimulation(tipping)
    tip_sim2 = ctrl.ControlSystemSimulation(tipping2)

    # Inputs added both possible ways
    inputs = {'quality': 6.5, 'service': 9.8}
    for key, value in inputs.items():
        tip_sim.input[key] = value

    tip_sim2.inputs(inputs)

    # Compute the system
    tip_sim.compute()
    tip_sim2.compute()

    # Ensure both methods of defining rules yield the same results
    for val0, val1 in zip(tip_sim.output.values(),
                          tip_sim2.output.values()):
        tst.assert_allclose(val0, val1)

    # Verify against manual computation
    tst.assert_allclose(tip_sim.output['tip'], 19.8578, atol=1e-2, rtol=1e-2)


def setup_rule_order():
    ''' We can define variables in FCL and add terms afterwards: '''
    global _parser  # Make this global so we can access vars elsewhere
    _parser = FCLParser()
    # Use the parser to define the variables and their universes
    _parser.function_block('''
        FUNCTION_BLOCK
        // Define variables, but not terms for the moment:
        FUZZIFY a RANGE := (0 .. 11) WITH 1 END_FUZZIFY
        FUZZIFY b RANGE := (0 .. 11) WITH 1 END_FUZZIFY
        FUZZIFY c RANGE := (0 .. 11) WITH 1 END_FUZZIFY
        FUZZIFY d RANGE := (0 .. 11) WITH 1 END_FUZZIFY
        // No rules at all; that's OK.
        END_FUNCTION_BLOCK
    ''')

    # The use skfuzzy to define the membership functions:
    for v in _parser.fuzzy_variables:
        v.automf(3)


@nose.with_setup(setup_rule_order)
def test_bad_rules():
    '''Can access variables by using parser as a dict'''
    not_rules = ['me', 192238, 42, dict()]
    tst.assert_raises(ValueError, ctrl.ControlSystem, not_rules)

    testsystem = ctrl.ControlSystem()
    tst.assert_raises(ValueError, testsystem.addrule, _parser['a'])


def test_multiple_rules_same_consequent_term():
    '''
        Here we define the variables fully in FCL,
        and use a rule-block for the set of rules.
    '''
    x1_inputs = [0.6, 0.2, 0.4, 0.7, 1, 1.2, 1.8]
    x2_inputs = [0.9, 1, 0.8, 0, 1.2, 0.6, 1.8]

    p = FCLParser()

    p.fuzzify_block('''
        FUZZIFY x1
            RANGE := (0 .. 2.1) WITH 0.01   // Hacked the FCL syntax here
            TERM label0 := Triangle 0.2 0.2 0.6
            TERM label1 := Triangle 0.2 0.6 1.0
            TERM label2 := Triangle 0.6 1.0 1.4
            TERM label3 := Triangle 1.0 1.4 1.8
            TERM label4 := Triangle 1.4 1.8 1.8
        END_FUZZIFY
    ''')

    p.fuzzify_block('''
        FUZZIFY x2
            RANGE := (0 .. 2.1) WITH 0.01
            TERM label0 := Triangle 0.0 0.0 0.45
            TERM label1 := Triangle 0.0 0.45 0.9
            TERM label2 := Triangle 0.45 0.9 1.35
            TERM label3 := Triangle 0.9 1.35 1.8
            TERM label4 := Triangle 1.35 1.8 1.8
        END_FUZZIFY
    ''')

    p.defuzzify_block('''
        DEFUZZIFY y
            RANGE := (0 .. 2.1) WITH 0.01
            TERM label0 := Triangle 0.3 0.3 0.725
            TERM label1 := Triangle 0.3 0.725 1.15
            TERM label2 := Triangle 0.725 1.15 1.575
            TERM label3 := Triangle 1.15 1.575 2.0
            TERM label4 := Triangle 1.575 2.0 2.0
        END_DEFUZZIFY
    ''')

    first_three = p.rule_block('''
        RULEBLOCK  // Name of rule-block is optional
        RULE 1: IF x1 is label0 AND x2 is label2 THEN y is label0
        RULE 2: IF x1 is label1 AND x2 is label0 THEN y is label0
        RULE 3: IF x1 is label1 AND x2 is label2 THEN y is label0
        END_RULEBLOCK
    ''')

    # Equivalent to above 3 rules
    r123 = p.rule('''
        IF x1 is label0 AND x2 is label2
        OR x1 is label1 AND x2 is label0
        OR x1 is label1 AND x2 is label2
        THEN y is label0
    ''')

    last_three = p.rule_block('''
        RULEBLOCK  // Name of rule-block is optional
        RULE 4: IF x1 is label2 AND x2 is label1 THEN y is label2
        RULE 5: IF x1 is label2 AND x2 is label3 THEN y is label3
        RULE 6: IF x1 is label4 AND x2 is label4 THEN y is label4
        END_RULEBLOCK
    ''')

    # Build a system with three rules targeting the same Consequent Term,
    # and then an equivalent system with those three rules combined into one.
    cs0 = ctrl.ControlSystem(first_three + last_three)
    cs1 = ctrl.ControlSystem([r123] + last_three)

    expected_results = [0.438372093023,
                        0.443962536855,
                        0.461436409933,
                        0.445290345769,
                        1.575,
                        1.15,
                        1.86162790698]

    # Ensure the results are equivalent within error
    for inst, expected in zip(range(7), expected_results):
        sim0 = ctrl.ControlSystemSimulation(cs0)
        sim1 = ctrl.ControlSystemSimulation(cs1)

        sim0.input["x1"] = x1_inputs[inst]
        sim0.input["x2"] = x2_inputs[inst]
        sim1.input["x1"] = x1_inputs[inst]
        sim1.input["x2"] = x2_inputs[inst]

        sim0.compute()
        sim1.compute()

        tst.assert_allclose(sim0.output['y'], sim1.output['y'])
        tst.assert_allclose(expected, sim0.output['y'], atol=1e-4, rtol=1e-4)


def test_multiple_rules_same_consequent_term_file():
    '''
        Here we define the whole system in an FCL file, and read it in...
    '''
    x1_inputs = [0.6, 0.2, 0.4, 0.7, 1, 1.2, 1.8]
    x2_inputs = [0.9, 1, 0.8, 0, 1.2, 0.6, 1.8]

    p = FCLParser()
    # FCL input file is in the same directory as this script:
    infile = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                          'multiple.fcl')
    p.read_fcl_file(infile)

    # Build a system with three rules targeting the same Consequent Term,
    # and then an equivalent system with those three rules combined into one.
    separate = [r for r in p.rules if not r.label.startswith('extra')]
    cs0 = ctrl.ControlSystem(separate)  # 6 rules, as before
    cs1 = ctrl.ControlSystem(p.rules)   # Throw in all 7 rules

    expected_results = [0.438372093023,
                        0.443962536855,
                        0.461436409933,
                        0.445290345769,
                        1.575,
                        1.15,
                        1.86162790698]

    # Ensure the results are equivalent within error
    for inst, expected in zip(range(7), expected_results):
        sim0 = ctrl.ControlSystemSimulation(cs0)
        sim1 = ctrl.ControlSystemSimulation(cs1)

        sim0.input["x1"] = x1_inputs[inst]
        sim0.input["x2"] = x2_inputs[inst]
        sim1.input["x1"] = x1_inputs[inst]
        sim1.input["x2"] = x2_inputs[inst]

        sim0.compute()
        sim1.compute()

        tst.assert_allclose(sim0.output['y'], sim1.output['y'])
        tst.assert_allclose(expected, sim0.output['y'], atol=1e-4, rtol=1e-4)


def test_complex_system():
    '''In this example we parse a whole rule-back in one go'''

    universe = np.linspace(-2, 2, 5)
    vars = [ctrl.Antecedent(universe, 'error'),
            ctrl.Antecedent(universe, 'delta'),
            ctrl.Consequent(universe, 'output')]

    for var in vars:
        var.automf(names=['nb', 'ns', 'ze', 'ps', 'pb'])

    # Define a FCL parser-object, tell it about the variables:
    p = FCLParser(vars)

    # Now supply all the rules as a ruleblock
    rulebase = p.rule_block('''
        RULEBLOCK ComplexSystem  // Name of rule-block is optional
        RULE rule_nb:
            IF error is nb and delta is nb
            or error is ns and delta is nb
            or error is nb and delta is ns
            THEN output is nb
        RULE rule_ns:
            IF error is nb and delta is ze or error is nb and delta is ps
            or error is ns and delta is ns or error is ns and delta is ze
            or error is ze and delta is ns or error is ze and delta is nb
            or error is ps and delta is nb
            THEN output is ns
        RULE rule_ze:
            IF error is nb and delta is pb
            or error is ns and delta is ps
            or error is ze and delta is ze
            or error is ps and delta is ns
            or error is pb and delta is nb
            THEN output is ze
        RULE rule_ps:
            IF error is ns and delta is pb
            or error is ze and delta is pb or error is ze and delta is ps
            or error is ps and delta is ps or error is ps and delta is ze
            or error is pb and delta is ze or error is pb and delta is ns
            THEN output is ps
        RULE rule_pb:
            IF error is ps and delta is pb
            or error is pb and delta is pb or error is pb and delta is ps
            THEN output is pb
        END_RULEBLOCK
    ''')

    # Same as before from here on...
    system = ctrl.ControlSystem(rules=rulebase)

    sim = ctrl.ControlSystemSimulation(system, cache=False)

    x, y = np.meshgrid(np.linspace(-2, 2, 21), np.linspace(-2, 2, 21))
    z0 = np.zeros_like(x)
    z1 = np.zeros_like(x)

    # The original, slow way - one set of values at a time
    for i in range(21):
        for j in range(21):
            sim.input['error'] = x[i, j]
            sim.input['delta'] = y[i, j]
            sim.compute()
            z0[i, j] = sim.output['output']

    sim.reset()

    # The new way - array inputs
    sim.input['error'] = x
    sim.input['delta'] = y
    sim.compute()
    z1 = sim.output['output']

    # Ensure results align
    np.testing.assert_allclose(z0, z1)

    # Big expected array
    expected = \
        np.array([[-1.66666667e+00,  -1.65555556e+00,  -1.62857143e+00,
                   -1.62857143e+00,  -1.65555556e+00,  -1.66666667e+00,
                   -1.34414414e+00,  -1.18294574e+00,  -1.10000000e+00,
                   -1.05641026e+00,  -1.00000000e+00,  -1.00000000e+00,
                   -1.00000000e+00,  -1.00000000e+00,  -1.00000000e+00,
                   -1.00000000e+00,  -7.37704918e-01,  -5.72916667e-01,
                   -4.27083333e-01,  -2.62295082e-01,  -2.77555756e-17],
                  [-1.65555556e+00,  -1.34414414e+00,  -1.29494949e+00,
                   -1.29494949e+00,  -1.34414414e+00,  -1.34414414e+00,
                   -1.34414414e+00,  -1.18294574e+00,  -1.10000000e+00,
                   -1.05641026e+00,  -1.00000000e+00,  -7.37704918e-01,
                   -7.13580247e-01,  -7.13580247e-01,  -7.37704918e-01,
                   -7.37704918e-01,  -4.36619718e-01,  -2.91555556e-01,
                   -1.56140351e-01,   1.96914557e-16,   2.62295082e-01],
                  [-1.62857143e+00,  -1.29494949e+00,  -1.18294574e+00,
                   -1.18294574e+00,  -1.18294574e+00,  -1.18294574e+00,
                   -1.18294574e+00,  -1.18294574e+00,  -1.10000000e+00,
                   -1.05333333e+00,  -1.00000000e+00,  -7.13580247e-01,
                   -5.72916667e-01,  -5.72916667e-01,  -5.72916667e-01,
                   -5.72916667e-01,  -2.91555556e-01,  -1.26984127e-01,
                    6.45478503e-17,   1.56140351e-01,   4.27083333e-01],
                  [-1.62857143e+00,  -1.29494949e+00,  -1.18294574e+00,
                   -1.10000000e+00,  -1.10000000e+00,  -1.10000000e+00,
                   -1.10000000e+00,  -1.10000000e+00,  -1.10000000e+00,
                   -1.05333333e+00,  -1.00000000e+00,  -7.13580247e-01,
                   -5.72916667e-01,  -4.27083333e-01,  -4.27083333e-01,
                   -4.27083333e-01,  -1.56140351e-01,   2.42054439e-16,
                    1.26984127e-01,   2.91555556e-01,   5.72916667e-01],
                  [-1.65555556e+00,  -1.34414414e+00,  -1.18294574e+00,
                   -1.10000000e+00,  -1.05641026e+00,  -1.05641026e+00,
                   -1.05641026e+00,  -1.05333333e+00,  -1.05333333e+00,
                   -1.05641026e+00,  -1.00000000e+00,  -7.37704918e-01,
                   -5.72916667e-01,  -4.27083333e-01,  -2.62295082e-01,
                   -2.62295082e-01,   2.29733650e-16,   1.56140351e-01,
                    2.91555556e-01,   4.36619718e-01,   7.37704918e-01],
                  [-1.66666667e+00,  -1.34414414e+00,  -1.18294574e+00,
                   -1.10000000e+00,  -1.05641026e+00,  -1.00000000e+00,
                   -1.00000000e+00,  -1.00000000e+00,  -1.00000000e+00,
                   -1.00000000e+00,  -1.00000000e+00,  -7.37704918e-01,
                   -5.72916667e-01,  -4.27083333e-01,  -2.62295082e-01,
                   -2.77555756e-17,   2.62295082e-01,   4.27083333e-01,
                    5.72916667e-01,   7.37704918e-01,   1.00000000e+00],
                  [-1.34414414e+00,  -1.34414414e+00,  -1.18294574e+00,
                   -1.10000000e+00,  -1.05641026e+00,  -1.00000000e+00,
                   -7.37704918e-01,  -7.13580247e-01,  -7.13580247e-01,
                   -7.37704918e-01,  -7.37704918e-01,  -4.36619718e-01,
                   -2.91555556e-01,  -1.56140351e-01,   4.17271323e-16,
                    2.62295082e-01,   2.62295082e-01,   4.27083333e-01,
                    5.72916667e-01,   7.37704918e-01,   1.00000000e+00],
                  [-1.18294574e+00,  -1.18294574e+00,  -1.18294574e+00,
                   -1.10000000e+00,  -1.05333333e+00,  -1.00000000e+00,
                   -7.13580247e-01,  -5.72916667e-01,  -5.72916667e-01,
                   -5.72916667e-01,  -5.72916667e-01,  -2.91555556e-01,
                   -1.26984127e-01,   2.09780513e-16,   1.56140351e-01,
                    4.27083333e-01,   4.27083333e-01,   4.27083333e-01,
                    5.72916667e-01,   7.13580247e-01,   1.00000000e+00],
                  [-1.10000000e+00,  -1.10000000e+00,  -1.10000000e+00,
                   -1.10000000e+00,  -1.05333333e+00,  -1.00000000e+00,
                   -7.13580247e-01,  -5.72916667e-01,  -4.27083333e-01,
                   -4.27083333e-01,  -4.27083333e-01,  -1.56140351e-01,
                    2.42054439e-16,   1.26984127e-01,   2.91555556e-01,
                    5.72916667e-01,   5.72916667e-01,   5.72916667e-01,
                    5.72916667e-01,   7.13580247e-01,   1.00000000e+00],
                  [-1.05641026e+00,  -1.05641026e+00,  -1.05333333e+00,
                   -1.05333333e+00,  -1.05641026e+00,  -1.00000000e+00,
                   -7.37704918e-01,  -5.72916667e-01,  -4.27083333e-01,
                   -2.62295082e-01,  -2.62295082e-01,   2.29733650e-16,
                    1.56140351e-01,   2.91555556e-01,   4.36619718e-01,
                    7.37704918e-01,   7.37704918e-01,   7.13580247e-01,
                    7.13580247e-01,   7.37704918e-01,   1.00000000e+00],
                  [-1.00000000e+00,  -1.00000000e+00,  -1.00000000e+00,
                   -1.00000000e+00,  -1.00000000e+00,  -1.00000000e+00,
                   -7.37704918e-01,  -5.72916667e-01,  -4.27083333e-01,
                   -2.62295082e-01,  -2.77555756e-17,   2.62295082e-01,
                    4.27083333e-01,   5.72916667e-01,   7.37704918e-01,
                    1.00000000e+00,   1.00000000e+00,   1.00000000e+00,
                    1.00000000e+00,   1.00000000e+00,   1.00000000e+00],
                  [-1.00000000e+00,  -7.37704918e-01,  -7.13580247e-01,
                   -7.13580247e-01,  -7.37704918e-01,  -7.37704918e-01,
                   -4.36619718e-01,  -2.91555556e-01,  -1.56140351e-01,
                    2.29733650e-16,   2.62295082e-01,   2.62295082e-01,
                    4.27083333e-01,   5.72916667e-01,   7.37704918e-01,
                     1.00000000e+00,   1.05641026e+00,   1.05333333e+00,
                     1.05333333e+00,   1.05641026e+00,   1.05641026e+00],
                  [-1.00000000e+00,  -7.13580247e-01,  -5.72916667e-01,
                    -5.72916667e-01,  -5.72916667e-01,  -5.72916667e-01,
                    -2.91555556e-01,  -1.26984127e-01,   2.42054439e-16,
                     1.56140351e-01,   4.27083333e-01,   4.27083333e-01,
                     4.27083333e-01,   5.72916667e-01,   7.13580247e-01,
                     1.00000000e+00,   1.05333333e+00,   1.10000000e+00,
                     1.10000000e+00,   1.10000000e+00,   1.10000000e+00],
                  [-1.00000000e+00,  -7.13580247e-01,  -5.72916667e-01,
                   -4.27083333e-01,  -4.27083333e-01,  -4.27083333e-01,
                   -1.56140351e-01,   2.09780513e-16,   1.26984127e-01,
                    2.91555556e-01,   5.72916667e-01,   5.72916667e-01,
                    5.72916667e-01,   5.72916667e-01,   7.13580247e-01,
                    1.00000000e+00,   1.05333333e+00,   1.10000000e+00,
                    1.18294574e+00,   1.18294574e+00,   1.18294574e+00],
                  [-1.00000000e+00,  -7.37704918e-01,  -5.72916667e-01,
                   -4.27083333e-01,  -2.62295082e-01,  -2.62295082e-01,
                    4.17271323e-16,   1.56140351e-01,   2.91555556e-01,
                    4.36619718e-01,   7.37704918e-01,   7.37704918e-01,
                    7.13580247e-01,   7.13580247e-01,   7.37704918e-01,
                    1.00000000e+00,   1.05641026e+00,   1.10000000e+00,
                    1.18294574e+00,   1.34414414e+00,   1.34414414e+00],
                  [-1.00000000e+00,  -7.37704918e-01,  -5.72916667e-01,
                   -4.27083333e-01,  -2.62295082e-01,  -2.77555756e-17,
                    2.62295082e-01,   4.27083333e-01,   5.72916667e-01,
                    7.37704918e-01,   1.00000000e+00,   1.00000000e+00,
                    1.00000000e+00,   1.00000000e+00,   1.00000000e+00,
                    1.00000000e+00,   1.05641026e+00,   1.10000000e+00,
                    1.18294574e+00,   1.34414414e+00,   1.66666667e+00],
                  [-7.37704918e-01,  -4.36619718e-01,  -2.91555556e-01,
                   -1.56140351e-01,   2.29733650e-16,   2.62295082e-01,
                    2.62295082e-01,   4.27083333e-01,   5.72916667e-01,
                    7.37704918e-01,   1.00000000e+00,   1.05641026e+00,
                    1.05333333e+00,   1.05333333e+00,   1.05641026e+00,
                    1.05641026e+00,   1.05641026e+00,   1.10000000e+00,
                    1.18294574e+00,   1.34414414e+00,   1.65555556e+00],
                  [-5.72916667e-01,  -2.91555556e-01,  -1.26984127e-01,
                    2.42054439e-16,   1.56140351e-01,   4.27083333e-01,
                    4.27083333e-01,   4.27083333e-01,   5.72916667e-01,
                    7.13580247e-01,   1.00000000e+00,   1.05333333e+00,
                    1.10000000e+00,   1.10000000e+00,   1.10000000e+00,
                    1.10000000e+00,   1.10000000e+00,   1.10000000e+00,
                    1.18294574e+00,   1.29494949e+00,   1.62857143e+00],
                  [-4.27083333e-01,  -1.56140351e-01,   6.45478503e-17,
                    1.26984127e-01,   2.91555556e-01,   5.72916667e-01,
                    5.72916667e-01,   5.72916667e-01,   5.72916667e-01,
                    7.13580247e-01,   1.00000000e+00,   1.05333333e+00,
                    1.10000000e+00,   1.18294574e+00,   1.18294574e+00,
                    1.18294574e+00,   1.18294574e+00,   1.18294574e+00,
                    1.18294574e+00,   1.29494949e+00,   1.62857143e+00],
                  [-2.62295082e-01,   1.96914557e-16,   1.56140351e-01,
                    2.91555556e-01,   4.36619718e-01,   7.37704918e-01,
                    7.37704918e-01,   7.13580247e-01,   7.13580247e-01,
                    7.37704918e-01,   1.00000000e+00,   1.05641026e+00,
                    1.10000000e+00,   1.18294574e+00,   1.34414414e+00,
                    1.34414414e+00,   1.34414414e+00,   1.29494949e+00,
                    1.29494949e+00,   1.34414414e+00,   1.65555556e+00],
                  [-2.77555756e-17,   2.62295082e-01,   4.27083333e-01,
                    5.72916667e-01,   7.37704918e-01,   1.00000000e+00,
                    1.00000000e+00,   1.00000000e+00,   1.00000000e+00,
                    1.00000000e+00,   1.00000000e+00,   1.05641026e+00,
                    1.10000000e+00,   1.18294574e+00,   1.34414414e+00,
                    1.66666667e+00,   1.65555556e+00,   1.62857143e+00,
                    1.62857143e+00,   1.65555556e+00,   1.66666667e+00]])  # nopep8

    # Ensure results are within expected limits
    np.testing.assert_allclose(z1, expected)


if __name__ == '__main__':
    tst.run_module_suite()
