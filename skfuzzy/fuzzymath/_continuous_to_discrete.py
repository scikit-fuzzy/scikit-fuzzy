import scipy.linalg
import numpy as np


def continuous_to_discrete(A, B, sampling_rate):
    """
    Converts a continuous-time system to its equivalent discrete-time version.

    Parameters
    ----------
    A : (N, N) array of floats
        State variable coefficients describing the continuous-time system.
    B : (N,) or (N, 1) array of floats
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
        this output maintains the shape passed as `B`.

    """
    A = A.astype(float)
    B = B.astype(float)

    phi = scipy.linalg.expm(A * sampling_rate)

    A_pinv = scipy.linalg.pinv2(A)

    gamma = np.dot(np.dot(A_pinv, phi - np.eye(A.shape[0])), B)

    return phi, gamma
