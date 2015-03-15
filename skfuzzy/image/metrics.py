from __future__ import division


def nmse(known, degraded):
    """
    Computes the percent normalized mean square error (NMSE %) between known
    and degraded arrays.

    Parameters
    ----------
    known : ndarray
        Known array of arbitrary size and shape. Must be convertible to float.
    degraded : ndarray, same shape as `known`
        Degraded version of `known`, must have same shape as `known`.

    Returns
    -------
    nmse : float
        Calculated NMSE, as a percentage.

    Notes
    -----
    Usually used to compare a true/original image to a degraded version.
    For this calculation, which image is provided as true and which degraded
    does not matter.

    """
    diff = known - degraded
    return 100. * diff.var() / known.var()
