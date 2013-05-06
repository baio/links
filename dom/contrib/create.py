__author__ = 'baio'

import pymongo as mongo
import datetime as dt
from config.config import config


def create(user_name, contrib_name, url):
    """create new contrib for the user"""
    client = mongo.MongoClient(config["MONGO_URI"])
    db = client[config["MONGO_DB"]]
    now = dt.datetime.now()

    ref = db.contribs.insert({})
    contrib = {"name": contrib_name, "date": now, "url": url, "ref": str(ref)}

    db.users.update({"_id": user_name}, {"$push" : { "contribs" :  contrib}})


