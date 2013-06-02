# -*- coding: utf-8 -*-
__author__ = 'baio'

import requests as req
import simplejson as json
import yaml
import os

_elastic_host_url = os.getenv("ES_URI", None)

"""
index - set type
type - field type
l - list with buckets: (key, val)
val_field_name = "val", name of the value field in es
"""
def mset(index, type, l, val_field_name = "val"):
    if not _elastic_host_url or len(l) == 0: return []
    def data2idx(i):
        return u"{}\n{}\n".format(
            json.dumps({"index" : {"_index" : index, "_type" : type, "_id" : i[0]}}),
            json.dumps({val_field_name : i[1]}))
    d = "".join(map(data2idx, l))
    print d
    res = req.post(_elastic_host_url + "/_bulk", data=d)
    content = yaml.load(res.content)
    return map(lambda x: x["index"]["ok"], content["items"])

def get(index, type, val, val_field_name = "val", search_val_field_name = "val.autocomplete"):
    if not _elastic_host_url: return []
    d = { "query" : {
            "fuzzy" : {
                search_val_field_name : val
            }
        }
    }
    res = req.post(_elastic_host_url + "/" + index + "/" + type + "/_search", data=json.dumps(d))
    hits = yaml.load(res.content)["hits"]
    hits = hits["hits"] if len(hits) > 0 else []
    return map(lambda x: (x["_id"], x["_source"][val_field_name]), hits)
