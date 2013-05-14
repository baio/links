__author__ = 'baio'
import pymongo as mongo
from config.config import config

def get(user_id):
    client = mongo.MongoClient(config["MONGO_URI"])
    db = client[config["MONGO_DB"]]
    user = db.users.find_one({"_id": user_id})
    return user
