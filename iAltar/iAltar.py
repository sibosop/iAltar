#!/usr/bin/env python 
import os
import sys
proj = os.environ['HOME'] + "//GitProjects/iAltar"
unbuff = os.environ['PYTHONUNBUFFERED'] 
sys.path.append(proj+"/config")
sys.path.append(proj+"/common")
sys.path.append(proj+"/server")
import server
import argparse
import config
import datetime
import time
import host
import CmdHandler
import DisplayHandler
import displayImage
import random
import Master
import PhraseHandler

masterThread=None
debug = True
if __name__ == '__main__':
  try:
    random.seed()
    pname = sys.argv[0]
    print(pname+" at "+datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'))
    print "%s unbuffered %s"%(pname,unbuff)
    os.environ['DISPLAY']=":0.0"
    os.chdir(os.path.dirname(sys.argv[0]))
    parser = argparse.ArgumentParser() 
    parser.add_argument('-d','--debug', action = 'store_true',help='set debug')
    parser.add_argument('-c','--config',nargs=1,type=str,default=[config.defaultSpecPath],help='specify different config file')
    args = parser.parse_args()
    if debug: print("config path"+args.config[0])
    config.load(args.config[0])
    host.setHostPort(config.specs['iAltarServerPort'])
    server.cmdHandler = CmdHandler.handleCmd
    sst = server.serverThread(config.specs['iAltarServerPort'])
    sst.setDaemon(True)
    sst.start()
    dtype = host.getLocalAttr('displayType') 
    if dtype == 'Image':
      displayImage.setup()
      displayThread = DisplayHandler.displayThread()
      displayThread.setDaemon(True)
      displayThread.start()
    if dtype == 'Phrase':
      displayImage.setup()
      PhraseThread = PhraseHandler.phraseThread()
      PhraseThread.setDaemon(True)
      PhraseThread.start()
    if host.getLocalAttr('isMaster'):
      masterThread = Master.masterThread()
      masterThread.setDaemon(True)
      masterThread.start()

    while True:
      try:
        time.sleep(2)
      except KeyboardInterrupt:
        print(pname+": keyboard interrupt")
        server.doExit(5)
        break
      except Exception as e:
        print(pname+":"+str(e))
        server.doExit(5)
        break
  except Exception, e:
    print("pname Main error:"+str(e))
    server.doExit(5)
  print(pname+" exiting")
  server.doExit(0)

  
