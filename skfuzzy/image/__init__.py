"""
skfuzzy.image : Essential operations for fuzzy logic on 2-D data and images.

"""
__all__ = ['defocus_local_means',
           'contrast_curves',
           'contrast_sigmoid',
           'nmse',
           'sinmse',
           'view_as_blocks',
           'view_as_windows',
           'pad']

from .imops import defocus_local_means, contrast_curves, contrast_sigmoid
from .shape import view_as_blocks, view_as_windows
from .metrics import nmse, sinmse
from .arraypad import pad
