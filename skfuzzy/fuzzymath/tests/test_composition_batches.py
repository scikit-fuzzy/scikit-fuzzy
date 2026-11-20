import numpy as np
import numpy.testing as tst
import pytest
from skfuzzy.fuzzymath.fuzzy_ops import maxmin_composition, maxprod_composition


@pytest.mark.parametrize('operation,pair', [(maxmin_composition, np.fmin),
                                           (maxprod_composition, np.multiply)])
@pytest.mark.parametrize('dtype', [np.float32, np.float64, np.int16])
def test_composition_matches_scalar_definition(operation, pair, dtype):
    rng = np.random.default_rng(1729)
    a = (rng.random((9, 7)) * 5).astype(dtype)
    b = (rng.random((7, 11)) * 5).astype(dtype)
    expected = np.array([[pair(row, b[:, j]).max() for j in range(b.shape[1])] for row in a])
    tst.assert_array_equal(operation(a, b), expected)


@pytest.mark.parametrize('operation', [maxmin_composition, maxprod_composition])
def test_empty_output_and_nan_semantics(operation):
    assert operation(np.empty((2, 0)), np.empty((0, 0))).shape == (2, 0)
    a, b = np.array([[.5, np.nan]]), np.array([[.4], [.8]])
    pair = np.fmin if operation is maxmin_composition else np.multiply
    tst.assert_array_equal(operation(a, b), [[pair(a[0], b[:, 0]).max()]])
