"""
Tests for the array padding functions.
"""
import os

import numpy as np
import skfuzzy.image
from numpy.testing import (assert_allclose, TestCase)
from skfuzzy.image import nmse


class TestNMSE(TestCase):
    def test_trivial_case(self):
        test = np.arange(30).reshape(5, 6)
        bad = np.fliplr(np.flipud(test))

        nmse_result = nmse(test, bad)
        assert nmse_result == 400.
        assert 0. == nmse(test, test)

    def test_astronaut(self):
        np.random.seed(42)
        im = np.load(os.path.join(skfuzzy.image.__path__[0],
                                  'astronaut_gray.npy'))
        assert 0. == nmse(im, im)

        noisy = im.astype(np.float64) + np.random.randint(-10, 10,
                                                          size=im.shape)
        assert_allclose(0.58482721617851174, nmse(im, noisy))


if __name__ == "__main__":
    np.testing.run_module_suite()
