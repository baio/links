__author__ = 'baio'

import pymongo as mongo
from  bson.objectid import ObjectId
from config.config import config

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

def patch(user_name, contrib_id, data):
    _validate(data)
    """append/modify/delete items in contrib"""
    client = mongo.MongoClient(config["MONGO_URI"])
    db = client[config["MONGO_DB"]]
    contrib_ref = ObjectId(contrib_id)

    res = map(lambda x: {"_id": x["_id"], "err": [], "warn": []}, data)

    crt_items = []
    for i, item in enumerate(data):
        if item["_id"] is None:
            dom = _json2dom(item)
            crt_items.append(dom)
            res[i]["_id"] = str(dom["_id"])

    upd_items = []
    for item in filter(lambda x: x["_id"] is not None and ("_isRemoved" not in x or not x["_isRemoved"]), data):
        dom = _json2dom(item)
        upd_items.append(dom)

    rm_ids = []
    for item in filter(lambda x: "_isRemoved" in x and x["_isRemoved"], data):
        rm_ids.append(ObjectId(item["_id"]))

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
