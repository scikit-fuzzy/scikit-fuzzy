"""
skfuzzy.image : Essential operations for fuzzy logic on 2-D data and images.

"""
__all__ = ['defocus_local_means',
           'nmse',
           'view_as_blocks',
           'view_as_windows',
           'pad']

from .imops import defocus_local_means
from .shape import view_as_blocks, view_as_windows
from .metrics import nmse
from .arraypad import pad
