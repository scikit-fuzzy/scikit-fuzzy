from __future__ import division


def nmse(I, J):
    """
    Computes the percent normalized mean square error (NMSE %) between known
    and degraded arrays.

    Parameters
    ----------
    I : ndarray
        Known array of arbitrary size and shape. Must be convertible to float.
    J : ndarray, same shape as `I`
        Degraded version of `I`, must have same shape as `I`.

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
    diff = I - J
    return 100. * diff.var() / I.var()
