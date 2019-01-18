#!/usr/bin/env python
import os
import sys
home = os.environ['HOME']
proj = home+"GitProjects/iAltar"
sys.path.append(proj+"/iAltar")
sys.path.append(proj+"/config")
sys.path.append(proj+"/common")
sys.path.append(proj+"/server")
import threading
import time
import archive
import DisplayHandler
import random
import config
import host
import base64
import PhraseHandler
import google
import words
import json
import requests
import re
import urllib2
import datetime
import traceback
import ssl


searchType=None

def setSearchType(t):
  global searchType
  searchType = t[0]
  return host.jsonStatus("ok")

def setImgData(fname):
  with open(fname,"rb") as ImageFile:
    d = {}
    d['name'] = os.path.basename(fname)
    d['img'] = base64.b64encode(ImageFile.read())
  return d

def urlsToImages(urls):
  cdir = archive.clearArchive()
  imageCount = 0
  images = []
  for url in urls:
    if debug: print( "url:%s"%url)
    imageTypes=['full','thumb']
    raw_img=None
    for t in imageTypes:
      try:
        #startTime = time.time()
        if debug: print( "open image type:"+t+" image:",url[t] )
        req = urllib2.Request(url[t],headers={'User-Agent' : "Magic Browser"})
        gcontext = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
        con = urllib2.urlopen( req, context=gcontext )
        raw_img = con.read()
        #raw_img = urllib2.urlopen(images[imageIndex]).read()
        #if debug: print( "elapsed:"+str(time.time() - startTime))
        break;
      except:
        print("return from exception for type %s url %s"%(t,url[t]))
        #print("elapsed:"+str(time.time() - startTime))
        #print(datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'))
        #print(traceback.format_exc())
        continue;
    if raw_img != None:
      fname = "%s/urlimage%d.jpg"%(cdir,imageCount)
      imageCount += 1
      f = open(fname,"wb")
      f.write(raw_img)
      f.close()
      images.append(fname)
  return images

debug=True
class masterThread(threading.Thread):
  def __init__(self):
    super(masterThread,self).__init__()
    self.name = "masterThread"
    print("starting: %s"%self.name)
    global searchType
    searchType = config.specs['defaultSearchType'];
    print("%s: default search type: %s"%(self.name,searchType))

  def run(self):
    global searchType
    print("%s in run loop"%self.name)
    hosts = host.getHosts()
    imageHosts = []
    phraseHosts = []
    lastCacheId = 0
    for h in hosts:
      ip = h['ip']
      if host.isLocalHost(ip):
        DisplayHandler.clearCache(None)
      else:
        host.sendToHost(ip,{'cmd' : 'ClearCache' , 'args' : None});
      dtype = host.getAttr(ip,'displayType')
      print("%s: display type: %s"%(self.name,dtype))
      if dtype == 'Image':
        imageHosts.append(ip)
      if dtype == 'Phrase':
        phraseHosts.append(ip)

    while True:
      cacheId = random.randint(10000,20000)
      images=[]
      choices=[]
      urls=[]
      if searchType == 'Archive':
        [images,choices] = archive.getArchive()
        if debug:
          for i in images:
            print("%s: image %s"%(self.name,i))
          for c in choices:
            print("%s: choice %s"%(self.name,c))
      elif searchType == 'Google':
        choices = words.getWords()
        urls = google.getUrls(choices);
        if urls == None:
          print("%s Google Error switching to Archive"%self.name)
          searchType = "Archive"
          continue
        if len(urls) == 0:
          print("%s Nothing found try again"%self.name)
          continue
        images = urlsToImages(google.getUrls(choices));
      else:
        print("%s unimplemented type %s switching to archive"%(self.name,searchType))
        searchType = 'Archive'

      if len(imageHosts) != 0:
        numImages = len(images)
        imagesPerHost = numImages/len(imageHosts)
        extraImages = numImages % len(imageHosts)
        extra = 0
        count = 0
        print(
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


        for ip in imageHosts:
          args =[cacheId]
          if host.isLocalHost(ip):
            DisplayHandler.setImageDir(args)
          else:
            host.sendToHost(ip,{'cmd' : 'SetImageDir' , 'args' : args});

        if lastCacheId != 0:
          for ip in imageHosts:
            args =[lastCacheId]
            if host.isLocalHost(ip):
              DisplayHandler.rmCacheDir(args)
            else:
              host.sendToHost(ip,{'cmd' : 'RmCacheDir' , 'args' : args});
        lastCacheId = cacheId

      if len(phraseHosts) != 0:
        for ip in phraseHosts:
          args = {}
          args['phrase'] = choices
          print("%s sending %s to %s"%(self.name,choices,ip))
          if host.isLocalHost(ip):
            PhraseHandler.setPhrase(args)
          else:
            host.sendToHost(ip,{'cmd' : 'Phrase' , 'args' : args});
    
      sleepTime = config.specs['masterSleepInterval']  
      print("%s: sleeping %d"%(self.name,sleepTime))
      time.sleep(sleepTime)
    
