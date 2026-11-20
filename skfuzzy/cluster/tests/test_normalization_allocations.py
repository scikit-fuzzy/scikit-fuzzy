import numpy as np
import numpy.testing as tst
import pytest
from skfuzzy.cluster.normalize_columns import normalize_power_columns


@pytest.mark.parametrize('exponent', [-20., -2., .5, 2.])
def test_normalization_is_stable_and_does_not_mutate(exponent):
    x = np.array([[1e-200, .2, .7], [1e200, .5, .3]])
    before = x.copy()
    result = normalize_power_columns(x, exponent)
    tst.assert_array_equal(x, before)
    assert not np.shares_memory(x, result)
    assert np.isfinite(result).all()
    tst.assert_allclose(result.sum(axis=0), 1)
