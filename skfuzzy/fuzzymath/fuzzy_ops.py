"""
fuzzy_ops.py : Package of general operations on fuzzy sets, fuzzy membership
               functions, and their associated universe variables.
"""
import warnings

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


def fuzzy_op(x, a, y, b, op, method='discrete', n_levels=None):
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
    method : {'discrete', 'alpha'}, optional
        How the Extension Principle is evaluated; see Notes.
        Default is ``'discrete'``.
    n_levels : int, optional
        Used only with ``method='alpha'``: number of equally spaced alpha
        levels in (0, 1] evaluated in addition to every membership value
        present in ``a`` and ``b``. Default is 100.

    Returns
    -------
    z : 1d array
        Output variable.
    mfz : 1d array
        Fuzzy membership set for variable ``z``.

    Notes
    -----
    Both methods implement Zadeh's Extension Principle,
    ``mfz(z) = sup {min(a(x), b(y)) : op(x, y) = z}``, as described in Ross,
    Fuzzy Logic with Engineering Applications (2010), pp. 414, Eq. 12.17.

    ``method='discrete'`` takes the supremum over the sample pairs only. It
    is exact for genuinely discrete fuzzy sets. When ``x`` and ``y`` sample
    continuous membership functions, a nonlinear ``op`` (``*``, ``/``) maps
    the grid onto an irregular set of outputs, most of which are reached by
    very few pairs. The supremum is then taken over too few pairs and the
    result shows spurious low degrees inside its support: it is saw-toothed
    and non-convex even when ``a`` and ``b`` are convex.

    ``method='alpha'`` uses the level-set form of the Extension Principle
    (Nguyen, 1978): for a continuous ``op`` and membership functions with
    compact alpha-cuts, ``C_alpha = op(A_alpha, B_alpha)``. The operands are
    interpolated linearly between samples, their alpha-cuts are computed
    exactly as unions of closed intervals (convexity is not required), and
    each pair of intervals is mapped through ``op`` by evaluating its four
    corners. This is exact for operators that are monotonic in each argument
    on each interval: ``np.add``, ``np.subtract``, ``np.multiply``,
    ``np.divide`` (divisor away from zero), ``np.fmin`` and ``np.fmax``.
    The returned universe holds the endpoints of every computed alpha-cut,
    where ``mfz`` is exact for the levels evaluated. Use this method when the
    universes are samplings of a continuum. For convex operands it agrees
    with the ``skfuzzy.dsw_*`` functions (Dong, Shah and Wong method).

    References
    ----------
    .. [1] H. T. Nguyen, A note on the extension principle for fuzzy sets,
           J. Math. Anal. Appl., 64(2), 1978, pp. 369-380.

    """
    if method == 'discrete':
        return _fuzzy_op_discrete(x, a, y, b, op)
    if method == 'alpha':
        return _fuzzy_op_alpha(x, a, y, b, op, n_levels)
    raise ValueError("method must be 'discrete' or 'alpha', got {!r}".format(method))


def _fuzzy_op_discrete(x, a, y, b, op):
    """Extension Principle over the sample pairs (discrete fuzzy sets)."""
    x, y = np.asarray(x).ravel(), np.asarray(y).ravel()
    a = np.asarray(a, dtype=np.float64).ravel()
    b = np.asarray(b, dtype=np.float64).ravel()

    # Every pair (x_i, y_j) produces op(x_i, y_j) with degree min(a_i, b_j)
    zz = op(x[:, np.newaxis], y[np.newaxis, :]).ravel()
    c = np.fmin(a[:, np.newaxis], b[np.newaxis, :]).ravel()

    # Supremum over the pairs that produce the same output value
    z, inverse = np.unique(zz, return_inverse=True)
    mfz = np.zeros(z.shape, dtype=np.float64)
    np.maximum.at(mfz, inverse.ravel(), c)
    return z, mfz


def _sorted_universe(x, mfx):
    """Return ``x`` and ``mfx`` as float arrays sorted by ``x``."""
    x = np.asarray(x, dtype=np.float64).ravel()
    mfx = np.asarray(mfx, dtype=np.float64).ravel()
    if x.shape != mfx.shape:
        raise ValueError('Universe and membership arrays must have the same length.')
    order = np.argsort(x, kind='stable')
    return x[order], mfx[order]


def _alpha_cut_intervals(x, mfx, alpha):
    """Alpha-cut of a piecewise-linear membership function.

    Returns an array of shape (K, 2) holding the closed intervals whose union
    is ``{u : mfx(u) >= alpha}``, with ``mfx`` linearly interpolated between
    the sorted samples ``x``. For ``alpha == 0`` the closure of the support
    is returned instead of the whole universe.
    """
    if alpha > 0:
        inside = mfx >= alpha
    else:
        positive = mfx > 0
        inside = positive.copy()
        inside[1:] |= positive[:-1]
        inside[:-1] |= positive[1:]
    if not inside.any():
        return np.empty((0, 2))

    edges = np.diff(inside.astype(np.int8))
    starts = np.flatnonzero(edges == 1) + 1
    ends = np.flatnonzero(edges == -1)
    if inside[0]:
        starts = np.r_[0, starts]
    if inside[-1]:
        ends = np.r_[ends, len(x) - 1]
    lo, hi = x[starts], x[ends]

    if alpha > 0:
        # Move interior endpoints to where the interpolant crosses alpha
        inner = starts > 0
        i = starts[inner]
        lo[inner] = x[i - 1] + (alpha - mfx[i - 1]) * (x[i] - x[i - 1]) / (mfx[i] - mfx[i - 1])
        inner = ends < len(x) - 1
        j = ends[inner]
        hi[inner] = x[j] + (alpha - mfx[j]) * (x[j + 1] - x[j]) / (mfx[j + 1] - mfx[j])
    return np.column_stack((lo, hi))


def _fuzzy_op_alpha(x, a, y, b, op, n_levels=None, include_support=True):
    """Level-set (alpha-cut) form of the Extension Principle."""
    x, a = _sorted_universe(x, a)
    y, b = _sorted_universe(y, b)
    n_levels = 100 if n_levels is None else int(n_levels)
    if n_levels < 1:
        raise ValueError('n_levels must be a positive integer.')

    height = min(a.max(initial=0.), b.max(initial=0.))
    if height <= 0:
        raise ValueError('Both fuzzy sets need at least one positive membership value.')
    levels = np.union1d(np.union1d(a[a > 0], b[b > 0]),
                        np.linspace(0., 1., n_levels + 1)[1:])
    levels = levels[levels <= height]
    if include_support:
        levels = np.r_[0., levels]

    alphas, lows, highs = [], [], []
    for alpha in levels:
        cut_a = _alpha_cut_intervals(x, a, alpha)
        cut_b = _alpha_cut_intervals(y, b, alpha)
        # Image of every pair of intervals: op evaluated at the four corners
        corners = np.stack([op(cut_a[:, i, np.newaxis], cut_b[np.newaxis, :, j])
                            for i in (0, 1) for j in (0, 1)])
        lows.append(corners.min(axis=0).ravel())
        highs.append(corners.max(axis=0).ravel())
        alphas.append(np.full(lows[-1].shape, alpha))
    alphas = np.concatenate(alphas)
    lows, highs = np.concatenate(lows), np.concatenate(highs)

    # mfz(z) is the largest alpha whose cut contains z
    z = np.unique(np.r_[lows, highs])
    tol = 1e-12 * max(1., float(np.abs(z).max()))
    contains = (z[:, np.newaxis] >= lows - tol) & (z[:, np.newaxis] <= highs + tol)
    mfz = np.where(contains, alphas, 0.).max(axis=1)
    return z, mfz


def fuzzy_add(x, a, y, b, method='discrete', n_levels=None):
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

    method : {'discrete', 'alpha'}, optional
        ``'discrete'`` (default) applies the Extension Principle to the
        sample pairs only, which is exact for discrete fuzzy sets.
        ``'alpha'`` treats ``a`` and ``b`` as piecewise-linear membership
        functions and works level by level on their alpha-cuts; use it when
        the universes sample a continuum. See ``fuzzy_op`` for details.
    n_levels : int, optional
        Number of equally spaced alpha levels used by ``method='alpha'``
        in addition to the membership values of ``a`` and ``b``.
        Default is 100.

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

    If ``x`` and ``y`` sample continuous membership functions, use
    ``method='alpha'``; the default discrete evaluation can produce a
    saw-toothed, non-convex result for nonlinear operations.

    """
    return fuzzy_op(x, a, y, b, op=np.add, method=method, n_levels=n_levels)


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


def fuzzy_div(x, a, y, b, method='discrete', n_levels=None):
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

    method : {'discrete', 'alpha'}, optional
        ``'discrete'`` (default) applies the Extension Principle to the
        sample pairs only, which is exact for discrete fuzzy sets.
        ``'alpha'`` treats ``a`` and ``b`` as piecewise-linear membership
        functions and works level by level on their alpha-cuts; use it when
        the universes sample a continuum. See ``fuzzy_op`` for details.
    n_levels : int, optional
        Number of equally spaced alpha levels used by ``method='alpha'``
        in addition to the membership values of ``a`` and ``b``.
        Default is 100.

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

    If ``x`` and ``y`` sample continuous membership functions, use
    ``method='alpha'``; the default discrete evaluation can produce a
    saw-toothed, non-convex result for nonlinear operations.

    """
    y = np.asarray(y).ravel()
    b = np.asarray(b, dtype=np.float64).ravel()
    if method == 'alpha':
        y_sorted, b_sorted = _sorted_universe(y, b)
        support = _alpha_cut_intervals(y_sorted, b_sorted, 0.)
        touches_zero = np.any((support[:, 0] <= 0) & (support[:, 1] >= 0))
        if touches_zero and np.interp(0., y_sorted, b_sorted) > 0:
            raise ValueError('Division by a fuzzy set whose support contains '
                             'zero is undefined.')
        # If zero is only a boundary point of the support, the alpha = 0 cut
        # of the quotient is unbounded; positive levels are still finite.
        return _fuzzy_op_alpha(x, a, y, b, np.divide, n_levels,
                               include_support=not touches_zero)

    zero = y == 0
    if zero.all():
        raise ValueError('The divisor universe ``y`` contains only zeros.')
    if zero.any():
        warnings.warn('Zero values in ``y`` are excluded from the division.',
                      RuntimeWarning, stacklevel=2)
        y, b = y[~zero], b[~zero]
    return fuzzy_op(x, a, y, b, op=np.divide, method=method)


def fuzzy_min(x, a, y, b, method='discrete', n_levels=None):
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

    method : {'discrete', 'alpha'}, optional
        ``'discrete'`` (default) applies the Extension Principle to the
        sample pairs only, which is exact for discrete fuzzy sets.
        ``'alpha'`` treats ``a`` and ``b`` as piecewise-linear membership
        functions and works level by level on their alpha-cuts; use it when
        the universes sample a continuum. See ``fuzzy_op`` for details.
    n_levels : int, optional
        Number of equally spaced alpha levels used by ``method='alpha'``
        in addition to the membership values of ``a`` and ``b``.
        Default is 100.

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

    If ``x`` and ``y`` sample continuous membership functions, use
    ``method='alpha'``; the default discrete evaluation can produce a
    saw-toothed, non-convex result for nonlinear operations.

    """
    return fuzzy_op(x, a, y, b, op=np.fmin, method=method, n_levels=n_levels)


def fuzzy_mult(x, a, y, b, method='discrete', n_levels=None):
    """
    Multiplies fuzzy set ``a`` and fuzzy set ``b``.

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

    method : {'discrete', 'alpha'}, optional
        ``'discrete'`` (default) applies the Extension Principle to the
        sample pairs only, which is exact for discrete fuzzy sets.
        ``'alpha'`` treats ``a`` and ``b`` as piecewise-linear membership
        functions and works level by level on their alpha-cuts; use it when
        the universes sample a continuum. See ``fuzzy_op`` for details.
    n_levels : int, optional
        Number of equally spaced alpha levels used by ``method='alpha'``
        in addition to the membership values of ``a`` and ``b``.
        Default is 100.

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

    If ``x`` and ``y`` sample continuous membership functions, use
    ``method='alpha'``; the default discrete evaluation can produce a
    saw-toothed, non-convex result for nonlinear operations.

    """
    return fuzzy_op(x, a, y, b, op=np.multiply, method=method, n_levels=n_levels)


def fuzzy_sub(x, a, y, b, method='discrete', n_levels=None):
    """
    Subtract fuzzy set ``b`` from fuzzy set ``a``.

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

    method : {'discrete', 'alpha'}, optional
        ``'discrete'`` (default) applies the Extension Principle to the
        sample pairs only, which is exact for discrete fuzzy sets.
        ``'alpha'`` treats ``a`` and ``b`` as piecewise-linear membership
        functions and works level by level on their alpha-cuts; use it when
        the universes sample a continuum. See ``fuzzy_op`` for details.
    n_levels : int, optional
        Number of equally spaced alpha levels used by ``method='alpha'``
        in addition to the membership values of ``a`` and ``b``.
        Default is 100.

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

    If ``x`` and ``y`` sample continuous membership functions, use
    ``method='alpha'``; the default discrete evaluation can produce a
    saw-toothed, non-convex result for nonlinear operations.

    """
    return fuzzy_op(x, a, y, b, op=np.subtract, method=method, n_levels=n_levels)


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
