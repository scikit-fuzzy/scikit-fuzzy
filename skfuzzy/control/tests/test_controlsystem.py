from __future__ import division

import sys

import numpy as np
import numpy.testing as tst
import nose

import skfuzzy as fuzz
import skfuzzy.control as ctrl


def test_tipping_problem():
    # The full tipping problem uses many of these methods
    food = ctrl.Antecedent(np.linspace(0, 10, 11), 'quality')
    service = ctrl.Antecedent(np.linspace(0, 10, 11), 'service')
    tip = ctrl.Consequent(np.linspace(0, 25, 26), 'tip')

    food.automf(3)
    service.automf(3)

    # Manual membership function definition
    tip['bad'] = fuzz.trimf(tip.universe, [0, 0, 13])
    tip['middling'] = fuzz.trimf(tip.universe, [0, 13, 25])
    tip['lots'] = fuzz.trimf(tip.universe, [13, 25, 25])

    # Define fuzzy rules
    rule1 = ctrl.Rule(food['poor'] | service['poor'], tip['bad'])
    rule2 = ctrl.Rule(service['average'], tip['middling'])
    rule3 = ctrl.Rule(service['good'] | food['good'], tip['lots'])

    # The control system - defined both possible ways
    tipping = ctrl.ControlSystem([rule1, rule2, rule3])

    tipping2 = ctrl.ControlSystem()
    tipping2.addrule(rule2)
    tipping2.addrule(rule3)
    tipping2.addrule(rule1)

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


def test_bad_rules():
    not_rules = ['me', 192238, 42, dict()]
    tst.assert_raises(ValueError, ctrl.ControlSystem, not_rules)


def setup_rule_order():
    global a, b, c, d
    a = ctrl.Antecedent(np.linspace(0, 10, 11), 'a')
    b = ctrl.Antecedent(np.linspace(0, 10, 11), 'b')
    c = ctrl.Antecedent(np.linspace(0, 10, 11), 'c')
    d = ctrl.Antecedent(np.linspace(0, 10, 11), 'd')

    for v in (a, b, c, d):
        v.automf(3)


@nose.with_setup(setup_rule_order)
def test_rule_order():
    # Make sure rules are exposed in the order needed to solve them
    #  correctly
    global a, b, c, d

    r1 = ctrl.Rule(a['average'] | a['poor'], c['poor'], label='r1')
    r2 = ctrl.Rule(c['poor'] | b['poor'], c['good'], label='r2')
    r3 = ctrl.Rule(c['good'] | a['good'], d['good'], label='r3')

    ctrl_sys = ctrl.ControlSystem([r1, r2, r3])
    resolved = list(ctrl_sys.rules)
    assert resolved == [r1, r2, r3], "Order given was: %s" % resolved


# The assert_raises decorator does not work in Python 2.6
@tst.decorators.skipif(sys.version_info < (2, 7))
@nose.with_setup(setup_rule_order)
def test_unresolvable_rule_order():
    # Make sure we don't get suck in an infinite loop when the user
    #  gives an unresolvable rule order
    global a, b, c, d

    r1 = ctrl.Rule(a['average'] | a['poor'], c['poor'], label='r1')
    r2 = ctrl.Rule(c['poor'] | b['poor'], c['poor'], label='r2')
    r3 = ctrl.Rule(c['good'] | a['good'], d['good'], label='r3')

    ex_msg = "Unable to resolve rule execution order"
    with tst.assert_raises(RuntimeError, expected_regexp=ex_msg):
        ctrl_sys = ctrl.ControlSystem([r1, r2, r3])
        list(ctrl_sys.rules)


def test_multiple_rules_same_consequent_term():
    # 2 input variables, 1 output variable and 7 instances.
    x1_inputs = [0.6, 0.2, 0.4, 0.7, 1, 1.2, 1.8]
    x2_inputs = [0.9, 1, 0.8, 0, 1.2, 0.6, 1.8]

    dom = np.arange(0, 2.1, 0.01)
    x1 = ctrl.Antecedent(dom, "x1")
    x1['label0'] = fuzz.trimf(x1.universe, (0.2, 0.2, 0.6))
    x1['label1'] = fuzz.trimf(x1.universe, (0.2, 0.6, 1.0))
    x1['label2'] = fuzz.trimf(x1.universe, (0.6, 1.0, 1.4))
    x1['label3'] = fuzz.trimf(x1.universe, (1.0, 1.4, 1.8))
    x1['label4'] = fuzz.trimf(x1.universe, (1.4, 1.8, 1.8))

    x2 = ctrl.Antecedent(dom, "x2")
    x2['label0'] = fuzz.trimf(x2.universe, (0.0, 0.0, 0.45))
    x2['label1'] = fuzz.trimf(x2.universe, (0.0, 0.45, 0.9))
    x2['label2'] = fuzz.trimf(x2.universe, (0.45, 0.9, 1.35))
    x2['label3'] = fuzz.trimf(x2.universe, (0.9, 1.35, 1.8))
    x2['label4'] = fuzz.trimf(x2.universe, (1.35, 1.8, 1.8))

    y = ctrl.Consequent(dom, "y")
    y['label0'] = fuzz.trimf(y.universe, (0.3, 0.3, 0.725))
    y['label1'] = fuzz.trimf(y.universe, (0.3, 0.725, 1.15))
    y['label2'] = fuzz.trimf(y.universe, (0.725, 1.15, 1.575))
    y['label3'] = fuzz.trimf(y.universe, (1.15, 1.575, 2.0))
    y['label4'] = fuzz.trimf(y.universe, (1.575, 2.0, 2.0))

    r1 = ctrl.Rule(x1['label0'] & x2['label2'], y['label0'])
    r2 = ctrl.Rule(x1['label1'] & x2['label0'], y['label0'])
    r3 = ctrl.Rule(x1['label1'] & x2['label2'], y['label0'])

    # Equivalent to above 3 rules
    r123 = ctrl.Rule((x1['label0'] & x2['label2']) |
                     (x1['label1'] & x2['label0']) |
                     (x1['label1'] & x2['label2']), y['label0'])

    r4 = ctrl.Rule(x1['label2'] & x2['label1'], y['label2'])
    r5 = ctrl.Rule(x1['label2'] & x2['label3'], y['label3'])
    r6 = ctrl.Rule(x1['label4'] & x2['label4'], y['label4'])

    # Build a system with three rules targeting the same Consequent Term,
    # and then an equivalent system with those three rules combined into one.
    cs0 = ctrl.ControlSystem([r1, r2, r3, r4, r5, r6])
    cs1 = ctrl.ControlSystem([r123, r4, r5, r6])

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


if __name__ == '__main__':
    tst.run_module_suite()
