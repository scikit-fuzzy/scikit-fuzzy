# -*- coding: utf-8 -*-
"""
    Some extra membership functions to augment those in skfuzzy.membership
    @author: james.power@mu.ie Created on Fri Jul 27 16:10:03 2018
"""
from collections import OrderedDict

import numpy as np

import skfuzzy
import skfuzzy.membership as skmemb
import scipy.interpolate as interp


def singletonmf(x, xpt):
    '''
    Find which x-val is nearest the given point, and set it to 1.

    Parameters
    ----------
    x : 1d array
        Input sequence.
    xpt : float
        Value in input array with membership of 1.

    Returns
    -------
    y : 1d array
        Membership with the point nearest x set to 1, all others 0
    '''
    mf = np.zeros(len(x))
    diffs = np.abs(x - xpt)
    idx = np.nonzero(diffs == diffs.min())[0][0]
    mf[idx] = 1
    return mf


def pointsetmf(x, pointset, method='linear'):
    '''
    Interpolate from a point-set using the chosen interpolation method.

    Parameters
    ----------
    x : 1d array
        Input sequence.
    pointset : list of (float, float) pairs
        These are the (x,y) co-ordinates of points on the function.
    method : string
        Controls which interpolation method will be used.
        * 'linear': linear 1-D interpolation, see scipy.interpolate.interp1d
        * 'lagrange': lagrange, see scipy.interpolate.lagrange
        * 'spline': B-spline, see scipy.interpolate.make_interp_spline
        * 'cubic': Cubic spline, see scipy.interpolate.CubicSpline

    Returns
    -------
    y : 1d array
        Membership with the points plotted as given; clipped to (0,1) interval.

    Notes
    -----
    Since this calls the corresponding scipy interpolitaion function,
    the actual meaning of the points are interpreted by that function.
    '''
    # Make sure we're in ascending order first:
    pointset = sorted(pointset, key=lambda p: p[0])
    x_min, x_max = x[0], x[-1]
    # Lead on left from y=0, unless otherwise specified:
    if pointset[0][0] > x_min:
        pointset = [(x_min, 0)] + pointset
    # Trail on right from last given y value
    if pointset[-1][0] < x_max:
        pointset = pointset + [(x_max, pointset[-1][1])]
    px, py = [p[0] for p in pointset], [p[1] for p in pointset]
    if method == 'linear':
        f = interp.interp1d(px, py)
    elif method == 'lagrange':
        f = interp.lagrange(px, py)
    elif method == 'spline':
        f = interp.make_interp_spline(px, py)
    elif method == 'cubic':
        f = interp.CubicSpline(px, py, bc_type='natural')
    # Sometimes interpoliation can go outside the bounds:
    return np.clip(f(x), 0, 1)


def gaussprod(x, mean1, sigma1, mean2, sigma2):
    '''
    Product of two Gaussians, BUT ensure the means are in the correct order.

    Parameters
    ----------
    x : 1d array or iterable
        Independent variable.
    mean1 : float
        Gaussian parameter for center (mean) value of the first Gaussian.
    sigma1 : float
        Standard deviation of the first Gaussian.
    mean2 : float
        Gaussian parameter for center (mean) value of the second Gaussian.
    sigma2 : float
        Standard deviation of the second Gaussian.

    Returns
    -------
    y : 1d array
        Membership function with left side up to `mean1` defined by the first
        Gaussian, and the right side above `mean2` defined by the second.
        In the range mean1 <= x <= mean2 the function has value = 1.

    Notes:
    ------
    This is just a wrapper for gauss2mf that swaps the parameters if needed.
    '''
    if mean1 > mean2:
        mean1, sigma1, mean2, sigma2 = mean2, sigma2, mean1, sigma1
    return skmemb.gauss2mf(x, mean1, sigma1, mean2, sigma2)


def rectanglemf(x, a, b):
    '''
    Zero before and after given points, one in between them.

    Parameters
    ----------
    x : 1d array
        Independent variable.
    a : float
        Left 'foot', where the function goes directly from zero to one.
    b : float
        Right 'foot', where the function goes directly from one to zero.

    Returns
    -------
    y : 1d array
        Rectangular function.
    '''
    mf = np.ones(len(x))
    mf[np.nonzero(x < a)] = 0
    mf[np.nonzero(x > b)] = 0
    return mf


def leftlinearmf(x, a, b):
    '''
    One to the left, zero to the right, slope down in-between

    Parameters
    ----------
    x : 1d array
        Independent variable.
    a : float
        Left 'ceiling', where the function begins to slope down from one.
    b : float
        Right 'foot', where the function reaches zero.

    Returns
    -------
    y : 1d array
        Left linear function, negative slope.
    '''
    mf = np.ones(len(x))
    midpts = np.nonzero(np.logical_and(a < x, x < b))
    mf[midpts] = (((b - x[midpts]) / (b - a)))
    mf[np.nonzero(x >= b)] = 0
    return mf


def rightlinearmf(x, a, b):
    '''
    Zero to the left, one to the right, slope up in-between.

    Parameters
    ----------
    x : 1d array
        Independent variable.
    a : float
        Left 'foot', where the function begins to slope up from zero.
    b : float
        Right 'ceiling', where the function reaches one.

    Returns
    -------
    y : 1d array
        Right linear function, positive slope.
    '''
    mf = np.zeros(len(x))
    midpts = np.nonzero(np.logical_and(a < x, x < b))
    mf[midpts] = 1 - (((b - x[midpts]) / (b - a)))
    mf[np.nonzero(x >= b)] = 1
    return mf


def rampmf(x, a, b):
    '''
    A line from a up/down to b (depending on the order of a and b).

    Parameters
    ----------
    x : 1d array
        Independent variable.
    a : float
        the 'foot' (y=0), if a<b then on left, else on right.
    b : float
        the 'ceiling' (y=1), if a<b then on right, else on left.

    Returns
    -------
    y : 1d array
        Membership function with positive or negative slope.

    Notes
    -----
    This just selects either a right- or left-linear function.
    '''
    if a < b:
        return rightlinearmf(x, a, b)
    elif a > b:
        return leftlinearmf(x, b, a)
    else:  # a == b
        return np.zeros(len(x))


def cosinemf(x, center, width):
    '''
    A cosine curve distributed about the center with the given width.

    Parameters
    ----------
    x : 1d array
        Independent variable.
    center : float
        the mid point of the curve; function is one here.
    width : float
        the amount left/right of midpoint for curve to slope to zero.

    Returns
    -------
    y : 1d array
        Cosine function, clipped between center +/- width, scaled 0<=y<=1.
    '''
    mf = np.zeros(len(x))
    # Only plot the curve within the given width either side the center:
    midpts = np.nonzero(np.logical_and(center - 0.5 * width <= x,
                                       x <= center + 0.5 * width))
    to_angle = 2.0 * np.pi / width
    mf[midpts] = (0.5 * (1.0 + np.cos(to_angle * (x[midpts] - center))))
    return mf


def concavemf(x, infl, end):
    '''
    A curve rising/falling to end point, bent according to inflexion pt.

    Parameters
    ----------
    x : 1d array
        Independent variable.
    infl : float
        the inflection point (x-value), controlling the slope of the curve
    end : float
        the end point (x-value) of the curve, where it reaches one.

    Returns
    -------
    y : 1d array
        Concave function, increasing/decreasing depending on parameter order.
    '''
    mf = np.ones(len(x))
    if infl <= end:  # Concave increasing
        incpts = np.nonzero(x < end)
        mf[incpts] = (end - infl) / (2.0 * end - infl - x[incpts])
    else:   # Concave decreasing
        decpts = np.nonzero(x > end)
        mf[decpts] = (infl - end) / (infl - 2.0 * end + x[decpts])
    return mf


def leftgaussmf(x, mean, sigma):
    '''
    Like Gaussian, but always 1 when <= mean (so, slopes down only).

    Parameters
    ----------
    x : 1d array
        Independent variable.
    mean : float
        Gaussian parameter for center (mean) value.
    sigma : float
        Gaussian parameter for standard deviation.

    Returns
    -------
    y : 1d array
        Gaussian, but with all left side set to one.
    '''
    mf = skmemb.gaussmf(x, mean, sigma)
    mf[np.nonzero(x <= mean)] = 1
    return mf


def rightgaussmf(x, mean, sigma):
    '''
    Like Gaussian, but always 1 when >= mean (so, slopes up only).

    Parameters
    ----------
    x : 1d array
        Independent variable.
    mean : float
        Gaussian parameter for center (mean) value.
    sigma : float
        Gaussian parameter for standard deviation.

    Returns
    -------
    y : 1d array
        Gaussian, but with all right side set to one.
    '''
    mf = skmemb.gaussmf(x, mean, sigma)
    mf[np.nonzero(x >= mean)] = 1
    return mf


def spikemf(x, center, width):
    '''
    A symmetrical curved (exp) spike centered at the given location.

    Parameters
    ----------
    x : 1d array
        Independent variable.
    center : float
        The center (x-value) of the curve where it peaks at one.
    width : float
        The amount either side for the slop down to zero.

    Returns
    -------
    y : 1d array
        Membership function for a spiked curve peaking at the given point.
    '''
    return np.exp(-np.abs(10.0 / width * (x - center)))


def jfl_sigmf(x, gain, center):
    '''
    Like sigmf, but jFuzzyLogic supplies parameters in a different order.

    Parameters
    ----------
    x : 1d array
        Data vector for independent variable.
    b : float
        Offset or bias.  This is the center value of the sigmoid, where it
        equals 1/2.
    c : float
        Controls 'width' of the sigmoidal region about `b` (magnitude).

    Returns
    -------
    y : 1d array
        Generated sigmoid values

    Notes
    -----
    This is just a wrapper for the skfuzzy sigmf function.
    '''
    return skmemb.sigmf(x, center, gain)


def fl_bellmf(x, center, width, slope):
    '''
    Like gbellmf, but fuzzylite supplies parameters in a different order.

    Parameters
    ----------
    x : 1d array
        Independent variable.
    a : float
        Bell function parameter controlling width.
    b : float
        Bell function parameter controlling slope.
    c : float
        Bell function parameter defining the center.

    Returns
    -------
    y : 1d array
        Generalized Bell fuzzy membership function.

    Notes
    -----
    This is just a wrapper for the skfuzzy gbellmf function.
    '''
    return skmemb.gbellmf(x, width, slope, center)


# ### Sanity check: plot some examples of the membership functions

import matplotlib.pyplot as plt


def visualise_all(x, y_list, titles, ncols=3):
    '''
        Just display the given plot-data on a grid of separate graphs.
        Also show the centroid as a vertical red line.
    '''
    nrows = np.int(np.ceil(len(y_list) / ncols))
    fig, axes = plt.subplots(nrows=nrows, ncols=ncols, figsize=(8, 9))
    fig.tight_layout()
    fig.subplots_adjust(bottom=-.25)
    for i, p in enumerate(y_list):
        r, c = divmod(i, ncols)
        axes[r][c].plot(x, p)
        cog = skfuzzy.centroid(x, p)
        axes[r][c].axvline(x=cog, color='red', linestyle='--')
        axes[r][c].set_title(titles[i])
        axes[r][c].set_ylim([-0.05, 1.05])  # so all have the same (0,1) y-axis
    fig.show()


def _plot_mf_for(x):
    '''Given the x-values, plot a series of example membership functions'''
    tests = OrderedDict([
        # Gaussians:
        ('gauss', skmemb.gaussmf(x, 50, 10)),
        ('left gauss', leftgaussmf(x, 50, 10)),
        ('right gauss', rightgaussmf(x, 50, 10)),
        # Triangles:
        ('triangular', skmemb.trimf(x, [25, 50, 75])),
        ('left linear', leftlinearmf(x, 25, 75)),
        ('right linear', rightlinearmf(x, 25, 75)),
        # fuzzylite:
        ('cosine', cosinemf(x, 50, 50)),
        ('inc concave', concavemf(x, 50, 75)),
        ('dec concave', concavemf(x, 50, 25)),
        ('spike', spikemf(x, 50, 50)),
        ('inc ramp', rampmf(x, 25, 75)),
        ('dec ramp', rampmf(x, 75, 25)),
        # Rectangle-ish
        ('trapezoid', skmemb.trapmf(x, [20, 40, 60, 80])),
        ('rectangle', rectanglemf(x, 25, 75)),
        ('singleton', singletonmf(x, 50)),
    ])
    # Example point sets:
    ps_tests = [
        [(40, 0.5), (60, 1)],
        [(10, 0.5), (25, 0.25), (40, 0.75), (80, .5)],
        [(0, 1), (40, 0.25), (50, .5), (99, 0)]
    ]
    # Now try some interpolation methods on these:
    for method in ['linear', 'lagrange', 'spline', 'cubic']:
        tests.update([('{} ex{}'.format(method, i), pointsetmf(x, ps, method))
                      for i, ps in enumerate(ps_tests)])
    return tests


if __name__ == '__main__':
    x = np.arange(0, 100)
    plots = _plot_mf_for(x)
    visualise_all(x, plots.values(), list(plots.keys()))
