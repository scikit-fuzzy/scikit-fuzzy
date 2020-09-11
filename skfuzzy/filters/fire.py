"""
fire.py : Collection of Fuzzy Inference Ruled by ELSE-action (FIRE) filters.

"""

import numpy as np
from ..image import view_as_windows
from ..membership import trimf


def fire1d(x, l1=0, l2=1):
    """
    1-D filtering using Fuzzy Inference Ruled by Else-action (FIRE) [1].

    FIRE filtering is nonlinear, and is specifically designed to remove
    impulse (salt and pepper) noise.

    Parameters
    ----------
    x : 1d array or iterable
        Input sequence, filtered range limited by ``l1`` and ``l2``.
    l1 : float
        Lower input range limit for ``x``.
    l2 : float
        Upper input range limit for ``x``.

    Returns
    -------
    y : 1d array
        FIRE filtered sequence.

    Notes
    -----
    Filtering occurs for ``l1 < |x| < l2``; for ``|x| < l1`` there is no
    effect.

    References
    ----------
    .. [1] Fabrizio Russo, Fuzzy Filtering of Noisy Sensor Data, IEEE
           Instrumentation and Measurement Technology Conference,
           Brussels, Belgium, June 4 - 6, 1996, pp 1281 - 1285.

    """
    from ..image import pad as padimg

    # Enforce range limit
    np.clip(x, -l2, l2, out=x)

    # Fuzzy input sequence
    dx = np.arange(-1000, 1001) * l2 / 1000.

    # Fuzzy membership functions
    po = np.atleast_2d(trimf(dx, [l1, l2, l2])).ravel()
    ne = np.atleast_2d(trimf(dx, [-l2, -l2, -l1])).ravel()

    # Fuzzy neighborhood rules (indices for comparison)
    rules = np.r_[[[0, 1, 3],
                   [1, 3, 4],
                   [0, 3, 4],
                   [0, 1, 4]]]

    # Padding the array
    x = padimg(x, 2, mode='reflect')

    # Generate rolling 5-point window view into the array
    xx = view_as_windows(x, (5,))

    # Zero each local window relative to center point
    center = xx[:, 2]
    dxx = xx - center[:, np.newaxis].repeat(5, axis=1)

    # Conduct interpolation all at once, on every point, for po and ne
    mpo = np.interp(dxx, dx, po)
    mne = np.interp(dxx, dx, ne)

    # Build output correction functions all at once
    lam = np.zeros((0, len(mpo)))
    lam2 = np.zeros((0, len(mne)))
    for rule in rules:
        lam = np.vstack((lam, np.atleast_2d(mpo[:, rule].min(axis=1))))
        lam2 = np.vstack((lam2, np.atleast_2d(mne[:, rule].min(axis=1))))

    lam = np.max(lam, axis=0)
    lam2 = np.max(lam2, axis=0)

    # Corrected result
    y = xx[:, 2] + l2 * (lam - lam2)

    return y


def fire2d(im, l1=0, l2=255, fuzzyresolution=1):
    """
    2-D filtering using Fuzzy Inference Ruled by Else-action (FIRE) [1].

    FIRE filtering is nonlinear, and is specifically designed to remove
    impulse (salt and pepper) noise.

    Parameters
    ----------
    I : 2d array
        Input image.
    l1 : float
        Lower limit of filtering range.
    l2 : float
        Upper limit of filtering range.
    fuzzyresolution : float, default = 1
        Resolution of fuzzy input sequence, or spacing between [-l2+1, l2-1].
        The default assumes an integer input; for floating point images a
        decimal value should be used approximately equal to the bit depth.

    Returns
    -------
    J : 2d array
        FIRE filtered image.

    Notes
    -----
    Filtering occurs for ``l1 < |x| < l2``; outside this range the data is
    unaffected.

    References
    ----------
    .. [1] Fabrizio Russo, Fuzzy Filtering of Noisy Sensor Data, IEEE
           Instrumentation and Measurement Technology Conference,
           Brussels, Belgium, June 4 - 6, 1996, pp 1281 - 1285.

    """
    from ..image import pad as padimg

    im = padimg(im.astype(float), 1, mode='reflect')

    # Fuzzy input sequence
    dx = np.arange(-l2 + fuzzyresolution,
                   l2 - fuzzyresolution,
                   fuzzyresolution)

    # Fuzzy membership functions
    po = np.atleast_2d(trimf(dx, [l1,
                                  l2 - fuzzyresolution,
                                  l2 - fuzzyresolution]))
    ne = np.atleast_2d(trimf(dx, [fuzzyresolution - l2,
                                  fuzzyresolution - l2,
                                  - l1]))

    # Combine into matrix
    multi_stack_rules = np.hstack([po.T, ne.T])
    rules1 = np.r_[[[2, 4, 8],
                    [4, 6, 8],
                    [2, 6, 8],
                    [2, 4, 6]]] - 1
    rules2 = np.r_[[[1, 3, 7, 9],
                    [1, 4, 8, 9],
                    [3, 6, 7, 8],
                    [1, 2, 6, 9],
                    [2, 3, 4, 7]]] - 1

    # Zero the local windows
    local_win = view_as_windows(im, (3, 3))
    im2 = im[1:-1, 1:-1].copy()
    im2 = im2[..., np.newaxis, np.newaxis].repeat(3, axis=2).repeat(3, axis=3)
    dx = local_win - im2

    # Vectorization allows concise, fast calculation of lam and lam2
    idx = l2 + dx
    idx = idx.reshape((idx.shape[0], idx.shape[1], -1))
    mu = multi_stack_rules[idx.astype(int), :]
    lam = np.concatenate((np.min(mu[:, :, rules1[range(4), :], 0], axis=3),
                          np.min(mu[:, :, rules2[range(5), :], 0], axis=3)),
                         axis=2).max(axis=2)
    lam2 = np.concatenate((np.min(mu[:, :, rules1[range(4), :], 1], axis=3),
                          np.min(mu[:, :, rules2[range(5), :], 1], axis=3)),
                          axis=2).max(axis=2)

    return im[1:-1, 1:-1] + (l2 - 1) * (lam - lam2)
