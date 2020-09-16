#! /usr/bin/env python

descr = """scikit-fuzzy (a.k.a. `skfuzzy`): Fuzzy logic toolbox for Python.

This package implements many useful tools for projects involving fuzzy logic,
also known as grey logic.
"""

DISTNAME            = 'scikit-fuzzy'
DESCRIPTION         = 'Fuzzy logic toolkit for SciPy'
LONG_DESCRIPTION    = descr
MAINTAINER          = 'Joshua Warner'
MAINTAINER_EMAIL    = 'joshua.dale.warner@gmail.com'
LICENSE             = 'Modified BSD'
URL                 = 'https://pypi.python.org/pypi/scikit-fuzzy'
DOWNLOAD_URL        = 'https://github.com/scikit-fuzzy/scikit-fuzzy'

import os
import sys

import setuptools
from distutils.command.build_py import build_py

if sys.version_info[0] < 3:
    import __builtin__ as builtins
else:
    import builtins

# This is a bit (!) hackish: we are setting a global variable so that the main
# skimage __init__ can detect if it is being loaded by the setup routine, to
# avoid attempting to load components that aren't built yet:
# the numpy distutils extensions that are used by scikit-image to recursively
# build the compiled extensions in sub-packages is based on the Python import
# machinery.
builtins.__SKIMAGE_SETUP__ = True


with open('skfuzzy/__init__.py') as fid:
    for line in fid:
        if line.startswith('__version__'):
            VERSION = line.strip().split()[-1][1:-1]
            break

with open('DEPENDS.txt') as fid:
    INSTALL_REQUIRES = []
    for line in fid.readlines():
        if line == '' or line[0] == '#' or line[0].isspace():
            continue
        INSTALL_REQUIRES.append(line.strip())

# requirements for those browsing PyPI
REQUIRES = [r.replace('>=', ' (>= ') + ')' for r in INSTALL_REQUIRES]
REQUIRES = [r.replace('==', ' (== ') for r in REQUIRES]
REQUIRES = [r.replace('[array]', '') for r in REQUIRES]


def configuration(parent_package='', top_path=None):
    if os.path.exists('MANIFEST'):
        os.remove('MANIFEST')

    from numpy.distutils.misc_util import Configuration
    config = Configuration(None, parent_package, top_path)

    config.set_options(
        ignore_setup_xxx_py=True,
        assume_default_configuration=True,
        delegate_options_to_subpackages=True,
        quiet=True)

    config.add_subpackage('skfuzzy')

    return config


if __name__ == "__main__":
    try:
        from numpy.distutils.core import setup
    except ImportError:
        from setuptools import setup
        extra = {}
    else:
        extra = {'configuration': configuration}

    setup(
        name=DISTNAME,
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        maintainer=MAINTAINER,
        maintainer_email=MAINTAINER_EMAIL,
        license=LICENSE,
        url=URL,
        download_url=DOWNLOAD_URL,
        version=VERSION,
        package_data={
            # Include saved test image
            '': ['*.npy', '*.md', '*.txt'],
        },

        classifiers=[
            'Development Status :: 4 - Beta',
            'Environment :: Console',
            'Intended Audience :: Developers',
            'Intended Audience :: Science/Research',
            'License :: OSI Approved :: BSD License',
            'Programming Language :: Python',
            'Programming Language :: Python :: 3',
            'Topic :: Scientific/Engineering',
            'Operating System :: Microsoft :: Windows',
            'Operating System :: POSIX',
            'Operating System :: Unix',
            'Operating System :: MacOS'],

        install_requires=INSTALL_REQUIRES,
        requires=REQUIRES,
        packages=setuptools.find_packages(exclude=['docs']),
        include_package_data=True,
        zip_safe=False,

        cmdclass={'build_py': build_py},
        **extra
    )
