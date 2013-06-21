"""shape.py - Padding & Block or rolling window views into arrays.

`view_as_windows` and `view_as_blocks` were brought into this project from
`scikit-image` in order to avoid adding same package as a dependency.  It was
originally released under the BSD 3-clause license, retained in `skfuzzy`.

"""
from __future__ import print_function
import numpy as np
from numpy.lib.stride_tricks import as_strided

__all__ = ['view_as_blocks', 'view_as_windows', 'pad']


def view_as_blocks(arr_in, block_shape):
    """Block view of the input n-dimensional array (using re-striding).

    Blocks are non-overlapping views of the input array.

    Parameters
    ----------
    arr_in: ndarray
        The n-dimensional input array.
    block_shape: tuple
        The shape of the block. Each dimension must divide evenly into the
        corresponding dimensions of `arr_in`.

    Returns
    -------
    arr_out: ndarray
        Block view of the input array.

    Examples
    --------
    >>> import numpy as np
    >>> from skimage.util.shape import view_as_blocks
    >>> A = np.arange(4*4).reshape(4,4)
    >>> A
    array([[ 0,  1,  2,  3],
           [ 4,  5,  6,  7],
           [ 8,  9, 10, 11],
           [12, 13, 14, 15]])
    >>> B = view_as_blocks(A, block_shape=(2, 2))
    >>> B[0, 0]
    array([[0, 1],
           [4, 5]])
    >>> B[0, 1]
    array([[2, 3],
           [6, 7]])
    >>> B[1, 0, 1, 1]
    13

    >>> A = np.arange(4*4*6).reshape(4,4,6)
    >>> A  # doctest: +NORMALIZE_WHITESPACE
    array([[[ 0,  1,  2,  3,  4,  5],
            [ 6,  7,  8,  9, 10, 11],
            [12, 13, 14, 15, 16, 17],
            [18, 19, 20, 21, 22, 23]],
           [[24, 25, 26, 27, 28, 29],
            [30, 31, 32, 33, 34, 35],
            [36, 37, 38, 39, 40, 41],
            [42, 43, 44, 45, 46, 47]],
           [[48, 49, 50, 51, 52, 53],
            [54, 55, 56, 57, 58, 59],
            [60, 61, 62, 63, 64, 65],
            [66, 67, 68, 69, 70, 71]],
           [[72, 73, 74, 75, 76, 77],
            [78, 79, 80, 81, 82, 83],
            [84, 85, 86, 87, 88, 89],
            [90, 91, 92, 93, 94, 95]]])
    >>> B = view_as_blocks(A, block_shape=(1, 2, 2))
    >>> B.shape
    (4, 2, 3, 1, 2, 2)
    >>> B[2:, 0, 2]  # doctest: +NORMALIZE_WHITESPACE
    array([[[[52, 53],
             [58, 59]]],
           [[[76, 77],
             [82, 83]]]])
    """

    # -- basic checks on arguments
    if not isinstance(block_shape, tuple):
        raise TypeError('block needs to be a tuple')

    block_shape = np.array(block_shape)
    if (block_shape <= 0).any():
        raise ValueError("'block_shape' elements must be strictly positive")

    if block_shape.size != arr_in.ndim:
        raise ValueError("'block_shape' must have the same length "
                         "as 'arr_in.shape'")

    arr_shape = np.array(arr_in.shape)
    if (arr_shape % block_shape).sum() != 0:
        raise ValueError("'block_shape' is not compatible with 'arr_in'")

    # -- restride the array to build the block view
    arr_in = np.ascontiguousarray(arr_in)

    new_shape = tuple(arr_shape / block_shape) + tuple(block_shape)
    new_strides = tuple(arr_in.strides * block_shape) + arr_in.strides

    arr_out = as_strided(arr_in, shape=new_shape, strides=new_strides)

    return arr_out


def view_as_windows(arr_in, window_shape):
    """Rolling window view of the input n-dimensional array.

    Windows are overlapping views of the input array, with adjacent windows
    shifted by a single row or column (or an index of a higher dimension).

    Parameters
    ----------
    arr_in: ndarray
        The n-dimensional input array.
    window_shape: tuple
        Defines the shape of the elementary n-dimensional orthotope
        (better know as hyperrectangle [1]_) of the rolling window view.

    Returns
    -------
    arr_out: ndarray
        (rolling) window view of the input array.

    Notes
    -----
    One should be very careful with rolling views when it comes to
    memory usage.  Indeed, although a 'view' has the same memory
    footprint as its base array, the actual array that emerges when this
    'view' is used in a computation is generally a (much) larger array
    than the original, especially for 2-dimensional arrays and above.

    For example, let us consider a 3 dimensional array of size (100,
    100, 100) of ``float64``. This array takes about 8*100**3 Bytes for
    storage which is just 8 MB. If one decides to build a rolling view
    on this array with a window of (3, 3, 3) the hypothetical size of
    the rolling view (if one was to reshape the view for example) would
    be 8*(100-3+1)**3*3**3 which is about 203 MB! The scaling becomes
    even worse as the dimension of the input array becomes larger.

    References
    ----------
    .. [1] http://en.wikipedia.org/wiki/Hyperrectangle

    Examples
    --------
    >>> import numpy as np
    >>> from skimage.util.shape import view_as_windows
    >>> A = np.arange(4*4).reshape(4,4)
    >>> A
    array([[ 0,  1,  2,  3],
           [ 4,  5,  6,  7],
           [ 8,  9, 10, 11],
           [12, 13, 14, 15]])
    >>> window_shape = (2, 2)
    >>> B = view_as_windows(A, window_shape)
    >>> B[0, 0]
    array([[0, 1],
           [4, 5]])
    >>> B[0, 1]
    array([[1, 2],
           [5, 6]])

    >>> A = np.arange(10)
    >>> A
    array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
    >>> window_shape = (3,)
    >>> B = view_as_windows(A, window_shape)
    >>> B.shape
    (8, 3)
    >>> B
    array([[0, 1, 2],
           [1, 2, 3],
           [2, 3, 4],
           [3, 4, 5],
           [4, 5, 6],
           [5, 6, 7],
           [6, 7, 8],
           [7, 8, 9]])

    >>> A = np.arange(5*4).reshape(5, 4)
    >>> A
    array([[ 0,  1,  2,  3],
           [ 4,  5,  6,  7],
           [ 8,  9, 10, 11],
           [12, 13, 14, 15],
           [16, 17, 18, 19]])
    >>> window_shape = (4, 3)
    >>> B = view_as_windows(A, window_shape)
    >>> B.shape
    (2, 2, 4, 3)
    >>> B  # doctest: +NORMALIZE_WHITESPACE
    array([[[[ 0,  1,  2],
             [ 4,  5,  6],
             [ 8,  9, 10],
             [12, 13, 14]],
            [[ 1,  2,  3],
             [ 5,  6,  7],
             [ 9, 10, 11],
             [13, 14, 15]]],
           [[[ 4,  5,  6],
             [ 8,  9, 10],
             [12, 13, 14],
             [16, 17, 18]],
            [[ 5,  6,  7],
             [ 9, 10, 11],
             [13, 14, 15],
             [17, 18, 19]]]])
    """

    # -- basic checks on arguments
    if not isinstance(arr_in, np.ndarray):
        raise TypeError("'arr_in' must be a numpy ndarray")
    if not isinstance(window_shape, tuple):
        raise TypeError("'window_shape' must be a tuple")
    if not (len(window_shape) == arr_in.ndim):
        raise ValueError("'window_shape' is incompatible with 'arr_in.shape'")

    arr_shape = np.array(arr_in.shape)
    window_shape = np.array(window_shape, dtype=arr_shape.dtype)

    if ((arr_shape - window_shape) < 0).any():
        raise ValueError("'window_shape' is too large")

    if ((window_shape - 1) < 0).any():
        raise ValueError("'window_shape' is too small")

    # -- build rolling window view
    arr_in = np.ascontiguousarray(arr_in)

    new_shape = tuple(arr_shape - window_shape + 1) + tuple(window_shape)
    new_strides = arr_in.strides + arr_in.strides

    arr_out = as_strided(arr_in, shape=new_shape, strides=new_strides)

    return arr_out


def pad(I, psf, mode='reflect'):
    """
    Function to pad borders of a 2d array.

    Parameters
    ----------
    I : 2d array (Ix, Iy)
        Input grayscale image
    psf : 2d array (mx, my)  OR  Tuple of ints
        Either the array which will be applied to I (region of interest)
        OR a length 2 Tuple, containing the size of the kernel to be applied
        to `I`.
    mode : string
        Option kwarg; controls how padding is done.

        * 'reflect' : Default, reflects values from interior to borders.
        * 'zero' : Pads with zeros.
        * 'replicate' : Pads by repeating outermost row. Corners repeat the
                        corner pixel in an ever-increasing region.

    Returns
    -------
    J : 2d array (Ix + mx - 1, Iy + my - 1)
        Padded version of `I` by reflection (including corners).
        Outer row NOT duplicated.

    Note
    ----
    For proper behavior, the `psf` dimensions mx and my should both be odd.

    """
    dx = I.shape[0]
    dy = I.shape[1]

    try:
        xpad = (psf.shape[0] - 1) / 2
        ypad = (psf.shape[1] - 1) / 2
    except AttributeError:
        xpad = (psf[0] - 1) / 2
        ypad = (psf[1] - 1) / 2

    if 'zero' in mode:
        sides = np.zeros((dx, ypad), dtype=I.dtype)
        J = np.hstack((sides, I, sides))
        top = np.zeros((xpad, dy + 2 * ypad), dtype=I.dtype)
        J = np.vstack((top, J, top))

    elif 'replicate' in mode:
        lside = np.atleast_2d(I[:, 0]).T.repeat(ypad, axis=1)
        rside = np.atleast_2d(I[:, -1]).T.repeat(ypad, axis=1)
        J = np.hstack((lside, I, rside))
        top = np.atleast_2d(J[0, :]).repeat(xpad, axis=0)
        bot = np.atleast_2d(J[-1, :]).repeat(ypad, axis=0)
        J = np.vstack((top, J, bot))

    else:
        # Check if this doesn't make sense for reflect
        if (xpad >= dx - 1) or (ypad >= dy - 1):
            print('Padding required is too large! I and m may be switched.')
            # Pad as much as possible
            xpad = dx - 2
            ypad = dy - 2

        # Pad left and right sides
        J = np.hstack((I[:, ypad:0: - 1], I, I[:, dy - 2:dy - ypad - 2:-1]))

        # Make top & bottom w/corners
        top = np.hstack((I[xpad:0:-1, ypad:0:-1],
                         I[xpad:0:-1, :],
                         I[xpad:0:-1, dy - 2:dy - ypad - 2:-1]))

        bot = np.hstack((I[dx - 2:dx - xpad - 2:-1, ypad:0:-1],
                         I[dx - 2:dx - xpad - 2:-1, :],
                         I[dx - 2:dx - xpad - 2:-1, dy - 2:dy - ypad - 2:-1]))

        J = np.vstack((top, J, bot))

    return J
