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
import Master
debug=True

  
def doProbe(args):
  state = {}
  state['status'] = "ok"
  state['displayType'] = host.getLocalAttr('displayType')
  state['displayId'] = DisplayHandler.currentId
  state['isMaster']=False
  if host.getLocalAttr('isMaster'):
    state['isMaster'] = True
    state['searchType'] = Master.searchType
  state['isRaspberry'] = host.getLocalAttr('isRaspberry')
  state['hasDisplay'] = host.getLocalAttr('hasDisplay')
  state['wantsPhrase'] = host.getLocalAttr('wantsPhrase')
  state['hasVoice'] = host.getLocalAttr('hasVoice')
  state['hasMusic'] = host.getLocalAttr('hasMusic')
  state['hasPowerCheck'] = host.getLocalAttr('hasPowerCheck')
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
    ,'Search' : Master.setSearchType
}
def handleCmd(cmd):
  if debug: print("handling cmd:"+str(cmd['cmd']));
  if cmd['cmd'] not in cmds.keys():
    return host.jsonStatus("%s: not implemented"%cmd['cmd']);
  status = cmds[cmd['cmd']](cmd['args'])
  return status


