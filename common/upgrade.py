#!/usr/bin/env python
import syslog
import os
import sys
from subprocess import CalledProcessError, check_output
home = os.environ['HOME']
debug=True

def upgrade():
  try:
    syslog.syslog("DOING UPGRADE")
    cmd = ['git','pull','--quiet','origin','master']
    output = check_output(cmd)
    if debug: syslog.syslog(output)
  except Exception, e:
    syslog.syslog("player error: "+repr(e))

if __name__ == '__main__':
  upgrade()
  #setVolume(sys.argv[1])
