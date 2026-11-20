import numpy as np
import numpy.testing as tst
import pytest
from skfuzzy import control as ctrl
from skfuzzy.membership import trimf


@pytest.mark.parametrize('dtype', [np.float32, np.float64])
@pytest.mark.parametrize('number', [3, 5, 7, 9, 15, 101])
def test_custom_terms_keep_shapes_order_and_independent_storage(number, dtype):
    universe = np.linspace(0, 10, 101, dtype=dtype)
    variable = ctrl.Antecedent(universe, 'x')
    names = ['term' + str(i) for i in range(number)]
    variable.automf(names=names)
    lower, upper = universe.min(), universe.max()
    width = (upper - lower) / ((number - 1) / 2.)
    for label, center in zip(names, np.linspace(lower, upper, number)):
        tst.assert_array_equal(variable[label].mf, trimf(universe, [center - width / 2, center, center + width / 2]))
    assert list(variable.terms) == names
    assert not np.shares_memory(variable[names[0]].mf, variable[names[1]].mf)
