import os
import sys
# TravisCI setup
if 'TRAVIS' in os.environ:
  sys.path.insert(0, '/usr/lib/pyshared/python2.7')

sys.path.insert(0, '../seammerging')
