# -*- coding: utf-8 -*-
"""
    Hedge functions, based on the definitions in the IEEE standard.
    Each function here maps a mf to a new mf.
    I'm following Annex A in IEEE 1855-2016, definintions A.1-A.13.
    @author: james.power@mu.ie Created on Wed Aug  1 14:14:46 2018
"""

# Each hedge takes a membership function and modifies it,
# returning a 'hedged' membership function of the same size.


import numpy as np

import skfuzzy.membership as skmemb

from skfuzzy.fcl.support import extramf


def above(mf):
    '''
    A.1: above(mf)=0 if x<x_max, 1-mf if x>= x_max

    Parameters
    ----------
    mf : 1d array of iterable, length N
        Fuzzy membership function.

    Returns
    -------
    new_mf : 1d array of iterable, length N
        An altered fuzzy membership function over the same universe.

    See Also
    --------
    extramf.below
    '''
    max_pos = np.argmax(mf)
    new_mf = 1 - mf
    new_mf[:max_pos] = 0
    return new_mf


def any_of(mf):
    '''
    A.2: any(mf) = 1.

    Parameters
    ----------
    mf : 1d array of iterable, length N
        Fuzzy membership function.

    Returns
    -------
    new_mf : 1d array of iterable, length N
        An altered fuzzy membership function over the same universe.

    Notes
    --------
    Should be called 'any', but this is a Python built-in.
    '''
    return np.ones_like(mf)


def below(mf):
    '''
    A.3: below(mf) = 0 if x>x_max, 1-mf(x) if x<x_max

    Parameters
    ----------
    mf : 1d array of iterable, length N
        Fuzzy membership function.

    Returns
    -------
    new_mf : 1d array of iterable, length N
        An altered fuzzy membership function over the same universe.

    See Also
    --------
    extramf.above
    '''
    max_pos = np.argmax(mf)
    new_mf = 1 - mf
    new_mf[max_pos:] = 0
    return new_mf


def extremely(mf):
    '''
    A.4: extremely(mf) = mf ** 3

    Parameters
    ----------
    mf : 1d array of iterable, length N
        Fuzzy membership function.

    Returns
    -------
    new_mf : 1d array of iterable, length N
        An altered fuzzy membership function over the same universe.
    '''
    return mf ** 3


def intensify(mf):
    '''
    A.5: 2*mf^2 if mf<0.5, 1-2*(1-mf)^2 otherwise

    Parameters
    ----------
    mf : 1d array of iterable, length N
        Fuzzy membership function.

    Returns
    -------
    new_mf : 1d array of iterable, length N
        An altered fuzzy membership function over the same universe.

    See Also
    --------
    extramf.seldom
    '''
    new_mf = np.zeros_like(mf)
    under, over = np.nonzero(mf <= 0.5), np.nonzero(mf > 0.5)
    new_mf[under] = 2 * (mf[under] ** 2)
    new_mf[over] = 1 - (2 * ((1 - mf[over]) ** 2))
    return new_mf


def more_or_less(mf):
    '''
    A.6: more_or_less(mf) = mf ^ 3

    Parameters
    ----------
    mf : 1d array of iterable, length N
        Fuzzy membership function.

    Returns
    -------
    new_mf : 1d array of iterable, length N
        An altered fuzzy membership function over the same universe.
    '''
    return mf ** (1/3)


def norm(mf):
    '''
    A.7:  norm divides all values by the maximum value.

    Parameters
    ----------
    mf : 1d array of iterable, length N
        Fuzzy membership function.

    Returns
    -------
    new_mf : 1d array of iterable, length N
        An altered fuzzy membership function over the same universe.
    '''
    return mf / mf.max()


def is_not(mf):
    '''
    A.8: not(mf) = 1-mf

    Parameters
    ----------
    mf : 1d array of iterable, length N
        Fuzzy membership function.

    Returns
    -------
    new_mf : 1d array of iterable, length N
        An altered fuzzy membership function over the same universe.

    Notes
    --------
    Should be called 'not', but this is a Python keyword.
    '''
    return 1 - mf


def plus(mf):
    '''
    A.9: plus(mf) = mf ^ (5/4)

    Parameters
    ----------
    mf : 1d array of iterable, length N
        Fuzzy membership function.

    Returns
    -------
    new_mf : 1d array of iterable, length N
        An altered fuzzy membership function over the same universe.
    '''
    return mf ** (5/4)


def seldom(mf):
    '''
    A.10: (mf/2)^(1/2) if mf<=0.5, and 1-((1-mf)/2)^(1/2) otherwise.

    Parameters
    ----------
    mf : 1d array of iterable, length N
        Fuzzy membership function.

    Returns
    -------
    new_mf : 1d array of iterable, length N
        An altered fuzzy membership function over the same universe.

    See Also
    --------
    extramf.intensify
    '''
    new_mf = np.zeros_like(mf)
    under, over = np.nonzero(mf <= 0.5), np.nonzero(mf > 0.5)
    new_mf[under] = np.sqrt(mf[under] / 2)
    new_mf[over] = 1 - np.sqrt((1 - mf[over]) / 2)
    return new_mf


def slightly(mf):
    '''
    A.11: Defined as: intensify [ norm (plus S AND not very S) ]

    Parameters
    ----------
    mf : 1d array of iterable, length N
        Fuzzy membership function.

    Returns
    -------
    new_mf : 1d array of iterable, length N
        An altered fuzzy membership function over the same universe.
    '''
    def min_and(x, y):
        ''' Let's implement AND as the elementwise min of two arrays'''
        return np.minimum.reduce([x, y])
    return intensify(norm(min_and(plus(mf), is_not(very(mf)))))


def somewhat(mf):
    '''
    A.12: somewhat(mf) = mf ^ (1/2)

    Parameters
    ----------
    mf : 1d array of iterable, length N
        Fuzzy membership function.

    Returns
    -------
    new_mf : 1d array of iterable, length N
        An altered fuzzy membership function over the same universe.
    '''
    return mf ** (1/2)


def very(mf):
    '''
    A.13: very(mf) = mf ^ 2

    Parameters
    ----------
    mf : 1d array of iterable, length N
        Fuzzy membership function.

    Returns
    -------
    new_mf : 1d array of iterable, length N
        An altered fuzzy membership function over the same universe.
    '''
    return mf ** 2


# List of all hedges, maps name to function
IEEE_HEDGES = {
    'above':        above,
    'any':          any_of,
    'below':        below,
    'extremely':    extremely,
    'intensify':    intensify,
    'more_or_less': more_or_less,
    'norm':         norm,
    'not':          is_not,
    'plus':         plus,
    'seldom':       seldom,
    'slightly':     slightly,
    'somewhat':     somewhat,
    'very':         very,
}


def test_all_hedges(origmf):
    '''
    Apply all the hedge functions to origmf, and then plot them.
    '''
    for mfname, yvals in origmf.items():
        results = []
        hedgenames = sorted(IEEE_HEDGES.keys())  # alphabetical order
        for name in hedgenames:
            func = IEEE_HEDGES[name]
            results.append(func(yvals))
        extramf.visualise_all(x, [yvals]+results,
                              ['original ({})'.format(mfname)]+hedgenames)


if __name__ == '__main__':
    x = np.arange(0, 100)
    # Some initial membership functions to test the hedges on:
    origmf = {
        'gaussian': skmemb.gaussmf(x, 50, 15),
        's': skmemb.smf(x, -10, 140),
    }
    test_all_hedges(origmf)
