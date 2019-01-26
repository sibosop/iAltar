#!/usr/bin/env python
import sys
import os
import argparse
import platform
import subprocess
home = os.environ['HOME']
sys.path.append(home+"/GitProjects/iAltar/config")
import sys
import json
import urllib2
import config

hosts = []
names = []
specs = {}
timeout = 2
debug=False
port=0

def setHostList():
  global hosts
  if debug: print( "getting host from specs" )
  if config.specs == None:
    config.load()
  if len(hosts) == 0:
    for a in config.specs['hosts']:
      hosts.append(a)
      if 'name' in a:
        names.append(a['name'])
  return hosts

def setHostPort(port_):
  global port
  port = port_


def getHosts():
  global hosts
  if len(hosts) == 0:
    setHostList()
  return hosts
  
def getHostIps():
  rval = []
  for h in hosts:
    rval.append(h['ip'])
  return rval

def printHostList():
  global hosts
  print "Host list:"
  for h in hosts:
    #print "h:",h
    o = h['ip']
    if 'attr' in h:
      if debug: print "attr",h['attr']
      o += " "+h['attr']
    print " ",o
  print

def sendToMaster(cmd):
  for h in hosts:
    if h['isMaster']:
      sendToHost(h['ip'],cmd)
      break

def sendByName(nameList,cmd):
  for n in nameList:
    for h in config.specs['hosts']:
      if h['name'] == n:
        sendToHost(h['ip'],cmd)
        break
        
def sendToHost(ip,cmd):
  rval = True
  try:
    if debug: print "send to host:",ip,cmd
    url = "http://%s:%d"%(ip,port)
    if debug: print("url:"+url)
    if debug: print("cmd json:"+json.dumps(cmd))
    req = urllib2.Request(url
                ,json.dumps(cmd),{'Content-Type': 'application/json'})
    f = urllib2.urlopen(req,None,timeout)
    test = f.read()
    if debug: print("got response:"+test)
  except Exception as e:
    error = "host [%s] send error:%s"%(ip,str(e))
    print(error)
    if debug: print error
    rval = False
  return rval

def sendWithSubnet(ip,cmd):
  for i in ip:
    h = config.specs['subnet']+"."+i
    sendToHost(h,cmd)

def sendToHosts(cmd):
  save = None
  for h in hosts:
    ip = h['ip']
    if isLocalHost(ip):
      save = ip
    else:
      sendToHost(h['ip'],cmd)
  if save is not None:
    sendToHost(save,cmd)
    
def jsonStatus(s):
  d = {}
  d['status'] = s
  return json.dumps(d) 
     

def isLocalHost(ip):
  plats=platform.platform().split('-');
  if plats[0] == 'Darwin':
    return False
  myIp = subprocess.check_output(["hostname","-I"]).split()
  for i in myIp:
    if debug: print("isLocalHost: ip:"+ip+ " myIp:"+i)
    if i == ip:
      if debug: print("isLocalHost is True:"+ip)
      return True
  if debug: print("isLocalHost is False:"+ip)
  return False

def getLocalHost():
  subnet = config.specs['subnet']
  ipList = subprocess.check_output(["hostname","-I"]).split()
  for ip in ipList:
    if subnet in ip:
      if debug: print("local host:"+ip)
      return ip
  return None
  
def getHost(ip):
    getHosts()
    for h in hosts:
      if h['ip'] == ip:
        return h
    print("Can't find ip"+ip)
    return None
    
def getAttr(ip,a):
  rval = getHost(ip)[a]
  if debug: print("Get Attr "+a+":"+str(rval))
  return rval 
  
def getLocalAttr(a):
  rval = getHost(getLocalHost())[a]
  if debug: print("Get Local Attr "+a+":"+str(rval))
  return rval

def internetOn():
  try:
    urllib2.urlopen('http://216.58.192.142', timeout=1)
    return True
  except urllib2.URLError as err: 
    return False

if __name__ == '__main__':
  run=True
  parser = argparse.ArgumentParser()
  parser.add_argument('-d','--debug', action = 'store_true',help='set debug')
  args = parser.parse_args()
  setHostList()
  printHostList()
  for h in hosts:
    if isLocalHost(h['ip']):
      print(h['ip']+"is local host")
