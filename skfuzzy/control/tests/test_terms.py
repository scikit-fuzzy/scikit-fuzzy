# test_terms

import numpy as np


from skfuzzy.control import (
    Antecedent,
)
# from skfuzzy.control.controlsystem import CrispValueCalculator
from skfuzzy.control.term import TermAggregate, FuzzyAggregationMethods


def test_term_aggregate_1():
    x1 = Antecedent(np.linspace(0, 10, 11), "x1")
    x1.automf(3)  # term labels: poor, average, good
    x2 = Antecedent(np.linspace(0, 10, 11), "x2")
    x2.automf(3)
    ta = (x1["poor"] & x2["good"])
    # print("- ta:", ta)
    assert isinstance(ta, TermAggregate)
    assert str(ta) == "x1[poor] AND x2[good]"


def test_fuzzy_aggregation_methods():
    fam = FuzzyAggregationMethods()
    # print("- type(fam.and_func):", type(fam.and_func))
    assert isinstance(fam.and_func, np.ufunc)
    assert isinstance(fam.or_func, np.ufunc)
