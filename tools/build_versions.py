#!/usr/bin/env python

import networkx as nx
import numpy as np
import scipy as sp
from PIL import Image

for m in (np, sp, Image, nx):
    if m is not None:
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
