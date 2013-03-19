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

######################
# Subpackage imports #
######################

# Core fuzzy mathematics subpackage
import fuzzymath as _fuzzymath
from fuzzymath import *
__all__.extend(_fuzzymath.__all__)

# Fuzzy membership function subpackage
import membership as _membership
from membership import *
__all__.extend(_membership.__all__)

# Clustering subpackage including fuzzy c-means
import cluster as _cluster
from cluster import *
__all__.extend(_cluster.__all__)

# Interval subpackage
import intervals as _intervals
from intervals import *
__all__.extend(_intervals.__all__)

# Filtering subpackage, including 1D and 2D FIRE functions
import filter as _filter
from filter import *
__all__.extend(_filter.__all__)

# Defuzzification subpackage
import defuzzify as _defuzz
from defuzzify import *
__all__.extend(_defuzz.__all__)

# Image processing subpackage
import image as _image
from image import *
__all__.extend(_image.__all__)
