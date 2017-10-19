"""
_normalize_columns.py : Normalize columns.
"""

import numpy as np


def normalize_columns(columns):
    """
    Normalize columns of matrix.

    Parameters
    ----------
    columns : 2d array (M x N)
        Matrix with columns

    Returns
    -------
    normalized_columns : 2d array (M x N)
        columns/np.sum(columns, axis=0, keepdims=1)
    """

    # broadcast sum over columns
    normalized_columns = columns/np.sum(columns, axis=0, keepdims=1)
    
    return normalized_columns


def normalize_power_columns(x, exponent):
    """
    Calculate normalize_columns(x**exponent)
    in a numerically safe manner.

    Parameters
    ----------
    x : 2d array (M x N)
        Matrix with columns
    n : float
        Exponent

    Returns
    -------
    result : 2d array (M x N)
        normalize_columns(x**n) but safe
    
    """

    # works better for positive exponents
    if exponent < 0:
        exponent = -exponent
        x = 1.0/x

    # y = a**n/(a**n + b**n)
    # 
    # is equivalent to:
    #
    # p = exp(n*log(a) - n*log(m))
    # q = exp(n*log(b) - n*log(m))
    # y = p/(p + q)
    # 
    # where m is a positive number
    #
    # see:
    # http://www.wolframalpha.com/input/?i=p%2F(p+%2B+q)+where+p+%3D+exp(n*log(a)+-+n*log(m))+and+q+%3D+exp(n*log(b)+-+n*log(m))
    
    columns = np.exp(exponent*np.log(x) -
        exponent*np.log(np.max(x, axis=0, keepdims=1)))
    
    # calculate sum of each column, then normalize column by its sum
    result = normalize_columns(columns)

    return result
