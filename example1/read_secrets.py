#!/usr/bin/python
import sys
# read username and password files
filepath='/etc/secrets/'
try:
  fu = open(filepath+'username','r')
  fp = open(filepath+'password','r')
except:
  print 'file open error'
  sys.exit(1)

username  = fu.read()
password  = fp.read()

print 'password ',password,'  username ',username,'\n\n'

