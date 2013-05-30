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
list with buckets: (key, val)
"""
def mset(index, type, l):
    if not _elastic_host_url or len(l) == 0: return []
    def data2idx(i):
        return u"{}\n{}\n".format(
            json.dumps({"index" : {"_index" : index, "_type" : type, "_id" : i[0]}}),
            json.dumps({"val" : i[1]}))
    d = "".join(map(data2idx, l))
    res = req.post(_elastic_host_url + "/_bulk", data=d)
    content = yaml.load(res.content)
    return map(lambda x: x["index"]["ok"], content["items"])
