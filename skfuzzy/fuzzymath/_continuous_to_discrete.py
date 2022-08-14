import numpy as np
import scipy.linalg


def continuous_to_discrete(a, b, sampling_rate):
    """
    Converts a continuous-time system to its equivalent discrete-time version.

    Parameters
    ----------
    a : (N, N) array of floats
        State variable coefficients describing the continuous-time system.
    b : (N,) or (N, 1) array of floats
        Constant coefficients describing the continuous-time system. Can be
        either a rank-1 array or a rank-2 array of shape (N, 1).
    sampling_rate : float
        Rate in Hz at which the continuous-time system is to be sampled.

    Returns
    -------
    phi : (N, N) array of floats
        Variable coefficients describing the discrete-time system.
    gamma : (N,) or (N, 1) array of floats
        Constant coefficients describing the discrete-time system. Shape of
        this output maintains the shape passed as `b`.

    """
    a = a.astype(float)
    b = b.astype(float)

    phi = scipy.linalg.expm(a * sampling_rate)

    a_pinv = scipy.linalg.pinv(a)

    gamma = np.dot(np.dot(a_pinv, phi - np.eye(a.shape[0])), b)

    return phi, gamma
