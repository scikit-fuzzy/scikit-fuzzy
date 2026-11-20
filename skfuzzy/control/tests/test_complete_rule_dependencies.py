import numpy as np
import numpy.testing as tst
from skfuzzy import control as ctrl


def test_all_producers_precede_dependent_rule():
    a = ctrl.Antecedent(np.linspace(0, 10, 11), 'a')
    c = ctrl.Consequent(np.linspace(0, 10, 11), 'c')
    d = ctrl.Consequent(np.linspace(0, 10, 11), 'd')
    for variable in [a, c, d]:
        variable.automf(3)
    first = ctrl.Rule(a['poor'], c['poor'], label='first')
    second = ctrl.Rule(a['good'], c['poor'], label='second')
    dependent = ctrl.Rule(c['poor'], d['poor'], label='dependent')
    system = ctrl.ControlSystem([first, dependent, second])
    tst.assert_array_equal(list(system.rules), [first, second, dependent])
