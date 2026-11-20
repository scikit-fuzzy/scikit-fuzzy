import numpy as np
import numpy.testing as tst
import pytest
from skfuzzy import control as ctrl


@pytest.mark.parametrize('mode', ['centroid', 'bisector', 'mom', 'som', 'lom'])
def test_array_controller_matches_independent_scalar_runs(mode):
    a = ctrl.Antecedent(np.linspace(0, 10, 21), 'a')
    out = ctrl.Consequent(np.linspace(0, 25, 51), 'out')
    a.automf(3)
    out.automf(3)
    out.defuzzify_method = mode
    rules = [ctrl.Rule(a[name], out[name]) for name in ['poor', 'average', 'good']]
    system = ctrl.ControlSystem(rules)
    values = np.linspace(0, 10, 15).reshape(3, 5)
    scalar = ctrl.ControlSystemSimulation(system, cache=False)
    expected = np.empty(values.shape)
    for index in np.ndindex(values.shape):
        scalar.input['a'] = values[index]
        scalar.compute()
        expected[index] = scalar.output['out']
    batch = ctrl.ControlSystemSimulation(system, cache=False)
    batch.input['a'] = values
    batch.compute()
    tst.assert_allclose(batch.output['out'], expected, rtol=2e-13, atol=2e-13)
