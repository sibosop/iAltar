#!/usr/bin/env python
import os
home = os.environ['HOME']
defaultSpecPath = home+"/GitProjects/iAltar/config/ialtar.json"
import json
import urllib2
from threading import Lock

mutex = Lock()
specs = None

debug=False

def load(specPath=defaultSpecPath):
  global specs
  if debug: print("config: specPath%s"%specPath)
  with open(specPath) as f:
    specs = json.load(f)
  if debug: print("%s"%(specs))
  
  
def internetOn():
  try:
    urllib2.urlopen('http://216.58.192.142', timeout=1)
    return True
  except urllib2.URLError as err: 
    return False
    
