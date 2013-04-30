__author__ = 'baio'

import pymongo as mongo
import datetime as dt
from config.config import config

def compile_graph(user, contrib_names, graph_name):

    now = dt.datetime.now()

    client = mongo.MongoClient(config["MONGO_URI"])
    db = client.links

    user = db.user.find_one({"_id": user}, {
        "contribs" : { "$elemMatch" : {"name" : {"$in" : contrib_names}}},
        "graphs" : { "$elemMatch" : {"name" : graph_name}}
    })

    if "graph" in user:
        graph = user["graphs"][0]
    else:
        graph = {"name" : graph_name, "date" : now, "nodes" : [], "edges" : []}

    old_nodes = graph["nodes"]
    graph["nodes"] = []
    graph["edges"] = []
    data = sum(sum(user["contribs"], []), [])
    nodes = dict()
    edges = dict()

    def create_node(name):
        node = {"_id": name.replace(" ", "_")}
        "copy old position if any"
        old_node = filter(lambda x: x["_id"] == node["_id"], old_nodes)
        if len(old_node) > 0 and "pos" in old_node[0]:
            node["pos"] = old_node[0]["pos"]
        node

    for d in data:
        node_1 = create_node(d["name_1"])
        node_2 = create_node(d["name_2"])
        nodes[node_1["_id"]] = node_1
        nodes[node_2["_id"]] = node_2

        edge_id = "{}_{}".format(node_1["_id"], node_2["_id"])
        edge = edges.get(edge_id, {"_id": edge_id, "tags": []})
        edges["edge_id"] = edge
        for tag in d["tags"]:
            edge_tag = filter(lambda x: x["name"] == tag, edge["tags"])
            if len(edge_tag):
                edge_tag = edge_tag[0]
            else:
                edge_tag = {"name" : tag, "urls" : []}
                edge["tags"].append(edge_tag)
            if d["url"] not in edge_tag["urls"]:
                edge_tag["urls"].append(d["url"])

    for node in nodes:
        graph["nodes"].append(nodes[node])
    for edge in edges:
        graph["edges"].append(edges[edge])

    db.user.update({"_id" : user, "gaphs.name" : graph_name}, {"$set" :  {"graphs.$" : graph}})