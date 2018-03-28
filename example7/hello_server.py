#!/usr/bin/python -u
#
# Simple HTTP server/receiver to use with in docker container.
#   return HTML hello message.
# command line: 
#     hello_server.py  
#
# credit to: bradmontgomery at https://gist.github.com/bradmontgomery/2219997
# R. Melton
# 3/27/18

"""
Very simple HTTP receiver in python.
"""
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import SocketServer, platform
import cgi, json, sys, ast, datetime
import time, os, string,urlparse
from termcolor import colored
import socket

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
        myhost = platform.node()
        hello_msg="hello from host: "+myhost
        print hello_msg
        self.wfile.write("<html><body><h1>"+hello_msg+"</h1></body></html>")
        self.send_response(200)
        print "got GET msg"
    def do_HEAD(self):
        self._set_headers()
        self.send_response(200)
        print "got HEAD msg"
    def do_POST(self):
        self._set_headers()
        self.send_response(200)
        print "got POST msg"
        
        
def run(server_class=HTTPServer, handler_class=S,bind_address='3.0.0.11', bind_port=81):
    server_address = (bind_address, bind_port)
    httpd = HTTPServer(server_address, S)
    print colored('\nAlarm receiver waiting... at:\t'+bind_address+":"+str(bind_port),'cyan')
    start_time = datetime.datetime.now().ctime()
    print colored('Time:             \t\t'+start_time,'cyan')
    httpd.serve_forever()

def run_start(ip,port):
    run(server_class=HTTPServer, handler_class=S,bind_address=ip, bind_port=port)
   

def usage():
    print "usage: sudo alarm_receiver.py <ip_address> <port>"
    sys.exit(1)




if __name__ == "__main__":
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('8.8.8.8', 1))  
    local_ip_address = s.getsockname()[0] #this is just a way to get local address
    print 'starting HTTP server on address ',local_ip_address
    run_start(local_ip_address,81)

  

