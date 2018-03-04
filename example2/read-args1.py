#!/usr/bin/python
# modified program to interprete 1st two args as env variables.
import sys,os

try:
  print 'arg list is ',sys.argv[1],sys.argv[2],sys.argv[3]
  print "all env variables ",os.environ
  print "arg 1 is ",os.environ[sys.argv[1]]
  print "arg 2 is ",os.environ[sys.argv[2]]
  print "arg 3 is ",sys.argv[3]
except Exception as e:
  print 'arg list is ',sys.argv[1],sys.argv[2],sys.argv[3]
  print 'exception is ',e
  print 'argv error from',sys.argv[0]
  sys.exit(1)

print 'exit program ',sys.argv[0],'\n\n'
sys.exit(0)

