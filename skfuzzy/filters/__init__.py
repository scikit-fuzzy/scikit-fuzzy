"""
skfuzzy.filters : Subpackage for filtering data, e.g. with Fuzzy Inference by
    Else-action (FIRE) filters to denoise 1d or 2d data.

"""
__all__ = ['fire1d',
           'fire2d']

from .fire import fire1d, fire2d
