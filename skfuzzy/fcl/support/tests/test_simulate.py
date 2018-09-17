# -*- coding: utf-8 -*-
'''
@author: james.power@mu.ie, created on Mon Sep 17 14:49:56 2018
'''
import os

import numpy as np
import numpy.testing as tst

import skfuzzy.fcl.support.simulate as simulate


def test_all_terms():
    testfile = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                            'AllTerms.fcl')
    harness = simulate.SimulationHarness(False)
    failed, tot = harness.simulate_from_file(testfile)
    tst.assert_allclose(failed, 0)


if __name__ == '__main__':
    tst.run_module_suite()
