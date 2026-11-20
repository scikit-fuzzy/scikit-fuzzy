import numpy as np
import numpy.testing as tst
import pytest
from skfuzzy.image import defocus_local_means


@pytest.mark.parametrize('dtype', [np.uint8, np.float32, np.float64])
def test_local_means_match_reflected_neighbors(dtype):
    image = np.arange(63).reshape(7, 9).astype(dtype)
    original = image.copy()
    padded = np.pad(image.astype(float), 1, mode='reflect')
    expected = np.empty(image.shape)
    for i, j in np.ndindex(image.shape):
        expected[i, j] = (padded[i + 1, j] + padded[i + 1, j + 2]
                          + padded[i, j + 1] + padded[i + 2, j + 1]) / 4
    tst.assert_array_equal(defocus_local_means(image), expected)
    tst.assert_array_equal(image, original)
