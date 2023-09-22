# -*- coding: utf-8 -*-
'''
    Norms and co-norms based on the definitions in the IEEE standard.
    Each function here returns a FuzzyAggregationMethods object,
    which is really just a pair of functions: (and_func, or_func).
    I'm following Annex A in IEEE 1855-2016, definintions A.14-A.27.
    @author: james.power@mu.ie Created on Fri Aug 10 12:48:30 2018
'''


import numpy as np
from skfuzzy.control.term import FuzzyAggregationMethods


''' Reminder of what's in term.py:
    class FuzzyAggregationMethods(object):
        def __init__(self, and_func=np.fmin, or_func=np.fmax):
            self.and_func = and_func
            self.or_func = or_func
'''


def _fam_vectorise(and_func, or_func):
    '''
    Vectorise an and/or function pair; return a FuzzyAggregationMethods.
    Make sure the function names are propoagated to the resulting object.
    '''
    fam = FuzzyAggregationMethods(np.vectorize(and_func),
                                  np.vectorize(or_func))
    fam.and_func.__name__ = and_func.__name__
    fam.or_func.__name__ = or_func.__name__
    return fam


# This is the default:
# A.14: minimum t-norm, A.21: maximum t-conorm
MIN_MAX = FuzzyAggregationMethods(np.fmin, np.fmax)


def ps_prod_and(a, b):
    '''A.15: product t-norm'''
    return a*b


def ps_sum_or(a, b):
    '''A.21: Probabilistic sum t-conorm'''
    return a+b - (a*b)


PRODUCT_SUM = FuzzyAggregationMethods(ps_prod_and, ps_sum_or)


def bounded_and(a, b):
    'A.16: bounded difference t-norm'
    return np.fmax(0, a+b - 1)


def bounded_or(a, b):
    'A.22: bounded sum t-conorm'
    return np.fmin(1, a+b)


BOUNDED = FuzzyAggregationMethods(bounded_and, bounded_or)


'''This is just a synonym for bounded'''
LUCASIEWICZ = BOUNDED


def drastic_and(a, b):
    'A.17: drastic product t-norm'
    if a == 1:
        return b
    elif b == 1:
        return a
    else:
        return 0


def drastic_or(a, b):
    'A.23: drastic sum t-conorm'
    if a == 0:
        return b
    elif b == 0:
        return a
    else:
        return 1

DRASTIC = _fam_vectorise(drastic_and, drastic_or)


def einstein_and(a, b):
    'A.18: Einstein product t-norm'
    return (a*b) / (2 - (a+b - a*b))


def einstein_or(a, b):
    'A.24: Einstein sum t-conorm'
    return (a+b) / (1 + a*b)


EINSTEIN = FuzzyAggregationMethods(einstein_and, einstein_or)


# Denoninator is wrong in A.19 whihc says: ((a+b) / ((a+b) - a*b))
def hamacher_and(a, b):
    '''A.19: Hamacher product t-norm; added divide-by-zero check'''
    if a == b == 0:
        return 0.0
    else:
        return (a*b) / ((a+b) - a*b)


def hamacher_or(a, b):
    'A.25: Hamacher sum t-conorm; added divide-by-zero check'
    if a == b == 1:
        return 1.0
    else:
        return (a+b - 2*a*b) / (1 - a*b)


HAMACHER = _fam_vectorise(hamacher_and, hamacher_or)


def nilpotent_and(a, b):
    'A.20: Nilpotent minum t-norm'
    if a+b > 1:
        return np.fmin(a, b)
    else:
        return 0.0


def nilpotent_or(a, b):
    'A.26: Nilpotent maximum t-conorm'
    if a+b < 1:
        return np.fmax(a, b)
    else:
        return 1.0


NILPOTENT = _fam_vectorise(nilpotent_and, nilpotent_or)


_IEEE_NORMS = {
    'Min/Max': MIN_MAX,
    'Prod/Sum': PRODUCT_SUM,
    'Bounded': BOUNDED,
    'Drastic': DRASTIC,
    'Einstein': EINSTEIN,
    'Hamacher': HAMACHER,
    'Nilpotent': NILPOTENT,
}


# ################# ###
# ### Test routines ###
# ################# ###

import matplotlib.pyplot as plt
import skfuzzy.membership as skmemb


def visualise_all(x, y1, y2, all_norms=_IEEE_NORMS):
    '''Plot the norm and conorm for the given sample inputs'''
    ncols = 3
    fig, axes = plt.subplots(nrows=len(all_norms), ncols=ncols, figsize=(8, 9))
    fig.tight_layout()
    fig.subplots_adjust(bottom=-.25)
    for row, name in enumerate(all_norms.keys()):
        for col in range(ncols):  # so all have the same (0,1) y-axis
            axes[row][col].set_ylim([-0.05, 1.05])
        axes[row][0].set_title('Sample inputs')
        axes[row][0].plot(x, y1)
        axes[row][0].plot(x, y2)
        axes[row][1].set_title(name + ' norm')
        axes[row][1].plot(x, all_norms[name].and_func(y1, y2))
        axes[row][2].set_title(name + ' co-norm')
        axes[row][2].plot(x, all_norms[name].or_func(y1, y2))

if __name__ == '__main__':
    sample_x = np.arange(0, 100)
    sample_y1 = skmemb.trapmf(sample_x, [15, 30, 55, 75])
    sample_y2 = skmemb.trapmf(sample_x, [25, 45, 70, 85])
    visualise_all(sample_x, sample_y1, sample_y2)
