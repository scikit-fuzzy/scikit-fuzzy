#! /usr/bin/env python

descr = """scikit-fuzzy (a.k.a. `skfuzzy`): Fuzzy Logic Toolbox for Python.

This package implements many useful tools and functions for computation and
projects involving fuzzy logic, also known as grey logic.

"""

DISTNAME            = 'scikit-fuzzy'
DESCRIPTION         = 'Fuzzy logic routines for SciPy'
LONG_DESCRIPTION    = descr
MAINTAINER          = 'Joshua Warner'
MAINTAINER_EMAIL    = 'joshua.dale.warner@gmail.com'
LICENSE             = 'Modified BSD'
DOWNLOAD_URL        = 'http://github.com/scikit-fuzzy/scikit-fuzzy'
VERSION             = '0.1dev'
PYTHON_VERSION      = (2, 5)
DEPENDENCIES        = {'numpy': (1, 6),
                       'scipy': (0, 9)}


import os
import sys
import re
import setuptools
from numpy.distutils.core import setup
try:
    from distutils.command.build_py import build_py_2to3 as build_py
except ImportError:
    from distutils.command.build_py import build_py


def check_requirements():
    if sys.version_info < PYTHON_VERSION:
        raise SystemExit('Python version %d.%d required; found %d.%d.'
                         % (PYTHON_VERSION[0], PYTHON_VERSION[1],
                            sys.version_info[0], sys.version_info[1]))

    for package_name, min_version in DEPENDENCIES.items():
        dep_err = False
        try:
            package = __import__(package_name)
        except ImportError:
            dep_err = True
        else:
            package_version = get_package_version(package)
            if min_version > package_version:
                dep_err = True

        if dep_err:
            raise ImportError('`%s` version %d.%d or later required.'
                              % ((package_name, ) + min_version))


def get_package_version(package):
    version = []
    for version_attr in ('version', 'VERSION', '__version__'):
        if hasattr(package, version_attr) \
                and isinstance(getattr(package, version_attr), str):
            version_info = getattr(package, version_attr, '')
            for part in re.split('\D+', version_info):
                try:
                    version.append(int(part))
                except ValueError:
                    pass

    return tuple(version)


def write_version_py(filename='skfuzzy/version.py'):
    template = """# THIS FILE IS GENERATED FROM THE SKFUZZY SETUP.PY
version='%s'
"""

    vfile = open(os.path.join(os.path.dirname(__file__),
                              filename), 'w')

    try:
        vfile.write(template % VERSION)
    finally:
        vfile.close()


def configuration(parent_package='', top_path=None):
    if os.path.exists('MANIFEST'):
        os.remove('MANIFEST')

    from numpy.distutils.misc_util import Configuration
    config = Configuration(None, parent_package, top_path)

    config.set_options(ignore_setup_xxx_py=True,
                       assume_default_configuration=True,
                       delegate_options_to_subpackages=True,
                       quiet=True)

    config.add_subpackage('skfuzzy')
    # config.add_data_dir('skfuzzy/data')

    return config


if __name__ == '__main__':
    check_requirements()
    write_version_py()

    setup(
        name=DISTNAME,
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        maintainer=MAINTAINER,
        maintainer_email=MAINTAINER_EMAIL,
        license=LICENSE,
        download_url=DOWNLOAD_URL,
        version=VERSION,

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

        configuration=configuration,

        packages=setuptools.find_packages(),
        include_package_data=True,
        zip_safe=False
    )

# Not included as this package has no post-install scripts or build req:
      # entry_points={
      #     'console_scripts': ['skivi = skimage.scripts.skivi:main'],
      # },
      # cmdclass={'build_py': build_py},
