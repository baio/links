__author__ = 'baio'
import pymongo as mongo
from config.config import config
from  bson.objectid import ObjectId

def get(user_name):
    client = mongo.MongoClient(config["MONGO_URI"])
    db = client[config["MONGO_DB"]]
    user = db.users.find({}, {"contribs" : 1}).limit(50)
    return sum(map(lambda x: x["contribs"], user), [])


