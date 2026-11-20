import numpy as np
import numpy.testing as tst
import pytest
from skfuzzy.defuzzify import lambda_cut_series
from skfuzzy.intervals import intervalops as ops
from skfuzzy.membership import trimf


@pytest.mark.parametrize('operation,scalar', [('dsw_add', 'addval'), ('dsw_sub', 'subval'),
                                            ('dsw_mult', 'multval'), ('dsw_div', 'divval')])
@pytest.mark.parametrize('offset', [-5., 2.])
def test_dsw_matches_interval_definition(operation, scalar, offset):
    x, y = np.linspace(offset, offset + 4, 101), np.linspace(2, 6, 101)
    a, b = trimf(x, [offset, offset + 2, offset + 4]), trimf(y, [2, 4, 6])
    ca, cb = lambda_cut_series(x, a, 21), lambda_cut_series(y, b, 21)
    expected = np.array([getattr(ops, scalar)(u[1:], v[1:]) for u, v in zip(ca, cb)])
    z, mf = getattr(ops, operation)(x, a, y, b, 21)
    tst.assert_array_equal(z, np.r_[expected[:, 0], expected[::-1, 1]])
    tst.assert_array_equal(mf, np.r_[ca[:, 0], ca[::-1, 0]])
