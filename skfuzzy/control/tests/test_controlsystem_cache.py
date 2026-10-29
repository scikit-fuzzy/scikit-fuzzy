import numpy as np
import numpy.testing as tst
import pytest

import skfuzzy as fuzz
import skfuzzy.control as ctrl


def sparse_system(two_outputs):
    universe = np.linspace(0, 10, 11)
    sensor = ctrl.Antecedent(universe, 'sensor')
    sensor['low'] = fuzz.trimf(universe, [0, 0, 10])
    sensor['high'] = fuzz.trimf(universe, [0, 10, 10])
    low = ctrl.Consequent(universe, 'low_output')
    low['active'] = fuzz.trimf(universe, [0, 0, 10])
    rules = [ctrl.Rule(sensor['low'], low['active'])]
    if two_outputs:
        high = ctrl.Consequent(universe, 'high_output')
        high['active'] = fuzz.trimf(universe, [0, 10, 10])
        rules.append(ctrl.Rule(sensor['high'], high['active']))
    return ctrl.ControlSystem(rules)


@pytest.mark.parametrize('cache', [False, True])
@pytest.mark.parametrize('two_outputs', [False, True])
def test_cached_sparse_outputs_match_current_input(cache, two_outputs):
    sim = ctrl.ControlSystemSimulation(sparse_system(two_outputs), cache=cache)
    # At the endpoints only one rule fires. The expected values are the
    # geometric centroids of right triangles on [0, 10], independent of defuzz.
    high_output = {'high_output': 20 / 3} if two_outputs else {}
    for value, expected in [(10, high_output), (0, {'low_output': 10 / 3}),
                            (10, high_output), (0, {'low_output': 10 / 3})]:
        sim.input['sensor'] = value
        sim.compute()
        assert sim.output.keys() == expected.keys()
        for label, centroid in expected.items():
            tst.assert_allclose(sim.output[label], centroid)


@pytest.mark.parametrize('cache', [False, True])
def test_strict_sparse_outputs_still_raise(cache):
    sim = ctrl.ControlSystemSimulation(sparse_system(False), cache=cache,
                                       lenient=False)
    sim.input['sensor'] = 0
    sim.compute()
    tst.assert_allclose(sim.output['low_output'], 10 / 3)
    for _ in range(2):
        sim.input['sensor'] = 10
        with pytest.raises(ctrl.EmptyMembershipError):
            sim.compute()
