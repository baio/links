# -*- coding: utf-8 -*-
__author__ = 'baio'
import web
import simplejson as json
from es import elastic_search as es

from dom.user.get import get as user_get
from dom.contrib.create import create as contrib_create
from dom.contrib.get import get as contrib_get
from dom.contrib.delete import delete as contrib_delete
from dom.contrib.update import update as contrib_update
from contrib_patch import contrib_patch
from dom.graph.get import get as get_graph
from dom.graph.patch import patch as patch_graph
from dom.graph.post import post as post_graph

render = web.template.render('gephi/', cache=False)

urls = [
    '/names', 'names',
    '/tags', 'tags',
    '/contribs', 'contribs',
    '/users', 'users',
    '/graphs', 'graphs'
]

app = web.application(urls, globals())

def _jsonforammter(obj):
    return obj.isoformat() if hasattr(obj, 'isoformat') else obj

class graphs:

    def OPTIONS(self):
        web.header('Access-Control-Allow-Origin','*')
        web.header('Access-Control-Allow-Credentials','true')
        web.header('Content-Type', 'application/json')
        web.header('Access-Control-Allow-Methods', 'POST, GET, PUT, PATCH, DELETE')

    def GET(self):
        web.header('Access-Control-Allow-Origin','*')
        web.header('Access-Control-Allow-Credentials','true')
        web.header('Content-Type', 'application/json')
        input = web.input()
        graph = input.graph if "graph" in input else None
        d = get_graph("baio", graph)
        return json.dumps(d, default=_jsonforammter)

    def PATCH(self):
        web.header('Access-Control-Allow-Origin','*')
        web.header('Access-Control-Allow-Credentials','true')
        web.header('Content-Type', 'application/json')
        input = json.loads(web.data())
        patch_graph(input["graph"], input["data"])
        return json.dumps({"ok": True}, default=_jsonforammter)

    def POST(self):
        web.header('Access-Control-Allow-Origin','*')
        web.header('Access-Control-Allow-Credentials','true')
        web.header('Content-Type', 'application/json')
        input = json.loads(web.data())
        d = post_graph("baio", input["name"], input["contribs"])
        return json.dumps(d, default=_jsonforammter)

class names:

    def GET(self):
        web.header('Access-Control-Allow-Origin','*')
        web.header('Access-Control-Allow-Credentials','true')
        web.header('Content-Type', 'application/json')
        return es.get_names_json(web.input().term)

class tags:
    def GET(self):
        web.header('Access-Control-Allow-Origin','*')
        web.header('Access-Control-Allow-Credentials','true')
        web.header('Content-Type', 'application/json')
        return es.get_tags_json(web.input().type, web.input().term)

class users:

    def GET(self):
        web.header('Access-Control-Allow-Origin','*')
        web.header('Access-Control-Allow-Credentials','true')
        web.header('Content-Type', 'application/json')
        return json.dumps(user_get("baio"), default=_jsonforammter)

class contribs:

    def GET(self):
        web.header('Access-Control-Allow-Origin','*')
        web.header('Access-Control-Allow-Credentials','true')
        web.header('Content-Type', 'application/json')
        d = contrib_get("baio", web.input()["id"])
        return json.dumps(d, default=_jsonforammter)

    def POST(self):
        web.header('Access-Control-Allow-Origin','*')
        web.header('Access-Control-Allow-Credentials','true')
        web.header('Content-Type', 'application/json')
        data = json.loads(web.data())
        d = contrib_create("baio", data["name"], data["url"])
        return json.dumps(d, default=_jsonforammter)

    def OPTIONS(self):
        web.header('Access-Control-Allow-Origin','*')
        web.header('Access-Control-Allow-Credentials','true')
        web.header('Content-Type', 'application/json')
        web.header('Access-Control-Allow-Methods', 'POST, GET, PUT, PATCH, DELETE')

    def PUT(self):
        web.header('Access-Control-Allow-Origin','*')
        web.header('Access-Control-Allow-Credentials','true')
        web.header('Content-Type', 'application/json')
        data = json.loads(web.data())
        d = contrib_update("baio", data["ref"], data["name"], data["url"])
        return json.dumps(d, default=_jsonforammter)

    def PATCH(self):
        web.header('Access-Control-Allow-Origin','*')
        web.header('Access-Control-Allow-Credentials','true')
        web.header('Content-Type', 'application/json')
        data = json.loads(web.data())
        res = contrib_patch("baio", data["id"], data["items"])
        return json.dumps(res)

    def DELETE(self):
        web.header('Access-Control-Allow-Origin','*')
        web.header('Access-Control-Allow-Credentials','true')
        web.header('Content-Type', 'application/json')
        data = json.loads(web.data())
        contrib_delete("baio", data["ref"])
        return json.dumps({"ok" : True})


if __name__ == "__main__":
    app.run()

