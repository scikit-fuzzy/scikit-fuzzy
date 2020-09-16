import numpy as np
import skfuzzy as fuzz
from numpy.testing import assert_allclose, assert_raises


def test_bisector():
    x = np.arange(6)
    mfx = fuzz.trimf(x, [0, 5, 5])
    expected = 3.53553390593274

    # Test both triangle code paths
    assert_allclose(expected, fuzz.defuzz(x, mfx, 'bisector'))
    assert_allclose(5 - expected, fuzz.defuzz(x, 1 - mfx, 'bisector'))

    # Test singleton input
    y = np.r_[2]
    mfy = np.r_[0.33]
    assert_allclose(y, fuzz.defuzz(y, mfy, 'bisector'))

    # Test rectangle code path
    mfx = fuzz.trapmf(x, [2, 2, 4, 4])
    assert_allclose(3., fuzz.defuzz(x, mfx, 'bisector'))


def test_centroid():

    def helper_centroid(mean=0, sigma=1):
        x = np.arange(21) - 10
        gmf = fuzz.gaussmf(x, mean, sigma)
        assert_allclose(mean, fuzz.centroid(x, gmf), atol=1e-1)
        return None

    def helper_dcentroid(mean=0, sigma=1, dc=0):
        x = np.arange(21) - 10
        gmf = fuzz.gaussmf(x, mean, sigma)
        assert_allclose(mean, fuzz.dcentroid(x, gmf, dc), atol=1e-1)
        assert_allclose(fuzz.centroid(x, gmf),
                        fuzz.dcentroid(x, gmf, 0))
        return None

    for mean in np.arange(-5, 5, 2):
        for sigma in range(1, 3):
            helper_centroid(mean, sigma)
            for differential_centroid in 42 * (np.arange(11) - 5):
                helper_dcentroid(mean, sigma, differential_centroid)

    # Test with ends @ zero, to evaluate special cases in new defuzz method
    x = np.arange(21) - 10
    gmf = fuzz.gaussmf(x, 0, np.pi)
    gmf[0] = 0
    gmf[-1] = 0
    assert_allclose(0, fuzz.centroid(x, gmf), atol=1e-8)


def test_centroid_singleton():
    x = np.r_[0]
    mfx = np.r_[0]
    assert_allclose(np.r_[0], fuzz.centroid(x, mfx))

    x = np.r_[3]
    mfx = np.r_[0.5]
    assert_allclose(x, fuzz.centroid(x, mfx))


def test_defuzz():
    x = np.arange(21) - 10
    gmf = fuzz.gaussmf(x, 0, 2)

    assert_allclose(0, fuzz.defuzz(x, gmf, 'centroid'), atol=1e-9)
    assert_allclose(0, fuzz.defuzz(x, gmf, 'bisector'), atol=1e-9)
    assert_allclose(0, fuzz.defuzz(x, gmf, 'mom'))
    assert_allclose(0, fuzz.defuzz(x, gmf, 'som'))
    assert_allclose(0, fuzz.defuzz(x, gmf, 'lom'))

    # Fuzzy plateau to differentiate mom, som, lom
    trapmf = fuzz.trapmf(x, [-1, 3, 7, 8])

    assert_allclose(3, fuzz.defuzz(x, trapmf, 'som'))
    assert_allclose(5, fuzz.defuzz(x, trapmf, 'mom'))
    assert_allclose(7, fuzz.defuzz(x, trapmf, 'lom'))

    # Make sure som/lom work for all-negative universes:
    x_neg = x-20
    assert_allclose(-17, fuzz.defuzz(x_neg, trapmf, 'som'))
    assert_allclose(-13, fuzz.defuzz(x_neg, trapmf, 'lom'))

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

    expected = np.array([[0., -2., 5.],
                         [0.25, 0., 4.],
                         [0.5, 1., 4.],
                         [0.75, 2., 3.],
                         [1., 3., 3.]])

    assert_allclose(expected, fuzz.lambda_cut_series(x, mfx, 5))


def test_lambda_cut_boundaries():
    x = np.arange(10)
    mfx = fuzz.trapmf(x, [0, 6, 7, 10])

    assert_allclose(fuzz.lambda_cut_boundaries(x, mfx, 0.2), np.r_[1.2])

    x = np.arange(11)
    mfx = fuzz.trapmf(x, [0, 6, 7, 10])
    assert_allclose(fuzz.lambda_cut_boundaries(x, mfx, 0.2), np.r_[1.2, 9.4])


def test_lambda_cut_boundaries_degenerate():
    x = np.arange(11)
    mfx = fuzz.trimf(x, [0, 7, 10])
    assert_allclose(fuzz.lambda_cut_boundaries(x, mfx, 1), np.r_[7])


if __name__ == '__main__':
    np.testing.run_module_suite()
