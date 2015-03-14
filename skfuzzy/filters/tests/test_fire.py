"""Tests for the array pading functions.

"""
from __future__ import division, absolute_import, print_function

import os
import numpy as np
from numpy.random import randint
import skfuzzy.image
from skfuzzy.filters import fire1d, fire2d


def _generatedata_1d(length=128, seed=42):
    # Make a pure sine tone
    x = np.arange(length) * 2 * np.pi / length
    y = np.sin(x)

    # Add some deterministic salt and pepper
    np.random.seed(seed)
    y[randint(0, 127, 20)] = 1   # Salt
    y[randint(0, 127, 20)] = -1  # Pepper

    return y


class TestFire1D():
    def __init__(self):
        self.data = _generatedata_1d()

    def test_fire1d(self):
        fired = fire1d(self.data)
        assert fired.std() < 0.65        # Lower variation
        assert fired[:64].min() >= -0.1  # Correction terminates at zero
        assert fired[64:].max() <= 0.1


class TestFire2D():
    def __init__(self):
        # Normalized astronaut image
        self.im = np.load(
            os.path.join(skfuzzy.image.__path__[0],
                         'astronaut_gray.npy')).astype(np.float64)

        # Add some deterministic salt and pepper
        np.random.seed(42)
        x, y = self.im.shape
        num = 13000
        self.im[randint(0, x, num), randint(0, y, num)] = 0  # Salt
        self.im[randint(0, x, num), randint(0, y, num)] = 1  # Pepper

    def test_fire2d(self):
        fired = fire2d(self.im, fuzzyresolution=0.1)

        assert fired.std() < self.im.std()

if __name__ == '__main__':
    np.testing.run_module_suite()
