import numpy as np
from skfuzzy.cluster import cmeans_predict


def test_prediction_preserves_metric_callback_calls():
    calls = []

    def metric(a, b):
        calls.append(1)
        return np.linalg.norm(a - b) + len(calls) * .0001

    data = np.array([[0., 1., 2., 3.], [2., 3., 1., 4.]])
    centers = np.array([[0., 1.], [3., 4.]])
    init = np.full((2, 4), .5)
    result = cmeans_predict(data, centers, 2., 0., 3, metric=metric, init=init)
    assert result[-2] == 3
    assert len(calls) == 2 * 4 * 3
