"""
cmeans.py : Fuzzy C-means clustering algorithm.

"""
import numpy as np
from scipy.spatial.distance import cdist


def _cmeans0(data, U_old, c, m):
    """
    Single step in generic fuzzy c-means clustering algorithm. Modified from
    Ross, Fuzzy Logic w/Engineering Applications (2010) p.352-353, equations
    10.28 - 10.35.

    Parameters inhereited from cmeans()

    This algorithm is a ripe target for Cython.

    """
    # Normalizing, then eliminating any potential zero values.
    U_old /= np.dot(np.ones((c, 1)), np.atleast_2d(U_old.sum(axis=0)))
    U_old = np.fmax(U_old, np.finfo(float).eps)

    Um = U_old ** m

    # Calculate cluster centers
    data = data.T
    cntr = np.dot(Um, data) / (np.dot(np.ones((data.shape[1], 1)),
                                      np.atleast_2d(Um.sum(axis=1))).T)

    d = _distance(data, cntr)
    d = np.fmax(d, np.finfo(float).eps)

    Jm = (Um * d ** 2).sum()

    U = d ** (- 2. / (m - 1))
    U /= np.ones((c, 1)).dot(np.atleast_2d(U.sum(axis=0)))

    return cntr, U, Jm, d


def _distance(data, centers):
    """
    Calcuate Euclidean distance from each point to each cluster center,
    returning results in matrix form.

    Parameters
    ----------
    data : 2d array (N x Q)
        Data to be analyzed. There are N data points.
    centers : 2d array (C x Q)
        Cluster centers. There are C clusters, with Q features.

    Returns
    -------
    dist : 2d array (C x N)
        Euclidean distance from each point, to each cluster center.

    See Also
    --------
    ``scipy.spatial.distance.cdist``

    """
    return cdist(data, centers).T


def _fp_coeff(U):
    """
    Fuzzy partition coefficient `fpc` relative to fuzzy c-partitioned
    matrix U. Measures 'fuzziness' in partitioned clustering.

    Parameter
    ---------
    U : 2d array (C, N)
        Fuzzy c-partitioned matrix; N = number of data points and C = number
        of clusters.

    Returns
    -------
    fpc : float
        Fuzzy partition coefficient.

    """
    c, n = U.shape[:2]

    return np.trace(U.dot(U.T)) / float(n)


def cmeans(data, c, m, error, maxiter, U_init=None):
    """
    Fuzzy c-means clustering.

    Parameters
    ----------
    data : 2d array, size (S, N)
        Data to be clustered.  N is the number of data sets; S is the number
        of features within each sample vector.
    c : int
        Desired number of clusters or classes.
    m : float
        Array exponentiation applied to the membership function U_old at each
        iteration, where U_new = U_old ** m.
    error : float
        Stopping criterion; stop early if the norm of (U[p] - U[p-1]) < error.
    maxiter : int
        Maximum number of iterations allowed.
    U_init : 2d array, size (S, N)
        Initial fuzzy c-partitioned matrix. If none provided, algorithm is
        randomly initialized.

    Returns
    -------
    cntr : 2d array, size (S, c)
        Cluster centers.  Data for each center along each feature provided
        for every cluster (of the `c` requested clusters).
    U : 2d array, (S, N)
        Final fuzzy c-partitioned matrix.
    U0 : 2d array, (S, N)
        Initial guess at fuzzy c-partitioned matrix (either provided U_init or
        random guess used if U_init was not provided).
    d : 2d array, (S, N)
        Final Euclidian distance matrix.
    Jm : 1d array, length P
        Objective function history.
    p : int
        Number of iterations run.
    fpc : float
        Final fuzzy partition coefficient.

    References
    ----------
    .. [1] Ross, Timothy J. Fuzzy Logic With Engineering Applications, 3rd ed.
           Wiley. 2010. ISBN 978-0-470-74376-8 pp 352-353, eq 10.28 - 10.35.

    """
    np.random.seed(seed=123)

    # Setup U0
    if U_init is None:
        n = data.shape[1]
        U0 = np.random.rand(c, n)
        U0 /= np.ones((c, 1)).dot(np.atleast_2d(U0.sum(axis=0))).astype(float)
        U_init = U0.copy()
    U0 = U_init
    U = np.fmax(U0, np.finfo(float).eps)

    # Initialize loop parameters
    Jm = np.empty(0)
    p = 0

    # Main cmeans loop
    while p < maxiter - 1:
        U2 = U.copy()
        [cntr, U, JJm, d] = _cmeans0(data, U2, c, m)
        Jm = np.hstack((Jm, JJm))
        p += 1

        # Stopping rule
        if np.linalg.norm(U - U2) < error:
            break

    # Final calculations
    error = np.linalg.norm(U - U2)
    fpc = _fp_coeff(U)

    return cntr, U, U0, d, Jm, p, fpc
