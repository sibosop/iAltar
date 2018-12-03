#!/usr/bin/env python
import os
import sys
proj = os.environ['HOME'] + "//GitProjects/iAltar"
sys.path.append(proj+"/config")
sys.path.append(proj+"/common")
sys.path.append(proj+"/server")
import iAltarServer
import syslog
import argparse
import config
import datetime


if __name__ == '__main__':
  try:
    pname = sys.argv[0]
    syslog.syslog(pname+" at "+datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'))
    os.environ['DISPLAY']=":0.0"
    os.chdir(os.path.dirname(sys.argv[0]))
    parser = argparse.ArgumentParser() 
    parser.add_argument('-d','--debug', action = 'store_true',help='set debug')
    parser.add_argument('-c','--config',nargs=1,type=str,default=[config.defaultSpecPath],help='specify different config file')
    args = parser.parse_args()
    if debug: syslog.syslog("config path"+args.config[0])
    config.load(args.config[0])
    sst = soundServer.soundServerThread(8080)
    sst.setDaemon(True)
    sst.start()
  except Exception, e:
    syslog.syslog("config error:"+str(e))
    exit(5)

  