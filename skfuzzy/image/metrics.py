import numpy as np


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


def sinmse(I, J):
    """
    Scale-invariant normalized mean square error (SINMSE) percentage.

    Parameters
    ----------
    I : ndarray
        Known array of arbitrary size and shape. Must be convertible to float.
    J : ndarray, same shape as `I`
        Degraded version of `I`, must have same shape as `I`

    Returns
    -------
    sinmse : float
        SINMSE value in percent (sinmse * 100%).

    """
    diff = np.abs(I - J)

    if diff.sum() == 0:
        return 0
    else:
        cross = I * J

    # Numpy by default computes statistics on flattened arrays
    a = (cross.mean() - I.mean() * J.mean()) / J.var()
    cross2 = I - a * J
    num = cross2.var()
    den = I.var()
    return 100. * num / den
