"""
control.py : Examples of fuzzy logic control systems.

"""

import numpy as np

try:
    import matplotlib.pyplot as plt
    can_plot = True
except:
    import warnings
    warnings.warn("""This system appears to be built without matplotlib.
    Automatic plotting will be disabled. For visualization of results, install
    matplotlib with `$ sudo pip install matplotlib` or continue and use your
    visualization package of choice to display control function outputs.
    """)
    can_plot = False

from ..defuzzify import centroid
from ..fuzzymath import continuous_to_discrete
from ..membership import trimf, trapmf


def _roundoff_error(exact, test_arr):
    out = np.zeros_like(test_arr)

    if exact == 0.:
        zero_mask = np.ones(test_arr.shape, dtype=np.bool)
        return abs(exact + test_arr)

    else:
        zero_mask = test_arr == 0.

        out[zero_mask] = abs(exact + test_arr[zero_mask])

        zero_mask = np.logical_not(zero_mask)
        out[zero_mask] = abs(test_arr / exact - 1.0)

        return out


def _float_equal(float1, arr2, epsilon=2.0e-9):
    float1_tmp = float1.astype(float)
    arr2_tmp = arr2.astype(float)
    return (_roundoff_error(float1_tmp, arr2_tmp) < epsilon)


def fcontrol(x1, M1, x2, M2, u, Mu, rules, x10, x20, K, Ts, N, A=None, B=None,
             Phi=None, Gamma=None, plot=True):
    """
    Fuzzy control of a plant with two input variables and one output variable.

    Parameters
    ----------
    x1 : 1d array, length N
        Fuzzy state variable #1.
    M1 : 2d array, shape (Q1, N)
        Matrix with Q1 membership functions for x1.
    x2 : 1d array, length M
        Fuzzy state variable #2.
    M2 : 2d array, shape (Q2, M)
        Matrix with Q2 membership functions for x2.
    u : 1d array, length U
        Feedback control action variable.
    Mu : 2d array, shape (Qu, U)
        Matrix containing Qu membership functions for control u.
    rules : 2d array, shape (Q, 3)
        Indices of Q fuzzy control rules.  Format: [x1, x2, u]
    x10 : float
        Initial condition for variable x1
    x20 : float
        Initial condition for variable x2
    K : float
        Output gain adjustment
    Ts : float
        Sampling period (in seconds)
    N : int
        Number of samples
    A : 2d array, shape (2, 2)
        Optional keyword argument. Continuous system matrix.
    B : 2d array, shape (2, 1)
        Optional keyword argument. Continuous input matrix.
    Phi : 2d array, shape (2, 2)
        Optional keyword argument. Discrete systm matrix.
    Gamma : 2d array, shape (2, 1)
        Optional keyword argument. Discrete input matrix.
    plot : bool, default = True
        Optional keyword argument. Toggles plotting of function results.

    Returns
    -------
    xx1 : 1d array, length N
        Crisp state variable x1
    xx2 : 1d array, length N
        Crisp state variable x2
    uu : 1d array, length N
        Corresponding control action
    tt : 1d array, length N
        Discrete time index (sec)

    Note
    ----
    While A, B, Phi, and Gamma are all technically optional kwargs, this
    function REQUIRES at one of the two pairs of arguments. Either BOTH A
    AND B are passed, OR BOTH Phi AND Gamma must be passed to define the
    system.

    In the event that all four are provided, A and B will be ignored in
    favor of Phi and Gamma.

    """

    if Phi is None and Gamma is None:
        assert A is not None and B is not None, 'If Phi and Gamma are not \
                                                 provided, both A and B \
                                                 must be!'
        # Continuous-time to discrete-time conversion
        Phi, Gamma = continuous_to_discrete(A, B, Ts)

    # Initial conditions and setup
    xx1, xx2 = x10, x20
    uu = np.zeros((1, N))
    xxx = np.vstack((x10, x20))

    Kp1 = np.abs(1. / (x1[1] - x1[0]))
    Kp2 = np.abs(1. / (x2[1] - x2[0]))

    tt = Ts * np.arange(N + 1)

    # Fuzzy logic controller loop
    for ii in range(N):
        # Firing members in M1
        xxx1 = M1[:, x1 == ((Kp1 * xxx[0, 0]).round() / Kp1).round()][0]
        # Firing members in M2
        xxx2 = M2[:, x2 == ((Kp2 * xxx[1, 0]).round() / Kp2).round()][0]

        # Indices of firing members of M1 & M2
        i1 = np.nonzero(xxx1 > 1e-6)[0]
        i2 = np.nonzero(xxx2 > 1e-6)[0]

        # Find truncated output membership (Mamdani) values & aggregation of
        # the union
        mu = np.zeros((1, len(u)))
        for jj in range(len(i1)):
            for kk in range(len(i2)):
                r = rules[np.logical_and(rules[:, 0] == i1[jj],
                                         rules[:, 1] == i2[kk]), 2]
                mm = np.fmin(xxx1[i1[jj], 0], xxx2[i2[kk], 0])
                mu = np.fmax(mu, np.fmin(mm, Mu[r, :]))

        # Defuzzify w/centroid method
        uu[ii] = K * centroid(u, mu)

        # Update time for discrete linearized inverting pendulum model
        xxx = Phi.dot(xxx) + Gamma.dot(uu[ii])
        xx1[ii + 1] = xxx[0, 0]
        xx2[ii + 1] = xxx[1, 0]

    uu = np.hstack((0, uu))
    uu = uu[np.arange(len(tt))]

    if plot and can_plot:
        # Create the plots.
        fig, ax = plt.subplots(ncols=1, nrows=3)
        ax[0].plot(tt, xx1, 'k')
        ax[0].grid()
        ax[0].axis([0, tt.max(), xx1.min(), xx1.max()])
        ax[0].set_xlabel('Time, t (sec)')
        ax[0].set_ylabel('Position x_1')
        ax[0].set_title('Position')
        ax[1].plot(tt, xx2, 'k')
        ax[1].grid()
        ax[1].axis([0, tt.max(), xx2.min(), xx2.max()])
        ax[1].set_xlabel('Time, t (sec)')
        ax[1].set_ylabel('Velocity x_1')
        ax[1].set_title('Velocity')
        ax[2].plot(tt, uu, 'k')
        ax[2].grid()
        ax[2].axis([0, tt.max(), 0, uu.max()])
        ax[2].set_xlabel('Time, t (sec)')
        ax[2].set_ylabel('Control u')
        ax[2].set_title('Fuzzy logic control action u')
        fig.suptitle('Simulation.  Gain K = ' + str(K))

        plt.show()

    return xx1, xx2, uu, tt


def inv_pen(x1, M1, x2, M2, u, Mu, rules, x10, x20, K):
    """
    Fuzzy control of an inverted pendulum.

    Parameters
    ----------
    x1 : 1d array, length N
        Angle of inverted pendulum relative to perpendicular.
    M1 : 2d array, shape (m1, N)
        Matrix with m1 membership functions for x1.
    x2 : 1d array, length M
        Angular velocity of inverted pendulum.
    M2 : 2d array, shape (m2, M)
        Matrix with m2 membership functions for x2.
    u : 1d array, length U
        Feedback control variable.
    Mu : 2d array, shape (mu, U)
        Matrix containing mu membership functions for control u.
    rules : 2d array, shape (M, 3)
        Indices of M fuzzy control rules.  Format: [x1, x2, u]
    x10 : float
        Initial condition for variable x1
    x20 : float
        Initial condition for variable x2
    K : float
        Output gain adjustment

    Returns
    -------
    xx1 : 1d array, length N
        Angle of inverted pendulum.
    xx2 : 1d array, length N
        Angular velocity of inverted pendulum.
    uu : 1d array, length N
        Control action.
    tt : 1d array, length N
        Discrete time index (sec).

    Note
    ----
    This models the discrete-time model of an inverted pendulum, defined:

        x[k + 1] = Phi * x[k] + Gamma * u[k]
        x[k] = [x1[k], x2[k]].T

    """
    Phi = np.ones((2, 2))
    Gamma = np.atleast_2d(np.r_[0, -1]).T

    # Initial conditions
    xxx = np.hstack((x10, x20)).T
    xx1, xx2 = x10, x20

    K1 = np.abs(1. / (x1[1] - x1[0]))
    K2 = np.abs(1. / (x2[1] - x2[0]))
    uu = np.zeros((1, 25))
    tt = np.arange(26)

    # Consider first 25 time samples
    for ii in range(25):
        # Firing members in M1 and M2
        xxx1 = M1[:,
            _float_equal(np.round(np.round(K1 * xxx[0, 0]) / float(K1)), x1)]
        xxx2 = M2[:,
            _float_equal(np.round(np.round(K2 * xxx[1, 0]) / float(K2)), x2)]

        # Determine indices for firing members
        i1 = np.nonzero(xxx1 > 1e-6)[0]
        i2 = np.nonzero(xxx2 > 1e-6)[0]

        # Truncated output membership (Mamdani) values & aggregation of union
        mu = np.zeros((1, len(u)))

        for jj in range(len(i1)):
            for kk in range(len(i2)):
                r = rules[np.logical_and(rules[:, 0] == i1[jj],
                                         rules[:, 1] == i2[kk]), 2]
                mm = np.fmin(xxx1[i1[jj], 0], xxx2[i2[kk], 0])
                mu = np.fmax(mu, np.fmin(mm, Mu[r, :]))

        # Defuzzify using centroid method
        uu[0, ii] = K * centroid(u, mu)

        # Update time step in model
        xxx = Phi.dot(xxx) + Gamma.dot(uu[:, ii].reshape(1, -1))
        xx1 = np.hstack((xx1, xxx[0, 0]))
        xx2 = np.hstack((xx2, xxx[1, 0]))

    uu = np.hstack((0, uu[0, :]))
    uu = uu[np.arange(1, len(tt))]

    return xx1, xx2, uu[:25], range(25)


def inv_pend(x10, x20, K, Ts, N, plot=True):
    """
    Another inverted pendulum control problem, using correct discrete-time
    model.

    Parameters
    ----------
    x10 : float
        Initial condition for angular position.
    x20 : float
        Initial condition for angular velocity.
    K : float
        Output gain adjustment
    Ts : float
        Sampling period (sec)
    N : int
        Number of samples in Ts.

    Returns
    -------
    xx1 : 1d array
        Angle of inverted pendulum
    xx2 : 1d array
        Angular velocity of inverted pendulum.
    uu : 1d array
        Control action.
    tt : 1d array
        Discrete time index (sec)

    Note
    ----
    This function uses hardcoded values to set up the problem.

    See Ex. 13.2, Ross, Fuzzy Logic w/Engineering Applications, 1st ed,
    pp. 483 - 490.

    """
    # Initial values for x1, N1, Z1, P1, M1, and X2, N1, etc.
    x1 = np.arange(-10, 10.1, 0.1)        # Angle range
    N1 = trapmf(x1, [-10, -10, -2, 0])    # `Negative` membership function
    Z1 = trimf(x1, [-2, 0, 2])            # `Zero` membership function
    P1 = trapmf(x1, [0, 2, 10, 10])       # `Positive` membership function

    x2 = np.arange(-10, 10.1, 0.1)        # Angular velocity range
    N2 = trapmf(x2, [-10, -10, -2, 0])    # `Negative` membership function
    Z2 = trimf(x2, [-2, 0, 2])            # `Zero` membership function
    P2 = trapmf(x2, [0, 2, 10, 10])       # `Positive` membership function

    M1 = np.vstack((N1, Z1, P1))          # (3 x 201) membership matrix
    M2 = np.vstack((N2, Z2, P2))          # (3 x 201) membership matrix

    # Fuzzy control output variable `u` and its membership functions
    u = np.arange(-25, 25.25, 0.25)
    NBu = trapmf(u, [-25, -25, -16, -8])  # `Big Negative` membership function
    Nu = trimf(u, [-16, -8, 0])           # `Negative` membership function
    Zu = trimf(u, [-8, 0, 8])             # `Zero` membership function
    Pu = trimf(u, [0, 8, 16])             # `Positive` membership function
    PBu = trapmf(u, [8, 16, 25, 25])      # `Big Positive` membership function

    Mu = np.vstack((NBu, Nu, Zu, Pu, PBu))  # (5 x 201) membership matrix

    # Define rulebase & indexing of membership matrices M1, M2, and Mu
    # Also known as Fuzzy Associated Memory (FAM)
    rules = np.r_[[[0, 0, 0],
                   [0, 1, 1],
                   [0, 2, 2],
                   [1, 0, 1],
                   [1, 1, 2],
                   [1, 2, 3],
                   [2, 0, 2],
                   [2, 1, 3],
                   [2, 2, 4]]]

    # Define continuous space system
    A = np.r_[[[0, 1],
               [1, 0]]]
    B = np.r_[[[0], [-np.pi / 180.]]]

    # Convert to discrete-time system
    Phi, Gamma = continuous_to_discrete(A, B, Ts)

    xx1, xx2 = x10, x20
    uu = np.zeros((1, N))
    xxx = np.vstack((x10, x20))

    # K1 and K2 found for scaling
    K1 = np.abs(1. / (x1[1] - x1[0]))
    K2 = np.abs(1. / (x2[1] - x2[0]))

    # Consider first N time samples
    tt = Ts * np.arange(N + 1)
    for ii in range(N):
        # Firing members in M1 and M2
        xxx1 = M1[:,
            _float_equal(np.round(np.round(K1 * xxx[0, 0]) / float(K1)), x1)]
        xxx2 = M2[:,
            _float_equal(np.round(np.round(K2 * xxx[1, 0]) / float(K2)), x2)]

        # Determine indices for firing members
        i1 = np.nonzero(xxx1 > 1e-6)[0]
        i2 = np.nonzero(xxx2 > 1e-6)[0]

        # Truncated output membership (Mamdani) values & aggregation of union
        mu = np.zeros((1, len(u)))

        for jj in range(len(i1)):
            for kk in range(len(i2)):
                r = rules[np.logical_and(rules[:, 0] == i1[jj],
                                         rules[:, 1] == i2[kk]), 2]
                mm = np.fmin(xxx1[i1[jj], 0],
                             xxx2[i2[kk], 0])
                mu = np.fmax(mu, np.fmin(mm, Mu[r, :]))

        # Defuzzify using centroid method
        uu[0, ii] = K * centroid(u, mu)

        # Update time step in model
        xxx = Phi.dot(xxx) + Gamma.dot(uu[:, ii].reshape(1, -1))
        xx1 = np.hstack((xx1, xxx[0, 0]))
        xx2 = np.hstack((xx2, xxx[1, 0]))

    uu = np.hstack((0, uu[0, :]))
    uu = uu[np.arange(len(tt))]

    if plot and can_plot:
        # Create the plots.
        fig, ax = plt.subplots(ncols=1, nrows=2)
        ax[0].plot(tt, xx1, 'k', tt, xx2, '--k', 0, 1, 'ok', 0, -4, 'ok')
        ax[0].grid()
        ax[0].axis([0, tt.max(), min(xx1.min(), xx2.min()),
                    max(xx1.max(), xx2.max())])
        ax[0].set_xlabel('Time, t (sec)')
        ax[0].set_ylabel('Angular position x_1  &  angular velocity x_2')
        ax[0].set_title('Angular position and velocity of inverted pendulum')
        ax[1].plot(tt, uu, 'k')
        ax[1].grid()
        ax[1].axis([0, tt.max(), 0, uu.max()])
        ax[1].set_xlabel('Time, t (sec)')
        ax[1].set_ylabel('Control u')
        ax[1].set_title('Fuzzy logic control action for inverted pendulum')
        fig.suptitle('Inverted Pendulum Simulation.  Gain K = ' + str(K))

        plt.show()

    return xx1, xx2, uu[:len(tt)], tt
