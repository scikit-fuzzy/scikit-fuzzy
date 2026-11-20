import numpy as np
import numpy.testing as tst
from skfuzzy.fuzzymath.fuzzy_ops import fuzzy_op


def test_alpha_callback_keeps_operand_rank_and_call_count():
    calls = []

    def add(a, b):
        calls.append((a.shape, b.shape))
        assert a.ndim == b.ndim == 2
        return a + b

    x = np.array([1., 2., 3.])
    y = np.array([2., 3., 4.])
    mf = np.array([0., 1., 0.])
    z, result = fuzzy_op(x, mf, y, mf, add, method='alpha', n_levels=5)
    assert len(calls) == 4 * 6
    assert all(a == (1, 1) and b == (1, 1) for a, b in calls)
    tst.assert_allclose(z[[0, -1]], [3., 7.])
    assert result.max() == 1
