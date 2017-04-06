"""
skfuzzy.control subpackage, providing a high-level API for fuzzy system design.

"""

__all__ = ['Antecedent',
           'Consequent',
           'ControlSystem',
           'ControlSystemSimulation',
           'Rule',
           'mult',
           ]

from .antecedent_consequent import Antecedent, Consequent
from .controlsystem import ControlSystem, ControlSystemSimulation
from .rule import Rule
from .term import mult
