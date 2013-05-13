# -*- coding: utf-8 -*-
__author__ = 'baio'

import pymongo as mongo
from config.config import config
from  bson.objectid import ObjectId
def patch(user_name, graph_id, nodes):
    #TODO: check user ownn graph
    client = mongo.MongoClient(config["MONGO_URI"])
    db = client[config["MONGO_DB"]]
    if db.users.find_one({"_id": user_name, "graphs.ref": graph_id}, {"_id" : 1}) is None:
        return 401
    def map_node_meta(node):
        return {"id": node["id"], "pos" : node["meta"]["pos"]}
    nodes_meta = map(map_node_meta, nodes)
    for meta in nodes_meta:
        f = db.graphs.meta.find({"_id": ObjectId(graph_id), "nodes.id": meta["id"]}).count()
        if f == 0:
            db.graphs.meta.update({"_id": ObjectId(graph_id)}, {"$push" : {"nodes": meta}},upsert=True)
        else:
            db.graphs.meta.update({"_id": ObjectId(graph_id), "nodes.id": meta["id"]}, {"$set" : {"nodes.$": meta}})
    return 200

