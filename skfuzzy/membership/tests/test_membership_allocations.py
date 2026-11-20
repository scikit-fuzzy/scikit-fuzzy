import numpy as np
import numpy.testing as tst
import pytest
from skfuzzy.membership.generatemf import trimf, trapmf, sigmoid


@pytest.mark.parametrize('vertices', [[0, 1, 2, 3], [0, 0, 2, 3], [0, 1, 3, 3], [1, 1, 1, 1]])
def test_trapezoid_shoulders_and_singleton(vertices):
    x = np.linspace(-1, 4, 101)
    a, b, c, d = vertices
    expected = np.ones(x.shape)
    left, right = x <= b, x >= c
    expected[left] = trimf(x[left], [a, b, b])
    expected[right] = trimf(x[right], [c, c, d])
    tst.assert_array_equal(trapmf(x, vertices), expected)


def test_sigmoid_bias_preserves_ones_product_promotion():
    wx = np.arange(12, dtype=np.float32).reshape(3, 4) / 10
    b = np.array([-.1, .2, .7], dtype=np.float32)
    expected = 1 / (1 + np.exp(-(wx + np.dot(np.atleast_2d(b).T, np.ones((1, 4))))))
    result = sigmoid(wx, b)
    assert result.dtype == expected.dtype
    tst.assert_array_equal(result, expected)

