import numpy as np
from numpy.testing import assert_allclose
from skfuzzy.membership import (gaussmf, gauss2mf, gbellmf, piecemf, pimf,
                                psigmf, sigmf, smf, trapmf, trimf, zmf)


def test_gaussmf():
    x = np.arange(-4, 5.1, 0.1)
    expected = np.exp(- (x - 1.33)**2 / (2 * 0.45**2))
    test = gaussmf(x, 1.33, 0.45)
    assert_allclose(test, expected)


def test_gauss2mf():
    x = np.arange(-4, 5.1, 0.1)
    expected = np.ones_like(x)
    expected[x < 1.2] = np.exp(- (x[x < 1.2] - 1.2)**2 / (2 * 0.45**2))
    expected[x > 3.1] = np.exp(- (x[x > 3.1] - 3.1)**2 / (2 * 0.9**2))
    test = gauss2mf(x, 1.2, 0.45, 3.1, 0.9)
    assert_allclose(test, expected)


def test_gbellmf():
    x = np.arange(-4, 5.1, 0.1)
    a, b, c = (2.4, 0.9, 1.33)
    expected = 1 / (1 + np.abs(np.r_[x - c] / a) ** [2 * b])
    test = gbellmf(x, a, b, c)
    assert_allclose(test, expected)


def test_piecemf():
    x = np.arange(0, 2.1, 0.1)
    expected = np.r_[0.,    0.,   0.,  0.,   0.,  0.,   0.,  0.,   0.,
                     0.,    0., 0.25, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85,
                     0.9, 0.95,   1.]
    test = piecemf(x, [1, 1.25, 2])
    assert_allclose(test, expected)


def test_pimf_smf_zmf():
    x = np.arange(-4.0, 4.1, 0.1)
    expected = smf(x, -1 / 137., np.pi / 2.) * zmf(x, np.exp(1.), np.pi)
    test = pimf(x, -1 / 137., np.pi / 2., np.exp(1.), np.pi)
    assert_allclose(test, expected)


def test_psigmf():
    x = np.arange(-4, 4.1, 0.1)
    b1, c1, b2, c2 = -1.75, -np.pi / 2., 0.972, 0.43
    expected = ((1 / (1. + np.exp(- c1 * (x - b1)))) *
                (1 / (1. + np.exp(- c2 * (x - b2)))))
    test = psigmf(x, b1, c1, b2, c2)
    assert_allclose(test, expected)


def test_sigmf():
    x = np.arange(-4, 4.1, 0.1)
    b1, c1 = 1.75, -np.pi / 2.
    expected = 1 / (1. + np.exp(- c1 * (x - b1)))
    test = sigmf(x, b1, c1)
    assert_allclose(test, expected)


def test_trapmf():
    x = np.arange(-4, 3.1, 0.1)
    abcd = (-4, -4, 2, np.pi)
    expected = np.ones_like(x)
    idx = np.logical_and(x > 2, x < np.pi)
    expected[idx] = np.interp(x[idx], np.r_[2, np.pi], np.r_[1, 0])
    expected[x > np.pi] = 0
    test = trapmf(x, abcd)
    assert_allclose(test, expected)


def test_trimf():
    x = np.arange(-4, 4.1, 0.1)
    abc = (-np.pi, -np.e / 2., np.pi / 5.)
    expected = np.zeros_like(x)
    idx = np.logical_and(x > abc[0], x < abc[1])
    expected[idx] = np.interp(x[idx], np.r_[abc[0], abc[1]], np.r_[0, 1])
    expected[x == abc[1]] = 1
    idx = np.logical_and(x > abc[1], x < abc[2])
    expected[idx] = np.interp(x[idx], np.r_[abc[1], abc[2]], np.r_[1, 0])
    test = trimf(x, abc)
    assert_allclose(test, expected)


if __name__ == '__main__':
    np.testing.run_module_suite()
