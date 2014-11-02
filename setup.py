#!/usr/bin/env python

from distutils.core import setup
from distutils.extension import Extension
import runpy
from Cython.Build import cythonize
import numpy
import sys

if sys.version_info < (2, 6):
    raise RuntimeError('must use python 2.6 or greater')

__version_str__ = runpy.run_path("seammerging/version.py")["version"]

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

include_path = [numpy.get_include()]

extensions = [
    Extension('native_seam_merging', ['seammerging/src/*.pyx'],
              include_dirs=include_path
              )
]

setup(name='py-seam-merging',
      version=__version_str__,
      description='Seam merging for images implementation.',
      author='Piero Dotti, Paolo Guglielmini',
      author_email='pnproductions.dev@gmail.com',
      license='MIT',
      url='http://github.com/PnProductions/py-seam-merging',
      packages=['seammerging'],
      ext_modules=cythonize(extensions),
      install_requires=requirements,
      setup_requires=requirements
      )
