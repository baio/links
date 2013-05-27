__author__ = 'baio'
import pymongo as mongo
from config.config import config

def get_graphs(user_name, contrib_ref):
    client = mongo.MongoClient(config["MONGO_URI"])
    db = client[config["MONGO_DB"]]
    user = db.users.find_one({"_id": user_name, "graphs.contribs": contrib_ref}, {"graphs.ref" : 1})
    return map(lambda x: x["ref"], user["graphs"])
