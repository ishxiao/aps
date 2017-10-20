#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 20 15:15:55 2017

@author: ishxiao
~Email~: me@ishxiao.com

"""

"""
Command line output of information on QuTiP and dependencies.
"""

__all__ = ['about']

import sys
import os
import platform
import numpy
import scipy
import inspect
import aps
import aps.settings
from aps.hardware_info import hardware_info

def about():
    """
    About box for aps. Gives version numbers for
    aps, NumPy, SciPy, Cython, and MatPlotLib.
    """
    print("")
    print("aps: APS Journals API in Python for Humans")
    print("Copyright (c) 2017 and later.")
    print("Xiao Shang")
    print("")
    print("aps Version:        %s" % aps.__version__)
    print("Numpy Version:      %s" % numpy.__version__)
    print("Scipy Version:      %s" % scipy.__version__)
    try:
        import Cython
        cython_ver = Cython.__version__
    except:
        cython_ver = 'None'
    print("Cython Version:     %s" % cython_ver)
    try:
        import matplotlib
        matplotlib_ver = matplotlib.__version__
    except:
        matplotlib_ver = 'None'
    print("Matplotlib Version: %s" % matplotlib_ver)
    print("Python Version:     %d.%d.%d" % sys.version_info[0:3])
    print("Number of CPUs:     %s" % hardware_info()['cpus'])
#    print("BLAS Info:          %s" % _blas_info())
    print("Platform Info:      %s (%s)" % (platform.system(),
                                           platform.machine()))
    aps_install_path = os.path.dirname(inspect.getsourcefile(aps))
    print("Installation path:  %s" % aps_install_path)
    print("")

if __name__ == "__main__":
    about()  