"""State ownership and cache lifetime regressions."""
import copy
import gc
import pickle
import weakref

import numpy as np
import pytest

from skfuzzy import control as ctrl


def make_simulation(**kwargs):
    antecedent = ctrl.Antecedent(np.linspace(0, 10, 11), 'input')
    consequent = ctrl.Consequent(np.linspace(0, 10, 11), 'output')
    antecedent.automf(3)
    consequent.automf(3)
    rules = [ctrl.Rule(antecedent[name], consequent[name])
             for name in ('poor', 'average', 'good')]
    return ctrl.ControlSystemSimulation(ctrl.ControlSystem(rules), **kwargs)


def discard_simulation(mode):
    kwargs = {'cache': False} if mode == 'uncached' else {}
    if mode == 'flush':
        kwargs['flush_after_run'] = 1
    sim = make_simulation(**kwargs)
    owners = list(sim.ctrl.antecedents) + list(sim.ctrl.consequents)
    terms = [term for owner in owners for term in owner.terms.values()]
    rules = list(sim.ctrl.rules)
    weighted_terms = [term for rule in rules for term in rule.consequent]
    refs = [weakref.ref(owner) for owner in
            owners + terms + rules + weighted_terms + [sim.ctrl, sim]]
    if mode != 'construct':
        sim.input['input'] = 4.5
        sim.compute()
        assert np.isfinite(sim.output['output'])
    if mode == 'reset':
        sim.reset()
    return refs


@pytest.mark.parametrize('mode', ['construct', 'cached', 'uncached', 'reset', 'flush'])
def test_discarded_control_objects_are_collected(mode):
    refs = []
    for _ in range(3):
        refs.extend(discard_simulation(mode))
    gc.collect()
    assert all(ref() is None for ref in refs)


def test_live_control_state_survives_other_controllers():
    sim = make_simulation()
    shared = ctrl.ControlSystemSimulation(sim.ctrl)
    sim.input['input'] = 2
    sim.compute()
    low = sim.output['output']
    shared.input['input'] = 8
    shared.compute()
    high = shared.output['output']
    assert high > low

    for mode in ('cached', 'uncached', 'reset', 'flush'):
        discard_simulation(mode)
    gc.collect()

    for current, value, expected in ((sim, 2, low), (shared, 8, high)):
        current.input['input'] = value
        # The original input is still cached, not merely recomputed.
        assert current.unique_id in current._calculated
        current.compute()
        assert current.output['output'] == expected


@pytest.mark.parametrize('transform', [copy.deepcopy,
                                      lambda obj: pickle.loads(pickle.dumps(obj))])
@pytest.mark.parametrize('computed', [False, True])
@pytest.mark.parametrize('copy_simulation', [False, True])
def test_copied_control_system_computes_independently(transform, computed, copy_simulation):
    sim = make_simulation()
    sim.input['input'] = 2
    sim.compute()
    expected = sim.output['output']
    source = sim if computed else make_simulation()
    other = (transform(source) if copy_simulation else
             ctrl.ControlSystemSimulation(transform(source.ctrl)))
    other.input['input'] = 2
    other.compute()
    assert other.output['output'] == expected
    other.input['input'] = 8
    other.compute()
    assert other.output['output'] > expected
    sim.input['input'] = 2
    sim.compute()
    assert sim.output['output'] == expected


def test_default_flush_and_reset_preserve_owner_state():
    sim = make_simulation()
    antecedent = next(sim.ctrl.antecedents)
    term = antecedent['average']
    assert antecedent.input[sim] is None
    assert antecedent.input['current'] is None
    assert term.cuts[sim] == {}
    for i in range(1000):
        sim.input['input'] = i / 100
        sim.compute()
        if i == 998:
            assert len(sim._calculated) == 999
    assert sim._calculated == []
    assert antecedent.input[sim] is None
    assert antecedent.input['current'] is None
    assert term.cuts[sim] == {}
    sim.input['input'] = 4.5
    sim.compute()
    expected = sim.output['output']
    sim.reset()
    assert antecedent.input['current'] is None
    assert antecedent.input[sim] is None
    assert term.cuts[sim] == {}
    sim.input['input'] = 4.5
    sim.compute()
    assert sim.output['output'] == expected


def test_descriptor_current_defaults_and_clear():
    from skfuzzy.control.state import StatefulProperty

    class Owner:
        value = StatefulProperty({})

    first, second = Owner(), Owner()
    sim = make_simulation()
    first.value[sim]['first'] = 1
    assert second.value[sim] == {}
    first.value['current'] = {'pending': 2}
    assert first.value['current'] == {'pending': 2}
    assert first.value[sim] == {'first': 1}
    descriptor = Owner.value
    descriptor.clear()
    assert Owner.value is descriptor
    assert first.value[sim] == {}
    assert first.value['current'] == {}
    assert second.value[sim] == {}
