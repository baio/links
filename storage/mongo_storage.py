__author__ = 'baio'

import pymongo as mongo
from converters import contrib2gexf as contrib
import datetime as dt

def store(lines):
    client = mongo.MongoClient('ds039447.mongolab.com', 39447)
    db = client.links
    bucks = contrib.parse_lines(lines)
    now = dt.now()
    ctb = {
        "name": "{}_{}".format("baio", now),
        "data": bucks,
        "date": dt
    }
    db.insert(ctb)

