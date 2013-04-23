# -*- coding: utf-8 -*-
__author__ = 'baio'

import requests as req
import simplejson as json
import yaml

_elastic_host_url = "http://localhost:9200/"

def _req_hits(q):
    res = req.get(_elastic_host_url + q)
    hits = yaml.load(res.content)["hits"]
    return hits["hits"] if len(hits) > 0 else []


def _req(q):
    hits = _req_hits(q)
    if len(hits):
        return hits[0]["_source"]
    else:
        return None


def get_similar_names(names):
    for name in names:
        sim_name = False
        spts = name.split(' ')
        if len(spts) == 2:
            sim_name = _req(u"names/name/_search?q=(fname:{0}~0.7 AND lname:{1}~0.7) OR (fname:{1}~0.7 AND lname:{0}~0.7)"
                .format(spts[0], spts[1]))
            if sim_name:
                if sim_name["fname"] == spts[0] and sim_name["lname"] == spts[1]:
                    sim_name = True
                else:
                    sim_name = u"{} {}".format(sim_name["fname"], sim_name["lname"])
        yield sim_name


def check_tags(tags):
    for tag in tags:
        yield True if _req("tags/tag/_search?q=tag:"+tag) else False


def _append(q, name_items_dict):
    r = []
    for name in name_items_dict:
        res = req.post(_elastic_host_url + q + name.replace(" ", "_"), data=json.dumps(name_items_dict[name]))
        r.append(res.json()["ok"])
    return r


def append_names(names):
    ns = map(lambda x: {"fname" : x.split(' ')[0], "lname" : x.split(' ')[1]}, names)
    return _append("names/name/", dict(zip(names, ns)))

def append_tags(tags):
    ts = map(lambda x: {"tag" : x}, tags)
    return _append("tags/tag/", dict(zip(tags, ts)))

def get_names(term):
    hits = _req_hits("names/name/_search?q=lname:"+term+"~0.7")
    return map(lambda x: {"key": x["_id"], "val": x["_source"]["name"]}, hits)

def get_names_json(term):
    res = get_names(term)
    return json.dumps(res)

def get_tags(term):
    hits = _req_hits("tags/tag/_search?q=tag:"+term+"~0.7")
    return map(lambda x: {"key": x["_id"], "val": x["_source"]["tag"]}, hits)

def get_tags_json(term):
    res = get_tags(term)
    return json.dumps(res)


def _init(dir):
    with open(dir + "/names.txt") as f:
        append_names(filter(lambda x: x, map(lambda x: x.strip("\r\n "), f.readlines())))
    with open(dir + "/tags.txt") as f:
        append_tags(filter(lambda x: x, map(lambda x: x.strip("\r\n "), f.readlines())))
