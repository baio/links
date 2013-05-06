__author__ = 'baio'

import pymongo as mongo
from config.config import config

def _json2dom(item):
    dom = {"name_1": item["name_1"], "name_2": item["name_2"]}
    if item["_id"] is not None:
        dom["_id"] = item["_id"]
    else:
        dom["_id"] = item["name_1"] + "_" + item["name_2"]
    dom["tags"] = []
    rel = item.get("family_rel", None)
    if rel is not None: dom["tags"].append({"name": rel, "type": "family"})
    rel = item.get("prof_rel", None)
    if rel is not None: dom["tags"].append({"name": rel, "type": "prof"})
    rel = item.get("private_rel", None)
    if rel is not None: dom["tags"].append({"name": rel, "type": "private"})
    return dom

def merge(user_name, contrib_name, data):
    """append/modify/delete items in contrib"""
    client = mongo.MongoClient(config["MONGO_URI"])
    db = client.links

    crt_items = []
    for item in filter(lambda x: x["_id"] is None, data):
        dom = _json2dom(item)
        crt_items.append(dom)

    upd_items = []
    for item in filter(lambda x: x["_id"] is not None and "_remove" not in x, data):
        dom = _json2dom(item)
        upd_items.append(dom)

    rm_ids = []
    for item in filter(lambda x: "_remove" in x, data):
        rm_ids[item["_id"]]

    if len(crt_items) > 0:
        db.contribs.update({"_id": user_name +"_"+ contrib_name}, {"$pushAll" : {"items" : crt_items}})

    if len(upd_items) > 0:
        for upd_item in upd_items:
            db.contribs.update({"_id": user_name +"_"+ contrib_name, "items._id": upd_item["_id"]}, {"$set": {"items.$" : upd_item}})
    #Waiting for the miracle to come, https://jira.mongodb.org/browse/SERVER-831
    #cnt = db.user.find({"_id": user_name, "contribs.name": contrib_name}, {"contribs.$.data": {"$elemMatch": {"_id" : "name_1_name_3"}}})

    if len(rm_ids) > 0:
        db.contribs.remove({"_id": {"$in" : rm_ids}})


