
#!/usr/bin/env python
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
from SocketServer import ThreadingMixIn
import threading
import time
import syslog
import os
import sys
home = os.environ['HOME']
proj = home+"GitProjects/iAltar"
sys.path.append(proj+"/iAltar")
sys.path.append(proj+"/config")
sys.path.append(proj+"/common")
sys.path.append(proj+"/server")
import json
import subprocess
import urlparse
import CmdHandler

debug=True

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """ This class allows to handle requests in separated threads.
            No further content needed, don't touch this. """

def jsonStatus(s):
  d = {}
  d['status'] = s
  return json.dumps(d)

class MyHandler(BaseHTTPRequestHandler):
  def do_HEAD(s):
    s.send_response(200)
    s.send_header("Content-type", "text/html")
    s.end_headers()

  def log_message(self, format, *args):
    syslog.syslog("%s - - [%s] %s\n" %
                         (self.address_string(),
                          self.log_date_time_string(),
                          format%args))

  def do_POST(self):
    # Begin the response
    content_len = int(self.headers.getheader('content-length', 0))
    post_body = self.rfile.read(content_len)
    
    if debug: syslog.syslog("Post:"+str(post_body))
    status = CmdHandler.handleCmd(json.loads(post_body))

    self.send_response(200)
    self.end_headers()
    self.wfile.write(status)
    s = json.loads(status)
    #if debug: syslog.syslog("handle cmd:"+str(s));
    if s['status'] == "poweroff":
      os._exit(3)
    if s['status'] == "reboot":
      os._exit(4)
    if s['status'] == "stop":
      os._exit(5)
    return


class iAltarServerThread(threading.Thread):
  def __init__(self,port):
    super(iAltarServerThread,self).__init__()
    host = subprocess.check_output(["hostname","-I"]).split();
    self.host = host[0]
    self.port = port
    syslog.syslog("%s %s %d"%(self.name,self.host,self.port))
    self.server = ThreadedHTTPServer((self.host, self.port), MyHandler)

  def run(self):
    syslog.syslog("starting server")
    self.server.serve_forever()
    syslog.syslog("shouldn't get here");

