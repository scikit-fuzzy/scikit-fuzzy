#!/usr/bin/env python
"""Script to auto-generate our API docs.
"""
# stdlib imports
import os, sys

# local imports
from apigen import ApiDocWriter

# version comparison
from distutils.version import LooseVersion as V

#*****************************************************************************

def abort(error):
    print('*WARNING* API documentation not generated: %s' % error)
    exit()

if __name__ == '__main__':
    package = 'skfuzzy'

    # Check that the 'image' package is available. If not, the API
    # documentation is not (re)generated and existing API documentation
    # sources will be used.
    try:
        curpath = os.path.dirname(__file__)
        src_dir = os.path.join(os.path.abspath(curpath), '..', '..')
        sys.path.append(src_dir)

        __import__(package)

    except ImportError, e:
        abort("Can not import skfuzzy in " + src_dir)

    module = sys.modules[package]

#    try:
#        installed_version = V(module.version.version)
#    except:
    setup_lines = open(os.path.join(curpath, '../../setup.py')).readlines()
    version = 'vUndefined'
    for l in setup_lines:
        if l.startswith('VERSION'):
            source_version = V(l.split("'")[1])
            break

#    if source_version != installed_version:
#        abort("Installed version does not match source version")

    outdir = 'api'
    docwriter = ApiDocWriter(package)
    docwriter.package_skip_patterns += [r'\.fixes$',
                                        r'\.externals$',
                                        ]
    docwriter.write_api_docs(outdir)
    docwriter.write_index(outdir, 'api', relative_to='api')
    print('%d files written' % len(docwriter.written_modules))
