#!/usr/bin/python
import sys

try:
  print "arg 1 is ",sys.argv[1]
  print "arg 2 is ",sys.argv[2]
  print "arg 3 is ",sys.argv[3]
except:
  print 'argv error'
  sys.exit(1)

print 'exit program ',sys.argv[0],'\n\n'
sys.exit(0)

