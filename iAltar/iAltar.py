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
import watchdog
import voice
import soundTrack
import shutdown

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
    wd = watchdog.WatchdogThread()
    wd.setDaemon(True)
    wd.start()
    host.setHostPort(config.specs['iAltarServerPort'])
    server.cmdHandler = CmdHandler.handleCmd
    print "%s starting Server Thread"%pname
    sst = server.serverThread(config.specs['iAltarServerPort'])
    sst.setDaemon(True)
    sst.start()
    hasDisplay = host.getLocalAttr('hasDisplay') 
    wantsPhrase = host.getLocalAttr('wantsPhrase')
    hasVoice = host.getLocalAttr('hasVoice')
    if hasDisplay:
      dtype = host.getLocalAttr('displayType') 
      if dtype == 'Image':
        print "%s starting Display"%pname
        displayImage.setup()
        displayThread = DisplayHandler.displayThread(wd)
        displayThread.setDaemon(True)
        displayThread.start()

      if dtype == 'Phrase':
        print "%s starting Phrase"%pname
        displayImage.setup()

    hasMusic = host.getLocalAttr('hasMusic')
    if hasMusic:
      print "%s starting Music"%pname
      MusicThread = soundTrack.playEvent(wd)
      MusicThread.setDaemon(True)
      MusicThread.start()
      

    if wantsPhrase:
      print "%s starting Phrase "%pname
      PhraseThread = PhraseHandler.phraseThread(wd)
      PhraseThread.setDaemon(True)
      PhraseThread.start()

    if host.getLocalAttr('isMaster'):
      print "%s starting Master "%pname
      masterThread = Master.masterThread(wd)
      masterThread.setDaemon(True)
      masterThread.start()

    if hasVoice:
      print "%s starting Voice "%pname
      voiceThread = voice.VoiceThread()
      voiceThread.setDaemon(True)
      voiceThread.start()

    if host.getLocalAttr('hasPowerCheck'):
      print "%s starting Power "%pname
      shutdownThread = shutdown.ShutdownThread()
      shutdownThread.setDaemon(True)
      shutdownThread.start()
    

    while True:
      try:
        time.sleep(2)
      except KeyboardInterrupt:
        print(pname+": keyboard interrupt")
        server.doExit(5)
        break
      except Exception as e:
        if e is None:
          print "pname what the fuck e=None"
        else:
          print "%s Main error: %s"%(pname,e)
        server.doExit(5)
        break
  except Exception, e:
    if e is None:
      print "pname what the fuck e=None"
    else:
      print "%s Main error: %s"%(pname,e)
    server.doExit(5)
  print(pname+" exiting")
  server.doExit(0)

  
