"""
generatemf.py: Library of standard fuzzy membership function generators.
"""
import numpy as np


def _nearest(x, y0):
    """
    Finds the index of the sequence elemnt value x0 in `x` that is closest
    to the provided value, `y0`.

    Parameters
    ----------
    x : 1d array
        Input sequence.
    y0 : float
        Desired matching value.

    Returns
    -------
    idx0 : int
        Index of the nearest value `x0` in x; e.g. x[idx0] = x0.
    x0 : float
        Value in `x` which is closest to `y0`.

    Notes
    -----
    This function does support extrapolation, but it is linear.
    Use with care.
    """
    # Distance map
    d = np.abs(x - y0)
    idx0 = np.nonzero(d == d.min())[0][0]
    return idx0, x[idx0]


def dsigmf(x, b1, c1, b2, c2):
    """
    Difference of two fuzzy sigmoid membership functions.

    Parameters
    ----------
    x : 1d array
        Independent variable.
    b1 : float
        Midpoint of first sigmoid; f1(b1) = 0.5
    c1 : float
        Width and sign of first sigmoid.
    b2 : float
        Midpoint of second sigmoid; f2(b2) = 0.5
    c2 : float
        Width and sign of second sigmoid.

    Returns
    -------
    y : 1d array
        Generated sigmoid values, defined as
            y = f1 - f2
            f1(x) = 1 / (1. + exp[- c1 * (x - b1)])
            f2(x) = 1 / (1. + exp[- c2 * (x - b2)])
    """
    return sigmf(x, b1, c=c1) - sigmf(x, b2, c=c2)


def gaussmf(x, mean, sigma):
    """
    Gaussian fuzzy membership function.

    Parameters
    ----------
    x : 1d array or iterable
        Independent variable.
    mean : float
        Gaussian parameter for center (mean) value.
    sigma : float
        Gaussian parameter for standard deviation.

    Returns
    -------
    y : 1d array
        Gaussian membership function for x.
    """
    return np.exp(-((x - mean)**2.) / (2 * sigma**2.))


def gauss2mf(x, mean1, sigma1, mean2, sigma2):
    """
    Gaussian fuzzy membership function of two combined Gaussians.

    Parameters
    ----------
    x : 1d array or iterable
        Independent variable.
    mean1 : float
        Gaussian parameter for center (mean) value of left-side Gaussian.
        Note mean1 <= mean2 reqiured.
    sigma1 : float
        Standard deviation of left Gaussian.
    mean2 : float
        Gaussian parameter for center (mean) value of right-side Gaussian.
        Note mean2 >= mean1 required.
    sigma2 : float
        Standard deviation of right Gaussian.

    Returns
    -------
    y : 1d array
        Membership function with left side up to `mean1` defined by the first
        Gaussian, and the right side above `mean2` defined by the second.
        In the range mean1 <= x <= mean2 the function has value = 1.
    """
    assert mean1 <= mean2, 'mean1 <= mean2 is required.  See docstring.'
    y = np.ones(len(x))
    idx1 = x <= mean1
    idx2 = x > mean2
    y[idx1] = gaussmf(x[idx1], mean1, sigma1)
    y[idx2] = gaussmf(x[idx2], mean2, sigma2)
    return y


def gbellmf(x, a, b, c):
    """
    Generalized Bell function fuzzy membership generator.

    Parameters
    ----------
    x : 1d array
        Independent variable.
    a : float
        Bell function parameter controlling width. See Note for definition.
    b : float
        Bell function parameter controlling slope. See Note for definition.
    c : float
        Bell function parameter defining the center. See Note for definition.

    Returns
    -------
    y : 1d array
        Generalized Bell fuzzy membership function.

    Notes
    -----
    Definition of Generalized Bell function is:

        y(x) = 1 / (1 + abs([x - c] / a) ** [2 * b])
    """
    return 1. / (1. + np.abs((x - c) / a) ** (2 * b))


def piecemf(x, abc):
    """
    Piecewise linear membership function (particularly used in FIRE filters).

    Parameters
    ----------
    x : 1d array
        Independent variable vector.
    abc : 1d array, length 3
        Defines the piecewise function. Important: if abc = [a, b, c] then
        a <= b <= c is REQUIRED!

    Returns
    -------
    y : 1d array
        Piecewise fuzzy membership function for x.

    Notes
    -----
    Piecewise definition:
                y = 0,                    min(x) <= x <= a
                y = b(x - a)/c(b - a),    a <= x <= b
                y = x/c,                  b <= x <= c
    """
    a, b, c = abc
    if c != x.max():
        c = x.max()

    assert a <= b and b <= c, '`abc` requires a <= b <= c.'

    n = len(x)
    y = np.zeros(n)

    idx0 = _nearest(x, 0)[0]
    idxa = _nearest(x, a)[0]
    idxb = _nearest(x, b)[0]

    n = np.r_[0:n - idx0]
    y[idx0 + n] = n / float(c)
    y[idx0:idxa] = 0
    m = np.r_[0:idxb - idxa]
    y[idxa:idxb] = b * m / (float(c) * (b - a))

    return y / y.max()


def pimf(x, a, b, c, d):
    """
    Pi-function fuzzy membership generator.

    Parameters
    ----------
    x : 1d array
        Independent variable.
    a : float
        Left 'foot', where the function begins to climb from zero.
    b : float
        Left 'ceiling', where the function levels off at 1.
    c : float
        Right 'ceiling', where the function begins falling from 1.
    d : float
        Right 'foot', where the function reattains zero.

    Returns
    -------
    y : 1d array
        Pi-function.

    Notes
    -----
    This is equivalently a product of smf and zmf.
    """
    y = np.ones(len(x))
    assert a <= b and b <= c and c <= d, 'a <= b <= c <= d is required.'

    idx = x <= a
    y[idx] = 0

    idx = np.logical_and(a <= x, x <= (a + b) / 2.)
    y[idx] = 2. * ((x[idx] - a) / (b - a)) ** 2.

    idx = np.logical_and((a + b) / 2. < x, x <= b)
    y[idx] = 1 - 2. * ((x[idx] - b) / (b - a)) ** 2.

    idx = np.logical_and(c <= x, x < (c + d) / 2.)
    y[idx] = 1 - 2. * ((x[idx] - c) / (d - c)) ** 2.

    idx = np.logical_and((c + d) / 2. <= x, x <= d)
    y[idx] = 2. * ((x[idx] - d) / (d - c)) ** 2.

    idx = x >= d
    y[idx] = 0

    return y


def psigmf(x, b1, c1, b2, c2):
    """
    Product of two sigmoid membership functions.

    Parameters
    ----------
    x : 1d array
        Data vector for independent variable.
    b1 : float
        Offset or bias for the first sigmoid.  This is the center value of the
        sigmoid, where it equals 1/2.
    c1 : float
        Controls 'width' of the first sigmoidal region about `b1` (magnitude),
        and also which side of the function is open (sign). A positive value of
        `c1` means the left side approaches zero while the right side
        approaches one; a negative value of `c1` means the opposite.
    b2 : float
        Offset or bias for the second sigmoid.  This is the center value of the
        sigmoid, where it equals 1/2.
    c2 : float
        Controls 'width' of the second sigmoidal region about `b2` (magnitude),
        and also which side of the function is open (sign). A positive value of
        `c2` means the left side approaches zero while the right side
        approaches one; a negative value of `c2` means the opposite.

    Returns
    -------
    y : 1d array
        Generated sigmoid values, defined as

        y = f1(x) * f2(x)

            f1(x) = 1 / (1. + exp[- c1 * (x - b1)])
            f2(x) = 1 / (1. + exp[- c2 * (x - b2)])

    Notes
    -----
    For a smoothed rect-like function, c2 < 0 < c1. For its inverse (zero in
    middle, one at edges) c1 < 0 < c2.
    """
    return sigmf(x, b1, c1) * sigmf(x, b2, c2)


def sigmoid(wx, b):
    """
    Generates a sigmoid function.

    Parameters
    ----------
    wx : 2d array, (K, N)
        Sum of the inner product of W and X, where W is a KxM data matrix
        and X is a MxN weight matrix.
    b : 1d array, length K
        Bias or threshold.

    Returns
    -------
    sigmoid : 2d array, (K, N)
        Sigmoid function result.
    """
    return 1. / (1. + np.exp(-(wx + np.dot(np.atleast_2d(b).T,
                                           np.ones((1, wx.shape[1]))))))


def sigmf(x, b, c):
    """
    The basic sigmoid membership function generator.

    Parameters
    ----------
    x : 1d array
        Data vector for independent variable.
    b : float
        Offset or bias.  This is the center value of the sigmoid, where it
        equals 1/2.
    c : float
        Controls 'width' of the sigmoidal region about `b` (magnitude); also
        which side of the function is open (sign). A positive value of `a`
        means the left side approaches 0.0 while the right side approaches 1.;
        a negative value of `c` means the opposite.

    Returns
    -------
    y : 1d array
        Generated sigmoid values, defined as y = 1 / (1. + exp[- c * (x - b)])

    Notes
    -----
    These are the same values, provided separately and in the opposite order
    compared to the publicly available MathWorks' Fuzzy Logic Toolbox
    documentation. Pay close attention to above docstring!
    """
    return 1. / (1. + np.exp(- c * (x - b)))


def smf(x, a, b):
    """
    S-function fuzzy membership generator.

    Parameters
    ----------
    x : 1d array
        Independent variable.
    a : float
        'foot', where the function begins to climb from zero.
    b : float
        'ceiling', where the function levels off at 1.

    Returns
    -------
    y : 1d array
        S-function.

    Notes
    -----
    Named such because of its S-like shape.
    """
    assert a <= b, 'a <= b is required.'
    y = np.ones(len(x))
    idx = x <= a
    y[idx] = 0

    idx = np.logical_and(a <= x, x <= (a + b) / 2.)
    y[idx] = 2. * ((x[idx] - a) / (b - a)) ** 2.

    idx = np.logical_and((a + b) / 2. <= x, x <= b)
    y[idx] = 1 - 2. * ((x[idx] - b) / (b - a)) ** 2.

    return y


def trapmf(x, abcd):
    """
    Trapezoidal membership function generator.

    Parameters
    ----------
    x : 1d array
        Independent variable.
    abcd : 1d array, length 4
        Four-element vector.  Ensure a <= b <= c <= d.

    Returns
    -------
    y : 1d array
        Trapezoidal membership function.
    """
    assert len(abcd) == 4, 'abcd parameter must have exactly four elements.'
    a, b, c, d = np.r_[abcd]
    assert a <= b and b <= c and c <= d, 'abcd requires the four elements \
                                          a <= b <= c <= d.'
    y = np.ones(len(x))

    idx = np.nonzero(x <= b)[0]
    y[idx] = trimf(x[idx], np.r_[a, b, b])

    idx = np.nonzero(x >= c)[0]
    y[idx] = trimf(x[idx], np.r_[c, c, d])

    idx = np.nonzero(x < a)[0]
    y[idx] = np.zeros(len(idx))

    idx = np.nonzero(x > d)[0]
    y[idx] = np.zeros(len(idx))

    return y


def trimf(x, abc):
    """
    Triangular membership function generator.

    Parameters
    ----------
    x : 1d array
        Independent variable.
    abc : 1d array, length 3
        Three-element vector controlling shape of triangular function.
        Requires a <= b <= c.

    Returns
    -------
    y : 1d array
        Triangular membership function.
    """
    assert len(abc) == 3, 'abc parameter must have exactly three elements.'
    a, b, c = np.r_[abc]     # Zero-indexing in Python
    assert a <= b and b <= c, 'abc requires the three elements a <= b <= c.'

    y = np.zeros(len(x))

    # Left side
    if a != b:
        idx = np.nonzero(np.logical_and(a < x, x < b))[0]
        y[idx] = (x[idx] - a) / float(b - a)

    # Right side
    if b != c:
        idx = np.nonzero(np.logical_and(b < x, x < c))[0]
        y[idx] = (c - x[idx]) / float(c - b)

    idx = np.nonzero(x == b)
    y[idx] = 1
    return y


def zmf(x, a, b):
    """
    Z-function fuzzy membership generator.

    Parameters
    ----------
    x : 1d array
        Independent variable.
    a : float
        'ceiling', where the function begins falling from 1.
    b : float
        'foot', where the function reattains zero.

    Returns
    -------
    y : 1d array
        Z-function.

    Notes
    -----
    Named such because of its Z-like shape.
    """
    assert a <= b, 'a <= b is required.'

    y = np.ones(len(x))

    idx = np.logical_and(a <= x, x < (a + b) / 2.)
    y[idx] = 1 - 2. * ((x[idx] - a) / (b - a)) ** 2.

    idx = np.logical_and((a + b) / 2. <= x, x <= b)
    y[idx] = 2. * ((x[idx] - b) / (b - a)) ** 2.

    idx = x >= b
    y[idx] = 0

    return y
