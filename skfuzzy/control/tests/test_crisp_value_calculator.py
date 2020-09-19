import numpy as np

from skfuzzy.control.controlsystem import (
    Antecedent, Consequent, ControlSystem, ControlSystemSimulation,
    CrispValueCalculator, Rule,
)


def test_crisp_value_calculator_1():
    x1 = Antecedent(np.linspace(0, 10, 11), "x1")
    x1.automf(3)  # term labels: poor, average, good
    x2 = Antecedent(np.linspace(0, 10, 11), "x2")
    x2.automf(3)

    y1 = Consequent(np.linspace(0, 10, 11), "y1")
    y1.automf(3)
    y2 = Consequent(np.linspace(0, 10, 11), "y2")
    y2.automf(3)

    r1 = Rule(x1["poor"], y1["good"])
    r2 = Rule(x2["poor"], y2["good"])
    sys = ControlSystem([r1, r2])

    sim = ControlSystemSimulation(sys)
    cvc = CrispValueCalculator(x1, sim)

    cvc.fuzz(0)
    values = {label: term.membership_value[sim]
              for label, term in x1.terms.items()}
    assert values == {
        "poor": 1,
        "average": 0,
        "good": 0,
    }

    cvc.fuzz(2.5)
    values = {label: term.membership_value[sim]
              for label, term in x1.terms.items()}
    assert values == {
        "poor": .5,
        "average": .5,
        "good": 0,
    }

    cvc.fuzz("average")
    values = {label: term.membership_value[sim]
              for label, term in x1.terms.items()}
    assert values == {
        "poor": 0,
        "average": 1,
        "good": 0,
    }
