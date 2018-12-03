#!/usr/bin/env python
import os
home = os.environ['HOME']
defaultSpecPath = home+"/GitProjects/iAltar/config/ialtar.json"
import json
import urllib2
import syslog
from threading import Lock

mutex = Lock()
specs = None

def load(specPath=defaultSpecPath):
  global specs
  syslog.syslog("config: specPath%s"%specPath)
  with open(specPath) as f:
    specs = json.load(f)
  print specs
  
  
def internetOn():
  try:
    urllib2.urlopen('http://216.58.192.142', timeout=1)
    return True
  except urllib2.URLError as err: 
    return False
    
