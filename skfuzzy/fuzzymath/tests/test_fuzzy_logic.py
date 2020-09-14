import numpy as np
from numpy.testing import assert_allclose, assert_array_equal
from skfuzzy.fuzzymath import fuzzy_not, fuzzy_and, fuzzy_or
from skfuzzy.membership import trimf


def test_fuzzy_not():
    x = np.r_[0:10.1:0.1]
    mfx = trimf(x, [0, 5, 10])
    expected = np.fmax(trimf(x, [0, 0, 5]), trimf(x, [5, 10, 10]))

    # Not exactly equal due to expected float error ~1e-16
    assert_allclose(fuzzy_not(mfx), expected)


def test_fuzzy_and():
    x = np.r_[0:10.1:0.1]
    mfx = trimf(x, [0, 5, 10])
    mfy = np.ones_like(mfx) - 0.5
    expected = np.fmin(mfy, mfx)
    z, mfz = fuzzy_and(x, mfx, x, mfy)

    # Not exactly equal due to expected float error ~1e-16
    assert_allclose(mfz, expected)
    assert_array_equal(z, x)


def test_fuzzy_or():
    x = np.r_[0:10.1:0.1]
    mfx = trimf(x, [0, 5, 10])
    mfy = np.ones_like(mfx) - 0.5
    expected = np.fmax(mfy, mfx)
    z, mfz = fuzzy_or(x, mfx, x, mfy)

    # Not exactly equal due to expected float error ~1e-16
    assert_allclose(mfz, expected)
    assert_array_equal(z, x)


def test_universe_resampling():
    x = np.r_[0:10.1:0.1]
    y = np.r_[-2:12.1:0.25]
    mfx = trimf(x, [0, 5, 10])
    mfy = trimf(y, [-2, 2, 12])

    # Tests for `fuzzy_and` resampling
    z, mfz = fuzzy_and(x, mfx, y, mfy)
    z_expected = np.r_[-2:12.1:0.1]
    assert_allclose(z, z_expected, atol=1e-14)
    mfz_expected = np.fmin(trimf(z_expected, [0, 5, 10]),
                           trimf(z_expected, [-2, 2, 12]))
    assert_allclose(mfz, mfz_expected, atol=1e-14)

    # Tests for `fuzzy_or` resampling
    z, mfz = fuzzy_or(x, mfx, y, mfy)
    z_expected = np.r_[-2:12.1:0.1]
    assert_allclose(z, z_expected, atol=1e-14)
    mfz_expected = np.fmax(trimf(z_expected, [0, 5, 10]),
                           trimf(z_expected, [-2, 2, 12]))
    assert_allclose(mfz, mfz_expected, atol=1e-14)


if __name__ == "__main__":
    np.testing.run_module_suite()
