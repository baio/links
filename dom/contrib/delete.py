__author__ = 'baio'

import pymongo as mongo
from  bson.objectid import ObjectId
from config.config import config

def delete(user_name, contrib_id):
    """delete contrib for the user"""
    client = mongo.MongoClient(config["MONGO_URI"])
    db = client[config["MONGO_DB"]]

    db.users.update({"_id": user_name}, {"$pull" : {"contribs" : {"ref" : contrib_id}} })
    db.users.update({"_id": user_name}, {"$pull" : {"graphs.contribs" : contrib_id} })
    db.contribs.remove({"_id" : ObjectId(contrib_id)})

