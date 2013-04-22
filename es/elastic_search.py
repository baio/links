# -*- coding: utf-8 -*-
__author__ = 'baio'

import requests as req
import simplejson as json
import yaml

_elastic_host_url = "http://localhost:9200/"

def _req_hits(q):
    res = req.get(_elastic_host_url + q)
    hits = yaml.load(res.content)["hits"]["hits"]
    return hits


def _req(name, q):
    hits = _req_hits(q)
    if len(hits):
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


def _append(names, q, field_name):
    r = []
    for name in names:
        res = req.post(_elastic_host_url + q + name.replace(" ", "_"), data=json.dumps({field_name: name}))
        r.append(res.json()["ok"])
    return r


def append_names(names):
    return _append(names, "names/name/", "name")


def get_names(term):
    hits = _req_hits("names/name/_search?q=name:"+term+"~0.7")
    res = map(lambda x: {"key": x["_id"], "val": x["_source"]["name"]}, hits)
    return json.dumps(res)


def get_tags(term):
    hits = _req_hits("tags/tag/_search?q=tag:"+term+"~0.7")
    res = map(lambda x: {"key": x["_id"], "val": x["_source"]["tag"]}, hits)
    return json.dumps(res)


def _init(dir):
    with open(dir + "/names.txt") as f:
        _append(filter(lambda x: x, map(lambda x: x.strip("\r\n "), f.readlines())), "names/name/", "name")
    with open(dir + "/tags.txt") as f:
        _append(filter(lambda x: x, map(lambda x: x.strip("\r\n "), f.readlines())), "tags/tag/", "tag")
