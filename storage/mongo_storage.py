__author__ = 'baio'

import pymongo as mongo
import datetime as dt
from config.config import config

def store(bucks):
    client = mongo.MongoClient(config["MONGO_URI"])#'mongodb://adm:123@ds039447.mongolab.com:39447/links')
    db = client.links
    now = dt.datetime.now()
    data = map(lambda x: {"name_1" : x[0], "name_2" : x[1], "tags" : x[2], "url" : x[3]}, bucks)
    ctb = {
        "_id": "{}_{}".format("baio", now.strftime("%Y%m%dT%M%S")),
        "data": data,
        "date": now
    }
    db.contribs.save(ctb)

