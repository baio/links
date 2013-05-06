__author__ = 'baio'

import pymongo as mongo
import datetime as dt
from config.config import config

def delete(user_name, contrib_name):
    """delete contrib for the user"""
    client = mongo.MongoClient(config["MONGO_URI"])
    db = client.links

    db.user.remove({"user": user_name, "name": contrib_name})

