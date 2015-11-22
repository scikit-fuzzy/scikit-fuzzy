"""
skfuzzy.control subpackage, providing a high-level API for fuzzy system design.

"""

__all__ = ['Antecedent',
           'Consequent',
           'ControlSystem',
           'Rule',
           ]

from .antecedent_consequent import Antecedent, Consequent
from .controlsystem import Rule, ControlSystem
