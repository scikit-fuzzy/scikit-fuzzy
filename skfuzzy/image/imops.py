"""
imops.py : scikit-fuzzy subpackage for 2-D fuzzy processing, usually applied
           to image data.

"""

import numpy as np
from .arraypad import pad
from .shape import view_as_windows


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
    out = view_as_windows(out, (3, 3))

    # Slice out & average along axis representing 4 nearest neighbors
    return out[:, :, [1, 1, 0, 2], [0, 2, 1, 1]].mean(axis=2)
