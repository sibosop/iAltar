#!/usr/bin/env python
import os
import sys
from subprocess import CalledProcessError, check_output
home = os.environ['HOME']
debug=True

def upgrade():
  try:
    print("DOING UPGRADE")
    cmd = ['git','pull','--quiet','origin','master']
    output = check_output(cmd)
    if debug: print(output)
  except Exception, e:
    print("player error: "+repr(e))

if __name__ == '__main__':
  upgrade()
  #setVolume(sys.argv[1])
