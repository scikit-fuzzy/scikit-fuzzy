"""
defuzz.py : Various methods for defuzzification and lambda-cuts, to convert
            'fuzzy' systems back into 'crisp' values for decisions.
"""
import numpy as np

from .exceptions import EmptyMembershipError, InconsistentMFDataError


def arglcut(ms, lambdacut):
    """
    Determines the subset of indices `mi` of the elements in an N-point
    resultant fuzzy membership sequence `ms` that have a grade of membership
    >= lambdacut.

    Parameters
    ----------
    ms : 1d array
        Fuzzy membership sequence.
    lambdacut : float
        Value used for lambda cutting.

    Returns
    -------
    lidx : 1d array
        Indices corresponding to the lambda-cut subset of `ms`.

    Notes
    -----
    This is a convenience function for `np.nonzero(lambdacut <= ms)` and only
    half of the indexing operation that can be more concisely accomplished
    via::

      ms[lambdacut <= ms]
    """
    return np.nonzero(lambdacut <= ms)


def centroid(x, mfx):
    """
    Defuzzification using centroid (`center of gravity`) method.

    Parameters
    ----------
    x : 1d array, length M
        Independent variable
    mfx : 1d array, length M
        Fuzzy membership function

    Returns
    -------
    u : 1d array, length M
        Defuzzified result

    See also
    --------
    skfuzzy.defuzzify.defuzz, skfuzzy.defuzzify.dcentroid
    """

    '''
    As we suppose linearity between each pair of points of x, we can calculate
    the exact area of the figure (a triangle or a rectangle).
    '''

    sum_moment_area = 0.0
    sum_area = 0.0

    # If the membership function is a singleton fuzzy set:
    if len(x) == 1:
        return (x[0] * mfx[0]
                / np.fmax(mfx[0], np.finfo(float).eps).astype(float))

    # else return the sum of moment*area/sum of area
    for i in range(1, len(x)):
        x1 = x[i - 1]
        x2 = x[i]
        y1 = mfx[i - 1]
        y2 = mfx[i]

        # if y1 == y2 == 0.0 or x1==x2: --> rectangle of zero height or width
        if not (y1 == y2 == 0.0 or x1 == x2):
            if y1 == y2:  # rectangle
                moment = 0.5 * (x1 + x2)
                area = (x2 - x1) * y1
            elif y1 == 0.0 and y2 != 0.0:  # triangle, height y2
                moment = 2.0 / 3.0 * (x2 - x1) + x1
                area = 0.5 * (x2 - x1) * y2
            elif y2 == 0.0 and y1 != 0.0:  # triangle, height y1
                moment = 1.0 / 3.0 * (x2 - x1) + x1
                area = 0.5 * (x2 - x1) * y1
            else:
                moment = ((2.0 / 3.0 * (x2 - x1) * (y2 + 0.5 * y1))
                          / (y1 + y2) + x1)
                area = 0.5 * (x2 - x1) * (y1 + y2)

            sum_moment_area += moment * area
            sum_area += area

    return (sum_moment_area
            / np.fmax(sum_area, np.finfo(float).eps).astype(float))


def dcentroid(x, mfx, x0):
    """
    Defuzzification using a differential centroidal method about `x0`.

    Parameters
    ----------
    x : 1d array or iterable
        Independent variable.
    mfx : 1d array or iterable
        Fuzzy membership function.
    x0 : float
        Central value to calculate differential centroid about.

    Returns
    -------
    u : 1d array
        Defuzzified result.

    See also
    --------
    skfuzzy.defuzzify.defuzz, skfuzzy.defuzzify.centroid
    """
    x = x - x0
    return x0 + centroid(x, mfx)


def bisector(x, mfx):
    """
    Defuzzification using bisector, or division of the area in two equal parts.

    Parameters
    ----------
    x : 1d array, length M
        Independent variable
    mfx : 1d array, length M
        Fuzzy membership function

    Returns
    -------
    u : 1d array, length M
        Defuzzified result

    See also
    --------
    skfuzzy.defuzzify.defuzz
    """
    '''
    As we suppose linearity between each pair of points of x, we can calculate
    the exact area of the figure (a triangle or a rectangle).
    '''
    sum_area = 0.0
    accum_area = [0.0] * (len(x) - 1)

    # If the membership function is a singleton fuzzy set:
    if len(x) == 1:
        return x[0]

    # else return the sum of moment*area/sum of area
    for i in range(1, len(x)):
        x1 = x[i - 1]
        x2 = x[i]
        y1 = mfx[i - 1]
        y2 = mfx[i]

        # if y1 == y2 == 0.0 or x1==x2: --> rectangle of zero height or width
        if not (y1 == y2 == 0. or x1 == x2):
            if y1 == y2:  # rectangle
                area = (x2 - x1) * y1
            elif y1 == 0. and y2 != 0.:  # triangle, height y2
                area = 0.5 * (x2 - x1) * y2
            elif y2 == 0. and y1 != 0.:  # triangle, height y1
                area = 0.5 * (x2 - x1) * y1
            else:
                area = 0.5 * (x2 - x1) * (y1 + y2)
            sum_area += area
            accum_area[i - 1] = sum_area

    # index to the figure which contains the x point that divide the area of
    # the whole fuzzy set in two
    index = np.nonzero(np.array(accum_area) >= sum_area / 2.)[0][0]

    # subarea will be the area in the left part of the bisection for this set
    if index == 0:
        subarea = 0
    else:
        subarea = accum_area[index - 1]
    x1 = x[index]
    x2 = x[index + 1]
    y1 = mfx[index]
    y2 = mfx[index + 1]

    # We are interested only in the subarea inside the figure in which the
    # bisection is present.
    subarea = sum_area / 2. - subarea

    x2minusx1 = x2 - x1
    if y1 == y2:  # rectangle
        u = subarea / y1 + x1
    elif y1 == 0.0 and y2 != 0.0:  # triangle, height y2
        root = np.sqrt(2. * subarea * x2minusx1 / y2)
        u = (x1 + root)
    elif y2 == 0.0 and y1 != 0.0:  # triangle, height y1
        root = np.sqrt(x2minusx1 * x2minusx1 - (2. * subarea * x2minusx1 / y1))
        u = (x2 - root)
    else:
        m = (y2 - y1) / x2minusx1
        root = np.sqrt(y1 * y1 + 2.0 * m * subarea)
        u = (x1 - (y1 - root) / m)
    return u


def defuzz(x, mfx, mode):
    """
    Defuzzification of a membership function, returning a defuzzified value
    of the function at x, using various defuzzification methods.

    Parameters
    ----------
    x : 1d array or iterable, length N
        Independent variable.
    mfx : 1d array of iterable, length N
        Fuzzy membership function.
    mode : string
        Controls which defuzzification method will be used.
        * 'centroid': Centroid of area
        * 'bisector': bisector of area
        * 'mom'     : mean of maximum
        * 'som'     : min of maximum
        * 'lom'     : max of maximum

    Returns
    -------
    u : float or int
        Defuzzified result.

    Raises
    ------
    - EmptyMembershipError : When the membership function area is empty.
    - InconsistentMFDataError : When the length of the 'x' and the fuzzy
        membership function arrays are not equal.

    See Also
    --------
    skfuzzy.defuzzify.centroid, skfuzzy.defuzzify.dcentroid
    """
    mode = mode.lower()
    x = x.ravel()
    mfx = mfx.ravel()
    n = len(x)
    if n != len(mfx):
        raise InconsistentMFDataError()

    if 'centroid' in mode or 'bisector' in mode:
        if mfx.sum() == 0:  # Approximation of total area
            raise EmptyMembershipError()

        if 'centroid' in mode:
            return centroid(x, mfx)

        elif 'bisector' in mode:
            return bisector(x, mfx)

    elif 'mom' in mode:
        return np.mean(x[mfx == mfx.max()])

    elif 'som' in mode:
        return np.min(x[mfx == mfx.max()])

    elif 'lom' in mode:
        return np.max(x[mfx == mfx.max()])

    else:
        raise ValueError("The input for `mode`, {}, was incorrect."
                         .format(mode))


def _interp_universe(x, xmf, mf_val):
    """
    Find the universe variable corresponding to membership `mf_val`.

    Parameters
    ----------
    x : 1d array
        Independent discrete variable vector.
    xmf : 1d array
        Fuzzy membership function for x.  Same length as x.
    mf_val : float
        Discrete singleton value on membership function mfx.

    Returns
    -------
    x_interp : float
        Universe variable value corresponding to `mf_val`.
    """
    slope = (xmf[1] - xmf[0]) / float(x[1] - x[0])

    x_interp = (mf_val - xmf[0]) / slope

    return x_interp


def lambda_cut_series(x, mfx, n):
    """
    Determine a series of lambda-cuts in a sweep from 0+ to 1.0 in n steps.

    Parameters
    ----------
    x : 1d array
        Universe function for fuzzy membership function mfx.
    mfx : 1d array
        Fuzzy membership function for x.
    n : int
        Number of steps.

    Returns
    -------
    z : 2d array, (n, 3)
        Lambda cut intevals.
    """

    x = np.asarray(x)
    mfx = np.asarray(mfx)
    step = (mfx.max() - mfx.min()) / float(n - 1)
    lambda_cuts = np.arange(mfx.min(), mfx.max() + np.finfo(float).eps, step)
    z = np.zeros((n, 3))
    z[:, 0] = lambda_cuts.T
    z[0, [1, 2]] = _support(x, mfx)
    # Sorting by membership turns every threshold into one suffix of the data.
    # Prefix reductions of reversed x provide all suffix extrema in linear work.
    order = np.argsort(mfx, kind='stable')
    ordered_x = x[order]
    lower = np.minimum.accumulate(ordered_x[::-1])[::-1]
    upper = np.maximum.accumulate(ordered_x[::-1])[::-1]
    index = np.searchsorted(mfx[order], lambda_cuts[1:] - 1e-6, side='left')
    if np.any(index == x.size):
        np.empty(0).min()  # Preserve the legacy empty-cut reduction error.
    z[1:, 1] = lower[index]
    z[1:, 2] = upper[index]
    return z


def _lcutinterval(x, mfx, lambdacut):
    """
    Determine upper & lower interval limits of the lambda-cut for membership
    function u(x) [here mfx].

    Parameters
    ----------
    x : 1d array
        Independent variable.
    mfx : 1d array
        Fuzzy membership function for x.
    lambdacut : float
        Value used for lambda-cut.

    Returns
    -------
    z : 1d array
        Lambda-cut output.

    Notes
    -----
    Membership function mfx must be convex and monotonic in rise or fall.
    """
    z = x[lambdacut - 1e-6 <= mfx]
    return np.hstack((z.min(), z.max()))


def lambda_cut(ms, lcut):
    """
    The crisp (binary) lambda-cut set of the membership sequence `ms`
    with membership >= `lcut`.

    Parameters
    ----------
    ms : 1d array
        Fuzzy membership set.
    lcut : float
        Value used for lambda-cut, on range [0, 1.0].

    Returns
    -------
    mlambda : 1d array
        Lambda-cut set of `ms`: ones if ms[i] >= lcut, zeros otherwise.
    """
    if lcut == 1:
        return (ms >= lcut) * 1
    else:
        return (ms > lcut) * 1


def lambda_cut_boundaries(x, mfx, lambdacut):
    """
    Find exact boundaries where `mfx` crosses `lambdacut` using interpolation.

    Parameters
    ----------
    x : 1d array, length N
        Universe variable
    mfx : 1d array, length N
        Fuzzy membership function
    lambdacut : float
        Floating point value on range [0, 1].

    Returns
    -------
    boundaries : 1d array
        Floating point values of `x` where `mfx` crosses `lambdacut`.
        Calculated using linear interpolation.

    Notes
    -----
    The values returned by this function can be thought of as intersections
    between a hypothetical horizontal line at ``lambdacut`` and the membership
    function ``mfx``. This function assumes the end values of ``mfx`` continue
    on forever in positive and negative directions. This means there will NOT
    be crossings found exactly at the bounds of ``x`` unless the value of
    ``mfx`` at the boundary is exactly ``lambdacut``.
    """

    lcutset = lambda_cut(mfx, lambdacut)
    # Edge extension creates no extra crossings, so no padded copy is necessary.
    cross = np.flatnonzero(np.diff(lcutset)) + 1
    if cross.size == 0:
        return np.empty(0, dtype=float)
    # Match NumPy's scalar promotion in the former per-crossing helper.
    slope_dtype = np.asarray((mfx[0] - mfx[0]) / 1.0).dtype
    slope = ((mfx[cross] - mfx[cross - 1])
             / (x[cross] - x[cross - 1]).astype(slope_dtype))
    boundaries = x[cross - 1] + (lambdacut - mfx[cross - 1]) / slope
    return np.unique(boundaries)


def _support(x, mfx):
    """
    Determine lower & upper limits of the support interval.

    Parameters
    ----------
    x : 1d array
        Independent variable.
    mfx : 1d array
        Fuzzy membership function for x; must be convex, continuous,
        and monotonic (rise XOR fall).

    Returns
    -------
    z : 1d array, length 2
        Interval representing lower & upper limits of the support interval.
    """
    apex = mfx.max()
    m = np.nonzero(mfx == apex)[0][0]
    n = len(x)
    xx = x[0:m + 1]
    mfxx = mfx[0:m + 1]
    z = xx[mfxx == mfxx.min()].max()
    xx = x[m:n]
    mfxx = mfx[m:n]
    return np.r_[z, xx[mfxx == mfxx.min()].min()]
