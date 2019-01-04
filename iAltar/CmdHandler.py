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
import DisplayHandler
import PhraseHandler
import host
import upgrade
import time
debug=True

  
def doProbe(args):
  state = {}
  state['status'] = "ok"
  state['displayType'] = host.getLocalAttr('displayType')
  state['displayId'] = DisplayHandler.currentId
  return json.dumps(state)


def doUpgrade(cmd):
  upgrade.upgrade()
  print("returned from upgrade")
  return host.jsonStatus("reboot")

def doPoweroff(cmd):
  return host.jsonStatus("poweroff");

def doReboot(cmd):
  return host.jsonStatus("reboot");

cmds = {
    'AddImage' : DisplayHandler.addImage
    ,'Probe' : doProbe
    ,'RmCacheDir' : DisplayHandler.rmCacheDir
    ,'SetImageDir' : DisplayHandler.setImageDir
    ,'ClearCache' : DisplayHandler.clearCache
    ,'Upgrade' : doUpgrade
    ,'Poweroff' : doPoweroff
    ,'Reboot' : doReboot
    ,'Phrase' : PhraseHandler.setPhrase
}
def handleCmd(cmd):
  if debug: print("handling cmd:"+str(cmd['cmd']));
  if cmd['cmd'] not in cmds.keys():
    return host.jsonStatus("%s: not implemented"%cmd['cmd']);
  status = cmds[cmd['cmd']](cmd['args'])
  return status


