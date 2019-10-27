#!/usr/bin/env python

from __future__ import print_function

import numpy as np
import scipy as sp
from PIL import Image
import six
import networkx

for m in (np, sp, Image, six, networkx):
    if not m is None:
        if m is Image:
            # Pillow 6.0.0 and above have removed the 'VERSION' attribute
            # https://bitbucket.org/rptlab/reportlab/issues/176/incompatibility-with-pillow-600
            try:
                im_ver = Image.__version__
            except AttributeError:
                im_ver = Image.VERSION
            print('PIL'.rjust(10), ' ', im_ver)
        else:
            print(m.__name__.rjust(10), ' ', m.__version__)
