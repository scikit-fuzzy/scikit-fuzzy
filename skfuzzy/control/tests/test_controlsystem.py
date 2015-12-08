import numpy as np
import numpy.testing as tst

from skfuzzy.control import Antecedent, Consequent, Rule, ControlSystem
from skfuzzy import trimf


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
    rule1 = Rule([food['poor'], service['poor']], tip['bad'], kind='or')
    rule2 = Rule(service['average'], tip['middling'])
    rule3 = Rule([service['good'], food['good']], tip['lots'])

    # The control system - defined both possible ways
    tipping = ControlSystem([rule1, rule2, rule3])

    tipping2 = ControlSystem()
    tipping2.addrule(rule2)
    tipping2.addrule(rule3)
    tipping2.addrule(rule1)

    # Inputs added both possible ways
    inputs = {'quality': 6.5, 'service': 9.8}
    for key, value in inputs.items():
        tipping.input[key] = value

    tipping2.inputs(inputs)

    # Compute the system
    tipping.compute()
    tipping2.compute()

    assert tipping.output == tipping2.output
    tst.assert_allclose(tipping.output['tip'], 20.244508118433625)


def test_bad_rules():
    not_rules = ['me', 192238, 42, dict()]
    tst.assert_raises(ValueError, ControlSystem, not_rules)

if __name__ == '__main__':
    tst.run_module_suite()
