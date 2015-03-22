"""
scikit-fuzzy (a.k.a. `skfuzzy`): Fuzzy Logic Toolbox for Python.

This package implements many useful tools and functions for computation and
projects involving fuzzy logic, also known as grey logic.

Most of the functionality is actually located in subpackages, but like numpy we
bring most of the core functionality into the base namespace.

Recommended Use
---------------
>>> import skfuzzy as fuzz

"""
__all__ = []

try:
    from .version import version as __version__
except ImportError:
    __version__ = "unbuilt-dev"
else:
    del version

######################
# Subpackage imports #
######################

# Core fuzzy mathematics subpackage
import skfuzzy.fuzzymath as _fuzzymath
from skfuzzy.fuzzymath import *
__all__.extend(_fuzzymath.__all__)

# Fuzzy membership function subpackage
import skfuzzy.membership as _membership
from skfuzzy.membership import *
__all__.extend(_membership.__all__)

# Clustering subpackage including fuzzy c-means
import skfuzzy.cluster as _cluster
from skfuzzy.cluster import *
__all__.extend(_cluster.__all__)

# Interval subpackage
import skfuzzy.intervals as _intervals
from skfuzzy.intervals import *
__all__.extend(_intervals.__all__)

# Filtering subpackage, including 1D and 2D FIRE functions
import skfuzzy.filters as _filters
from skfuzzy.filters import *
__all__.extend(_filters.__all__)

# Defuzzification subpackage
import skfuzzy.defuzzify as _defuzz
from skfuzzy.defuzzify import *
__all__.extend(_defuzz.__all__)

# Image processing subpackage
import skfuzzy.image as _image
from skfuzzy.image import *
__all__.extend(_image.__all__)
