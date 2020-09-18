"""
Tests for the array padding functions.
"""
import os

import numpy as np
import skfuzzy.image
from numpy.random import randint
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
    def test_fire1d(self):
        data = _generatedata_1d()
        fired = fire1d(data)
        assert fired.std() < 0.65        # Lower variation
        assert fired[:64].min() >= -0.1  # Correction terminates at zero
        assert fired[64:].max() <= 0.1


class TestFire2D():
    def test_fire2d(self):
        # Normalized astronaut image
        img = np.load(os.path.join(skfuzzy.image.__path__[0],
                                   'astronaut_gray.npy')).astype(np.float64)

        # Add some deterministic salt and pepper
        np.random.seed(42)
        x, y = img.shape
        num = 13000
        img[randint(0, x, num), randint(0, y, num)] = 0  # Salt
        img[randint(0, x, num), randint(0, y, num)] = 1  # Pepper

        fired = fire2d(img, fuzzyresolution=0.1)

        assert fired.std() < img.std()


if __name__ == '__main__':
    np.testing.run_module_suite()
