"""
fire.py : Collection of Fuzzy Inference Ruled by ELSE-action (FIRE) filters.

"""

import numpy as np
from ..image import view_as_windows
from ..membership import trimf


def fire1d(x, L1=0, L2=1):
    """
    1-D fuzzy filtering using Fuzzy Inference Ruled by Else-action (FIRE)

    FIRE filtering is nonlinear, and is specifically designed to remove
    impulse (salt and pepper) noise.

    Parameters
    ----------
    x : 1d array or iterable
        Input sequence, filtered range limited by `L1` and `L2`.
    L1 : float
        Lower input range limit for `x`.
    L2 : float
        Upper input range limit for `x`.

    Returns
    -------
    y : 1d array
        FIRE filtered sequence.

    Note
    ----
    Filtering occurs for `L1` < |`x`| < `L2`; for |`x`| < `L1` there is no
    effect.

    Reference
    ---------
    .. [1] Fabrizio Russo, Fuzzy Filtering of Noisy Sensor Data, IEEE
           Instrumentation and Measurement Technology Conference,
           Brussels, Belgium, June 4 - 6, 1996, pp 1281 - 1285.

    """
    from ..image import pad as padimg

    # Enforce range limit
    np.clip(x, -L2, L2, out=x)

    # Fuzzy input sequence
    dx = np.arange(-1000, 1001) * L2 / 1000.

    # Fuzzy membership functions
    PO = np.atleast_2d(trimf(dx, [L1, L2, L2])).ravel()
    NE = np.atleast_2d(trimf(dx, [-L2, -L2, -L1])).ravel()

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
    center.shape += (1,)
    center = center.repeat(5, axis=1)
    dxx = xx - center

    # Conduct interpolation all at once, on every point, for PO and NE
    mPO = np.interp(dxx, dx, PO)
    mNE = np.interp(dxx, dx, NE)

    # Build output correction functions all at once
    lam = np.empty((0, len(mPO)))
    Lam = np.empty((0, len(mNE)))
    for rule in rules:
        lam = np.vstack((lam, np.atleast_2d(mPO[:, rule].min(axis=1))))
        Lam = np.vstack((Lam, np.atleast_2d(mNE[:, rule].min(axis=1))))

    lam = np.max(lam, axis=0)
    Lam = np.max(Lam, axis=0)

    # Corrected result
    y = xx[:, 2] + L2 * (lam - Lam)

    return y


def fire2d(I, L1=0, L2=255, fuzzyresolution=1):
    """
    2-D fuzzy filtering using Fuzzy Inference Ruled by Else-action (FIRE)

    FIRE filtering is nonlinear, and is specifically designed to remove
    impulse (salt and pepper) noise.

    Parameters
    ----------
    I : 2d array
        Input image.
    L1 : float
        Lower limit of filtering range.
    L2 : float
        Upper limit of filtering range.
    fuzzyresolution : float, default = 1
        Resolution of fuzzy input sequence, or spacing between [-L2+1, L2-1].

    Returns
    -------
    J : 2d array
        FIRE filtered image.

    Note
    ----
    Filtering occurs for `L1` < |`x`| < `L2`; outside this range the data is
    unaffected.

    Reference
    ---------
    .. [1] Fabrizio Russo, Fuzzy Filtering of Noisy Sensor Data, IEEE
           Instrumentation and Measurement Technology Conference,
           Brussels, Belgium, June 4 - 6, 1996, pp 1281 - 1285.

    """
    from ..image import pad as padimg

    I = padimg(I.astype(float), 1, mode='reflect')

    # Fuzzy input sequence
    dx = np.arange(- L2 + 1, L2 - 1, fuzzyresolution)

    # Fuzzy membership functions
    PO = np.atleast_2d(trimf(dx, [L1,      L2 - 1,  L2 - 1]))
    NE = np.atleast_2d(trimf(dx, [1 - L2,  1 - L2,    - L1]))

    # Combine into matrix
    MS = np.hstack([PO.T, NE.T])
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
    Q = view_as_windows(I, (3, 3))
    I2 = I[1:-1, 1:-1].copy()
    I2 = I2[..., np.newaxis, np.newaxis].repeat(3, axis=2).repeat(3, axis=3)
    dx = Q - I2

    # Vectorization allows concise, fast calculation of lam and Lam
    idx = L2 + dx
    idx = idx.reshape((idx.shape[0], idx.shape[1], -1))
    mu = MS[idx.astype(int), :]
    lam = np.concatenate((np.min(mu[:, :, rules1[range(4), :], 0], axis=3),
                          np.min(mu[:, :, rules2[range(5), :], 0], axis=3)),
                         axis=2).max(axis=2)
    Lam = np.concatenate((np.min(mu[:, :, rules1[range(4), :], 1], axis=3),
                          np.min(mu[:, :, rules2[range(5), :], 1], axis=3)),
                         axis=2).max(axis=2)

    return I[1:-1, 1:-1] + (L2 - 1) * (lam - Lam)
