import numpy as np
from numpy.testing import assert_array_equal
from skfuzzy.intervals import addval, divval, multval, scaleval, subval


def test_addval():
    test = addval([2, 3], [3, 4])  # Generalized iterable input
    test2 = addval(np.r_[2, 3], np.r_[3, 4])   # Numpy array input
    test_broadcast = addval(3, np.r_[3, 4])
    test_singleton = addval(3, 4)
    expected = np.r_[5, 7]
    assert_array_equal(test, expected)
    assert_array_equal(test2, expected)
    assert_array_equal(test_broadcast, np.r_[6, 7])
    assert test_singleton == 7


def test_divval():
    test = divval([3, 6], [1, 3])  # Generalized iterable input
    test2 = divval(np.r_[3, 6], np.r_[1, 3])   # Numpy array input
    test_broadcast = divval(6, np.r_[1, 3])
    test_singleton = divval(6, 3)
    expected = np.r_[1, 6]
    assert_array_equal(test, expected)
    assert_array_equal(test2, expected)
    assert_array_equal(test_broadcast, np.r_[6, 2])
    assert test_singleton == 2


def test_multval():
    test = multval([1, 2], [2, 3])  # Generalized iterable input
    test2 = multval(np.r_[1, 2], np.r_[2, 3])   # Numpy array input
    test_broadcast = multval(2, np.r_[2, 3])
    test_singleton = multval(2, 3)
    expected = np.r_[2, 6]
    assert_array_equal(test, expected)
    assert_array_equal(test2, expected)
    assert_array_equal(test_broadcast, np.r_[4, 6])
    assert test_singleton == 6


def test_scaleval():
    test = scaleval(5, [2, 9])  # General iterable
    test2 = scaleval(5, np.r_[2, 9])    # Numpy array
    test_reverse = scaleval(5, [2, -9])    # Fix reverse interval
    test_singleton = scaleval(5, 4)
    expected = np.r_[10, 45]
    assert_array_equal(test, expected)
    assert_array_equal(test2, expected)
    assert_array_equal(test_reverse, np.r_[-45, 10])
    assert test_singleton == 20


def test_subval():
    test = subval([2, 5], [4, 6])  # Generalized iterable input
    test2 = subval(np.r_[2, 5], np.r_[4, 6])   # Numpy array input
    test_broadcast = subval(5, np.r_[4, 6])
    test_singleton = subval(5, 4)
    expected = np.r_[-4, 1]
    assert_array_equal(test, expected)
    assert_array_equal(test2, expected)
    assert_array_equal(test_broadcast, np.r_[1, -1])
    assert test_singleton == 1


# todo: DSW method tests (check lit / probs)


if __name__ == "__main__":
    np.testing.run_module_suite()
