"""
Tests for the array padding functions.
"""
import os

import numpy as np
import skfuzzy.image
from numpy.testing import (assert_allclose, TestCase, run_module_suite)
from skfuzzy.image import defocus_local_means, view_as_windows, pad


class TestDefocusLocalMeans(TestCase):
    def test_trivial_defocus(self):
        im = np.r_[[[0, 3, 4, 6, 1],
                    [3, 6, 1, 1, 8],
                    [4, 2, 6, 0, 7],
                    [5, 5, 9, 0, 2]]]
        result = defocus_local_means(im)

        expected = np.array(
           [[ 3. ,  4.  ,  2.75,  1.75,  7.  ],
            [ 4. ,  2.25,  4.25,  3.75,  2.5 ],
            [ 3. ,  5.25,  3.  ,  3.5 ,  2.5 ],
            [ 4.5,  4.5 ,  4.25,  2.75,  3.5 ]])

        assert_allclose(result, expected)

    def test_defocus_astronaut(self):
        im = np.load(os.path.join(skfuzzy.image.__path__[0],
                                  'astronaut_gray.npy')).astype(np.float64)
        result = defocus_local_means(im)

        expected = view_as_windows(
            pad(im, 1, mode='reflect'),
            (3, 3))[:, :, [1, 1, 0, 2], [0, 2, 1, 1]].mean(axis=2)

        assert_allclose(result, expected)


if __name__ == "__main__":
    run_module_suite()
