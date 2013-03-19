"""
intervalops.py : Functions for proper mathematical treatment of intervals.

"""

import numpy as np
from ..defuzzify import lambda_cut_series


def addval(I, J):
    """
    Adds intervals I and J.

    Parameters
    ----------
    I : 2-element iterable
        First interval set.
    J : 2-element iterable
        Second interval set.

    Returns
    -------
    Z : 2-element array
        Sum of I and J, defined as Z = I + J = [a + c, b + d]

    """
    # Handle arrays
    if not isinstance(I, np.ndarray):
        I = np.asarray(I)
    if not isinstance(J, np.ndarray):
        J = np.asarray(J)

    try:
        return np.r_[I] + np.r_[J]
    except:
        return I + J


def divval(I, J):
    """
    Divides intervals J into I, by inverting J and multiplying.

    Parameters
    ----------
    I : 2-element iterable
        First interval set.
    J : 2-element iterable
        Second interval set.

    Returns
    -------
    z : 2-element array

    """
    # Handle arrays
    if not isinstance(I, np.ndarray):
        I = np.asarray(I)
    if not isinstance(J, np.ndarray):
        J = np.asarray(J)

    # Invert J and multiply
    J = 1. / J
    return multval(I, J)


def dsw_add(x, mfx, y, mfy, N):
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
    N : int
        Number of lambda-cuts to use.

    Returns
    -------
    z : 1d array
        Output universe variable
    mfz : 1d array
        Output fuzzy membership on universe `z`

    """
    # Restricted DSW w/N lambda cuts
    X = lambda_cut_series(x, mfx, N)
    Y = lambda_cut_series(y, mfy, N)
    N1, N2 = X.shape
    ff = np.zeros((N1, N2))
    ff[:, 0] = X[:, 0]

    # Compute F = X + Y
    for n in range(N1):
        ff[n, [1, 2]] = addval(X[n, [1, 2]], Y[n, [1, 2]])

    # Arrange for output or plotting
    FF = np.zeros((2 * N1, 2))
    FF[0:N1, 1] = ff[:, 0]
    FF[N1:2 * N1, 1] = np.flipud(ff[:, 0])
    FF[0:N1, 0] = ff[:, 1]
    FF[N1:2 * N1, 0] = np.flipud(ff[:, 2])

    # No need for transposes; rank-1 arrays have no transpose in Python
    return FF[:, 0], FF[:, 1]


def dsw_div(x, mfx, y, mfy, N):
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
    N : int
        Number of lambda-cuts to use.

    Returns
    -------
    z : 1d array
        Output universe variable
    mfz : 1d array
        Output fuzzy membership on universe `z`

    """
    # Restricted DSW w/N lambda cuts
    X = lambda_cut_series(x, mfx, N)
    Y = lambda_cut_series(y, mfy, N)
    N1, N2 = X.shape
    ff = np.zeros((N1, N2))
    ff[:, 0] = X[:, 0]

    # Compute F = X / Y
    for n in range(N1):
        ff[n, [1, 2]] = divval(X[n, [1, 2]], Y[n, [1, 2]])

    # Arrange for output or plotting
    FF = np.zeros((2 * N1, 2))
    FF[0:N1, 1] = ff[:, 0]
    FF[N1:2 * N1, 1] = np.flipud(ff[:, 0])
    FF[0:N1, 0] = ff[:, 1]
    FF[N1:2 * N1, 0] = np.flipud(ff[:, 2])

    # No need for transposes; rank-1 arrays have no transpose in Python
    return FF[:, 0], FF[:, 1]


def dsw_mult(x, mfx, y, mfy, N):
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
    N : int
        Number of lambda-cuts to use.

    Returns
    -------
    z : 1d array
        Output universe variable
    mfz : 1d array
        Output fuzzy membership on universe `z`

    """
    # Restricted DSW w/N lambda cuts
    X = lambda_cut_series(x, mfx, N)
    Y = lambda_cut_series(y, mfy, N)
    N1, N2 = X.shape
    ff = np.zeros((N1, N2))
    ff[:, 0] = X[:, 0]

    # Compute F = X * Y
    for n in range(N1):
        ff[n, [1, 2]] = multval(X[n, [1, 2]], Y[n, [1, 2]])

    # Arrange for output or plotting
    FF = np.zeros((2 * N1, 2))
    FF[0:N1, 1] = ff[:, 0]
    FF[N1:2 * N1, 1] = np.flipud(ff[:, 0])
    FF[0:N1, 0] = ff[:, 1]
    FF[N1:2 * N1, 0] = np.flipud(ff[:, 2])

    # No need for transposes; rank-1 arrays have no transpose in Python
    return FF[:, 0], FF[:, 1]


def dsw_sub(x, mfx, y, mfy, N):
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
    N : int
        Number of lambda-cuts to use.

    Returns
    -------
    z : 1d array
        Output universe variable
    mfz : 1d array
        Output fuzzy membership on universe `z`

    """
    # Restricted DSW w/N lambda cuts
    X = lambda_cut_series(x, mfx, N)
    Y = lambda_cut_series(y, mfy, N)
    N1, N2 = X.shape
    ff = np.zeros((N1, N2))
    ff[:, 0] = X[:, 0]

    # Compute F = X - Y
    for n in range(N1):
        ff[n, [1, 2]] = subval(X[n, [1, 2]], Y[n, [1, 2]])

    # Arrange for output or plotting
    FF = np.zeros((2 * N1, 2))
    FF[0:N1, 1] = ff[:, 0]
    FF[N1:2 * N1, 1] = np.flipud(ff[:, 0])
    FF[0:N1, 0] = ff[:, 1]
    FF[N1:2 * N1, 0] = np.flipud(ff[:, 2])

    # No need for transposes; rank-1 arrays have no transpose in Python
    return FF[:, 0], FF[:, 1]


def multval(I, J):
    """
    Multiplies intervals I and J.

    Parameters
    ----------
    I : 1d array, length 2
        First interval.
    J : 1d array, length 2
        Second interval.

    Returns
    -------
    z : 1d array, length 2
        Interval resulting from multiplication of I and J.

    """
    # Handle arrays
    if not isinstance(I, np.ndarray):
        I = np.asarray(I)
    if not isinstance(J, np.ndarray):
        J = np.asarray(J)

    try:
        crosses = np.r_[I[0] * J[0],
                        I[0] * J[1],
                        I[1] * J[0],
                        I[1] * J[1]]
        return np.r_[crosses.min(), crosses.max()]
    except:
        return I * J


def scaleval(q, I):
    """
    Multiplies scalar q with interval I.

    Parameters
    q : float
        Scalar to multiply interval with.
    I : 1d array, length 2
        Interval.  Must have exactly two elements.

    Returns
    -------
    z : 1d array, length 2
        New interval; z = q x I.

    """
    # Handle array
    if not isinstance(I, np.ndarray):
        I = np.asarray(I)

    try:
        return np.r_[min(q * I[0], q * I[1]), max(q * I[0], q * I[1])]
    except:
        return q * I


def subval(I, J):
    """
    Subtracts interval J from interval I.

    Parameters
    ----------
    I : 1d array, length 2
        First interval.
    J : 1d array, length 2
        Second interval.

    Returns
    -------
    Z : 1d array, length 2
        Resultant subtracted interval.

    """
    # Handle arrays
    if not isinstance(I, np.ndarray):
        I = np.asarray(I)
    if not isinstance(J, np.ndarray):
        J = np.asarray(J)

    try:
        return np.r_[I[0] - J[1], I[1] - J[0]]
    except:
        return I - J
