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

__version__ = '0.4.2'

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

# Fuzzy control system subpackage
# import skfuzzy.control as _control
# from skfuzzy.control import *
# __all__.extend(_control.__all__)

# Enable testing of the package
import os.path as osp
import imp
import functools
import warnings
import sys

pkg_dir = osp.abspath(osp.dirname(__file__))
data_dir = osp.join(pkg_dir, 'data')

try:
    imp.find_module('nose')
except ImportError:
    def _test(doctest=False, verbose=False):
        """This would run all unit tests, but nose couldn't be
        imported so the test suite can not run.
        """
        raise ImportError("Could not load nose. Unit tests not available.")

else:
    def _test(doctest=False, verbose=False):
        """Run all unit tests."""
        import nose
        import warnings
        args = ['', pkg_dir, '--exe', '--ignore-files=^_test']
        if verbose:
            args.extend(['-v', '-s'])
        if doctest:
            args.extend(['--with-doctest', '--ignore-files=^\.',
                         '--ignore-files=^setup\.py$$', '--ignore-files=test'])
            # Make sure warnings do not break the doc tests
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                success = nose.run('skfuzzy', argv=args)
        else:
            success = nose.run('skfuzzy', argv=args)
        # Return sys.exit code
        if success:
            return 0
        else:
            return 1


# do not use `test` as function name as this leads to a recursion problem with
# the nose test suite
test = _test
test_verbose = functools.partial(test, verbose=True)
test_verbose.__doc__ = test.__doc__
doctest = functools.partial(test, doctest=True)
doctest.__doc__ = doctest.__doc__
doctest_verbose = functools.partial(test, doctest=True, verbose=True)
doctest_verbose.__doc__ = doctest.__doc__


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
    local_dir = osp.split(__file__)[0]
    msg = _STANDARD_MSG
    if local_dir == "skfuzzy":
        # Picking up the local install: this will work only if the
        # install is an 'inplace build'
        msg = _INPLACE_MSG
    raise ImportError("""%s
It seems that scikit-fuzzy has not been built correctly.
%s""" % (e, msg))

try:
    # This variable is injected in the __builtins__ by the build
    # process. It used to enable importing subpackages of skimage when
    # the binaries are not built
    __SKFUZZY_SETUP__
except NameError:
    __SKFUZZY_SETUP__ = False

if __SKFUZZY_SETUP__:
    sys.stderr.write('Partial import of skfuzzy during the build process.\n')
    # We are not importing the rest of the scikit during the build
    # process, as it may not be compiled yet

del warnings, functools, osp, imp, sys
