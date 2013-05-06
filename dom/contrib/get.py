__author__ = 'baio'
import pymongo as mongo
from config.config import config
from  bson.objectid import ObjectId

def get(user_name, contrib_name):
    client = mongo.MongoClient(config["MONGO_URI"])
    db = client[config["MONGO_URI"]]
    contrib_ref = db.users.find_one({"_id": user_name, "contribs.name": contrib_name},
                                    {"contribs.$.ref" : 1})["contribs"][0]["ref"]
    contrib_ref = ObjectId(contrib_ref)
    contrib = db.contribs.find_one({"_id" : contrib_ref})
    return contrib


