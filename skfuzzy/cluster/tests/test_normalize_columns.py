import numpy as np
from skfuzzy.cluster.normalize_columns import normalize_power_columns


def test_normalize_power_columns():
    """
    Test normalize_power_columns
    """

    a = np.array([
        [0, 1, 1, 3],
        [0, 0, 1, 3],
        [1, 1, 1, 3],
        [0, 0, 1, 3],
    ])

    a_normalized_expected = np.array([
        [0.0, 0.5, 0.25, 0.25],
        [0.0, 0.0, 0.25, 0.25],
        [1.0, 0.5, 0.25, 0.25],
        [0.0, 0.0, 0.25, 0.25],
    ])

    a_normalized = normalize_power_columns(a, 1)

    np.testing.assert_allclose(a_normalized, a_normalized_expected, atol=1e-10)

    b = np.array([
        [0, 1e-100],
        [1, 1e-100],
        [1, 0.0000],
    ])

    b_normalized_expected = np.array([
        [0.0, 0.5],
        [0.5, 0.5],
        [0.5, 0.0],
    ])

    b_normalized = normalize_power_columns(b, 1)

    np.testing.assert_allclose(b_normalized, b_normalized_expected, atol=1e-10)

    c = np.array([
        [0, 1e-100, 0, 1e100],
        [1, 1e-100, 1, 1],
        [1, 0.0000, 2, 0],
    ])

    c_normalized_expected = np.array([
        [0.0, 0.5, 0.0, 1],
        [0.5, 0.5, 0.0, 0],
        [0.5, 0.0, 1.0, 0],
    ])

    c_normalized = normalize_power_columns(c, 1000)

    np.testing.assert_allclose(c_normalized, c_normalized_expected, atol=1e-10)

    d = np.array([
        [0, 1e-100, 0, 1e100],
        [1, 1e-100, 1, 1],
        [1, 0.0000, 2, 0],
    ])

    d_normalized_expected = np.array([
        [1.0, 0.0, 1.0, 0.0],
        [0.0, 0.0, 0.0, 0.5],
        [0.0, 1.0, 0.0, 0.5],
    ])

    d_normalized = normalize_power_columns(d, -1000)

    np.testing.assert_allclose(d_normalized, d_normalized_expected, atol=1e-10)


if __name__ == '__main__':
    np.testing.run_module_suite()
