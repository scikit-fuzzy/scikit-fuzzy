"""
skfuzzy.image : Essential operations for fuzzy logic on 2-D data and images.

"""
__all__ = ['defocus',
           'focus',
           'imcontrast',
           'nmse',
           'sinmse',
           'view_as_blocks',
           'view_as_windows',
           'pad']

from .imops import defocus, focus, imcontrast, nmse, sinmse
from .shape import view_as_blocks, view_as_windows, pad
