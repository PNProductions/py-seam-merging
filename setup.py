#!/usr/bin/env python

from distutils.core import setup
from distutils.extension import Extension
from Cython.Build import cythonize
import numpy


include_path = [numpy.get_include()]
print include_path

extensions = [
    Extension('native_seam_merging', ['seammerging/src/*.pyx'],
              include_dirs=include_path
              )
]

setup(name='Seam Merging',
      version='0.1',
      description='Seam merging for images implementation.',
      author='Piero Dotti, Paolo Guglielmini',
      author_email='pnproductions.dev@gmail.com',
      url='http://github.com/PnProductions/py-seam-merging',
      packages=['seammerging'],
      ext_modules=cythonize(extensions)
      )
