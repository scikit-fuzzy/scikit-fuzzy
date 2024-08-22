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

__version__ = '0.5.0'

######################
# Subpackage imports #
######################

# Core fuzzy mathematics subpackage
import skfuzzy.fuzzymath as _fuzzymath  # noqa: E402
from skfuzzy.fuzzymath import *  # noqa: E402,F403
__all__.extend(_fuzzymath.__all__)

# Fuzzy membership function subpackage
import skfuzzy.membership as _membership  # noqa: E402
from skfuzzy.membership import *  # noqa: E402,F403
__all__.extend(_membership.__all__)

# Clustering subpackage including fuzzy c-means
import skfuzzy.cluster as _cluster  # noqa: E402
from skfuzzy.cluster import *  # noqa: E402,F403
__all__.extend(_cluster.__all__)

# Interval subpackage
import skfuzzy.intervals as _intervals  # noqa: E402
from skfuzzy.intervals import *  # noqa: E402,F403
__all__.extend(_intervals.__all__)

# Filtering subpackage, including 1D and 2D FIRE functions
import skfuzzy.filters as _filters  # noqa: E402
from skfuzzy.filters import *  # noqa: E402,F403
__all__.extend(_filters.__all__)

# Defuzzification subpackage
import skfuzzy.defuzzify as _defuzz  # noqa: E402
from skfuzzy.defuzzify import *  # noqa: E402,F403
__all__.extend(_defuzz.__all__)

# Image processing subpackage
import skfuzzy.image as _image  # noqa: E402
from skfuzzy.image import *  # noqa: E402,F403
__all__.extend(_image.__all__)

# Fuzzy control system subpackage
# import skfuzzy.control as _control
# from skfuzzy.control import *
# __all__.extend(_control.__all__)

# Enable testing of the package
import os.path as osp  # noqa: E402
import functools  # noqa: E402
import warnings  # noqa: E402
import sys  # noqa: E402
from importlib import util as importlib_utils  # noqa: E402

pkg_dir = osp.abspath(osp.dirname(__file__))
data_dir = osp.join(pkg_dir, 'data')

# Logic for checking for improper install and importing while in the source
# tree when package has not been installed inplace.
# Code adapted from scikit-learn's __check_build module.
_INPLACE_MSG = """
It appears that you are importing a local scikit-fuzzy source tree. For
this, you need to have an inplace install. Maybe you are in the source
directory and you need to try from another location."""

_STANDARD_MSG = """
Your install of scikit-fuzzy appears to be broken.
Try re-installing the package."""


def _raise_build_error(e):
    # Raise a comprehensible error
    local_dir = osp.split(__file__)[0]  # noqa: F405,F821
    msg = _STANDARD_MSG
    if local_dir == "skfuzzy":
        # Picking up the local install: this will work only if the
        # install is an 'inplace build'
        msg = _INPLACE_MSG
    raise ImportError("""{!s}
It seems that scikit-fuzzy has not been built correctly.
{!s}""".format(e, msg))


try:
    # This variable is injected in the __builtins__ by the build
    # process. It used to enable importing subpackages of skimage when
    # the binaries are not built
    __SKFUZZY_SETUP__  # noqa: F405
except NameError:
    __SKFUZZY_SETUP__ = False

if __SKFUZZY_SETUP__:
    sys.stderr.write('Partial import of skfuzzy during the build process.\n')
    # We are not importing the rest of the scikit during the build
    # process, as it may not be compiled yet

del warnings, functools, importlib_utils, osp, sys
