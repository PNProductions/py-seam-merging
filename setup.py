#!/usr/bin/env python

__module_name__ = 'py-seam-merging'

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import runpy
from distutils.extension import Extension
import sys

if sys.version_info < (2, 6):
    raise RuntimeError('must use python 2.6 or greater')

__version_str__ = runpy.run_path("seammerging/version.py")["version"]

with open('requirements.txt') as f:
    requirements = f.read().splitlines()


class CythonExtList(list):
    def __init__(self):
        self._list = None
    def c_list(self):
        if self._list is None:
            import numpy
            from Cython.Build import cythonize
            include_path = [numpy.get_include()]
            self._list = cythonize([
              Extension('native_seam_merging', ['seammerging/src/*.pyx'],
                  include_dirs=include_path
              )])
        return self._list
    def __iter__(self):
        _list = self.c_list()
        for e in _list:
            yield e
    def __getitem__(self, ii):
        return self.c_list()[ii]
    def __delitem__(self, ii):
        del self.c_list()[ii]
    def __setitem__(self, ii, val):
        return self.c_list()[ii]
    def __str__(self):
        return self.__repr__()
    def __repr__(self):
        return """<CythonExtList %s>""" % self.c_list()
    def __len__(self):
        return len(self.c_list())
    def append(self, val):
        self.c_list().append(val)


extensions = CythonExtList()


setup(name=__module_name__,
      version=__version_str__,
      description='Seam merging for images implementation.',
      author='Piero Dotti, Paolo Guglielmini',
      author_email='pnproductions.dev@gmail.com',
      license='MIT',
      url='http://github.com/PnProductions/py-seam-merging',
      packages=['seammerging'],
      ext_modules=extensions,
      install_requires=requirements,
      setup_requires=requirements
      )
