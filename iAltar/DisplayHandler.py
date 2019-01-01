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
import config
import base64
import host
import shutil
import threading
import glob
import time
import displayImage
import random
debug=True

currentId = None;
imageDir = None;
idLock = threading.Lock()


def mkpath(path):
  try: 
    os.makedirs(path)
  except OSError:
    if not os.path.isdir(path):
      raise
  return path

def getImageCache():
  path = "%s/%s/imageCache"%(home,config.specs['tmpdir'])
  return mkpath(path)

def getCacheDir(id):
  path = getImageCache()+"/%d"%id
  return mkpath(path)

def rmCacheDir(args):
  rval = "ok"
  id = args[0]
  path = getCacheDir(id)
  try:
    shutil.rmtree(path)
  except OSError as e:
    rval = "Error: %s - %s." % (e.filename, e.strerror)
  syslog.syslog ("rmCacheDir: path %s %s"%(path,rval))
  return host.jsonStatus(rval)
  

def addImage(args):
  global currentId
  id = args['id']
  imgData = args['imgData']
  if currentId is None or currentId != id:
    currentId = id
  syslog.syslog("addImage currentId: %d"%currentId)
  path = getCacheDir(currentId)
  for d in imgData:
    file = path + "/%s"%d['name']
    syslog.syslog("---name: %s\n"%file)
    with open(file, 'wb') as f:
      f.write(base64.b64decode(d['img']))

  return host.jsonStatus("ok");

def getImageDir():
  global imageDir
  rval = None
  idLock.acquire()
  rval = imageDir
  idLock.release()

  return rval

def setImageDir(args):
  rval = "ok"
  id = args[0]
  global imageDir
  path = getCacheDir(id)
  idLock.acquire()
  imageDir = path
  idLock.release()
  syslog.syslog ("SetImageDir to %s: %s"%(imageDir,rval))
  return host.jsonStatus(rval)

def clearCache(args):
  path = getImageCache()
  for f in os.listdir(path):
    try:
      r = path+"/%s"%f
      syslog.syslog("rm: %s"%r)
      shutil.rmtree(path)
    except OSError as e:
      rval = "Error: %s - %s." % (e.filename, e.strerror)
  return host.jsonStatus("ok")


class displayThread(threading.Thread):
  def __init__(self):
    super(displayThread,self).__init__()
    self.name = "displayThread"
    syslog.syslog("starting: %s"%self.name)


  def run(self):
    afiles = []
    (minTime,maxTime) = config.specs["displayTimeRange"]
    lastImageDir=""
    imageIndex=0
    while True:
      path = getImageDir()
      if path is None:
        time.sleep(1)
        continue
      syslog.syslog("%s: path %s lastImageDir %s"%(self.name,path,lastImageDir))
      if path != lastImageDir:
        syslog.syslog("%s reseting imageIndex"%self.name)
        imageIndex = 0
        lastImageDir = path
        if len(afiles) == 0:
          syslog.syslog("empty image file. waiting")
          time.sleep(1)
          continue
      afiles=glob.glob(path+"/*.jpg")
      numFiles = len(afiles)
      if numFiles == 0:
        syslog.syslog("%s directory removed"%self.name)
        continue
      syslog.syslog("imageIndex %d len afiles %d"%(imageIndex,numFiles))
      if imageIndex >= numFiles:
        syslog.syslog("resetting imageIndex");
        imageIndex = 0
      f = afiles[imageIndex]
      syslog.syslog("displaying f:%s"%f)
      displayImage.displayImage(f)
      next = (random.random() * (maxTime - minTime)) + minTime
      syslog.syslog("next display %f"%next)
      time.sleep(next)
      imageIndex += 1

      

    


