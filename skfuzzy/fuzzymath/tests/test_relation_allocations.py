import numpy as np
import numpy.testing as tst
import pytest
from skfuzzy.fuzzymath import fuzzy_ops as ops


@pytest.mark.parametrize('dtype', [np.float32, np.float64, np.int16])
def test_relations_match_cartesian_definitions(dtype):
    a, b = np.array([0, 1, 2], dtype=dtype), np.array([2, 1], dtype=dtype)
    aa, bb = a[:, None], b[None, :]
    tst.assert_array_equal(ops.cartadd(a, b), aa + bb)
    tst.assert_array_equal(ops.cartprod(a, b), np.fmin(aa, bb))
    tst.assert_array_equal(ops.relation_min(a, b), np.fmin(aa, bb))
    tst.assert_array_equal(ops.relation_product(a, b), aa * bb)


def test_products_preserve_list_and_nonfinite_behavior():
    a, b = np.array([.2, np.nan, .7]), np.array([.4, .3, np.nan])
    tst.assert_array_equal(ops.inner_product(a, b), np.fmin(a, b).max())
    tst.assert_array_equal(ops.outer_product(a, b), np.fmax(a, b).min())
    assert ops.inner_product([.2, .7], [.4, .3]) == .3
