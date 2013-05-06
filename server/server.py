# -*- coding: utf-8 -*-
__author__ = 'baio'
import web
import simplejson as json
from es import elastic_search as es
from dom.user.get_gexf import get_gexf

from dom import contrib
from dom.user.get import get as user_get
from dom.contrib.create import create as contrib_create

render = web.template.render('gephi/', cache=False)

urls = [
    '/names', 'names',
    '/tags', 'tags',
    '/contribs', 'contribs',
    '/users', 'users',
    '/gexf', 'gexf'
]

app = web.application(urls, globals())


class gexf:

    def GET(self):
        web.header('Access-Control-Allow-Origin','*')
        web.header('Access-Control-Allow-Credentials','true')
        web.header('Content-Type', 'application/xml')
        return get_gexf("baio", "gov-ru")

    def POST(self):
        print "gexf uload"
        web.header('Access-Control-Allow-Origin','*')
        web.header('Access-Control-Allow-Credentials','true')
        web.header('Content-Type', 'application/json')
        x = web.input(gexf_file={})
        xml = x['gexf_file'].file.read()
        update_contrib_from_gexf("baio", "gov-ru", xml)
        return json.dumps({"ok" : True})

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
        return es.get_tags_json(web.input().term)

class users:

    def GET(self):
        web.header('Access-Control-Allow-Origin','*')
        web.header('Access-Control-Allow-Credentials','true')
        web.header('Content-Type', 'application/json')
        return json.dumps(user_get("baio"))


class contribs:

    def GET(self):
        web.header('Access-Control-Allow-Origin','*')
        web.header('Access-Control-Allow-Credentials','true')
        web.header('Content-Type', 'application/json')
        def date_handler(obj):
            return obj.isoformat() if hasattr(obj, 'isoformat') else obj
        d = contrib.get.get("baio", "gov-ru")
        return json.dumps(d, default=date_handler)

    def POST(self):
        web.header('Access-Control-Allow-Origin','*')
        web.header('Access-Control-Allow-Credentials','true')
        web.header('Content-Type', 'application/json')
        data = json.loads(web.data())
        contrib_create("baio", data["name"], data["url"])
        return json.dumps({"ok" : True})

    def PUT(self):
        web.header('Access-Control-Allow-Origin','*')
        web.header('Access-Control-Allow-Credentials','true')
        web.header('Content-Type', 'application/json')
        data = json.loads(web.data())
        contrib.get.update("baio", data["name"], data["new_name"], data["new_url"])
        return json.dumps({"ok" : True})

    def MERGE(self):
        web.header('Access-Control-Allow-Origin','*')
        web.header('Access-Control-Allow-Credentials','true')
        web.header('Content-Type', 'application/json')
        data = json.loads(web.data())
        contrib.get.merge("baio", data["name"], data["data"])
        return json.dumps({"ok" : True})

if __name__ == "__main__":
    app.run()

