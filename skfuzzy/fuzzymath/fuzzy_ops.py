"""
fuzzy_ops.py : Package of general operations on fuzzy sets, fuzzy membership
               functions, and their associated universe variables.

"""
import numpy as np


def cartadd(x, y):
    """
    Cartesian addition of two fuzzy membership vectors; algebraic method.

    Parameters
    ----------
    x : 1D array or iterable, length M
        First fuzzy membership vector.
    y : 1D array or iterable, length N
        Second fuzzy membership vector.

    Returns
    -------
    z : 2D array, (M, N)
        Resultant fuzzy membership vector.

    """
    # Ensure rank-1 input
    x, y = np.asarray(x).ravel(), np.asarray(y).ravel()

    m, n = len(x), len(y)

    a = np.dot(np.atleast_2d(x).T, np.ones((1, n)))
    b = np.dot(np.ones((m, 1)), np.atleast_2d(y))

    return a + b


def cartprod(x, y):
    """
    Cartesian product of two fuzzy membership vectors. Uses `min()`.

    Parameters
    ----------
    x : 1D array or iterable, length M
        First fuzzy membership vector.
    y : 1D array or iterable, length N
        Second fuzzy membership vector.

    Returns
    -------
    z : 2D array, size (M, N)
        Resultant fuzzy membership vector.

    """
    # Ensure rank-1 input
    x, y = np.asarray(x).ravel(), np.asarray(y).ravel()

    m, n = len(x), len(y)

    a = np.dot(np.atleast_2d(x).T, np.ones((1, n)))
    b = np.dot(np.ones((m, 1)), np.atleast_2d(y))

    return np.fmin(a, b)


def classic_relation(A, B):
    """
    Determines the classic relation matrix, R, between fuzzy sets A and B,
    on universes X and Y, respectively.

    Parameters
    ----------
    A : 1D array or iterable, length M
        First fuzzy membership vector.
    B : 1D array or iterable, length N
        Second fuzzy membership vector.

    Returns
    -------
    R : 2D array
        Classic relation matrix defined as
            R = [A x B] U [(1 - A) x ones(1, N)],
        where x represents a cartesian product and N is len(`B`).

    """
    return np.fmax(cartprod(A, B), cartprod(1 - A, np.ones(len(B))))


def contrast(x, p, m=0.5):
    """
    General contrast booster or diffuser of membership vector x.

    Parameters
    ----------
    x : 1d array
        Fuzzy membership vector.
    p : float
        Positive scalar (norm of p taken to ensure this).
    m : float
        Scalar on range [0, 1].  Values below `m` decreased; values above `m`
        increased.

    Returns
    -------
    y : 1d array
        Resultant membership vector after contrast adjustment.

    Note
    ----
    Algorithm is defined as follows:

               | 2 ** (p - 1) * x ** p                 0 <= x <= m
        y(x) = |
               | 1 - 2 ** (p - 1) * (1 - x) ** p     m <= x <= 1.0

    See also
    --------
    INTENSE, DINTENSE

    """
    p = abs(p)
    y = np.zeros(x.shape)

    y[x <= m] = (2 ** (p - 1) * x ** p)[x <= m]
    y[x > m] = (1 - 2 ** (p - 1) * (1 - x) ** p)[x > m]

    return y


def fuzzy_add(x, A, y, B):
    """
    Adds fuzzy set A in universe x with fuzzy set B in universe y.

    Parameters
    ----------
    x : 1d array, length N
        Universe variable for fuzzy set A.
    A : 1d array, length N
        Fuzzy set for universe x.
    y : 1d array, length M
        Universe variable for fuzzy set B.
    B : 1d array, length M
        Fuzzy set for universe y.

    Returns
    -------
    z : 1d array
        Output variable.
    mfz : 1d array
        Fuzzy membership set for variable z.

    Note
    ----
    Uses Zadeh's Extension Principle as described in Ross, Fuzzy Logic with
    Engineering Applications (2010), pp. 414, Eq. 12.17.

    """
    # A and x, and B and y, are formed into (MxN) matrices.  The former has
    # identical rows; the latter identical identical columns.
    N = len(B)
    AA = np.dot(np.atleast_2d(A).T, np.ones((1, N)))
    X = np.dot(np.atleast_2d(x).T, np.ones((1, N)))
    M = len(A)
    BB = np.dot(np.ones((M, 1)), np.atleast_2d(B))
    Y = np.dot(np.ones((M, 1)), np.atleast_2d(y))

    # Actually do the addition
    Z = (X + Y).ravel()
    Z_index = np.argsort(Z)
    Z = np.sort(Z)

    # Array min() operation
    C = np.fmin(AA, BB).ravel()
    C = C[Z_index]

    # Initialize loop
    z, mfz = np.empty(0), np.empty(0)
    idx = 0

    for i in range(len(C)):
        index = np.nonzero(Z == Z[idx])[0]
        z = np.hstack((z, Z[idx]))
        mfz = np.hstack((mfz, C[index].max()))
        if Z[idx] == Z.max():
            break
        idx = index.max() + 1

    return z, mfz


def fuzzy_compare(Q):
    """
    Determines the comparison matrix, C, based on the fuzzy pairwise
    comparison matrix, Q, using Shimura's special relativity formula.

    Parameter
    ---------
    Q : 2d array, (N, N)
        Fuzzy pairwise comparison matrix.

    Returns
    -------
    C : 2d array, (N, N)
        Comparison matrix.

    """
    return Q.T / np.fmax(Q, Q.T).astype(np.float)


def fuzzy_div(x, A, y, B):
    """
    Divides fuzzy set B in universe y into fuzzy set A in universe X.

    Parameters
    ----------
    x : 1d array, length N
        Universe variable for fuzzy set A.
    A : 1d array, length N
        Fuzzy set for universe x.
    y : 1d array, length M
        Universe variable for fuzzy set B.
    B : 1d array, length M
        Fuzzy set for universe y.

    Returns
    -------
    z : 1d array
        Output variable.
    mfz : 1d array
        Fuzzy membership set for variable z.

    Note
    ----
    Uses Zadeh's Extension Principle from Ross, Fuzzy Logic w/Engineering
    Applications, (2010), pp.414, Eq. 12.17.

    """
    # A and x, and B and y, are formed into (MxN) matrices.  The former has
    # identical rows; the latter identical identical columns.
    N = len(B)
    AA = np.dot(np.atleast_2d(A).T, np.ones((1, N)))
    X = np.dot(np.atleast_2d(x).T, np.ones((1, N)))
    M = len(A)
    BB = np.dot(np.ones((M, 1)), np.atleast_2d(B))
    Y = np.dot(np.ones((M, 1)), np.atleast_2d(y))

    # Actually do the division (add eps to avoid div0 errors)
    Z = (X / (Y + np.finfo(float).eps)).ravel()
    Z_index = np.argsort(Z)
    Z = np.sort(Z)

    # Array min() operation
    C = np.fmin(AA, BB).ravel()
    C = C[Z_index]

    # Initialize loop
    z, mfz = np.empty(0), np.empty(0)
    idx = 0

    for i in range(len(C)):
        index = np.nonzero(Z == Z[idx])[0]
        z = np.hstack((z, Z[idx]))
        mfz = np.hstack((mfz, C[index].max()))
        if Z[idx] == Z.max():
            break
        idx = index.max() + 1

    return z, mfz


def fuzzy_min(x, A, y, B):
    """
    Finds minimum between fuzzy set A in universe x and fuzzy set B in
    universe y.

    Parameters
    ----------
    x : 1d array, length N
        Universe variable for fuzzy set A.
    A : 1d array, length N
        Fuzzy set for universe x.
    y : 1d array, length M
        Universe variable for fuzzy set B.
    B : 1d array, length M
        Fuzzy set for universe y.

    Returns
    -------
    z : 1d array
        Output variable.
    mfz : 1d array
        Fuzzy membership set for variable z.

    Note
    ----
    Uses Zadeh's Extension Principle from Ross, Fuzzy Logic w/Engineering
    Applications, (2010), pp.414, Eq. 12.17.

    """
    # A and x, and B and y, are formed into (MxN) matrices.  The former has
    # identical rows; the latter identical identical columns.
    N = len(B)
    AA = np.dot(np.atleast_2d(A).T, np.ones((1, N)))
    X = np.dot(np.atleast_2d(x).T, np.ones((1, N)))
    M = len(A)
    BB = np.dot(np.ones((M, 1)), np.atleast_2d(B))
    Y = np.dot(np.ones((M, 1)), np.atleast_2d(y))

    # Take the element-wise minimum
    Z = np.fmin(X, Y).ravel()
    Z_index = np.argsort(Z)
    Z = np.sort(Z)

    # Array min() operation
    C = np.fmin(AA, BB).ravel()
    C = C[Z_index]

    # Initialize loop
    z, mfz = np.empty(0), np.empty(0)
    idx = 0

    for i in range(len(C)):
        index = np.nonzero(Z == Z[idx])[0]
        z = np.hstack((z, Z[idx]))
        mfz = np.hstack((mfz, C[index].max()))
        if Z[idx] == Z.max():
            break
        idx = index.max() + 1

    return z, mfz


def fuzzy_mult(x, A, y, B):
    """
    Multiplies fuzzy set A in universe x and fuzzy set B in universe y.

    Parameters
    ----------
    x : 1d array, length N
        Universe variable for fuzzy set A.
    A : 1d array, length N
        Fuzzy set for universe x.
    y : 1d array, length M
        Universe variable for fuzzy set B.
    B : 1d array, length M
        Fuzzy set for universe y.

    Returns
    -------
    z : 1d array
        Output variable.
    mfz : 1d array
        Fuzzy membership set for variable z.

    Note
    ----
    Uses Zadeh's Extension Principle from Ross, Fuzzy Logic w/Engineering
    Applications, (2010), pp.414, Eq. 12.17.

    """
    # A and x, and B and y, are formed into (MxN) matrices.  The former has
    # identical rows; the latter identical identical columns.
    N = len(B)
    AA = np.dot(np.atleast_2d(A).T, np.ones((1, N)))
    X = np.dot(np.atleast_2d(x).T, np.ones((1, N)))
    M = len(A)
    BB = np.dot(np.ones((M, 1)), np.atleast_2d(B))
    Y = np.dot(np.ones((M, 1)), np.atleast_2d(y))

    # Take the element-wise minimum
    Z = (X * Y).ravel()
    Z_index = np.argsort(Z)
    Z = np.sort(Z)

    # Array min() operation
    C = np.fmin(AA, BB).ravel()
    C = C[Z_index]

    # Initialize loop
    z, mfz = np.empty(0), np.empty(0)
    idx = 0

    for i in range(len(C)):
        index = np.nonzero(Z == Z[idx])[0]
        z = np.hstack((z, Z[idx]))
        mfz = np.hstack((mfz, C[index].max()))
        if Z[idx] == Z.max():
            break
        idx = index.max() + 1

    return z, mfz


def fuzzy_sub(x, A, y, B):
    """
    Subtracts fuzzy set B in universe y into fuzzy set A in universe X.

    Parameters
    ----------
    x : 1d array, length N
        Universe variable for fuzzy set A.
    A : 1d array, length N
        Fuzzy set for universe x.
    y : 1d array, length M
        Universe variable for fuzzy set B.
    B : 1d array, length M
        Fuzzy set for universe y.

    Returns
    -------
    z : 1d array
        Output variable.
    mfz : 1d array
        Fuzzy membership set for variable z.

    Note
    ----
    Uses Zadeh's Extension Principle from Ross, Fuzzy Logic w/Engineering
    Applications, (2010), pp.414, Eq. 12.17.

    """
    # A and x, and B and y, are formed into (MxN) matrices.  The former has
    # identical rows; the latter identical identical columns.
    N = len(B)
    AA = np.dot(np.atleast_2d(A).T, np.ones((1, N)))
    X = np.dot(np.atleast_2d(x).T, np.ones((1, N)))
    M = len(A)
    BB = np.dot(np.ones((M, 1)), np.atleast_2d(B))
    Y = np.dot(np.ones((M, 1)), np.atleast_2d(y))

    # Actually do the division (add eps to avoid div0 errors)
    Z = (X - Y).ravel()
    Z_index = np.argsort(Z)
    Z = np.sort(Z)

    # Array min() operation
    C = np.fmin(AA, BB).ravel()
    C = C[Z_index]

    # Initialize loop
    z, mfz = np.empty(0), np.empty(0)
    idx = 0

    for i in range(len(C)):
        index = np.nonzero(Z == Z[idx])[0]
        z = np.hstack((z, Z[idx]))
        mfz = np.hstack((mfz, C[index].max()))
        if Z[idx] == Z.max():
            break
        idx = index.max() + 1

    return z, mfz


def inner_product(A, B):
    """
    Inner product (dot product) of two fuzzy sets.

    Parameters
    ----------
    A : 1d array or iterable
        Fuzzy membership function.
    B : 1d array or iterable
        Fuzzy membership function.

    Returns
    -------
    y : float
        Fuzzy inner product value, on range [0, 1]

    """
    return np.max(np.fmin(np.r_[A], np.r_[B]))


def interp10(x):
    """
    Utility function which conducts linear interpolation of any rank-1 array.
    Result will have 10x resolution.

    Parameters
    ----------
    x : 1d array, length N
        Input array to be interpolated.

    Returns
    -------
    y : 1d array, length 10 * N + 1
        Linearly interpolated output.

    """
    return np.interp(np.r_[0:len(x) - 0.9:0.1], range(len(x)), x)


def maxmin_composition(S, R):
    """
    Determines max-min composition `T` of fuzzy relation matrices `S` and `R`

    Parameters
    ----------
    S : 2d array, (M, N)
        Fuzzy relation matrix #1.
    R : 2d array, (N, P)
        Fuzzy relation matrix #2.

    Returns
    -------
    T ; 2d array, (M, P)
        Max-min composition, defined by T = S o R.

    """
    if S.ndim < 2:
        S = np.atleast_2d(S)
    if R.ndim < 2:
        R = np.atleast_2d(R).T
    M = S.shape[0]
    P = R.shape[1]
    T = np.zeros((M, P))

    for p in range(P):
        for m in range(M):
            T[m, p] = (np.fmin(S[m, :], R[:, p].T)).max()

    return T


def maxprod_composition(S, R):
    """
    Determines the max-product composition `T` of two fuzzy relation matrices

    Parameters
    ----------
    S : 2d array, (M, N)
        Fuzzy relation matrix #1.
    R : 2d array, (N, P)
        Fuzzy relation matrix #2.

    Returns
    -------
    T : 2d array, (M, P)
        max-product composition matrix.

    """
    if S.ndim < 2:
        S = np.atleast_2d(S)
    if R.ndim < 2:
        R = np.atleast_2d(R).T
    M = S.shape[0]
    P = R.shape[1]
    T = np.zeros((M, P))

    for m in range(M):
        for p in range(P):
            T[m, p] = (S[m, :] * R[:, p].T).max()

    return T


def interp_membership(x, xmf, xx):
    """
    Finds the degree of membership `u(xx)` for a given value of x = xx.

    Parameters
    ----------
    x : 1d array
        Independent discrete variable vector.
    xmf : 1d array
        Fuzzy membership function for x.  Same length as x.
    xx : float
        Discrete singleton value on universe X.

    Returns
    -------
    xxmf : float
        Membership function value at xx, `u(xx)`.

    Note
    ----
    For use in Fuzzy Logic, where an interpolated discrete membership function
    u(x) for discrete values of x on the universe of X is given. Then, assume
    that a new value x = xx, whose value does not correspond to any of the
    discrete values of x. The function computes the membership value u(xx)
    corresponding to the value xx using a linear interpolation.

    """
    # Nearest discrete x-values
    x1 = x[x <= xx][-1]
    x2 = x[x >= xx][0]

    idx1 = np.nonzero(x == x1)[0][0]
    idx2 = np.nonzero(x == x2)[0][0]

    xmf1 = xmf[idx1]
    xmf2 = xmf[idx2]

    if x1 == x2:
        xxmf = xmf[idx1]
    else:
        slope = (xmf2 - xmf1) / float(x2 - x1)
        xxmf = slope * (xx - x1) + xmf1

    return xxmf


def modus_ponens(A, B, Ap, C=None):
    """
    Generalized modus ponens deduction to make approximate reasoning in a
    rules-base system.

    Parameters
    ----------
    A : 1d array
        Fuzzy set A on universe X
    B : 1d array
        Fuzzy set B on universe Y
    Ap : 1d array
        New fuzzy fact A' (A prime, not transpose)
    C : 1d array, OPTIONAL
        Keyword argument (must be provided as `C=arrayname` in function call)
        which represents fuzzy set C on universe Y.
        Default = None, which will use a np.ones() array instead.

    Returns
    -------
    R : 2d array
        Full fuzzy relation.
    Bp : 1d array
        Fuzzy conclusion B' (B prime)

    """
    if C is None:
        C = np.ones(len(B))
    R = np.fmax(cartprod(A, B), cartprod(1 - A, C))
    Bp = maxmin_composition(Ap, R)
    return R, Bp.squeeze()


def outer_product(A, B):
    """
    Outer product of two fuzzy sets.

    Parameters
    ----------
    A : 1d array or iterable
        Fuzzy membership function.
    B : 1d array or iterable
        Fuzzy membership function.

    Returns
    -------
    y : float
        Fuzzy outer product value, on range [0, 1]

    """
    return np.min(np.fmax(np.r_[A], np.r_[B]))


def relation_min(A, B):
    """
    Determines fuzzy relation matrix `R` using Mamdani implication for the
    fuzzy antecedent `A` and consequent `B` inputs.

    Parameters
    ----------
    A : 1d array
        Fuzzy antecedent matrix.
    B : 1d array
        Fuzzy consequent matrix.

    Returns
    -------
    R : 2d array
        Fuzzy relation matrix.

    """
    m = len(A)
    n = len(B)
    A = np.atleast_2d(A)
    B = np.atleast_2d(B)
    return np.fmin(np.dot(A.T, np.ones((1, m))), np.dot(np.ones((n, 1)), B))


def relation_product(A, B):
    """
    Determines the fuzzy relation matrix, `R`, using product implication for
    the fuzzy antecedent `A` and the fuzzy consequent `B`.

    Parameters
    ----------
    A : 1d array, length M
        Fuzzy antecedent vector.
    B : 1d array, length N
        Fuzzy consequent vector.

    Returns
    -------
    R : 2d array, (M, N)
        Fuzzy relational matrix.

    """
    m = len(A)
    n = len(B)
    A = np.atleast_2d(A)
    B = np.atleast_2d(B)
    return np.dot(A.T, np.ones((1, n))) * np.dot(np.ones((m, 1)), B)


def fuzzy_similarity(Ai, B, mode='min'):
    """
    Calculates the fuzzy similarity between the fuzzy set Ai and observation
    fuzzy set B.

    Parameters
    ----------
    Ai : 1d array
        Fuzzy membership function of set Ai.
    B : 1d array
        Fuzzy membership function of set B.
    mode : string
        Controls the method of similarity calculation.
        * 'min' : Computed by array minimum operation.
        * 'avg' : Computed by taking the array average.

    Returns
    -------
    s : float
        Fuzzy similarity.

    """
    if 'min' in mode.lower():
        return min(inner_product(Ai, B), 1 - outer_product(Ai, B))
    else:
        return (inner_product(Ai, B) + (1 - outer_product(Ai, B))) / 2.
