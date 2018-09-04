"""
fuzzy_logic.py : General logical operations on fuzzy membership functions,
                 a.k.a. fuzzy sets.
"""

import numpy as np


def _resampleuniverse(x, mfx, y, mfy):
    """
    Resamples fuzzy universes `x` and `y` to include the full range of either
    universe, with resolution of the lowest difference between any two
    reported points.

    """
    minstep = np.asarray([np.diff(x).min(), np.diff(y).min()]).min()

    mi = min(x.min(), y.min())
    ma = max(x.max(), y.max())
    z = np.r_[mi:ma:minstep]

    xidx = np.argsort(x)
    mfx = mfx[xidx]
    x = x[xidx]
    mfx2 = np.interp(z, x, mfx)

    yidx = np.argsort(y)
    mfy = mfy[yidx]
    y = y[yidx]
    mfy2 = np.interp(z, y, mfy)

    return z, mfx2, mfy2


def fuzzy_norm(x, mfx, y, mfy, norm):
    """
    Fuzzy operator, logic operatrion of two fuzzy sets.

    Parameters
    ----------
    x : 1d array
        Universe variable for fuzzy membership function `mfx`.
    mfx : 1d array
        Fuzzy membership function for universe variable `x`.
    y : 1d array
        Universe variable for fuzzy membership function `mfy`.
    mfy : 1d array
        Fuzzy membership function for universe variable `y`.
    norm : Function
        T-norm or T-conorm (S-norm)

    Returns
    -------
    z : 1d array
        Universe variable for union of the two provided fuzzy sets.
    mfz : 1d array
        Fuzzy membership function, the result of the operation
        of `mfx` and `mfy`.

    Notes
    -------
    See `T-Norm <https://en.wikipedia.org/wiki/T-norm>`_ for t-norms.

    """
    # Check if universes are the same
    sameuniverse = False
    if x.shape == y.shape and (x == y).all():
        z = x
        mfx2 = mfx
        mfy2 = mfy
        sameuniverse = True

    if not sameuniverse:
        z, mfx2, mfy2 = _resampleuniverse(x, mfx, y, mfy)

    return z, norm(mfx2, mfy2)


def fuzzy_and(x, mfx, y, mfy):
    """
    Fuzzy AND operator, a.k.a. the intersection of two fuzzy sets.

    Parameters
    ----------
    x : 1d array
        Universe variable for fuzzy membership function `mfx`.
    mfx : 1d array
        Fuzzy membership function for universe variable `x`.
    y : 1d array
        Universe variable for fuzzy membership function `mfy`.
    mfy : 1d array
        Fuzzy membership function for universe variable `y`.

    Returns
    -------
    z : 1d array
        Universe variable for union of the two provided fuzzy sets.
    mfz : 1d array
        Fuzzy AND (intersection) of `mfx` and `mfy`.

    """
    # Check if universes are the same
    return fuzzy_norm(x, mfx, y, mfy, norm=np.fmin)


def fuzzy_or(x, mfx, y, mfy):
    """
    Fuzzy OR operator, a.k.a. union of two fuzzy sets.

    Parameters
    ----------
    x : 1d array
        Universe variable for fuzzy membership function `mfx`.
    mfx : 1d array
        Fuzzy membership function for universe variable `x`.
    y : 1d array
        Universe variable for fuzzy membership function `mfy`.
    mfy : 1d array
        Fuzzy membership function for universe variable `y`.

    Returns
    -------
    z : 1d array
        Universe variable for intersection of the two provided fuzzy sets.
    mfz : 1d array
        Fuzzy OR (union) of `mfx` and `mfy`.

    """
    # Check if universes are the same
    return fuzzy_norm(x, mfx, y, mfy, norm=np.fmax)


def fuzzy_not(mfx):
    """
    Fuzzy NOT operator, a.k.a. complement of a fuzzy set.

    Parameters
    ----------
    mfx : 1d array
        Fuzzy membership function.

    Returns
    -------
    mfz : 1d array
        Fuzzy NOT (complement) of `mfx`.

    Notes
    -----
    This operation does not require a universe variable, because the
    complement is defined for a single set. The output remains defined on the
    same universe.

    """
    return 1. - mfx
