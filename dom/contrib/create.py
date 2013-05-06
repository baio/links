__author__ = 'baio'

import pymongo as mongo
import datetime as dt
from config.config import config


def create(user_name, contrib_name, url):
    """create new contrib for the user"""
    client = mongo.MongoClient(config["MONGO_URI"])
    db = client.links
    now = dt.datetime.now()

    contrib = {"name": contrib_name, "date": now, "url": url}

    db.user.update({"_id": user_name}, {"$push" : { "contribs" :  contrib}})
    db.contribs.insert({"_id": user_name+"_"+contrib_name})

