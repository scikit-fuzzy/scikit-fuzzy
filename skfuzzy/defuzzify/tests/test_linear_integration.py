import numpy as np
import numpy.testing as tst
import pytest
from skfuzzy.defuzzify.defuzz import centroid, bisector
from skfuzzy.membership import trimf


def test_bisector_carries_area_across_empty_gap():
    x = np.arange(7.)
    mf = np.array([0., 1., 0., 0., 0., 1., 1.])
    # Left triangle area is 1. Total area is 2.5. The right rising edge
    # must supply 0.25, so (u - 4)^2 / 2 = 0.25.
    tst.assert_allclose(bisector(x, mf), 4. + np.sqrt(.5), rtol=0, atol=1e-14)


@pytest.mark.parametrize('a,b,c', [(-5., -2., 7.), (0., 1., 3.), (2., 2., 9.), (1., 8., 8.)])
def test_triangle_centroid_analytic(a, b, c):
    x = np.unique(np.array([a, b, c]))
    mf = trimf(x, [a, b, c])
    tst.assert_allclose(centroid(x, mf), (a + b + c) / 3., rtol=1e-13)
