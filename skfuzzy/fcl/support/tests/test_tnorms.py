# -*- coding: utf-8 -*-
'''


@author: james.power@mu.ie, created on Mon Sep 17 13:45:42 2018
'''

import numpy as np
import numpy.testing as tst

import tnorms


def _check_classic(fam):
    '''
        Test that norm and co-norm work like classic and/or for 0, 1 inputs.
    '''
    a = np.array([0, 0, 1, 1])
    b = np.array([0, 1, 0, 1])
    # First check that the product works like the AND function:
    expected = np.logical_and(a, b)
    fprod = fam.and_func(a, b)
    tst.assert_allclose(expected, fprod)
    # Now check that the sum works like the OR function:
    expected = np.logical_or(a, b)
    fsum = fam.or_func(a, b)
    tst.assert_allclose(expected, fsum)


def _check_duality(fam):
    '''
        Run some tests to make sure that the norm and co-norm are duals.
        That is, they obey de Morgan's law: (a and b) = not((not a) or (not b))
    '''
    # Test a range of values between 0.0 and 1.0 inclusive:
    a = np.arange(0.0, 1.1, 0.1)
    b = np.arange(0.0, 1.1, 0.1)
    prod = fam.and_func(a, b)
    # Need to round, since e.g. 1-0.7 is not 0.3 otherwise:
    dual_sum = 1 - fam.or_func(np.round(1-a, 1), np.round(1-b, 1))
    tst.assert_allclose(prod, dual_sum)


def test_classic():
    for fam in tnorms._IEEE_NORMS.values():
        _check_classic(fam)


def test_duality():
    for fam in tnorms._IEEE_NORMS.values():
        _check_duality(fam)


if __name__ == '__main__':
    tst.run_module_suite()
