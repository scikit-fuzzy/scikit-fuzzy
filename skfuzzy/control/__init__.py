"""
skfuzzy.control subpackage, providing a high-level API for fuzzy system design.

"""

__all__ = ['Antecedent',
           'Consequent',
           'ControlSystem',
           'ControlSystemSimulation',
           'Rule',
           'accumulation_max',
           'accumulation_mult',
           ]

from .antecedent_consequent import (Antecedent, Consequent,
                                    accumulation_max, accumulation_mult)
from .controlsystem import ControlSystem, ControlSystemSimulation
from .rule import Rule
