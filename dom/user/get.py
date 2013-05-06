__author__ = 'baio'
import pymongo as mongo
from config.config import config

def get(user_name):
    client = mongo.MongoClient(config["MONGO_URI"])
    db = client[config["MONGO_DB"]]
    return db.users.find_one({"_id": user_name})
