#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
aps: APS Journals API in Python for Humans.

@author: ishxiao
~Email~: me@ishxiao.com

"""
DOCLINES = __doc__.split('\n')

CLASSIFIERS = """\
Development Status :: 0 - alpha
Intended Audience :: Science/Research
License :: OSI Approved :: MIT License
Programming Language :: Python
Programming Language :: Python :: 3
Topic :: Scientific/Engineering
Operating System :: MacOS
Operating System :: POSIX
Operating System :: Unix
Operating System :: Microsoft :: Windows
"""

# import statements
import os
import sys
# The following is required to get unit tests up and running.
# If the user doesn't have, then that's OK, we'll just skip unit tests.
try:
    from setuptools import setup, Extension
    TEST_SUITE = 'nose.collector'
    TESTS_REQUIRE = ['nose']
    EXTRA_KWARGS = {
        'test_suite': TEST_SUITE,
        'tests_require': TESTS_REQUIRE
    }
except:
    from distutils.core import setup
    from distutils.extension import Extension
    EXTRA_KWARGS = {}

try:
    import numpy as np
except:
    np = None

from Cython.Build import cythonize
from Cython.Distutils import build_ext

# all information about aps goes here
MAJOR = 0
MINOR = 0
MICRO = 0
ISRELEASED = False
VERSION = '%d.%d.%d' % (MAJOR, MINOR, MICRO)
REQUIRES = ['numpy (>=1.8)', 'scipy (>=0.15)', 'cython (>=0.21)']
INSTALL_REQUIRES = ['numpy>=1.8', 'scipy>=0.15', 'cython>=0.21']
PACKAGES = ['aps', 'aps/tests']
PACKAGE_DATA = {
    'aps': ['configspec.ini'],
    'aps/tests': ['*.ini']
}
# If we're missing numpy, exclude import directories until we can
# figure them out properly.
INCLUDE_DIRS = [np.get_include()] if np is not None else []

#from setuptools import setup
HEADERS = []
NAME = "aps"
AUTHOR = ("Xiao Shang")
AUTHOR_EMAIL = ("me@ishxiao.com")
LICENSE = "MIT"
DESCRIPTION = DOCLINES[0]
LONG_DESCRIPTION = "\n".join(DOCLINES[2:])
KEYWORDS = "physics"
URL = "https://github.com/ishxiao/aps"
CLASSIFIERS = [_f for _f in CLASSIFIERS.split('\n') if _f]
PLATFORMS = ["Linux", "Mac OSX", "Unix", "Windows"]


def git_short_hash():
    try:
        git_str = "+" + os.popen('git log -1 --format="%h"').read().strip()
    except:
        git_str = ""
    else:
        if git_str == '+': #fixes setuptools PEP issues with versioning
            git_str = ''
    return git_str

FULLVERSION = VERSION

# NumPy's distutils reads in versions differently than
# our fallback. To make sure that versions are added to
# egg-info correctly, we need to add FULLVERSION to
# EXTRA_KWARGS if NumPy wasn't imported correctly.
if np is None:
    EXTRA_KWARGS['version'] = FULLVERSION

def write_version_py(filename='aps/version.py'):
    cnt = """\
# THIS FILE IS GENERATED FROM ASP SETUP.PY
short_version = '%(version)s'
version = '%(fullversion)s'
release = %(isrelease)s
"""
    a = open(filename, 'w')
    try:
        a.write(cnt % {'version': VERSION, 'fullversion':
                FULLVERSION, 'isrelease': str(ISRELEASED)})
    finally:
        a.close()

local_path = os.path.dirname(os.path.abspath(sys.argv[0]))
os.chdir(local_path)
sys.path.insert(0, local_path)
sys.path.insert(0, os.path.join(local_path, 'aps'))  # to retrive _version

# always rewrite _version
if os.path.exists('asp/version.py'):
    os.remove('asp/version.py')

write_version_py()

EXT_MODULES =[]

if not ISRELEASED:
    FULLVERSION += '.dev'+str(MICRO)+git_short_hash()

# Setup commands go here
setup(name = NAME,
      version = FULLVERSION,
      packages = PACKAGES,
      include_package_data = True,
      include_dirs = INCLUDE_DIRS,
      headers = HEADERS,
      ext_modules = cythonize(EXT_MODULES),
      cmdclass = {'build_ext': build_ext},
      author = AUTHOR,
      author_email = AUTHOR_EMAIL,
      license = LICENSE,
      description = DESCRIPTION,
      long_description = LONG_DESCRIPTION,
      keywords = KEYWORDS,
      url = URL,
      classifiers = CLASSIFIERS,
      platforms = PLATFORMS,
      requires = REQUIRES,
      package_data = PACKAGE_DATA,
      zip_safe = False,
      install_requires=INSTALL_REQUIRES,
      **EXTRA_KWARGS
)
