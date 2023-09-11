"""
fuzzy_ops.py : Package of general operations on fuzzy sets, fuzzy membership
               functions, and their associated universe variables.
"""
import numpy as np


def cartadd(x, y):
    """
    Cartesian addition of fuzzy membership vectors using the algebraic method.

    Parameters
    ----------
    x : 1D array or iterable
        First fuzzy membership vector, of length M.
    y : 1D array or iterable
        Second fuzzy membership vector, of length N.

    Returns
    -------
    z : 2D array
        Cartesian addition of ``x`` and ``y``, of shape (M, N).

    """
    # Ensure rank-1 input
    x, y = np.asarray(x).ravel(), np.asarray(y).ravel()
    b, a = np.meshgrid(y, x, sparse=True)
    return a + b


def cartprod(x, y):
    """
    Cartesian product of two fuzzy membership vectors. Uses ``min()``.

    Parameters
    ----------
    x : 1D array or iterable
        First fuzzy membership vector, of length M.
    y : 1D array or iterable
        Second fuzzy membership vector, of length N.

    Returns
    -------
    z : 2D array
        Cartesian product of ``x`` and ``y``, of shape (M, N).

    """
    # Ensure rank-1 input
    x, y = np.asarray(x).ravel(), np.asarray(y).ravel()
    b, a = np.meshgrid(y, x, sparse=True)
    return np.fmin(a, b)


def classic_relation(a, b):
    """
    Determine the classic relation matrix, ``R``, between two fuzzy sets.

    Parameters
    ----------
    a : 1D array or iterable
        First fuzzy membership vector, of length M.
    b : 1D array or iterable
        Second fuzzy membership vector, of length N.

    Returns
    -------
    R : 2D array
        Classic relation matrix between ``a`` and ``b``, shape (M, N)

    Notes
    -----
    The classic relation is defined as::

      r = [a x b] U [(1 - a) x ones(1, N)],

    where ``x`` represents a cartesian product and ``N`` is len(``b``).

    """
    a = np.asarray(a)
    return np.fmax(cartprod(a, b), cartprod(1 - a, np.ones_like(b)))


def contrast(arr, amount=0.2, split=0.5, normalize=True):
    """
    General contrast booster or diffuser of normalized array-like data.

    Parameters
    ----------
    arr : ndarray
        Input array (of floats on range [0, 1] if ``normalize=False``). If
        values exist outside this range, with ``normalize=True`` the image
        will be normalized for calculation.
    amount : float or length-2 iterable of floats
        Controls the exponential contrast mechanism for values above and below
        ``split`` in ``I``. If positive, the curve provides added contrast;
        if negative, the curve provides reduced contrast.

        If provided as a lenth-2 iterable of floats, they control the regions
        (below, above) ``split`` separately.
    split : float
        Positive scalar, on range [0, 1], determining the midpoint of the
        exponential contrast. Default of 0.5 is reasonable for well-exposed
        images.
    normalize : bool, default True
        Controls normalization to the range [0, 1].

    Returns
    -------
    focused : ndarray
        Contrast adjusted, normalized, floating-point image on range [0, 1].

    Notes
    -----
    The result of this algorithm is like applying a Curves adjustment in the
    GIMP or Photoshop.

    Algorithm for curves adjustment at a given pixel, x, is given by::

             | split * (x/split)^below,                        0 <= x <= split
      y(x) = |
             | 1 - (1-split) * ((1-x) / (1-split))^above,   split < x <= 1.0

    See Also
    --------
    skfuzzy.fuzzymath.sigmoid

    """
    split = float(split)
    im = arr.astype(float)
    amount_ = np.asarray(amount, dtype=np.float64).ravel()

    if len(amount_) == 1:
        # One argument -> Equal amount applied on either side of `split`
        above = below = amount_[0]
    else:
        # Two arguments -> Control contrast separately in light/dark regions
        below = amount_[0]
        above = amount_[1]

    # Normalize if required
    if im.max() > 1. and normalize is True:
        ma = float(im.max())
        im /= float(im.max())
    else:
        ma = 1.

    focused = np.zeros_like(im, dtype=np.float64)

    # Simplified array-wise algorithm using fancy indexing rather than looping
    focused[im <= split] = split * (im[im <= split] / split) ** below
    focused[im > split] = (1 - (1. - split) *
                           ((1 - im[im > split]) / (1. - split)) ** above)

    # Reapply multiplicative factor
    return focused * ma


def fuzzy_op(x, a, y, b, op):
    """Operation of two fuzzy sets.

    Operate fuzzy set ``a`` with fuzzy set ``b``,
    using +, * or any other binary operator.

    Parameters
    ----------
    x : 1d array, length N
        Universe variable for fuzzy set ``a``.
    a : 1d array, length N
        Fuzzy set for universe ``x``.
    y : 1d array, length M
        Universe variable for fuzzy set ``b``.
    b : 1d array, length M
        Fuzzy set for universe ``y``.
    op: Function, pointwise binary operator on two matrices
        (pointwise version of) +, -, *, /, min, max etc.

    Returns
    -------
    z : 1d array
        Output variable.
    mfz : 1d array
        Fuzzy membership set for variable ``z``.

    Notes
    -----
    Uses Zadeh's Extension Principle as described in Ross, Fuzzy Logic with
    Engineering Applications (2010), pp. 414, Eq. 12.17.

    If these results are unexpected and your membership functions are convex,
    consider trying the ``skfuzzy.dsw_*`` functions for fuzzy mathematics
    using interval arithmetic via the restricted Dong, Shah, and Wong method.

    """
    # a and x, and b and y, are formed into (MxN) matrices.  The former has
    # identical rows; the latter identical identical columns.

    yy, xx = np.meshgrid(y, x, sparse=True)       # consider broadcasting rules
    bb, aa = np.meshgrid(b, a, sparse=True)

    # Do the operation
    zz = op(xx, yy).ravel()
    zz_index = np.argsort(zz)
    zz = np.sort(zz)

    # Array min() operation
    c = np.fmin(aa, bb).ravel()
    c = c[zz_index]

    # Initialize loop
    z, mfz = np.zeros(0), np.zeros(0)
    idx = 0

    for _ in range(len(c)):
        index = np.nonzero(zz == zz[idx])[0]
        z = np.hstack((z, zz[idx]))
        mfz = np.hstack((mfz, c[index].max()))
        idx = index[-1] + 1
        if idx >= len(zz):
            break

    return z, mfz


def fuzzy_add(x, a, y, b):
    """
    Add fuzzy set ``a`` to fuzzy set ``b``.

    Parameters
    ----------
    x : 1d array, length N
        Universe variable for fuzzy set ``a``.
    a : 1d array, length N
        Fuzzy set for universe ``x``.
    y : 1d array, length M
        Universe variable for fuzzy set ``b``.
    b : 1d array, length M
        Fuzzy set for universe ``y``.

    Returns
    -------
    z : 1d array
        Output variable.
    mfz : 1d array
        Fuzzy membership set for variable ``z``.

    Notes
    -----
    Uses Zadeh's Extension Principle as described in Ross, Fuzzy Logic with
    Engineering Applications (2010), pp. 414, Eq. 12.17.

    If these results are unexpected and your membership functions are convex,
    consider trying the ``skfuzzy.dsw_*`` functions for fuzzy mathematics
    using interval arithmetic via the restricted Dong, Shah, and Wong method.

    """
    return fuzzy_op(x, a, y, b, op=np.add)


def fuzzy_compare(q):
    """
    Determine the comparison matrix, ``c``, based on the fuzzy pairwise
    comparison matrix, ``q``, using Shimura's special relativity formula.

    Parameters
    ----------
    q : 2d array, (N, N)
        Fuzzy pairwise comparison matrix.

    Returns
    -------
    c : 2d array, (N, N)
        Comparison matrix.

    """
    return q.T / np.fmax(q, q.T).astype(float)


def fuzzy_div(x, a, y, b):
    """
    Divide fuzzy set ``b`` into fuzzy set ``a``.

    Parameters
    ----------
    x : 1d array, length N
        Universe variable for fuzzy set ``a``.
    a : 1d array, length N
        Fuzzy set for universe ``x``.
    y : 1d array, length M (excluding zero array)
        Universe variable for fuzzy set ``b``.
    b : 1d array, length M
        Fuzzy set for universe ``y``.

    Returns
    -------
    z : 1d array
        Output variable.
    mfz : 1d array
        Fuzzy membership set for variable z.

    Notes
    -----
    Uses Zadeh's Extension Principle from Ross, Fuzzy Logic w/Engineering
    Applications, (2010), pp.414, Eq. 12.17.

    If these results are unexpected and your membership functions are convex,
    consider trying the ``skfuzzy.dsw_*`` functions for fuzzy mathematics
    using interval arithmetic via the restricted Dong, Shah, and Wong method.

    """
    # a and x, and b and y, are formed into (MxN) matrices.  The former has
    # identical rows; the latter identical identical columns.
    if np.all(np.asarray(y) == 0):
        Warning('The 0 value(s) will never be used in the calculation!')
    index = np.where(y == 0)[0]
    np.delete(y, index)
    np.delete(b, index)
    return fuzzy_op(x, a, y, b, op=np.divide)


def fuzzy_min(x, a, y, b):
    """
    Find minimum between fuzzy set ``a`` fuzzy set ``b``.

    Parameters
    ----------
    x : 1d array, length N
        Universe variable for fuzzy set ``a``.
    a : 1d array, length N
        Fuzzy set for universe ``x``.
    y : 1d array, length M
        Universe variable for fuzzy set ``b``.
    b : 1d array, length M
        Fuzzy set for universe ``y``.

    Returns
    -------
    z : 1d array
        Output variable.
    mfz : 1d array
        Fuzzy membership set for variable z.

    Notes
    -----
    Uses Zadeh's Extension Principle from Ross, Fuzzy Logic w/Engineering
    Applications, (2010), pp.414, Eq. 12.17.

    If these results are unexpected and your membership functions are convex,
    consider trying the ``skfuzzy.dsw_*`` functions for fuzzy mathematics
    using interval arithmetic via the restricted Dong, Shah, and Wong method.

    """
    return fuzzy_op(x, a, y, b, op=np.fmin)


def fuzzy_mult(x, a, y, b):
    """
    Multiplies fuzzy set ``a`` and fuzzy set ``b``.

    Parameters
    ----------
    x : 1d array, length N
        Universe variable for fuzzy set ``a``.
    A : 1d array, length N
        Fuzzy set for universe ``x``.
    y : 1d array, length M
        Universe variable for fuzzy set ``b``.
    b : 1d array, length M
        Fuzzy set for universe ``y``.

    Returns
    -------
    z : 1d array
        Output variable.
    mfz : 1d array
        Fuzzy membership set for variable z.

    Notes
    -----
    Uses Zadeh's Extension Principle from Ross, Fuzzy Logic w/Engineering
    Applications, (2010), pp.414, Eq. 12.17.

    If these results are unexpected and your membership functions are convex,
    consider trying the ``skfuzzy.dsw_*`` functions for fuzzy mathematics
    using interval arithmetic via the restricted Dong, Shah, and Wong method.

    """
    return fuzzy_op(x, a, y, b, op=np.multiply)


def fuzzy_sub(x, a, y, b):
    """
    Subtract fuzzy set ``b`` from fuzzy set ``a``.

    Parameters
    ----------
    x : 1d array, length N
        Universe variable for fuzzy set ``a``.
    A : 1d array, length N
        Fuzzy set for universe ``x``.
    y : 1d array, length M
        Universe variable for fuzzy set ``b``.
    b : 1d array, length M
        Fuzzy set for universe ``y``.

    Returns
    -------
    z : 1d array
        Output variable.
    mfz : 1d array
        Fuzzy membership set for variable z.

    Notes
    -----
    Uses Zadeh's Extension Principle from Ross, Fuzzy Logic w/Engineering
    Applications, (2010), pp.414, Eq. 12.17.

    If these results are unexpected and your membership functions are convex,
    consider trying the ``skfuzzy.dsw_*`` functions for fuzzy mathematics
    using interval arithmetic via the restricted Dong, Shah, and Wong method.

    """
    return fuzzy_op(x, a, y, b, op=np.subtract)


def inner_product(a, b):
    """
    Inner product (dot product) of two fuzzy sets.

    Parameters
    ----------
    a : 1d array or iterable
        Fuzzy membership function.
    b : 1d array or iterable
        Fuzzy membership function.

    Returns
    -------
    y : float
        Fuzzy inner product value, on range [0, 1]

    """
    return np.max(np.fmin(np.r_[a], np.r_[b]))


def interp10(x):
    """
    Utility function which conducts linear interpolation of any rank-1 array.
    Result will have 10x resolution.

    Parameters
    ----------
    x : 1d array, length N
        Input array to be interpolated.

    Returns
    -------
    y : 1d array, length 10 * N + 1
        Linearly interpolated output.

    """
    L = len(x)
    return np.interp(np.r_[0:L - 0.9:0.1], range(L), x)


def maxmin_composition(s, r):
    """
    The max-min composition ``t`` of two fuzzy relation matrices.

    Parameters
    ----------
    s : 2d array, (M, N)
        Fuzzy relation matrix #1.
    r : 2d array, (N, P)
        Fuzzy relation matrix #2.

    Returns
    -------
    T ; 2d array, (M, P)
        Max-min composition, defined by ``T = s o r``.

    """
    if s.ndim < 2:
        s = np.atleast_2d(s)
    if r.ndim < 2:
        r = np.atleast_2d(r).T
    m = s.shape[0]
    p = r.shape[1]
    t = np.zeros((m, p))

    for pp in range(p):
        for mm in range(m):
            t[mm, pp] = (np.fmin(s[mm, :], r[:, pp].T)).max()

    return t


def maxprod_composition(s, r):
    """
    The max-product composition ``t`` of two fuzzy relation matrices.

    Parameters
    ----------
    s : 2d array, (M, N)
        Fuzzy relation matrix #1.
    r : 2d array, (N, P)
        Fuzzy relation matrix #2.

    Returns
    -------
    t : 2d array, (M, P)
        Max-product composition matrix.

    """
    if s.ndim < 2:
        s = np.atleast_2d(s)
    if r.ndim < 2:
        r = np.atleast_2d(r).T
    m = s.shape[0]
    p = r.shape[1]
    t = np.zeros((m, p))

    for mm in range(m):
        for pp in range(p):
            t[mm, pp] = (s[mm, :] * r[:, pp].T).max()

    return t


def interp_membership(x, xmf, xx, zero_outside_x=True):
    """
    Find the degree of membership ``u(xx)`` for a given value of ``x = xx``.

    Parameters
    ----------
    x : 1d array
        Independent discrete variable vector.
    xmf : 1d array
        Fuzzy membership function for ``x``.  Same length as ``x``.
    xx : float or array of floats
        Value(s) on universe ``x`` where the interpolated membership is
        desired.
    zero_outside_x : bool, optional
        Defines the behavior if ``xx`` contains value(s) which are outside the
        universe range as defined by ``x``.  If `True` (default), all
        extrapolated values will be zero.  If `False`, the first or last value
        in ``x`` will be what is returned to the left or right of the range,
        respectively.

    Returns
    -------
    xxmf : float or array of floats
        Membership function value at ``xx``, ``u(xx)``.  If ``xx`` is a single
        value, this will be a single value; if it is an array or iterable the
        result will be returned as a NumPy array of like shape.

    Notes
    -----
    For use in Fuzzy Logic, where an interpolated discrete membership function
    u(x) for discrete values of x on the universe of ``x`` is given. Then,
    consider a new value x = xx, which does not correspond to any discrete
    values of ``x``. This function computes the membership value ``u(xx)``
    corresponding to the value ``xx`` using linear interpolation.

    """
    # Not much beats NumPy's built-in interpolation
    if not zero_outside_x:
        kwargs = (None, None)
    else:
        kwargs = (0.0, 0.0)
    return np.interp(xx, x, xmf, left=kwargs[0], right=kwargs[1])


def interp_universe(x, xmf, y):
    """
    Find interpolated universe value(s) for a given fuzzy membership value.

    Parameters
    ----------
    x : 1d array
        Independent discrete variable vector.
    xmf : 1d array
        Fuzzy membership function for ``x``.  Same length as ``x``.
    y : float
        Specific fuzzy membership value.

    Returns
    -------
    xx : list
        List of discrete singleton values on universe ``x`` whose
        membership function value is y, ``u(xx[i])==y``.
        If there are not points xx[i] such that ``u(xx[i])==y``
        it returns an empty list.

    Notes
    -----
    For use in Fuzzy Logic, where a membership function level ``y`` is given.
    Consider there is some value (or set of values) ``xx`` for which
    ``u(xx) == y`` is true, though ``xx`` may not correspond to any discrete
    values on ``x``. This function computes the value (or values) of ``xx``
    such that ``u(xx) == y`` using linear interpolation.

    """
    # Special case required or zero-level cut does not work with faster method
    if y == 0.:
        idx = np.where(np.diff(xmf > y))[0]
    else:
        idx = np.where(np.diff(xmf >= y))[0]
    xx = (x[idx]
          + (y - xmf[idx])
          * (x[idx + 1] - x[idx])
          / (xmf[idx + 1] - xmf[idx]))

    # The above method is fast, but duplicates point values where
    # y == peak of a membership function. Ducking briefly into a set
    # eliminates this. Benchmarked multiple ways; this is by far the fastest.
    # Speed penalty approximately 10%, worth it.
    return list(set(xx.tolist()))


def _interp_universe_fast(x, xmf, y):
    """
    Find interpolated universe value(s) for a given fuzzy membership value.

    Fast version, with possible duplication.

    Parameters
    ----------
    x : 1d array
        Independent discrete variable vector.
    xmf : 1d array
        Fuzzy membership function for ``x``.  Same length as ``x``.
    y : float
        Specific fuzzy membership value.

    Returns
    -------
    xx : list
        List of discrete singleton values on universe ``x`` whose
        membership function value is y, ``u(xx[i])==y``.
        If there are not points xx[i] such that ``u(xx[i])==y``
        it returns an empty list.

    Notes
    -----
    For use in Fuzzy Logic, where a membership function level ``y`` is given.
    Consider there is some value (or set of values) ``xx`` for which
    ``u(xx) == y`` is true, though ``xx`` may not correspond to any discrete
    values on ``x``. This function computes the value (or values) of ``xx``
    such that ``u(xx) == y`` using linear interpolation.
    """
    # Special case required or zero-level cut does not work with faster method
    if y == 0.:
        idx = np.where(np.diff(xmf > y))[0]
    else:
        idx = np.where(np.diff(xmf >= y))[0]

    # This method is fast, but duplicates point values where
    # y == peak of a membership function.
    return (x[idx]
            + (y - xmf[idx])
            * (x[idx+1] - x[idx])
            / (xmf[idx+1] - xmf[idx]))


def modus_ponens(a, b, ap, c=None):
    """
    Generalized *modus ponens* deduction to make approximate reasoning in a
    rules-base system.

    Parameters
    ----------
    a : 1d array
        Fuzzy set ``a`` on universe ``x``
    b : 1d array
        Fuzzy set ``b`` on universe ``y``
    ap : 1d array
        New fuzzy fact a' (a prime, not transpose)
    c : 1d array, OPTIONAL
        Keyword argument representing fuzzy set ``c`` on universe ``y``.
        Default = None, which will use ``np.ones()`` instead.

    Returns
    -------
    R : 2d array
        Full fuzzy relation.
    bp : 1d array
        Fuzzy conclusion b' (b prime)

    """
    if c is None:
        c = np.ones_like(b)
    r = np.fmax(cartprod(a, b), cartprod(1 - a, c))
    bp = maxmin_composition(ap, r)
    return r, bp.squeeze()


def outer_product(a, b):
    """
    Outer product of two fuzzy sets.

    Parameters
    ----------
    a : 1d array or iterable
        Fuzzy membership function.
    b : 1d array or iterable
        Fuzzy membership function.

    Returns
    -------
    y : float
        Fuzzy outer product value, on range [0, 1]

    """
    return np.min(np.fmax(np.r_[a], np.r_[b]))


def relation_min(a, b):
    """
    Determine fuzzy relation matrix ``R`` using Mamdani implication for the
    fuzzy antecedent ``a`` and consequent ``b`` inputs.

    Parameters
    ----------
    a : 1d array
        Fuzzy antecedent variable of length M.
    b : 1d array
        Fuzzy consequent variable of length N.

    Returns
    -------
    R : 2d array
        Fuzzy relation between ``a`` and ``b``, of shape (M, N).

    """
    bb, aa = np.meshgrid(b, a, sparse=True)
    return np.fmin(aa, bb)


def relation_product(a, b):
    """
    Determine the fuzzy relation matrix, ``R``, using product implication for
    the fuzzy antecedent ``a`` and the fuzzy consequent ``b``.

    Parameters
    ----------
    a : 1d array
        Fuzzy antecedent variable of length M.
    b : 1d array
        Fuzzy consequent variable of length N.

    Returns
    -------
    R : 2d array
        Fuzzy relation between ``a`` and ``b``, of shape (M, N).

    """
    bb, aa = np.meshgrid(b, a, sparse=True)
    return aa * bb


def fuzzy_similarity(ai, b, mode='min'):
    """
    The fuzzy similarity between set ``ai`` and observation set ``b``.

    Parameters
    ----------
    ai : 1d array
        Fuzzy membership function of set ``ai``.
    b : 1d array
        Fuzzy membership function of set ``b``.
    mode : string
        Controls the method of similarity calculation.
        * ``'min'`` : Computed by array minimum operation.
        * ``'avg'`` : Computed by taking the array average.

    Returns
    -------
    s : float
        Fuzzy similarity.

    """
    if 'min' in mode.lower():
        return min(inner_product(ai, b), 1 - outer_product(ai, b))
    else:
        return (inner_product(ai, b) + (1 - outer_product(ai, b))) / 2.


def partial_dmf(x, mf_name, mf_parameter_dict, partial_parameter):
    """
    Calculate the *partial derivative* of a specified membership function.

    Parameters
    ----------
    x : float
        input variable.
    mf_name : string
        Membership function name as a string. The following are supported:
        * ``'gaussmf'`` : parameters ``'sigma'`` or ``'mean'``
        * ``'gbellmf'`` : parameters ``'a'``, ``'b'``, or ``'c'``
        * ``'sigmf'`` : parameters ``'b'`` or ``'c'``
    mf_parameter_dict : dict
        A dictionary of ``{param : key-value, ...}`` pairs for a particular
        membership function as defined above.
    partial_parameter : string
        Name of the parameter against which we take the partial derivative.

    Returns
    -------
    d : float
        Partial derivative of the membership function with respect to the
        chosen parameter, at input point ``x``.

    Notes
    -----
    Partial derivatives of fuzzy membership functions are only meaningful for
    continuous functions. Triangular, trapezoidal designs have no partial
    derivatives to calculate. The following
    """

    if mf_name == 'gaussmf':

        sigma = mf_parameter_dict['sigma']
        mean = mf_parameter_dict['mean']

        if partial_parameter == 'sigma':
            result = ((2. / sigma**3) *
                      np.exp(-(((x - mean)**2) / (sigma)**2)) * (x - mean)**2)
        elif partial_parameter == 'mean':
            result = ((2. / sigma**2) *
                      np.exp(-(((x - mean)**2) / (sigma)**2)) * (x - mean))

    elif mf_name == 'gbellmf':

        a = mf_parameter_dict['a']
        b = mf_parameter_dict['b']
        c = mf_parameter_dict['c']

        # Partial result for speed and conciseness in derived eqs below
        d = np.abs((c - x) / a)

        if partial_parameter == 'a':
            result = ((2. * b * (c - x)**2.) * d**((2 * b) - 2) /
                      (a**3. * (d**(2. * b) + 1)**2.))

        elif partial_parameter == 'b':
            result = (-1 * (2 * d**(2. * b) * np.log(d)) /
                      ((d**(2. * b) + 1)**2.))

        elif partial_parameter == 'c':
            result = ((2. * b * (x - c) * d**((2. * b) - 2)) /
                      (a**2. * (d**(2. * b) + 1)**2.))

    elif mf_name == 'sigmf':

        b = mf_parameter_dict['b']
        c = mf_parameter_dict['c']

        if partial_parameter == 'b':
            # Partial result for speed and conciseness
            d = np.exp(c * (b + x))
            result = -1 * (c * d) / (np.exp(b * c) + np.exp(c * x))**2.

        elif partial_parameter == 'c':
            # Partial result for speed and conciseness
            d = np.exp(c * (x - b))
            result = ((x - b) * d) / (d + 1)**2.

    return result


def sigmoid(x, power, split=0.5):
    """
    Intensify grayscale values in an array using a sigmoid function.

    Parameters
    ----------
    x : ndarray
        Input vector or image array. Should be pre-normalized to range [0, 1]
    p : float
        Power of the intensification (p > 0). Experiment with small, decimal
        values and increase as necessary.
    split : float
        Threshold for intensification. Values above ``split`` will be
        intensified, while values below `split` will be deintensified. Note
        range for ``split`` is (0, 1). Default of 0.5 is reasonable for many
        well-exposed images.

    Returns
    -------
    y : ndarray, same size as x
        Output vector or image with contrast adjusted.

    Notes
    -----
    The sigmoid used herein is defined as::

      y = 1 / (1 + exp(- exp(- power * (x-split))))

    See Also
    --------
    skfuzzy.fuzzymath.contrast
    """

    return 1. / (1. + np.exp(- power * (x - split)))
