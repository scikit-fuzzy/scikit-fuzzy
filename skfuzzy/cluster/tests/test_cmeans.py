import pytest
import numpy as np
import skfuzzy as fuzz


@pytest.fixture
def setup():
    global features, x_corr, y_corr

    # Set random seed
    np.random.seed(42)

    # Generate pseudo-random reasonably well distinguished clusters
    xpts = np.zeros(0)
    ypts = np.zeros(0)

    x_corr = [7, 1, 4]
    y_corr = [3, 2, 1]

    for x, y, in zip(x_corr, y_corr):
        xpts = np.concatenate((xpts, np.r_[np.random.normal(x, 0.5, 200)]))
        ypts = np.concatenate((ypts, np.r_[np.random.normal(y, 0.5, 200)]))

    # Combine into a feature array
    features = np.c_[xpts, ypts].T


def test_fuzzy_cmeans_centers(setup):
    """
    Test fuzzy c-means ability to find cluster centers.

    """
    global features, x_corr, y_corr

    # Cluster using correct number of clusters (3)
    cntr, U, U0, d, Jm, p, fpc = fuzz.cluster.cmeans(
        features, 3, 2., error=0.005, maxiter=1000, init=None)

    # Expected result appears in this order given this random seed
    expected = np.c_[x_corr, y_corr][(1, 0, 2), :]

    np.testing.assert_allclose(expected, cntr, rtol=0.1)

    # Cluster twice, setting the seed for random initialization
    cntr1, _, _, _, _, _, _ = fuzz.cluster.cmeans(
        features, 3, 2., error=0.005, maxiter=1000, init=None, seed=123)

    cntr2, _, _, _, _, _, _ = fuzz.cluster.cmeans(
        features, 3, 2., error=0.005, maxiter=1000, init=None, seed=123)

    # Should be exactly identical
    np.testing.assert_array_equal(cntr1, cntr2)


def test_fuzzy_cmeans_fpc(setup):
    """
    Test utility of fuzzy partition coefficient.

    Note: The correct cluster number is NOT guaranteed to be the maximum
          fuzzy partition coefficient! It is only a (good) approx guideline.

    """
    global features
    fuzzy_partition_coefficients = []

    # Do repeated clustering on this data for n=range(2, 11) clusters
    for n in range(2, 11):
        _, _, _, _, _, _, fpc = fuzz.cluster.cmeans(
            features, n, 2., error=0.005, maxiter=1000, init=None)

        fuzzy_partition_coefficients.append(fpc)

    # Expected maximum is at index 1, corresponding to n=3 clusters
    expected = 1

    test = np.r_[fuzzy_partition_coefficients].argmax()

    assert test == expected


def test_fuzzy_cmeans_predict(setup):
    """
    Test ability to classify new data.

    """
    global features
    global x_corr
    global y_corr

    # Generate slightly smaller new dataset, clustered tighter around seeds
    xtest = np.zeros(0)
    ytest = np.zeros(0)
    cluster = np.zeros(0)

    # Given this initialization, the clustering will be [1, 2, 0]
    for x, y, label in zip(x_corr, y_corr, [1, 2, 0]):
        xtest = np.concatenate((xtest, np.r_[np.random.normal(x, 0.05, 100)]))
        ytest = np.concatenate((ytest, np.r_[np.random.normal(y, 0.05, 100)]))
        cluster = np.concatenate((cluster, np.r_[[label] * 100]))

    test_data = np.c_[xtest, ytest].T

    # Cluster the data to obtain centers
    cntr, _, _, _, _, _, _ = fuzz.cluster.cmeans(
        features, 3, 2., error=0.005, maxiter=1000, init=None)

    # Predict fuzzy memberships, U, for all points in test_data, twice with
    # set seed
    U, _, _, _, _, fpc = fuzz.cluster.cmeans_predict(
        test_data, cntr, 2., error=0.005, maxiter=1000, seed=1234)

    U2, _, _, _, _, fpc2 = fuzz.cluster.cmeans_predict(
        test_data, cntr, 2., error=0.005, maxiter=1000, seed=1234)

    # Verify results are identical
    assert fpc == fpc2
    np.testing.assert_array_equal(U, U2)

    # For this perfect dataset, fpc should be very high
    assert fpc > 0.99

    # Assert data points are correctly labeled (must harden U for comparison)
    np.testing.assert_array_equal(cluster, U.argmax(axis=0))


def test_fuzzy_cmeans_predict_numerically(setup):
    """
    Test ability to classify new data in a numerically safe manner.

    """
    global features
    global x_corr
    global y_corr

    m = 1.0001

    # Generate slightly smaller new dataset, clustered tighter around seeds
    xtest = np.zeros(0)
    ytest = np.zeros(0)
    cluster = np.zeros(0)

    # Given this initialization, the clustering will be [1, 2, 0]
    for x, y, label in zip(x_corr, y_corr, [1, 2, 0]):
        xtest = np.concatenate((xtest, np.r_[np.random.normal(x, 0.05, 100)]))
        ytest = np.concatenate((ytest, np.r_[np.random.normal(y, 0.05, 100)]))
        cluster = np.concatenate((cluster, np.r_[[label] * 100]))

    test_data = np.c_[xtest, ytest].T

    # Cluster the data to obtain centers
    cntr, _, _, _, _, _, _ = fuzz.cluster.cmeans(
        features, 3, m, error=0.005, maxiter=1000, init=None)

    # Predict fuzzy memberships, U, for all points in test_data, twice with
    # set seed
    U, _, _, _, _, fpc = fuzz.cluster.cmeans_predict(
        test_data, cntr, m, error=0.005, maxiter=1000, seed=1234)

    U2, _, _, _, _, fpc2 = fuzz.cluster.cmeans_predict(
        test_data, cntr, m, error=0.005, maxiter=1000, seed=1234)

    # Verify results are identical
    assert fpc == fpc2
    np.testing.assert_array_equal(U, U2)

    # For this perfect dataset, fpc should be very high
    assert fpc > 0.99

    # Assert data points are correctly labeled (must harden U for comparison)
    np.testing.assert_array_equal(cluster, U.argmax(axis=0))


if __name__ == '__main__':
    np.testing.run_module_suite()
