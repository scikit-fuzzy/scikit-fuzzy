"""
intervalops.py : Functions for proper mathematical treatment of intervals.

"""
from __future__ import division, print_function
import numpy as np
from ..defuzzify import lambda_cut_series


def addval(interval1, interval2):
    """
    Adds intervals interval1 and interval2.

    Parameters
    ----------
    interval1 : 2-element iterable
        First interval set.
    interval2 : 2-element iterable
        Second interval set.

    Returns
    -------
    Z : 2-element array
        Sum of interval1 and interval2, defined as::

          Z = interval1 + interval2 = [a + c, b + d]

    """
    # Handle arrays
    if not isinstance(interval1, np.ndarray):
        interval1 = np.asarray(interval1)
    if not isinstance(interval2, np.ndarray):
        interval2 = np.asarray(interval2)

    try:
        return np.r_[interval1] + np.r_[interval2]
    except:
        return interval1 + interval2


def divval(interval1, interval2):
    """
    Divides interval2 into interval1, by inverting interval2 and multiplying.

    Parameters
    ----------
    interval1 : 2-element iterable
        First interval set.
    interval2 : 2-element iterable
        Second interval set.

    Returns
    -------
    z : 2-element array

    """
    # Handle arrays
    if not isinstance(interval1, np.ndarray):
        interval1 = np.asarray(interval1)
    if not isinstance(interval2, np.ndarray):
        interval2 = np.asarray(interval2)

    # Invert interval2 and multiply
    interval2 = 1. / interval2
    return multval(interval1, interval2)


def dsw_add(x, mfx, y, mfy, n):
    """
    Uses the restricted Dong, Shah, & Wong (DSW) method to arithmetically add
    two fuzzy variables together.

    Parameters
    ----------
    x : 1d array
        Universe for first fuzzy variable
    mfx : 1d array
        Fuzzy membership for universe `x`
    y : 1d array
        Universe for second fuzzy variable
    mfy : 1d array
        Fuzzy membership for universe `y`
    n : int
        Number of lambda-cuts to use.

    Returns
    -------
    z : 1d array
        Output universe variable
    mfz : 1d array
        Output fuzzy membership on universe `z`

    """
    # Restricted DSW w/n lambda cuts
    x = lambda_cut_series(x, mfx, n)
    y = lambda_cut_series(y, mfy, n)
    n1, n2 = x.shape
    ff = np.zeros((n1, n2))
    ff[:, 0] = x[:, 0]

    # Compute F = x + y
    for n in range(n1):
        ff[n, [1, 2]] = addval(x[n, [1, 2]], y[n, [1, 2]])

    # Arrange for output or plotting
    out = np.zeros((2 * n1, 2))
    out[0:n1, 1] = ff[:, 0]
    out[n1:2 * n1, 1] = np.flipud(ff[:, 0])
    out[0:n1, 0] = ff[:, 1]
    out[n1:2 * n1, 0] = np.flipud(ff[:, 2])

    # No need for transposes; rank-1 arrays have no transpose in Python
    return out[:, 0], out[:, 1]


def dsw_div(x, mfx, y, mfy, n):
    """
    Uses the restricted Dong, Shah, & Wong (DSW) method to arithmetically
    divide two fuzzy variables, yielding z = x / y.

    Parameters
    ----------
    x : 1d array
        Universe for first fuzzy variable
    mfx : 1d array
        Fuzzy membership for universe `x`
    y : 1d array
        Universe for second fuzzy variable
    mfy : 1d array
        Fuzzy membership for universe `y`
    n : int
        Number of lambda-cuts to use.

    Returns
    -------
    z : 1d array
        Output universe variable
    mfz : 1d array
        Output fuzzy membership on universe `z`

    """
    # Restricted DSW w/n lambda cuts
    x = lambda_cut_series(x, mfx, n)
    y = lambda_cut_series(y, mfy, n)
    n1, n2 = x.shape
    ff = np.zeros((n1, n2))
    ff[:, 0] = x[:, 0]

    # Compute F = x / y
    for n in range(n1):
        ff[n, [1, 2]] = divval(x[n, [1, 2]], y[n, [1, 2]])

    # Arrange for output or plotting
    out = np.zeros((2 * n1, 2))
    out[0:n1, 1] = ff[:, 0]
    out[n1:2 * n1, 1] = np.flipud(ff[:, 0])
    out[0:n1, 0] = ff[:, 1]
    out[n1:2 * n1, 0] = np.flipud(ff[:, 2])

    # No need for transposes; rank-1 arrays have no transpose in Python
    return out[:, 0], out[:, 1]


def dsw_mult(x, mfx, y, mfy, n):
    """
    Uses the restricted Dong, Shah, & Wong (DSW) method to arithmetically
    multiply two fuzzy variables, i.e. z = x * y.

    Parameters
    ----------
    x : 1d array
        Universe for first fuzzy variable
    mfx : 1d array
        Fuzzy membership for universe `x`
    y : 1d array
        Universe for second fuzzy variable
    mfy : 1d array
        Fuzzy membership for universe `y`
    n : int
        Number of lambda-cuts to use.

    Returns
    -------
    z : 1d array
        Output universe variable
    mfz : 1d array
        Output fuzzy membership on universe `z`

    """
    # Restricted DSW w/n lambda cuts
    x = lambda_cut_series(x, mfx, n)
    y = lambda_cut_series(y, mfy, n)
    n1, n2 = x.shape
    ff = np.zeros((n1, n2))
    ff[:, 0] = x[:, 0]

    # Compute F = x * y
    for n in range(n1):
        ff[n, [1, 2]] = multval(x[n, [1, 2]], y[n, [1, 2]])

    # Arrange for output or plotting
    out = np.zeros((2 * n1, 2))
    out[0:n1, 1] = ff[:, 0]
    out[n1:2 * n1, 1] = np.flipud(ff[:, 0])
    out[0:n1, 0] = ff[:, 1]
    out[n1:2 * n1, 0] = np.flipud(ff[:, 2])

    # No need for transposes; rank-1 arrays have no transpose in Python
    return out[:, 0], out[:, 1]


def dsw_sub(x, mfx, y, mfy, n):
    """
    Uses the restricted Dong, Shah, & Wong (DSW) method to arithmetically
    divide two fuzzy variables, yielding z = x - y.

    Parameters
    ----------
    x : 1d array
        Universe for first fuzzy variable
    mfx : 1d array
        Fuzzy membership for universe `x`
    y : 1d array
        Universe for second fuzzy variable
    mfy : 1d array
        Fuzzy membership for universe `y`
    n : int
        Number of lambda-cuts to use.

    Returns
    -------
    z : 1d array
        Output universe variable
    mfz : 1d array
        Output fuzzy membership on universe `z`

    """
    # Restricted DSW w/n lambda cuts
    x = lambda_cut_series(x, mfx, n)
    y = lambda_cut_series(y, mfy, n)
    n1, n2 = x.shape
    ff = np.zeros((n1, n2))
    ff[:, 0] = x[:, 0]

    # Compute F = x - y
    for n in range(n1):
        ff[n, [1, 2]] = subval(x[n, [1, 2]], y[n, [1, 2]])

    # Arrange for output or plotting
    out = np.zeros((2 * n1, 2))
    out[0:n1, 1] = ff[:, 0]
    out[n1:2 * n1, 1] = np.flipud(ff[:, 0])
    out[0:n1, 0] = ff[:, 1]
    out[n1:2 * n1, 0] = np.flipud(ff[:, 2])

    # No need for transposes; rank-1 arrays have no transpose in Python
    return out[:, 0], out[:, 1]


def multval(interval1, interval2):
    """
    Multiplies intervals interval1 and interval2.

    Parameters
    ----------
    interval1 : 1d array, length 2
        First interval.
    interval2 : 1d array, length 2
        Second interval.

    Returns
    -------
    z : 1d array, length 2
        Interval resulting from multiplication of interval1 and interval2.

    """
    # Handle arrays
    if not isinstance(interval1, np.ndarray):
        interval1 = np.asarray(interval1)
    if not isinstance(interval2, np.ndarray):
        interval2 = np.asarray(interval2)

    try:
        crosses = np.r_[interval1[0] * interval2[0],
                        interval1[0] * interval2[1],
                        interval1[1] * interval2[0],
                        interval1[1] * interval2[1]]
        return np.r_[crosses.min(), crosses.max()]
    except:
        return interval1 * interval2


def scaleval(q, interval):
    """
    Multiplies scalar q with interval interval.

    Parameters
    ----------
    q : float
        Scalar to multiply interval with.
    interval : 1d array, length 2
        Interval.  Must have exactly two elements.

    Returns
    -------
    z : 1d array, length 2
        New interval; z = q x interval.

    """
    # Handle array
    if not isinstance(interval, np.ndarray):
        interval = np.asarray(interval)

    try:
        return np.r_[min(q * interval[0], q * interval[1]),
                     max(q * interval[0], q * interval[1])]
    except:
        return q * interval


def subval(interval1, interval2):
    """
    Subtracts interval interval2 from interval interval1.

    Parameters
    ----------
    interval1 : 1d array, length 2
        First interval.
    interval2 : 1d array, length 2
        Second interval.

    Returns
    -------
    Z : 1d array, length 2
        Resultant subtracted interval.

    """
    # Handle arrays
    if not isinstance(interval1, np.ndarray):
        interval1 = np.asarray(interval1)
    if not isinstance(interval2, np.ndarray):
        interval2 = np.asarray(interval2)

    try:
        return np.r_[interval1[0] - interval2[1], interval1[1] - interval2[0]]
    except:
        return interval1 - interval2
