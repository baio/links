__author__ = 'baio'

import pymongo as mongo
from  bson.objectid import ObjectId
from config.config import config

def _prepare(data):
    for item in data:
        if "name_1" in item and item["name_2"] > item["name_1"]:
            n = item["name_2"]
            item["name_2"] = item["name_1"]
            item["name_1"] = n

def _validate(data):
    #names not empty
    #names consists of 2 words
    #one of the rel exists
    #existsent rel not empty
    #es similar names
    #es similar rels
    return [{"errs": [], "warns": []}] * len(data)

def _json2dom(item):
    dom = {"name_1": item["name_1"], "name_2": item["name_2"]}
    if item["_id"] is not None:
        dom["_id"] = ObjectId(item["_id"])
    else:
        dom["_id"] = ObjectId()
    dom["tags"] = []
    rel = item.get("family_rel", None)
    if rel is not None: dom["tags"].append({"name": rel, "type": "family"})
    rel = item.get("prof_rel", None)
    if rel is not None: dom["tags"].append({"name": rel, "type": "prof"})
    rel = item.get("private_rel", None)
    if rel is not None: dom["tags"].append({"name": rel, "type": "private"})
    return dom

def merge(user_name, contrib_id, data):
    _prepare(data)
    _validate(data)
    """append/modify/delete items in contrib"""
    client = mongo.MongoClient(config["MONGO_URI"])
    db = client[config["MONGO_DB"]]
    """
    contrib_ref = db.users.find_one({"_id": user_name, "contribs.name": contrib_name},
                                    {"contribs.$.ref" : 1})["contribs"][0]["ref"]
    """
    contrib_ref = ObjectId(contrib_id)

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
        rm_ids.append(ObjectId(item["_id"]))

    res = map(lambda x: {"id": x["_id"], "errs": [], "warns": []}, crt_items)

    if len(crt_items) > 0:
        db.contribs.update({"_id": contrib_ref}, {"$pushAll" : {"items" : crt_items}})

    if len(upd_items) > 0:
        for upd_item in upd_items:
            db.contribs.update({"_id": contrib_ref, "items._id": upd_item["_id"]}, {"$set": {"items.$" : upd_item}})

        #Waiting for the miracle to come, https://jira.mongodb.org/browse/SERVER-831
        #cnt = db.user.find({"_id": user_name, "contribs.name": contrib_name}, {"contribs.$.data": {"$elemMatch": {"_id" : "name_1_name_3"}}})

    if len(rm_ids) > 0:
        db.contribs.update({"_id" : contrib_ref},
                            {"$pull": {"items" : {"_id" : {"$in" : rm_ids}}}})

    return res
