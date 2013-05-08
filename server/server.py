# -*- coding: utf-8 -*-
__author__ = 'baio'
import web
import simplejson as json
from es import elastic_search as es
from dom.user.get_gexf import get_gexf

from dom import contrib
from dom.user.get import get as user_get
from dom.contrib.create import create as contrib_create
from dom.contrib.get import get as contrib_get
from contrib_patch import contrib_patch

render = web.template.render('gephi/', cache=False)

urls = [
    '/names', 'names',
    '/tags', 'tags',
    '/contribs', 'contribs',
    '/users', 'users',
    '/gexf', 'gexf'
]

app = web.application(urls, globals())

def _jsonforammter(obj):
    return obj.isoformat() if hasattr(obj, 'isoformat') else obj
    """
    if hasattr(obj, 'isoformat'):
        obj.isoformat()
    else:
        raise TypeError("Unserializable object {} of type {}".format(obj, type(obj)))
    """

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
        return es.get_tags_json(web.input().type, web.input().term)

class users:

    def GET(self):
        web.header('Access-Control-Allow-Origin','*')
        web.header('Access-Control-Allow-Credentials','true')
        web.header('Content-Type', 'application/json')
        """
        def date_handler(obj):
            return obj.isoformat() if hasattr(obj, 'isoformat') else obj
        """
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
        contrib_create("baio", data["name"], data["url"])
        return json.dumps({"ok" : True})

    def OPTIONS(self):
        web.header('Access-Control-Allow-Origin','*')
        web.header('Access-Control-Allow-Credentials','true')
        web.header('Content-Type', 'application/json')
        web.header('Access-Control-Allow-Methods', 'POST, GET, PUT, PATCH')

    def PUT(self):
        web.header('Access-Control-Allow-Origin','*')
        web.header('Access-Control-Allow-Credentials','true')
        web.header('Content-Type', 'application/json')
        data = json.loads(web.data())
        contrib.get.update("baio", data["name"], data["new_name"], data["new_url"])
        return json.dumps({"ok" : True})

    def PATCH(self):
        web.header('Access-Control-Allow-Origin','*')
        web.header('Access-Control-Allow-Credentials','true')
        web.header('Content-Type', 'application/json')
        data = json.loads(web.data())
        res = contrib_patch("baio", data["id"], data["items"])
        return json.dumps(res)

if __name__ == "__main__":
    app.run()

