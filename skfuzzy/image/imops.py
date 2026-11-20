"""
imops.py : scikit-fuzzy subpackage for 2-D fuzzy processing, usually applied
           to image data.

"""

import numpy as np
from .arraypad import pad


def defocus_local_means(im):
    """
    Defocusing non-normalized image ``im`` using local arithmatic mean.

    Parameters
    ----------
    im : ndarray
        Input image, normalization not required. NaN values unsupported.

    Returns
    -------
    D : ndarray of floats, same shape as ``im``
        Defocused output image. By definition will not extend the range of
        ``im``, but the result returned will be an array of floats
        regardless of input dtype.

    Notes
    -----
    Reduces 'salt & pepper' noise in a quantized image by taking the
    arithmatic mean of the 4-connected neighborhood. So the new value at
    ``X``, given the 4-connected neighborhood::

          +---+
          | c |
      +---+---+---+
      | a | X | b |
      +---+---+---+
          | d |
          +---+

    is defined by the relationship::

      X = 0.25 * (a + b + c + d)

    """
    # Pad input
    out = pad(im.astype(np.float64), ((1, 1), (1, 1)), mode='reflect')

    # Rolling windows into array
    # Accumulate in the same left right up down order without gathering
    # a height by width by four tensor.
    result = out[1:-1, :-2] + out[1:-1, 2:]
    result += out[:-2, 1:-1]
    result += out[2:, 1:-1]
    result /= 4
    return result
