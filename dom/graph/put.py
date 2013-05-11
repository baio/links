# -*- coding: utf-8 -*-
__author__ = 'baio'

import pymongo as mongo
from config.config import config

def put(user_name, graph_id, graph_name, contribs):
    """create new graph for the user"""
    client = mongo.MongoClient(config["MONGO_URI"])
    db = client[config["MONGO_DB"]]

    db.users.update({"_id": user_name, "graphs.ref": graph_id}, {"$set": {"graphs.$.name": graph_name, "graphs.$.contribs":  contribs}})
    return db.users.find_one({"_id": user_name, "graphs.ref": graph_id}, {"graphs.$" : 1})["graphs"][0]


