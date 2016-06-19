#!/usr/bin/env python
"""Script to auto-generate our API docs."""
# stdlib imports
import sys
import os

# local imports
from apigen import ApiDocWriter

# version comparison
from distutils.version import LooseVersion


def abort(error):
    print('*WARNING* API documentation not generated: %s' % error)
    exit()

if __name__ == '__main__':
    package = 'skfuzzy'
    import skfuzzy

    # Check that the 'image' package is available. If not, the API
    # documentation is not (re)generated and existing API documentation
    # sources will be used.

    try:
        __import__(package)
    except ImportError, e:
        abort("Can not import skfuzzy")

    module = sys.modules[package]

    installed_version = LooseVersion(module.__version__)

    # Check that the source version is equal to the installed
    # version. If the versions mismatch the API documentation sources
    # are not (re)generated. This avoids automatic generation of documentation
    # for older or newer versions if such versions are installed on the system.

    source_lines = open(os.path.join(skfuzzy.__path__[0],
                                     '__init__.py')).readlines()
    version = 'vUndefined'
    for l in source_lines:
        if l.startswith('__version__'):
            source_version = LooseVersion(l.split("'")[1])
            break

    # if source_version != installed_version:
    #     abort("Installed version does not match source version")

    outdir = 'api'
    docwriter = ApiDocWriter(package)
    # docwriter.package_skip_patterns += [r'\.fixes$',
    #                                     r'\.externals$',
    #                                     ]
    docwriter.write_api_docs(outdir)
    docwriter.write_index(outdir, 'api', relative_to='api')
    print('%d files written' % len(docwriter.written_modules))
