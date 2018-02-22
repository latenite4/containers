#!/usr/bin/python
#
# Simple HTTP server/receiver to use to listen for incoming HTTP messages
# command line: 
#     lifecycle_listener.py IPaddress port  (try port 5623)
#
# credit to: bradmontgomery at https://gist.github.com/bradmontgomery/2219997
# R. Melton
# 3/12/16

"""
Very simple HTTP receiver in python.
"""
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import SocketServer
import cgi, json, sys, ast, datetime
import time, os, string,urlparse
from termcolor import colored

# HTTP message handler class
class S(BaseHTTPRequestHandler):

    # overload base class log routine to turn OFF unwanted output
    def log_message(self, format, *args):
        return

    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        self._set_headers()
        self.wfile.write("<html><body><h1>hi!</h1></body></html>")
        self.send_response(200)
        print "got GET msg"
    def do_HEAD(self):
        self._set_headers()
        self.send_response(200)
        print "got HEAD msg"
    def do_POST(self):
        self.send_response(200)
        length = int(self.headers.getheader('content-length'))
        data = cgi.parse_qs(self.rfile.read(length), keep_blank_values=1)
        self._set_headers()
        self.wfile.write("<html><body><h1>ok</h1></body></html>")
        ctype, pdict = cgi.parse_header(self.headers['content-type'])
        data = data.keys()[0]
        json_struct = json.loads(data)
        
        #recover the incoming URL and parse it
        url =  'http://'+self.server.server_address[0]+':'+str(self.server.server_address[1])+self.path
        parsed = urlparse.parse_qs(urlparse.urlparse(url).query)
        tenant = parsed['tenant'][0]
        vmid = parsed['VMID'][0]
        #print '\n\n',url ,tenant, vmid 
              
        data = ast.literal_eval(data)

        alarm = data["alarm_name"]
        now = data["current"]
        alarm_name = data["alarm_name"]
        reason_data = data["reason_data"]
        cpu_avg = reason_data["most_recent"]
        prev = data["previous"]
           
        alarm_rcvd_time = datetime.datetime.now().ctime()
        # print results
        if now.find('ok') < 0:
           #print alarm_rcvd_time ,alarm,now, " CPU ",cpu_avg
           print colored(alarm_rcvd_time , 'white'),colored(alarm, 'red'), colored(now, 'red'),colored("CPU%", 'red'),colored(cpu_avg, 'red'),colored('\t('+tenant+' '+vmid+')' , 'white')
        else:
           print colored(alarm_rcvd_time , 'white'),colored(alarm, 'green'), colored(now, 'green'),colored("\tCPU%", 'green'),colored(cpu_avg, 'green'),colored('\t('+tenant+' '+vmid+')' , 'white')
           
        
        
def run(server_class=HTTPServer, handler_class=S,bind_address='3.0.0.11', bind_port=81):
    server_address = (bind_address, bind_port)
    httpd = HTTPServer(server_address, S)
    print colored('\nLifecycle_listener  listening at:\t'+bind_address+":"+str(bind_port),'cyan')
    start_time = datetime.datetime.now().ctime()
    print colored('Time:             \t\t'+start_time,'cyan')
    httpd.serve_forever()

def run_start(ip,port):
    run(server_class=HTTPServer, handler_class=S,bind_address=ip, bind_port=port)
   

def usage():
    print "usage: sudo lifecycle_listener.py <ip_address> <port>"
    sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        usage()
        sys.exit(1)

    run_start(sys.argv[1],string.atoi(sys.argv[2],10))

  

