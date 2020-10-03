import networkx
import nose
import numpy as np
import numpy.testing as tst
import skfuzzy as fuzz
import skfuzzy.control as ctrl
from pytest import approx, raises

try:
    from numpy.testing.decorators import skipif
except AttributeError:
    from numpy.testing.dec import skipif
except ModuleNotFoundError:
    from numpy.testing import dec
    skipif = dec.skipif

from skfuzzy.control import EmptyMembershipError


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
    global a, b, c, d
    a = ctrl.Antecedent(np.linspace(0, 10, 11), 'a')
    b = ctrl.Antecedent(np.linspace(0, 10, 11), 'b')
    c = ctrl.Antecedent(np.linspace(0, 10, 11), 'c')
    d = ctrl.Antecedent(np.linspace(0, 10, 11), 'd')

    for v in (a, b, c, d):
        v.automf(3)


def test_bad_inputs():
    # Start with the tipping problem
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

    tipping2 = ctrl.ControlSystem(rule1)
    tipping2.addrule(rule2)
    tipping2.addrule(rule3)

    tip_sim = ctrl.ControlSystemSimulation(tipping, clip_to_bounds=False)
    tip_sim2 = ctrl.ControlSystemSimulation(tipping2, clip_to_bounds=True)

    # With clipping to bounds, these should work
    tip_sim2.input['quality'] = -np.pi  # below minimum, clipped to 0
    tip_sim2.input['service'] = 15  # above maximum, clipped to 10

    # Ensure the input checking is working properly when bounds aren't clipped
    negative_pass = False
    try:
        tip_sim.input['quality'] = -np.pi  # below minimum in universe
    except IndexError:
        negative_pass = True  # It should raise this
    else:
        if not negative_pass:
            raise ValueError('Input checking is not working correctly!  '
                             'Minimum universe valuse is 0, but -3.14 did not '
                             'raise an IndexError.')

    positive_pass = False
    try:
        tip_sim.input['quality'] = 15  # above maximum in universe
    except IndexError:
        positive_pass = True  # It should raise this
    else:
        if not positive_pass:
            raise ValueError('Input checking is not working correctly!  '
                             'Maximum universe valuse is 10, but 15 did not '
                             'raise an IndexError.')


@skipif(float(networkx.__version__) >= 2.0)
@nose.with_setup(setup_rule_order)
def test_rule_order():
    # Make sure rules are exposed in the order needed to solve them
    # correctly
    global a, b, c, d

    r1 = ctrl.Rule(a['average'] | a['poor'], c['poor'], label='r1')
    r2 = ctrl.Rule(c['poor'] | b['poor'], c['good'], label='r2')
    r3 = ctrl.Rule(c['good'] | a['good'], d['good'], label='r3')

    ctrl_sys = ctrl.ControlSystem([r1, r2, r3])
    resolved = list(ctrl_sys.rules)
    assert resolved == [r1, r2, r3], ("Order given was: {0}, expected {1}"
                                      .format(resolved,
                                              [r1.label, r2.label, r3.label]))


# The assert_raises decorator does not work in Python 2.6
@skipif(float(networkx.__version__) >= 2.0)
@nose.with_setup(setup_rule_order)
def test_unresolvable_rule_order():
    # Make sure we don't get suck in an infinite loop when the user
    # gives an unresolvable rule order
    global a, b, c, d

    r1 = ctrl.Rule(a['average'] | a['poor'], c['poor'], label='r1')
    r2 = ctrl.Rule(c['poor'] | b['poor'], c['poor'], label='r2')
    r3 = ctrl.Rule(c['good'] | a['good'], d['good'], label='r3')

    ex_msg = "Unable to resolve rule execution order"
    with tst.assert_raises(RuntimeError, expected_regexp=ex_msg):
        ctrl_sys = ctrl.ControlSystem([r1, r2, r3])
        list(ctrl_sys.rules)


@nose.with_setup(setup_rule_order)
def test_bad_rules():
    global a

    not_rules = ['me', 192238, 42, dict()]
    tst.assert_raises(ValueError, ctrl.ControlSystem, not_rules)

    testsystem = ctrl.ControlSystem()
    tst.assert_raises(ValueError, testsystem.addrule, a)


def test_lenient_simulation():
    x1 = ctrl.Antecedent(np.linspace(0, 10, 11), "x1")
    x1.automf(3)  # term labels: poor, average, good
    x2 = ctrl.Antecedent(np.linspace(0, 10, 11), "x2")
    x2.automf(3)

    y1 = ctrl.Consequent(np.linspace(0, 10, 11), "y1")
    y1.automf(3)
    y2 = ctrl.Consequent(np.linspace(0, 10, 11), "y2")
    y2.automf(3)

    r1 = ctrl.Rule(x1["poor"], y1["good"])
    r2 = ctrl.Rule(x2["poor"], y2["good"])
    sys = ctrl.ControlSystem([r1, r2])

    sim = ctrl.ControlSystemSimulation(sys)
    sim.input["x1"] = 0
    sim.input["x2"] = 0
    sim.compute()
    assert set(sim.output.keys()) == {"y1", "y2"}
    # print("- sim.output['y1']:", sim.output["y1"])
    # print("- sim.output['y2']:", sim.output["y2"])
    assert sim.output["y1"] == approx(8.333333)
    assert sim.output["y2"] == approx(8.333333)

    sim = ctrl.ControlSystemSimulation(sys, lenient=False)
    sim.input["x1"] = 10
    sim.input["x2"] = 0
    with raises(EmptyMembershipError):
        sim.compute()

    sim = ctrl.ControlSystemSimulation(sys, lenient=True)
    sim.input["x1"] = 10
    sim.input["x2"] = 0
    sim.compute()
    assert set(sim.output.keys()) == {"y2"}
    assert sim.output["y2"] == approx(8.333333)


def test_cached_lenient_simulation():
    x1 = ctrl.Antecedent(np.linspace(0, 10, 11), "x1")
    x1.automf(3)  # term labels: poor, average, good
    x2 = ctrl.Antecedent(np.linspace(0, 10, 11), "x2")
    x2.automf(3)

    y1 = ctrl.Consequent(np.linspace(0, 10, 11), "y1")
    y1.automf(3)
    y2 = ctrl.Consequent(np.linspace(0, 10, 11), "y2")
    y2.automf(3)

    r1 = ctrl.Rule(x1["poor"], y1["good"])
    r2 = ctrl.Rule(x2["poor"], y2["good"])
    sys = ctrl.ControlSystem([r1, r2])

    sim = ctrl.ControlSystemSimulation(sys)
    sim.input["x1"] = 10
    sim.input["x2"] = 0
    sim.compute()
    # print("- sim.output.keys:", set(sim.output.keys()))
    assert set(sim.output.keys()) == {"y2"}

    sim.compute()
    assert set(sim.output.keys()) == {"y2"}


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


def test_complex_system():
    # A much more complex system, run multiple times & with array inputs
    universe = np.linspace(-2, 2, 5)
    error = ctrl.Antecedent(universe, 'error')
    delta = ctrl.Antecedent(universe, 'delta')
    output = ctrl.Consequent(universe, 'output')

    names = ['nb', 'ns', 'ze', 'ps', 'pb']
    error.automf(names=names)
    delta.automf(names=names)
    output.automf(names=names)

    # The rulebase:
    # rule 1:  IF e = ZE AND delta = ZE THEN output = ZE
    # rule 2:  IF e = ZE AND delta = SP THEN output = SN
    # rule 3:  IF e = SN AND delta = SN THEN output = LP
    # rule 4:  IF e = LP OR  delta = LP THEN output = LN

    rule0 = ctrl.Rule(antecedent=((error['nb'] & delta['nb']) |
                                  (error['ns'] & delta['nb']) |
                                  (error['nb'] & delta['ns'])),
                      consequent=output['nb'], label='rule nb')

    rule1 = ctrl.Rule(antecedent=((error['nb'] & delta['ze']) |
                                  (error['nb'] & delta['ps']) |
                                  (error['ns'] & delta['ns']) |
                                  (error['ns'] & delta['ze']) |
                                  (error['ze'] & delta['ns']) |
                                  (error['ze'] & delta['nb']) |
                                  (error['ps'] & delta['nb'])),
                      consequent=output['ns'], label='rule ns')

    rule2 = ctrl.Rule(antecedent=((error['nb'] & delta['pb']) |
                                  (error['ns'] & delta['ps']) |
                                  (error['ze'] & delta['ze']) |
                                  (error['ps'] & delta['ns']) |
                                  (error['pb'] & delta['nb'])),
                      consequent=output['ze'], label='rule ze')

    rule3 = ctrl.Rule(antecedent=((error['ns'] & delta['pb']) |
                                  (error['ze'] & delta['pb']) |
                                  (error['ze'] & delta['ps']) |
                                  (error['ps'] & delta['ps']) |
                                  (error['ps'] & delta['ze']) |
                                  (error['pb'] & delta['ze']) |
                                  (error['pb'] & delta['ns'])),
                      consequent=output['ps'], label='rule ps')

    rule4 = ctrl.Rule(antecedent=((error['ps'] & delta['pb']) |
                                  (error['pb'] & delta['pb']) |
                                  (error['pb'] & delta['ps'])),
                      consequent=output['pb'], label='rule pb')

    system = ctrl.ControlSystem(rules=[rule0, rule1, rule2, rule3, rule4])

    sim = ctrl.ControlSystemSimulation(system, cache=False)

    x, y = np.meshgrid(np.linspace(-2, 2, 21), np.linspace(-2, 2, 21))
    z0 = np.zeros_like(x)

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
        np.array([[ -1.66666667e+00,  -1.65555556e+00,  -1.62857143e+00,
                    -1.62857143e+00,  -1.65555556e+00,  -1.66666667e+00,
                    -1.34414414e+00,  -1.18294574e+00,  -1.10000000e+00,
                    -1.05641026e+00,  -1.00000000e+00,  -1.00000000e+00,
                    -1.00000000e+00,  -1.00000000e+00,  -1.00000000e+00,
                    -1.00000000e+00,  -7.37704918e-01,  -5.72916667e-01,
                    -4.27083333e-01,  -2.62295082e-01,  -2.77555756e-17],
                  [ -1.65555556e+00,  -1.34414414e+00,  -1.29494949e+00,
                    -1.29494949e+00,  -1.34414414e+00,  -1.34414414e+00,
                    -1.34414414e+00,  -1.18294574e+00,  -1.10000000e+00,
                    -1.05641026e+00,  -1.00000000e+00,  -7.37704918e-01,
                    -7.13580247e-01,  -7.13580247e-01,  -7.37704918e-01,
                    -7.37704918e-01,  -4.36619718e-01,  -2.91555556e-01,
                    -1.56140351e-01,   1.96914557e-16,   2.62295082e-01],
                  [ -1.62857143e+00,  -1.29494949e+00,  -1.18294574e+00,
                    -1.18294574e+00,  -1.18294574e+00,  -1.18294574e+00,
                    -1.18294574e+00,  -1.18294574e+00,  -1.10000000e+00,
                    -1.05333333e+00,  -1.00000000e+00,  -7.13580247e-01,
                    -5.72916667e-01,  -5.72916667e-01,  -5.72916667e-01,
                    -5.72916667e-01,  -2.91555556e-01,  -1.26984127e-01,
                     6.45478503e-17,   1.56140351e-01,   4.27083333e-01],
                  [ -1.62857143e+00,  -1.29494949e+00,  -1.18294574e+00,
                    -1.10000000e+00,  -1.10000000e+00,  -1.10000000e+00,
                    -1.10000000e+00,  -1.10000000e+00,  -1.10000000e+00,
                    -1.05333333e+00,  -1.00000000e+00,  -7.13580247e-01,
                    -5.72916667e-01,  -4.27083333e-01,  -4.27083333e-01,
                    -4.27083333e-01,  -1.56140351e-01,   2.42054439e-16,
                     1.26984127e-01,   2.91555556e-01,   5.72916667e-01],
                  [ -1.65555556e+00,  -1.34414414e+00,  -1.18294574e+00,
                    -1.10000000e+00,  -1.05641026e+00,  -1.05641026e+00,
                    -1.05641026e+00,  -1.05333333e+00,  -1.05333333e+00,
                    -1.05641026e+00,  -1.00000000e+00,  -7.37704918e-01,
                    -5.72916667e-01,  -4.27083333e-01,  -2.62295082e-01,
                    -2.62295082e-01,   2.29733650e-16,   1.56140351e-01,
                     2.91555556e-01,   4.36619718e-01,   7.37704918e-01],
                  [ -1.66666667e+00,  -1.34414414e+00,  -1.18294574e+00,
                    -1.10000000e+00,  -1.05641026e+00,  -1.00000000e+00,
                    -1.00000000e+00,  -1.00000000e+00,  -1.00000000e+00,
                    -1.00000000e+00,  -1.00000000e+00,  -7.37704918e-01,
                    -5.72916667e-01,  -4.27083333e-01,  -2.62295082e-01,
                    -2.77555756e-17,   2.62295082e-01,   4.27083333e-01,
                     5.72916667e-01,   7.37704918e-01,   1.00000000e+00],
                  [ -1.34414414e+00,  -1.34414414e+00,  -1.18294574e+00,
                    -1.10000000e+00,  -1.05641026e+00,  -1.00000000e+00,
                    -7.37704918e-01,  -7.13580247e-01,  -7.13580247e-01,
                    -7.37704918e-01,  -7.37704918e-01,  -4.36619718e-01,
                    -2.91555556e-01,  -1.56140351e-01,   4.17271323e-16,
                     2.62295082e-01,   2.62295082e-01,   4.27083333e-01,
                     5.72916667e-01,   7.37704918e-01,   1.00000000e+00],
                  [ -1.18294574e+00,  -1.18294574e+00,  -1.18294574e+00,
                    -1.10000000e+00,  -1.05333333e+00,  -1.00000000e+00,
                    -7.13580247e-01,  -5.72916667e-01,  -5.72916667e-01,
                    -5.72916667e-01,  -5.72916667e-01,  -2.91555556e-01,
                    -1.26984127e-01,   2.09780513e-16,   1.56140351e-01,
                     4.27083333e-01,   4.27083333e-01,   4.27083333e-01,
                     5.72916667e-01,   7.13580247e-01,   1.00000000e+00],
                  [ -1.10000000e+00,  -1.10000000e+00,  -1.10000000e+00,
                    -1.10000000e+00,  -1.05333333e+00,  -1.00000000e+00,
                    -7.13580247e-01,  -5.72916667e-01,  -4.27083333e-01,
                    -4.27083333e-01,  -4.27083333e-01,  -1.56140351e-01,
                     2.42054439e-16,   1.26984127e-01,   2.91555556e-01,
                     5.72916667e-01,   5.72916667e-01,   5.72916667e-01,
                     5.72916667e-01,   7.13580247e-01,   1.00000000e+00],
                  [ -1.05641026e+00,  -1.05641026e+00,  -1.05333333e+00,
                    -1.05333333e+00,  -1.05641026e+00,  -1.00000000e+00,
                    -7.37704918e-01,  -5.72916667e-01,  -4.27083333e-01,
                    -2.62295082e-01,  -2.62295082e-01,   2.29733650e-16,
                     1.56140351e-01,   2.91555556e-01,   4.36619718e-01,
                     7.37704918e-01,   7.37704918e-01,   7.13580247e-01,
                     7.13580247e-01,   7.37704918e-01,   1.00000000e+00],
                  [ -1.00000000e+00,  -1.00000000e+00,  -1.00000000e+00,
                    -1.00000000e+00,  -1.00000000e+00,  -1.00000000e+00,
                    -7.37704918e-01,  -5.72916667e-01,  -4.27083333e-01,
                    -2.62295082e-01,  -2.77555756e-17,   2.62295082e-01,
                     4.27083333e-01,   5.72916667e-01,   7.37704918e-01,
                     1.00000000e+00,   1.00000000e+00,   1.00000000e+00,
                     1.00000000e+00,   1.00000000e+00,   1.00000000e+00],
                  [ -1.00000000e+00,  -7.37704918e-01,  -7.13580247e-01,
                    -7.13580247e-01,  -7.37704918e-01,  -7.37704918e-01,
                    -4.36619718e-01,  -2.91555556e-01,  -1.56140351e-01,
                     2.29733650e-16,   2.62295082e-01,   2.62295082e-01,
                     4.27083333e-01,   5.72916667e-01,   7.37704918e-01,
                     1.00000000e+00,   1.05641026e+00,   1.05333333e+00,
                     1.05333333e+00,   1.05641026e+00,   1.05641026e+00],
                  [ -1.00000000e+00,  -7.13580247e-01,  -5.72916667e-01,
                    -5.72916667e-01,  -5.72916667e-01,  -5.72916667e-01,
                    -2.91555556e-01,  -1.26984127e-01,   2.42054439e-16,
                     1.56140351e-01,   4.27083333e-01,   4.27083333e-01,
                     4.27083333e-01,   5.72916667e-01,   7.13580247e-01,
                     1.00000000e+00,   1.05333333e+00,   1.10000000e+00,
                     1.10000000e+00,   1.10000000e+00,   1.10000000e+00],
                  [ -1.00000000e+00,  -7.13580247e-01,  -5.72916667e-01,
                    -4.27083333e-01,  -4.27083333e-01,  -4.27083333e-01,
                    -1.56140351e-01,   2.09780513e-16,   1.26984127e-01,
                     2.91555556e-01,   5.72916667e-01,   5.72916667e-01,
                     5.72916667e-01,   5.72916667e-01,   7.13580247e-01,
                     1.00000000e+00,   1.05333333e+00,   1.10000000e+00,
                     1.18294574e+00,   1.18294574e+00,   1.18294574e+00],
                  [ -1.00000000e+00,  -7.37704918e-01,  -5.72916667e-01,
                    -4.27083333e-01,  -2.62295082e-01,  -2.62295082e-01,
                     4.17271323e-16,   1.56140351e-01,   2.91555556e-01,
                     4.36619718e-01,   7.37704918e-01,   7.37704918e-01,
                     7.13580247e-01,   7.13580247e-01,   7.37704918e-01,
                     1.00000000e+00,   1.05641026e+00,   1.10000000e+00,
                     1.18294574e+00,   1.34414414e+00,   1.34414414e+00],
                  [ -1.00000000e+00,  -7.37704918e-01,  -5.72916667e-01,
                    -4.27083333e-01,  -2.62295082e-01,  -2.77555756e-17,
                     2.62295082e-01,   4.27083333e-01,   5.72916667e-01,
                     7.37704918e-01,   1.00000000e+00,   1.00000000e+00,
                     1.00000000e+00,   1.00000000e+00,   1.00000000e+00,
                     1.00000000e+00,   1.05641026e+00,   1.10000000e+00,
                     1.18294574e+00,   1.34414414e+00,   1.66666667e+00],
                  [ -7.37704918e-01,  -4.36619718e-01,  -2.91555556e-01,
                    -1.56140351e-01,   2.29733650e-16,   2.62295082e-01,
                     2.62295082e-01,   4.27083333e-01,   5.72916667e-01,
                     7.37704918e-01,   1.00000000e+00,   1.05641026e+00,
                     1.05333333e+00,   1.05333333e+00,   1.05641026e+00,
                     1.05641026e+00,   1.05641026e+00,   1.10000000e+00,
                     1.18294574e+00,   1.34414414e+00,   1.65555556e+00],
                  [ -5.72916667e-01,  -2.91555556e-01,  -1.26984127e-01,
                     2.42054439e-16,   1.56140351e-01,   4.27083333e-01,
                     4.27083333e-01,   4.27083333e-01,   5.72916667e-01,
                     7.13580247e-01,   1.00000000e+00,   1.05333333e+00,
                     1.10000000e+00,   1.10000000e+00,   1.10000000e+00,
                     1.10000000e+00,   1.10000000e+00,   1.10000000e+00,
                     1.18294574e+00,   1.29494949e+00,   1.62857143e+00],
                  [ -4.27083333e-01,  -1.56140351e-01,   6.45478503e-17,
                     1.26984127e-01,   2.91555556e-01,   5.72916667e-01,
                     5.72916667e-01,   5.72916667e-01,   5.72916667e-01,
                     7.13580247e-01,   1.00000000e+00,   1.05333333e+00,
                     1.10000000e+00,   1.18294574e+00,   1.18294574e+00,
                     1.18294574e+00,   1.18294574e+00,   1.18294574e+00,
                     1.18294574e+00,   1.29494949e+00,   1.62857143e+00],
                  [ -2.62295082e-01,   1.96914557e-16,   1.56140351e-01,
                     2.91555556e-01,   4.36619718e-01,   7.37704918e-01,
                     7.37704918e-01,   7.13580247e-01,   7.13580247e-01,
                     7.37704918e-01,   1.00000000e+00,   1.05641026e+00,
                     1.10000000e+00,   1.18294574e+00,   1.34414414e+00,
                     1.34414414e+00,   1.34414414e+00,   1.29494949e+00,
                     1.29494949e+00,   1.34414414e+00,   1.65555556e+00],
                  [ -2.77555756e-17,   2.62295082e-01,   4.27083333e-01,
                     5.72916667e-01,   7.37704918e-01,   1.00000000e+00,
                     1.00000000e+00,   1.00000000e+00,   1.00000000e+00,
                     1.00000000e+00,   1.00000000e+00,   1.05641026e+00,
                     1.10000000e+00,   1.18294574e+00,   1.34414414e+00,
                     1.66666667e+00,   1.65555556e+00,   1.62857143e+00,
                     1.62857143e+00,   1.65555556e+00,   1.66666667e+00]])

    # Ensure results are within expected limits
    np.testing.assert_allclose(z1, expected)


if __name__ == '__main__':
    tst.run_module_suite()
