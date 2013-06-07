__author__ = 'baio'
import pymongo as mongo
from config.config import config


def get_scheme(user_name, contrib_id):
    client = mongo.MongoClient(config["MONGO_URI"])
    db = client[config["MONGO_DB"]]
    user = db.users.find_one({"_id": user_name, "contribs.ref": contrib_id}, {"contribs.$.scheme_ref" : 1})
    if user:
        res = db.contribs.scheme.find_one({"_id": user["contribs"][0]["scheme_ref"]})
        del res["_id"]
        return res
    else:
        return None


