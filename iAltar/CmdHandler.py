#!/usr/bin/env python
import os
import sys
home = os.environ['HOME']
proj = home+"GitProjects/iAltar"
sys.path.append(proj+"/iAltar")
sys.path.append(proj+"/config")
sys.path.append(proj+"/common")
sys.path.append(proj+"/server")
import json
import syslog
debug=True

  
def doProbe(cmd):
  state = {}
  state['status'] = "ok"
  return json.dumps(state)

def handleCmd(cmd):
  if debug: syslog.syslog("handling cmd:"+cmd['cmd']);
  return cmds[cmd['cmd']](cmd)

cmds = {
    'Probe' : doProbe
}
