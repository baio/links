__author__ = 'baio'

import pymongo as mongo
import datetime as dt
from config.config import config
from  bson.objectid import ObjectId

def copy(user_id, contrib_ref_from):

    client = mongo.MongoClient(config["MONGO_URI"])
    db = client[config["MONGO_DB"]]

    src_user = db.users.find_one({"contribs.ref": contrib_ref_from}, {"name": 1, "contribs.$": 1})

    if src_user["_id"] == user_id:
        raise ValueError("Contib couldn't be copied to the same user")

    user_contrib =  src_user["contribs"][0]
    contrib = db.contribs.find_one({"_id": ObjectId(contrib_ref_from)})
    contrib["_id"] = ObjectId()

    user_contrib.update({"ref": str(contrib["_id"]), "date": dt.datetime.now(),
                         "copied_from": {"user": src_user["_id"], "contrib": contrib_ref_from}})

    db.contribs.insert(contrib)

    db.users.update({"_id": user_id}, {"$push" : {"contribs" :  user_contrib}})


