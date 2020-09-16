import numpy as np
from numpy.testing import assert_allclose
from skfuzzy.cluster._cmeans import _distance


def test_distance():
    data = np.r_[[[0, 2, 5, -1],
                  [2, 4, 9, 4],
                  [6, 6, 6, 0]]]

    centers = np.r_[[[1, 3, 7.5, 1],
                     [5, 5.5, 6, 0]]]

    test = _distance(data, centers)

    c, p = centers.shape
    n, q = data.shape

    expected = np.zeros((c, n))

    for i in range(c):
        expected[i, :] = (((data - np.ones((n, 1)).dot(
            np.atleast_2d(centers[i, :]))) ** 2).T).sum(axis=0) ** 0.5

    assert_allclose(test, expected)


if __name__ == '__main__':
    np.testing.run_module_suite()
