"""
imops.py : scikit-fuzzy subpackage for 2-D fuzzy processing, usually applied
           to image data.

"""

import numpy as np
from .arraypad import pad
from .shape import view_as_windows


def defocus_local_means(I):
    """
    Defocusing non-normalized image I using local arithmatic mean.

    Parameters
    ----------
    I : ndarray
        Input image; normalization not required.

    Returns
    -------
    D : ndarray of floats, same shape as I
        Defocused output image. By definition will not extend the range of `I`
        but the result will be an array of floats.

    Notes
    -----
    Reduces 'salt & pepper' noise in a quantized image by taking the
    arithmatic mean of the 4-connected neighborhood. So the new value at X

            +---+
            | c |
        +---+---+---+
        | a | X | b |
        +---+---+---+
            | d |
            +---+

    is defined by

        X = 0.25 * (a + b + c + d)

    """
    # Pad input
    J = pad(I.astype(np.float64), ((1, 1), (1, 1)), mode='reflect')

    # Rolling windows into array
    J = view_as_windows(J, (3, 3))

    # Slice out & average along axis representing 4 nearest neighbors
    return J[:, :, [1, 1, 0, 2], [0, 2, 1, 1]].mean(axis=2)


def contrast_curves(I, above, below, split=0.5, normalize=True):
    """
    General contrast booster or diffuser of normalized image I.

    Parameters
    ----------
    I : 2d array
        Input image (of floats on range [0, 1] if normalize=False). If values
        exist outside this range with normalize=True the image will be
        normalized for calculation.
    above : float
        Scalar, controlling the exponential contrast mechanism for values
        above `split` in `I`. If positive, the curve provides added contrast;
        if negative, the curve provides reduced contrast in lighter regions.
        See Note for details.
    below : float
        Scalar, controlling the exponential contrast mechanism for values
        below `split` in `I`. If positive, the curve provides added contrast;
        if negative, the curve provides reduced contrast in lighter regions.
        See Note for details.
    split : float
        Positive scalar, on range [0, 1], determining the midpoint of the
        exponential contrast. The contrast below `split` is controlled by
        `below`, while the contrast above `split` is controlled by `above`.
        Default of 0.5 is reasonable for well-exposed images.
    normalize : bool, default True
        Controls if intensities in `I` will be normalized to the range [0, 1].

    Returns
    -------
    focused : 2d array
        Contrast adjusted, normalized, floating-point image on range [0, 1].

    Note
    ----
    The result of this algorithm is like applying a Curves adjustment in the
    GIMP or Photoshop.

    Algorithm for curves adjustment at a given pixel, x, is given by:

             | split * (x/split)^below,                        0 <= x <= split
    y(x)  =  |
             | 1 - (1-split) * ((1-x) / (1-split))^above,   split < x <= 1.0

    """
    # Ensure scalars are floats, to avoid truncating division in Python 2.x
    split = float(split)
    above = float(above)
    below = float(below)
    im = I.astype(float)

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

    return focused * ma


def contrast_sigmoid(x, power, split=0.5):
    """
    Intensifies the gray scale in an image. Uses array implementation of
    the sigmoid function,  y = 1 / (1 + exp(- exp(- p * (x-q))))

    Parameters
    ----------
    x : ndarray
        Input vector or image array.  Should be pre-normalized to range [0, 1]
    p : float
        Power of the intensification (p > 0). Experiment with small, decimal
        values and increase if necessary.
    split : float
        Threshold for intensification. Values above `split` will be
        intensified, while values below `split` will be deintensified. Note
        range for `split` is (0, 1). Default of 0.5 is reasonable for many
        well-exposed images.

    Returns
    -------
    y : ndarray, same size as x
        Output vector or image with contrast adjusted.

    """
    return 1. / (1. + np.exp(- power * (x - split)))
