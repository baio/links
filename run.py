__author__ = 'baio'

#! /usr/bin/env python

from os import fork, chdir, setsid, umask
from sys import exit
import os
import sys
import time
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

print "run server with config"
lines = [x.strip() for x in open(".env")]
for line in lines:
    spt=line.split("=")
    print spt
    os.environ[spt[0]] = spt[1]


from server.server import run


max_attempts = 3
for i in xrange(max_attempts):
    try:
        run()	
    except:
        time.sleep(10)


