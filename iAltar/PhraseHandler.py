#!/usr/bin/env python
import os
import sys
home = os.environ['HOME']
proj = home+"GitProjects/iAltar"
sys.path.append(proj+"/iAltar")
sys.path.append(proj+"/config")
sys.path.append(proj+"/common")
import json
import config
import threading
import host
import time
import displayImage

phraseMutex = threading.Lock()
phrase = []

name = "Phrase Handler"
def setPhrase(args):
  global phrase
  p = args['phrase']
  print("%s setting phrase to %s"%(name,p))
  phraseMutex.acquire()
  phrase=p
  phraseMutex.release()
  return host.jsonStatus("ok")

def getPhrase():
  global phrase
  rval = []
  phraseMutex.acquire()
  rval = phrase
  phraseMutex.release()
  return rval

class phraseThread(threading.Thread):
  def __init__(self):
    super(phraseThread,self).__init__()
    self.name = "pisplayThread"
    print("starting: %s"%self.name)

  def run(self):
    lastPhrase = []
    splash = "%s/%s"%(home,config.specs['splashImg'])
    print("%s displaying f:%s"%(name,splash))
    displayImage.displayImage(splash)
    while True:
      p = getPhrase()
      if p != lastPhrase:
        print("%s Displaying Phrase %s"%(self.name,p))
        displayImage.printText(p)
        lastPhrase = p
      time.sleep(1)



      
      
