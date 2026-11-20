import numpy as np
import numpy.testing as tst
import pytest
from skfuzzy.defuzzify.defuzz import lambda_cut_boundaries, lambda_cut_series
from skfuzzy.membership import trimf


@pytest.mark.parametrize('dtype', [np.float32, np.float64])
def test_boundaries_and_cut_extrema(dtype):
    x = np.linspace(0, 10, 101, dtype=dtype)
    mf = trimf(x, [0., 5., 10.])
    tst.assert_allclose(lambda_cut_boundaries(x, mf, .5), [2.5, 7.5])
    cuts = lambda_cut_series(x, mf, 11)
    for level, lower, upper in cuts[1:]:
        selected = x[level - 1e-6 <= mf]
        tst.assert_array_equal([lower, upper], [selected.min(), selected.max()])
