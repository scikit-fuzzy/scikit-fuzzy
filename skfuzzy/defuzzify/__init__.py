"""
skfuzzy.defuzzify subpackage, containing various defuzzification algorithms.

"""

__all__ = ['arglcut',
           'centroid',
           'dcentroid',
           'defuzz',
           'lambda_cut_series',
           'lambda_cut',
           'vertex']

from .defuzz import (arglcut, centroid, dcentroid, defuzz, lambda_cut_series,
                     lambda_cut, vertex)
