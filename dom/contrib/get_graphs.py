__author__ = 'baio'
import pymongo as mongo
from config.config import config


def get_graphs(db, user_name, contrib_id):
    if not db:
        client = mongo.MongoClient(config["MONGO_URI"])
        db = client[config["MONGO_DB"]]
    user = db.users.find_one({"_id": user_name, "graphs.contribs": contrib_id}, {"graphs.ref" : 1})
    if user:
        res = map(lambda x: x["ref"], user["graphs"])
        return res
    else:
        return []

