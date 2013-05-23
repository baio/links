__author__ = 'baio'
import pymongo as mongo
from config.config import config
from  bson.objectid import ObjectId

def get(user_name, contrib_ref):
    client = mongo.MongoClient(config["MONGO_URI"])
    db = client[config["MONGO_DB"]]
    user = db.users.find_one({"contribs.ref": contrib_ref}, {"contribs.$.ref" : 1})
    contrib_ref = db.contribs.find_one({"_id" : ObjectId(contrib_ref)})
    contrib = user["contribs"][0]
    contrib["items"] = contrib_ref.get("items", [])[::-1]
    for item in contrib["items"]:
        item["_id"] = str(item["_id"])
        for tag in item["tags"]:
            item["{}_rel".format(tag["type"])] = tag["name"]
        del item["tags"]
    return contrib


