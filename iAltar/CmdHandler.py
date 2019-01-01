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
import DisplayHandler
debug=True


  
def doProbe(args):
  state = {}
  state['status'] = "ok"
  state['displayId'] = DisplayHandler.currentId
  return json.dumps(state)

cmds = {
    'AddImage' : DisplayHandler.addImage
    ,'Probe' : doProbe
    ,'RmCacheDir' : DisplayHandler.rmCacheDir
    ,'SetImageDir' : DisplayHandler.setImageDir
    ,'ClearCache' : DisplayHandler.clearCache
}
def handleCmd(cmd):
  if debug: syslog.syslog("handling cmd:"+str(cmd));
  return cmds[cmd['cmd']](cmd['args'])

