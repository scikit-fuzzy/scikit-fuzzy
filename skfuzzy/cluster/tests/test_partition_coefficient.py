import math
import numpy as np
import numpy.testing as tst
import pytest
from skfuzzy.cluster._cmeans import _fp_coeff


@pytest.mark.parametrize('dtype', [np.float32, np.float64])
def test_partition_coefficient_definition(dtype):
    u = np.random.default_rng(1729).random((13, 97)).astype(dtype)
    u /= u.sum(axis=0)
    expected = math.fsum(float(v) * float(v) for v in u.ravel()) / u.shape[1]
    tst.assert_allclose(_fp_coeff(u), expected, rtol=2e-6 if dtype == np.float32 else 2e-14)
    tst.assert_allclose(_fp_coeff(np.full((4, 10), .25, dtype=dtype)), .25)
    crisp = np.zeros((4, 10), dtype=dtype)
    crisp[0] = 1
    tst.assert_allclose(_fp_coeff(crisp), 1)
