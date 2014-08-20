import numpy as np
import skfuzzy as fuzz
from numpy.testing import assert_allclose, assert_raises


def test_centroid():

    def helper_centroid(mean=0, sigma=1):
        x = np.arange(21) - 10
        gmf = fuzz.gaussmf(x, mean, sigma)
        assert_allclose(mean, fuzz.centroid(x, gmf), atol=1e-3)
        return None

    def helper_dcentroid(mean=0, sigma=1, dc=0):
        x = np.arange(21) - 10
        gmf = fuzz.gaussmf(x, mean, sigma)
        assert_allclose(mean, fuzz.dcentroid(x, gmf, dc), atol=1e-3)
        assert_allclose(fuzz.centroid(x, gmf),
                        fuzz.dcentroid(x, gmf, 0))
        return None

    for mean in np.arange(-5, 5, 2):
        for sigma in range(1, 3):
            helper_centroid(mean, sigma)
            for differential_centroid in 42 * (np.arange(11) - 5):
                helper_dcentroid(mean, sigma, differential_centroid)


def test_defuzz():
    x = np.arange(21) - 10
    gmf = fuzz.gaussmf(x, 0, 2)

    assert_allclose(0, fuzz.defuzz(x, gmf, 'centroid'), atol=1e-9)
    assert_allclose(0, fuzz.defuzz(x, gmf, 'bisector'))
    assert_allclose(0, fuzz.defuzz(x, gmf, 'mom'))
    assert_allclose(0, fuzz.defuzz(x, gmf, 'som'))
    assert_allclose(0, fuzz.defuzz(x, gmf, 'lom'))

    # Fuzzy plateau to differentiate mom, som, lom
    trapmf = fuzz.trapmf(x, [-1, 3, 7, 8])

    assert_allclose(3, fuzz.defuzz(x, trapmf, 'som'))
    assert_allclose(5, fuzz.defuzz(x, trapmf, 'mom'))
    assert_allclose(7, fuzz.defuzz(x, trapmf, 'lom'))

    # Bad string argument
    assert_raises(ValueError, fuzz.defuzz, x, trapmf, 'bad string')


def test_lambda_cut():
    x = np.arange(21) - 10
    mfx = fuzz.trimf(x, [-2, 3, 5])

    # fuzz.lambda_cut test
    expected = np.r_[0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                     1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0]
    result = fuzz.lambda_cut(mfx, 0.33)
    assert_allclose(expected, result)

    # fuzz.arglcut test
    expected = np.r_[10, 11, 12, 13, 14]
    result = fuzz.arglcut(mfx, 0.33)

    assert len(result) == 1
    assert_allclose(expected, result[0])


def test_lambda_cut_series():
    x = np.arange(21) - 10
    mfx = fuzz.trimf(x, [-2, 3, 5])

    expected = np.array([[ 0.  , -2.,  5.],
                         [ 0.25,  0.,  4.],
                         [ 0.5 ,  1.,  4.],
                         [ 0.75,  2.,  3.],
                         [ 1.  ,  3.,  3.]])

    assert_allclose(expected, fuzz.lambda_cut_series(x, mfx, 5))


if __name__ == '__main__':
    np.testing.run_module_suite()
