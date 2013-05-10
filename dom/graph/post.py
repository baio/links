# -*- coding: utf-8 -*-
__author__ = 'baio'

import pymongo as mongo
from config.config import config
from  bson.objectid import ObjectId


def post_contrib(contrib_id, nodes):
    client = mongo.MongoClient(config["MONGO_URI"])
    db = client[config["MONGO_DB"]]
    contrib_meta = db.contribs.meta.find_one({"_id" : ObjectId(contrib_id)})
    def map_node_meta(node):
        return {"id": node["id"], "pos" : node["meta"]["pos"]}
    nodes_meta = map(map_node_meta, nodes)
    for meta in nodes_meta:
        f = db.contribs.meta.find({"_id": ObjectId(contrib_id), "nodes.id": meta["id"]}).count()
        if f == 0:
            db.contribs.meta.update({"_id": ObjectId(contrib_id)}, {"$push" : {"nodes": meta}},upsert=True)
        else:
            db.contribs.meta.update({"_id": ObjectId(contrib_id), "nodes.id": meta["id"]}, {"$set" : {"nodes.$": meta}})

