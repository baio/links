# -*- coding: utf-8 -*-
__author__ = 'baio'
from dom.connection import get_db
from  bson.objectid import ObjectId

def get(user_name, contrib_ref):
    db = get_db()
    user = db.users.find_one({"_id": user_name, "contribs.ref": contrib_ref}, {"contribs.$" : 1})
    contrib_ref = db.contribs_v2.find_one({"_id" : ObjectId(contrib_ref)})
    contrib = user["contribs"][0]
    contrib["items"] = contrib_ref.get("items", [])[::-1]
    if "schemes" in contrib:
        contrib["schemes"] = list(db.contribs.scheme.find({"_id": { "$in" : contrib["schemes"]}}))
    for item in contrib["items"]:
        item["_id"] = str(item["_id"])
        item["name_1"] = item["object"]
        item["name_2"] = item["subject"]
        item["relations"] = item["predicates"]
    return contrib


