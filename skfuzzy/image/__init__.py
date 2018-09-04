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

import numpy as np
from distutils.version import LooseVersion
if LooseVersion(np.__version__) > LooseVersion("1.8"):
	from numpy import pad
else:
	from .arraypad import pad
