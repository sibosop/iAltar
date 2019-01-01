#!/usr/bin/env python
import os
import sys
home = os.environ['HOME']
proj = home+"GitProjects/iAltar"
sys.path.append(proj+"/iAltar")
sys.path.append(proj+"/config")
sys.path.append(proj+"/common")
sys.path.append(proj+"/server")
import glob
import random
import subprocess
import os
import sys
import syslog
import time
import config
import DisplayHandler

debug=False

global init
init=False
archives=[]
def getArchiveCache():
  path = "%s/%s/archiveCache"%(home,config.specs['tmpdir'])
  return DisplayHandler.mkpath(path)

def getArchive():
  global init
  adir=config.specs["archiveDir"]
  cdir=getArchiveCache()
  if init == False:
    if debug: syslog.syslog("init seed")
    random.seed()
    init=True
    for a in glob.glob(adir+"/*.tgz"):
      if debug: syslog.syslog ("a: %s"%a)
      archives.append(a)
  files = glob.glob(cdir+"/*")
  for f in files:
    os.remove(f)
  n = random.randint(0,len(archives)-1)
  syslog.syslog("n:"+str(n)+" archive:"+archives[n])
  try:  
    cmd=["tar","xzf",archives[n],"-C",cdir]
    if debug: syslog.syslog( "cmd: %s"%cmd)
    subprocess.check_output(cmd)
  except subprocess.CalledProcessError, e:
    syslog.syslog("archive problem: "+', '.join(cmd)+str(e.output))
  images=[]
  choices=[]
  try:
    for a in glob.glob(cdir+"/*.jpg"):
      if debug: syslog.syslog("archive image %s"%a)
      images.append(a);
  except:
    e = sys.exc_info()[0]
    syslog.syslog("return from archive image append "+str(e))
  
  textName=cdir+"/"+config.specs['archiveTextName']
  if debug: syslog.syslog("textName %s"%textName)
  try:  
    with open(textName) as fp:
      for line in fp:
        if debug: syslog.syslog(line.rstrip())
        choices.append(line.rstrip())
  except:
    e = sys.exc_info()[0]
    syslog.syslog("choice name append "+str(e))

  return [images,choices]
  
    

if __name__ == '__main__':
  rval=getArchive()
  images=rval[0]
  choices=rval[1]
  for i in images:
    print i
  for i in choices:
    print i
