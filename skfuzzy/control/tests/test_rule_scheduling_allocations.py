import numpy as np
from skfuzzy import control as ctrl


def test_independent_rule_order_stays_stable():
    a = ctrl.Antecedent(np.arange(11.), 'a')
    b = ctrl.Consequent(np.arange(11.), 'b')
    a.automf(3)
    b.automf(3)
    rules = [ctrl.Rule(a['average'], b['good'], label=str(i)) for i in range(100)]
    system = ctrl.ControlSystem(rules)
    assert list(system.rules) == rules
    assert list(system.rules) == rules
