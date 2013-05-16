__author__ = 'baio'

import os
import sys
import time
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from server.server import run
lines = [x.strip() for x in open(".env")]

print "run server with config"
for line in lines:
    spt=line.split("=")
    print spt
    os.environ[spt[0]] = spt[1]

max_attempts = 3
for i in xrange(max_attempts):
    try:
        run()
    except:
        time.sleep(10)
