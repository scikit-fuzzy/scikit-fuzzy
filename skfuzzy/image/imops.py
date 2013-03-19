"""
imops.py : scikit-fuzzy subpackage for 2-D fuzzy processing, usually applied
           to image data.

"""

import numpy as np
from .shape import pad as padimg


def defocus(I, bits, pad=True, unpad=False):
    """
    Defocusing non-normalized image I.

    Parameters
    ----------
    I : ndarray
        Input image; normalization not required.
    bits : float
        Bit depth of the input image.
    pad : bool
        Controls edge padding. Default = True (DO use padding).
    unpad : bool
        Controls removal of padding in output. Default = False (retain pad).

    Returns
    -------
    D : ndarray, same shape as I
        Defocused output image.

    Notes
    -----
    Reduces 'salt & pepper' noise in a quantized image.  Edge padding is used.

    """
    dims = I.shape
    M = 2 ** bits - 1
    J = I.copy()
    J = J / float(M)

    # Padding
    if pad:
        J = padimg(J, [3, 3])

    D = np.zeros_like(I).astype(float)

    for ii in np.arange(dims[0]) + 1:
        for jj in np.arange(dims[1]) + 1:
            D[ii - 1, jj - 1] = 0.25 * (J[ii - 1, jj] + J[ii + 1, jj] +
                                        J[ii, jj - 1] + J[ii, jj + 1])

    if not unpad:
        return np.round(D * M)
    else:
        return np.round(D[1:-1, 1:-1] * M)


def focus(I, p, a):
    """
    General contrast booster or diffuser of normalized image I.

    Parameters
    ----------
    I : 2d array
        Input image on range [0, 1]. If values exist outside this range,
        the image will be normalized and returned normalized.
    p : float
        Positive scalar, controlling the contrast mechanism. See Note.
    a : float
        Positive scalar, on range [0, 1]. See Note.

    Returns
    -------
    F : 2d array
        Output normalized image with contrast adjusted.

    Note
    ----
    Algorithm for a given pixel, x, is given by:

                 | a * (x/a)^p,                    0 <= x <= 0.5
        y(x)  =  |
                 | 1 - (1-a) * ((1-x)/(1-a))^p,   0.5 < x <= 1.0

    """
    a = float(a)
    p = float(p)
    I = I.astype(float)
    if I.max() > 1.:
        I /= float(I.max())
    N1, N2 = I.shape[:2]

    # Simplified array-wise algorithm with no looping by JDW
    # Equivalent results, more than 4x greater speed (and simplicity)
    F = np.zeros_like(I)

    F[I <= a] = a * (I[I <= a] / a) ** p
    F[I > a] = 1. - (1. - a) * ((1 - I[I > a]) / (1. - a)) ** p

    return F


def imcontrast(x, p, q):
    """
    Intensifies the gray scale in an image. Uses array implementation of
    the sigmoid function,  y = 1 / (1 + exp(- exp(-p*(x - q)) ))

    Parameters
    ----------
    x : ndarray
        Input vector or image array.  Should be pre-normalized to range [0, 1]
    p : float
        Power of the intensification (p > 0).
    q : float
        Threshold for intensification.  Values above q will be intensified,
        while values below q will be deintensified (0 < q < 1).

    Returns
    -------
    y : ndarray, same size as x
        Output vector or image.

    """
    return 1. / (1. + np.exp(- p * (x - q)))


def nmse(I, J):
    """
    Computes the percent normalized mean square error (NMSE %) between known
    and degraded arrays.

    Parameters
    ----------
    I : ndarray
        Known array of arbitrary size and shape. Must be convertible to float.
    J : ndarray, same shape as I
        Degraded array, only requirement is identical shape as I.

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
    I = I.astype(float)
    D = I - J.astype(float)
    num = D.ravel().var()
    den = I.ravel().var()
    return 100. * num / den


def sinmse(F, P):
    """
    Scale-invariant normalized mean square error (SINMSE) percentage.

    Parameters
    ----------
    F : ndarray
        Known array of arbitrary size and shape. Must be convertible to float.
    P : ndarray, same shape as I
        Degraded array, only requirement is identical shape as I.

    Returns
    -------
    sinmse : float
        SINMSE value in percent (sinmse * 100%).

    """
    F = F.astype(float)
    P = P.astype(float)

    D = np.abs(F - P)

    if D.sum() == 0:
        return 0
    else:
        FP = F * P

        # Numpy by default computes statistics on flattened arrays
        a = (FP.mean() - F.mean() * P.mean()) / P.astype(float).var()
        FaP = F - a * P
        num = FaP.var()
        den = F.var()
        return 100. * num / den
