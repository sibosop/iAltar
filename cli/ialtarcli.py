#!/usr/bin/env python
import subprocess
import platform

import os
proj = os.environ['HOME'] + "/GitProjects/iAltar"
import sys

sys.path.append(proj+"/common")
sys.path.append(proj+"/config")
import host
import json
import argparse
import config
import readline
import base64
import random



debug=True

isRaspberry=platform.uname()[1] == 'raspberrypi'

defParse=None

currentId = None

def sendCargs(p,cargs):
  if len(p.name) + len(p.ip) + len(p.sub) == 0:
    host.sendToHosts(cargs)
    return 0
  if len(p.name) != 0:
    host.sendByName(p.name,cargs)
  if len(p.sub) != 0:
    host.sendWithSubnet(p.sub,cargs)
  if len(p.ip) != 0:
    for h in parms.ip:
      print "h:",h
      host.sendToHost(h,cargs)
  return 0

def doCmd(cmd):
  parse=argparse.ArgumentParser(prog=cmd[0],parents=[defParse]) 
  parms=parse.parse_args(cmd[1:])
  sendCargs(parms,{'cmd' : cmd[0], 'args' : [""] })
  return 0

def doMasterCmd(cmd):
  host.sendToMaster({'cmd' : cmd[0], 'args' : [""] })
  return 0

def doMasterArg(cmd):
  host.sendToMaster({'cmd' : cmd[0], 'args' : [cmd[1]] })
  return 0
  
def doNum(cmd):
  parse=argparse.ArgumentParser(prog=cmd[0],parents=[defParse]) 
  parse.add_argument('value',type=int,nargs=1)
  parms=parse.parse_args(cmd[1:])
  print parms.value
  sendCargs(parms,{'cmd' : cmd[0], 'args' :  parms.value})
  return 0

def doShow(cmd):
  parse=argparse.ArgumentParser(prog=cmd[0],parents=[defParse]) 
  parse.add_argument('words',nargs='*',default=[])
  parse.add_argument('-c','--color',nargs=1,default=["FFFF00"])
  parms=parse.parse_args(cmd[1:])
  phrase = ""
  for c in parms.words:
    phrase += c + " "
  args={}
  args['phrase'] = phrase
  args['color'] = parms.color[0]
  sendCargs(parms,{'cmd' : cmd[0], 'args' : args })
  return 0
  
def doPlay(cmd):
  parse=argparse.ArgumentParser(prog=cmd[0],parents=[defParse]) 
  parse.add_argument('path',nargs='?',default="")
  parms=parse.parse_args(cmd[1:])
  print parms
  args={}
  args['path'] = parms.path
  sendCargs(parms,{'cmd' : cmd[0], 'args' : args })
  return 0
  


langFile = proj+"lists/lang_codes.json"
langs=[]
def getLangs():
  global langs
  if len(langs) == 0:
    with open(langFile) as f:
      langs = json.load(f)
  return langs

def doPhrase(cmd):
  parse=argparse.ArgumentParser(prog=cmd[0],parents=[defParse]) 
  parse.add_argument('words',nargs='*',default=[])
  parse.add_argument('-r','--reps',type=int,nargs=1,default=[1],help='set number of repititions (default 1)')
  parse.add_argument('-v','--vol',type=int,nargs=1,default=[100],help='set volume [default 100]')
  parse.add_argument('-l','--lang',type=str,nargs=1,default=["en"],help='set language',choices=getLangs())
  parse.add_argument('-d','--scat',action='store_true',help='set scatter')
  parse.add_argument('-f','--factor',nargs=1,type=float,default=[1.0],help='pitch factor x.x')
  parms=parse.parse_args(cmd[1:])
  phrase = ""
  for c in parms.words:
    phrase += c + " "
  args = {}
  args['phrase'] = phrase
  args['reps'] = parms.reps[0]
  args['scatter'] = parms.scat
  args['lang'] = parms.lang[0]
  args['vol'] = parms.vol[0]
  args['factor'] = parms.factor[0]
  sendCargs(parms,{'cmd' : cmd[0], 'args' : args })
  return 0

def doAddImage(cmd):
  global currentId
  if currentId is None:
    currentId = random.randint(1,50000)
  parse=argparse.ArgumentParser(prog=cmd[0],parents=[defParse]) 
  parse.add_argument('image',nargs='*',default=[])
  parse.add_argument('-d','--dir',type=int,nargs=1,default=[currentId],help='set image dir id (-1) means display immediately')
  parms=parse.parse_args(cmd[1:])
  phrase = ""
  
   
  args = {}
  args['id'] = parms.dir[0]
  args['imgData'] = []
  for image in parms.image:
    with open(image, "rb") as image_file:
      d={}
      d['name'] =  os.path.basename(image)
      d['img'] = base64.b64encode(image_file.read())
      #d['img'] = "imagedata"
      args['imgData'].append(d)
  sendCargs(parms,{'cmd' : cmd[0], 'args' : args })
  return 0


def doQuit(args):
  print "bye"
  readline.write_history_file()
  return -1


def printCmds(cmd):
  print "SchlubCmds:"
  for c in cmds:
    print c
  print

def doNewCache(cmd):
  global currentId
  currentId = random.randint(1,50000)
  return 0
  

def doImageDir(cmd):
  if currentId is None:
    print("no current Id")
    return
  parse=argparse.ArgumentParser(prog=cmd[0],parents=[defParse]) 
  parms=parse.parse_args(cmd[1:])
  sendCargs(parms,{'cmd' : cmd[0], 'args' :  [currentId]})
  return 0

def doSearch(cmd):
  host.sendToMaster(cmd)
  return 0
  
cmds = {
      'AddImage' : doAddImage
      ,'RmCacheDir' : doNum
      ,'ClearCache' : doCmd
      ,'SetImageDir' : doImageDir
      ,'NewCache' : doNewCache
      ,'Probe'     : doCmd
      ,'Phrase'   : doPhrase
      ,'Poweroff' : doCmd
      ,'Reboot'   : doCmd
      ,'Upgrade'  : doCmd
      ,'Show' : doCmd
      ,'Quit' : doQuit
      ,'Search' : doMasterArg
      ,'Help' : printCmds
    }


def completer(text, state):
  options = [i for i in cmds.keys() if i.upper().startswith(text.upper())]
  if state < len(options):
      return options[state]
  else:
      return None


if __name__ == '__main__':
  random.seed()
  host.debug = True
  run=True
  try:
    readline.read_history_file()
  except:
    pass
  if isRaspberry:
    readline.parse_and_bind("tab: complete")
  else:
    readline.parse_and_bind("bind ^I rl_complete")
  readline.set_completer(completer)
  parser = argparse.ArgumentParser()
  parser.add_argument('-d','--debug', action = 'store_true',help='set debug')
  parser.add_argument('-c','--config',nargs=1,type=str,default=[config.defaultSpecPath],help='specify different config file')
  args = parser.parse_args()
  print "config path",args.config
  config.load(args.config[0])
  host.setHostPort(config.specs['iAltarServerPort'])
  host.setHostList()
  host.printHostList()
  printCmds("")

    
  cmdParser = argparse.ArgumentParser()
  cmdParser.add_argument('cmd',nargs=1,type=str,default=['Help'],choices=cmds.keys())
  
  while run:
    try:
      inp=raw_input("iAltar-> ").split()
      cmdargs = cmdParser.parse_args([inp[0]])
      defParse=argparse.ArgumentParser(add_help=False) 
      defParse.add_argument('-i','--ip',nargs='+',default=[],help='specify dest ip')
      defParse.add_argument('-s','--sub',nargs='+',default=[],help='specify dest ip using subnet')
      defParse.add_argument('-n','--name',nargs='+',default=[],help='specify dest ip by name')
      if cmds[cmdargs.cmd[0]](inp) == -1:
        break
    except KeyboardInterrupt:
      doQuit("")
      break
    except Exception, e:
      print "got exception"
      print str(e)
      continue
    except:
      print "parse error"
      continue
        

