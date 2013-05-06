__author__ = 'baio'

import pymongo as mongo
from config.config import config

def update(user_name, contrib_name, contrib_new_name, new_url):
    """update contrib name, url"""
    client = mongo.MongoClient(config["MONGO_URI"])
    db = client[config["MONGO_DB"]]

    db.users.update({"_id": user_name, "contribs.name" : contrib_name},
                   {"$set" : {"contribs.$.name" :  contrib_new_name, "contribs.$.url" :  new_url}})
