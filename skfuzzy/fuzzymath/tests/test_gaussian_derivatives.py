import numpy as np
import pytest
from numpy.testing import assert_allclose

from skfuzzy import gaussmf, partial_dmf


@pytest.mark.parametrize('parameter', ['mean', 'sigma'])
@pytest.mark.parametrize('mean', [-1.5, 0., 2.])
@pytest.mark.parametrize('sigma', [0.5, 1., 2., -1.])
def test_gaussian_partials_match_public_membership_derivative(parameter, mean,
                                                            sigma):
    x = mean + sigma * np.array([-2., -1., -.25, 0., .5, 1.5, 2.])
    original = x.copy()
    params = {'mean': mean, 'sigma': sigma}
    lower, upper = params.copy(), params.copy()
    step = 1e-5 * max(1., abs(params[parameter]))
    lower[parameter] -= step
    upper[parameter] += step
    expected = (gaussmf(x, **upper) - gaussmf(x, **lower)) / (2 * step)

    actual = partial_dmf(x, 'gaussmf', params, parameter)

    assert_allclose(actual, expected, rtol=1e-6, atol=1e-9)
    assert_allclose(x, original)
    assert params == {'mean': mean, 'sigma': sigma}


@pytest.mark.parametrize('parameter', ['mean', 'sigma'])
def test_gaussian_partials_scalar_and_array_agree(parameter):
    params = {'mean': -.5, 'sigma': 1.25}
    x = np.array([-2., -.5, 1.])
    expected = [partial_dmf(value, 'gaussmf', params, parameter) for value in x]
    assert_allclose(partial_dmf(x, 'gaussmf', params, parameter), expected)


@pytest.mark.parametrize('parameter', ['mean', 'sigma'])
def test_gaussian_partials_one_standard_deviation(parameter):
    params = {'mean': 0., 'sigma': 1.}
    assert_allclose(partial_dmf(1., 'gaussmf', params, parameter),
                    np.exp(-0.5))
