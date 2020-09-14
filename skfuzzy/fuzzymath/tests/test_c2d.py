import numpy as np
from numpy.testing import assert_allclose
from skfuzzy.fuzzymath import continuous_to_discrete


def test_c2d():
    a = np.r_[[[1, 0], [1, -1]]]
    b = np.r_[1, 0.1]
    b2 = np.r_[[[1], [0.1]]]
    ts = [0.1, 0.5, 1.0]

    expected_a0 = np.r_[[[ 1.10517092,  0.        ],
                         [ 0.10016675,  0.90483742]]]
    expected_b0 = np.r_[ 0.10517092,  0.01452043]

    phi, gamma = continuous_to_discrete(a, b, ts[0])
    assert_allclose(phi, expected_a0)
    assert_allclose(gamma, expected_b0, atol=1e-6)
    assert_allclose(continuous_to_discrete(a, b2, ts[0])[1].T,
                    np.atleast_2d(expected_b0), atol=1e-6)

    expected_a1 = np.r_[[[ 1.64872127,  0.        ],
                         [ 0.52109531,  0.60653066]]]
    expected_b1 = np.r_[ 0.64872127,  0.1669729 ]

    phi, gamma = continuous_to_discrete(a, b, ts[1])
    assert_allclose(phi, expected_a1)
    assert_allclose(gamma, expected_b1, atol=1e-6)

    expected_a2 = np.r_[[[ 2.71828183,  0.        ],
                         [ 1.17520119,  0.36787944]]]
    expected_b2 = np.r_[ 1.71828183,  0.60629269]

    phi, gamma = continuous_to_discrete(a, b, ts[2])
    assert_allclose(phi, expected_a2)
    assert_allclose(gamma, expected_b2, atol=1e-6)


if __name__ == "__main__":
    np.testing.run_module_suite()
