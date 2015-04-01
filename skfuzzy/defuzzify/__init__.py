"""
skfuzzy.defuzzify subpackage, containing various defuzzification algorithms.

"""

__all__ = ['arglcut',
           'centroid',
           'dcentroid',
           'defuzz',
           'lambda_cut_series',
           'lambda_cut',
           'lambda_cut_boundaries',
           ]

from .defuzz import (arglcut, centroid, dcentroid, defuzz, lambda_cut_series,
                     lambda_cut, lambda_cut_boundaries)
