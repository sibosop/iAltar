#!/usr/bin/env python 
import os
import sys
proj = os.environ['HOME'] + "//GitProjects/iAltar"
unbuff = os.environ['PYTHONUNBUFFERED'] 
sys.path.append(proj+"/config")
sys.path.append(proj+"/common")
import random
import	 datetime
import time
import argparse
import host
import watchdog
import config

def doExit(num):
  print "Doing Exit with %d"%num
  sys.stdout.flush()
  sys.stderr.flush()
  os._exit(num)


debug = False
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
    parser.add_argument('-t','--time',nargs=1,type=str,default=[10],help='specify timing loop time')
    args = parser.parse_args()
    debug =args.debug
    loopTime = args.time[0]
    if debug: print("config path"+args.config[0])
    print "config path",args.config
    config.load(args.config[0])
    host.setHostPort(config.specs['iAltarServerPort'])
    host.setHostList()
    host.printHostList()
    while True:
      try:
        for ip in host.getHostIps():
          r = host.hostReq(ip,{'cmd' : "Probe", 'args' : [""] })
          if debug: print("Probe: ip: %s Response:%s"%(ip,r))
        time.sleep(loopTime)
      except KeyboardInterrupt:
        print(pname+": keyboard interrupt")
        doExit(5)
        break
      except Exception as e:
        if e is None:
          print "pname what the fuck e=None"
        else:
          print "%s Main error: %s"%(pname,e)
        doExit(5)
        break
  except Exception, e:
    if e is None:
      print "pname what the fuck e=None"
    else:
      print "%s Main error: %s"%(pname,e)
    doExit(5)
  print(pname+" exiting")
  doExit(0)

