#!/usr/bin/env python
import os
import sys
home = os.environ['HOME']
proj = home+"GitProjects/iAltar"
sys.path.append(proj+"/iAltar")
sys.path.append(proj+"/config")
sys.path.append(proj+"/common")
sys.path.append(proj+"/server")
import syslog
import threading
import time
import archive
import DisplayHandler
import random
import config
import host
import base64

def setImgData(fname):
  with open(fname,"rb") as ImageFile:
    d = {}
    d['name'] = os.path.basename(fname)
    d['img'] = base64.b64encode(ImageFile.read())
  return d

debug=True
class masterThread(threading.Thread):
  def __init__(self):
    super(masterThread,self).__init__()
    self.name = "masterThread"
    syslog.syslog("starting: %s"%self.name)
    self.searchType = config.specs['defaultSearchType'];
    syslog.syslog("%s: default search type: %s"%(self.name,self.searchType))

  def run(self):
    syslog.syslog("%s in run loop"%self.name)
    hosts = host.getHosts()
    imageHosts = []
    panelHosts = []
    phraseHosts = []
    lastCacheId = 0
    for h in hosts:
      ip = h['ip']
      if host.isLocalHost(ip):
        DisplayHandler.clearCache(None)
      else:
        host.sendToHost(ip,{'cmd' : 'ClearCache' , 'args' : None});
      if host.getAttr(ip,'imageDisplay'):
        imageHosts.append(ip)
      if host.getAttr(ip,'hasPanel'):
        panelHosts.append(ip)
      if host.getAttr(ip,'phraseDisplay'):
        phraseHosts.append(ip)

    while True:
      cacheId = random.randint(10000,20000)
      if self.searchType == 'Archive':
        images=[]
        choices=[]
        [images,choices] = archive.getArchive()
        if debug:
          for i in images:
            syslog.syslog("%s: image %s"%(self.name,i))
          for c in choices:
            syslog.syslog("%s: choice %s"%(self.name,c))
      else:
        syslog.syslog("%s unimplemented type %s"%(self.name,self.searchType))

      if len(imageHosts) != 0:
        numImages = len(images)
        imagesPerHost = numImages/len(imageHosts)
        extraImages = numImages % len(imageHosts)
        extra = 0
        count = 0
        syslog.syslog(
              "%s numImages:%d imagesPerHost:%d extraImages:%d"
              %(self.name,numImages,imagesPerHost,extraImages))
        for ip in imageHosts:
          args = {}
          args['id'] = cacheId
          args['imgData'] = []
          for i in range(0,imagesPerHost):
            fname = images[i+count]
            args['imgData'].append(setImgData(fname))
          count += imagesPerHost
          if extra < extraImages:
            fname = images[count+extra]
            args['imgData'].append(setImgData(fname))
            extra += 1
          cmd = {'cmd' : "AddImage", 'args' : args}
          if host.isLocalHost(ip):
            DisplayHandler.addImage(args)
          else:
            host.sendToHost(ip,cmd)

        for ip in panelHosts:
          syslog.syslog("%s: sending phrase to ip:%s"%self.name)

        for ip in phraseHosts:
          syslog.syslog("%s: sending phrase to ip:%s"%self.name)

      for h in hosts:
        ip = h['ip']
        args =[cacheId]
        if host.isLocalHost(ip):
          DisplayHandler.setImageDir(args)
        else:
          host.sendToHost(ip,{'cmd' : 'SetImageDir' , 'args' : None});

      if lastCacheId != 0:
        for h in hosts:
          ip = h['ip']
          args =[lastCacheId]
          if host.isLocalHost(ip):
            DisplayHandler.rmCacheDir(args)
          else:
            host.sendToHost(ip,{'cmd' : 'RmCacheDir' , 'args' : args});
      lastCacheId = cacheId
      sleepTime = config.specs['masterSleepInterval']  
      syslog.syslog("%s: sleeping %d"%(self.name,sleepTime))
      time.sleep(sleepTime)
      