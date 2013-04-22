# -*- coding: utf-8 -*-
__author__ = 'baio'

import requests as req
import json
import yaml

_elastic_host_url = "http://localhost:9200/"

def _req(name, q):
    res = req.get(_elastic_host_url + q)
    hits = yaml.load(res.content)["hits"]["hits"]
    if len(hits) != 0:
        return hits[0]["_source"][name]
    else:
        return False

def get_similar_names(names):
    for name in names:
        sim_name = _req("name", "names/name/_search?q=name:"+name+"~0.7")
        if sim_name:
            if sim_name == name:
                sim_name = True
        yield sim_name

def check_tags(tags):
    for tag in tags:
        yield True if _req("tag", "tags/tag/_search?q=tag:"+tag) else False

def append_names(names):
    r = []
    for name in names:
        res = req.post(_elastic_host_url + "names/name/" + name.replace(" ", "_"), data=json.dumps({"name": name}))
        r.append(res.json()["ok"])
    return r
