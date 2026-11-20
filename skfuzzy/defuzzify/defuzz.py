"""
defuzz.py : Various methods for defuzzification and lambda-cuts, to convert
            'fuzzy' systems back into 'crisp' values for decisions.
"""
import numpy as np

from .exceptions import EmptyMembershipError, InconsistentMFDataError
from ..image.arraypad import pad


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

    if len(x) == 1:
        return (x[0] * mfx[0]
                / np.fmax(mfx[0], np.finfo(float).eps).astype(float))
    area, moment, valid = _linear_segments(x, mfx, moments=True)
    sum_area = _ordered_sum(area[valid])
    sum_moment_area = _ordered_sum((moment * area)[valid])
    return sum_moment_area / np.fmax(sum_area, np.finfo(float).eps).astype(float)


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

    if len(x) == 1:
        return x[0]
    areas, valid = _linear_segments(x, mfx)
    sum_area = _ordered_sum(areas[valid])
    cumulative = np.cumsum(np.concatenate((np.zeros(1, dtype=areas.dtype), areas)))[1:]
    # A zero-area segment must carry the previous cumulative area forward.
    # Resetting it to zero can place the reported bisector outside its segment.
    accum_area = cumulative
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

    for ii in range(1, n):
        xx = _lcutinterval(x, mfx, lambda_cuts[ii])
        z[ii, [1, 2]] = xx

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
    # Pad binary set two values by extension
    mfxx = pad(mfx, [2, 2], 'edge')

    # Find binary lambda cut set
    lcutset = lambda_cut(mfxx, lambdacut)

    # Detect crossings with convolution, cutting off one padded value
    crossings = np.convolve(lcutset, [1, -1])[1:-1]
    argcrossings = np.where(np.abs(crossings) > 0)[0] - 1

    # Calculate exact crossing points, removing the last padded value
    boundaries = []
    for cross in argcrossings:
        idx = slice(cross - 1, cross + 1)
        boundaries.append(
            x[cross - 1] + _interp_universe(x[idx], mfx[idx], lambdacut))

    # Eliminate degenerate points at peaks with np.unique
    return np.unique(np.r_[boundaries])


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


def _linear_segments(x, mfx, moments=False):
    """Areas and first moments with the scalar formulas and branch order."""
    x, mfx = np.asarray(x), np.asarray(mfx)
    x1, x2 = x[..., :-1], x[..., 1:]
    y1, y2 = mfx[..., :-1], mfx[..., 1:]
    dx = x2 - x1
    valid = ~(((y1 == 0) & (y2 == 0)) | (x1 == x2))
    dtype = np.result_type(dx, y1, np.asarray(0.5 * dx.dtype.type(0)).dtype)
    area = np.zeros(dx.shape, dtype=dtype)
    rect = valid & (y1 == y2)
    rise = valid & ~rect & (y1 == 0) & (y2 != 0)
    fall = valid & ~rect & ~rise & (y2 == 0) & (y1 != 0)
    general = valid & ~rect & ~rise & ~fall
    area[rect] = dx[rect] * y1[rect]
    area[rise] = _scalar_scale(0.5, dx[rise]) * y2[rise]
    area[fall] = _scalar_scale(0.5, dx[fall]) * y1[fall]
    area[general] = _scalar_scale(0.5, dx[general]) * (y1[general] + y2[general])
    if not moments:
        return area, valid
    moment = np.zeros(dx.shape, dtype=dtype)
    moment[rect] = _scalar_scale(0.5, x1[rect] + x2[rect])
    moment[rise] = _scalar_scale(2.0 / 3.0, dx[rise]) + x1[rise]
    moment[fall] = _scalar_scale(1.0 / 3.0, dx[fall]) + x1[fall]
    moment[general] = ((_scalar_scale(2.0 / 3.0, dx[general])
                       * (y2[general] + _scalar_scale(0.5, y1[general])))
                      / (y1[general] + y2[general]) + x1[general])
    return area, moment, valid


def _ordered_sum(values):
    """Preserve the scalar loop's left to right additions including its zero."""
    values = np.asarray(values)
    return np.cumsum(np.concatenate((np.zeros(1, dtype=values.dtype), values)))[-1]



def _scalar_scale(factor, values):
    """Match Python float times NumPy scalar promotion on NumPy 1 and 2."""
    dtype = np.asarray(factor * values.dtype.type(0)).dtype
    return np.multiply(factor, values, dtype=dtype)
