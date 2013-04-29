# -*- coding: utf-8 -*-
__author__ = 'baio'

import requests as req
import simplejson as json
import yaml
from config.config import config

_elastic_host_url = config["ES_URI"]

def _req_hits(q):
    res = req.get(_elastic_host_url + "/" + q)
    hits = yaml.load(res.content)["hits"]
    return hits["hits"] if len(hits) > 0 else []

def _req_hits_multi(q, data):
    d = "{}\n" + "{}\n".join(map(lambda x: json.dumps(x) + "\n", data))
    res = req.get(_elastic_host_url + "/" + q, data=d)
    content = yaml.load(res.content)
    return map(lambda x: x["hits"]["hits"], content["responses"])

def _req_hits_multi_1(index_data):
    """
    index_data - list of buckets:
    index : index/type for es request
    data : [requests]
    """
    index_data = filter(lambda x: len(x[1]) > 0, index_data)
    d = "".join(map(lambda x: u"".join(
                    map(
                        lambda y: "{}\n{}\n".format(json.dumps({"index" : x[0]}),json.dumps(y)),
                        x[1]))
        , index_data))
    res = req.get(_elastic_host_url + "/_msearch", data=d)
    content = yaml.load(res.content)
    hits = map(lambda x: x["hits"]["hits"], content["responses"])

    res = []
    start_bound = 0
    for bound in map(lambda x: len(x[1]), index_data):
        res.append(hits[start_bound:start_bound+bound])
        start_bound += bound

    return res

def _req(q):
    hits = _req_hits(q)
    if len(hits):
        return hits[0]["_source"]
    else:
        return None

def get_similar_names(names):
    def name2q(name):
        spts = name.split(' ')
        return {
            "filter": {
                "query": {
                    "query_string": {
                        "query": u"fname:{}~0.7 AND lname:{}~0.7".format(spts[0], spts[1])
                    }
                }
            }
        }
    def hits2res(name_hits):
        name = name_hits[0]
        hits = name_hits[1]
        if (len(hits) > 0):
            src = hits[0]["_source"]
            if src["fname"] + u" " + src["lname"] == name:
                return True
            else:
                return u"{} {}".format(src["fname"], src["lname"])
        else:
            return False
    if len(filter(lambda x: len(x.split(' ')) != 2, names)) > 0:
        raise ValueError("Name should consists of 2 words separated by space")
    data = filter(None, map(name2q, names))
    hits = _req_hits_multi("names/name/_msearch", data)
    return map(hits2res, zip(names, hits))


"""
def check_tags(tags):
    for tag in tags:
        yield True if _req("tags/tag/_search?q=tag:"+tag) else False
"""

def _append(q, name_items_dict):
    r = []
    for name in name_items_dict:
        res = req.post(_elastic_host_url + "/" + q + name.replace(" ", "_"), data=json.dumps(name_items_dict[name]))
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

def check_tags(tags):
    def tag2q(tag):
        return {
            "filter": {
                "query": {
                    "query_string": {
                        "query": u"tag:%s" % tag
                    }
                }
            }
        }
    def hits2res(hits):
        return len(hits) > 0
    q = map(tag2q, tags)
    hits = _req_hits_multi("tags/tag/_msearch", q)
    return map(hits2res, hits)

def check_tags_and_names(names, tags):
    def name2q(name):
        spts = name.split(' ')
        return {
            "filter": {
                "query": {
                    "query_string": {
                        "query": u"fname:{}~0.7 AND lname:{}~0.7".format(spts[0], spts[1])
                    }
                }
            }
        }
    def tag2q(tag):
        return {
            "filter": {
                "query": {
                    "query_string": {
                        "query": u"tag:%s" % tag
                    }
                }
            }
        }
    def hits2res(name_hits):
        name = name_hits[0]
        hits = name_hits[1]
        if (len(hits) > 0):
            src = hits[0]["_source"]
            if src["fname"] + u" " + src["lname"] == name:
                return True
            else:
                return u"{} {}".format(src["fname"], src["lname"])
        else:
            return False
    def tags2res(hits):
        return len(hits) > 0
    if len(filter(lambda x: len(x.split(' ')) != 2, names)) > 0:
        raise ValueError("Name should consists of 2 words separated by space")
    names_d = map(name2q, names)
    tags_d = map(tag2q, tags)
    names_h, tags_h = _req_hits_multi_1(zip(["names", "tags"], [names_d, tags_d]))
    return map(hits2res, zip(names, names_h)), map(tags2res, tags_h)


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
