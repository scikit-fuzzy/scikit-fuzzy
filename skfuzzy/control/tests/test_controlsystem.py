import numpy as np
import numpy.testing as tst
import nose

from skfuzzy.control import (Antecedent, Consequent, Rule, ControlSystem,
                             ControlSystemSimulation)
from skfuzzy import trimf
from nose.tools import assert_raises


def test_tipping_problem():
    # The full tipping problem uses many of these methods
    food = Antecedent(np.linspace(0, 10, 11), 'quality')
    service = Antecedent(np.linspace(0, 10, 11), 'service')
    tip = Consequent(np.linspace(0, 25, 26), 'tip')

    food.automf(3)
    service.automf(3)

    # Manual membership function definition
    tip['bad'] = trimf(tip.universe, [0, 0, 13])
    tip['middling'] = trimf(tip.universe, [0, 13, 25])
    tip['lots'] = trimf(tip.universe, [13, 25, 25])

    # Define fuzzy rules
    rule1 = Rule(food['poor'] | service['poor'], tip['bad'])
    rule2 = Rule(service['average'], tip['middling'])
    rule3 = Rule(service['good'] | food['good'], tip['lots'])

    # The control system - defined both possible ways
    tipping = ControlSystem([rule1, rule2, rule3])

    tipping2 = ControlSystem()
    tipping2.addrule(rule2)
    tipping2.addrule(rule3)
    tipping2.addrule(rule1)

    tip_sim = ControlSystemSimulation(tipping)
    tip_sim2 = ControlSystemSimulation(tipping2)

    # Inputs added both possible ways
    inputs = {'quality': 6.5, 'service': 9.8}
    for key, value in inputs.items():
        tip_sim.input[key] = value

    tip_sim2.inputs(inputs)

    # Compute the system
    tip_sim.compute()
    tip_sim2.compute()

    assert tip_sim.output == tip_sim2.output
    tst.assert_allclose(tip_sim.output['tip'], 20.244508118433625)


def test_bad_rules():
    not_rules = ['me', 192238, 42, dict()]
    tst.assert_raises(ValueError, ControlSystem, not_rules)

def setup_rule_order():
    global a, b, c, d
    a = Antecedent(np.linspace(0, 10, 11), 'a')
    b = Antecedent(np.linspace(0, 10, 11), 'b')
    c = Antecedent(np.linspace(0, 10, 11), 'c')
    d = Antecedent(np.linspace(0, 10, 11), 'd')

    for v in (a,b,c,d):
        v.automf(3)

@nose.with_setup(setup_rule_order)
def test_rule_order():
    # Make sure rules are exposed in the order needed to solve them
    #  correctly
    global a, b, c, d

    r1 = Rule(a['average'] | a['poor'], c['poor'], label='r1')
    r2 = Rule(c['poor'] | b['poor'], c['good'], label='r2')
    r3 = Rule(c['good'] | a['good'], d['good'], label='r3')

    ctrl = ControlSystem([r1, r2, r3])
    resolved = list(ctrl.rules)
    assert resolved == [r1, r2, r3], "Order given was: %s" % resolved

@nose.with_setup(setup_rule_order)
def test_unresolvable_rule_order():
    # Make sure we don't get suck in an infinite loop when the user
    #  gives an unresolvable rule order
    global a, b, c, d

    r1 = Rule(a['average'] | a['poor'], c['poor'], label='r1')
    r2 = Rule(c['poor'] | b['poor'], c['poor'], label='r2')
    r3 = Rule(c['good'] | a['good'], d['good'], label='r3')

    ctrl = ControlSystem([r1, r2, r3])
    ex_msg = "Unable to resolve rule execution order"
    with assert_raises(RuntimeError, expected_regexp=ex_msg):
        list(ctrl.rules)

if __name__ == '__main__':
    tst.run_module_suite()
