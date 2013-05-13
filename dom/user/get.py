__author__ = 'baio'
import pymongo as mongo
from config.config import config

def get(user_name):
    client = mongo.MongoClient(config["MONGO_URI"])
    db = client[config["MONGO_DB"]]
    user = db.users.find_one({"_id": user_name})
    if not user:
        user = {"_id": user_name, "contribs": [], "graphs": []}
        db.users.insert(user)
    return user
