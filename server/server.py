# -*- coding: utf-8 -*-
__author__ = 'baio'
import web
import simplejson as json
from es import elastic_search as es
from dom.user.get_gexf import get_gexf
from dom.user.get_contrib import get_contrib
from update_contrib import *
import datetime as dt


render = web.template.render('gephi/', cache=False)

urls = [
    '/names', 'names',
    '/tags', 'tags',
    '/contribs', 'contribs',
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

class contribs:

    def GET(self):
        web.header('Access-Control-Allow-Origin','*')
        web.header('Access-Control-Allow-Credentials','true')
        web.header('Content-Type', 'application/json')
        def date_handler(obj):
            return obj.isoformat() if hasattr(obj, 'isoformat') else obj
        d = get_contrib("baio", "gov-ru")
        return json.dumps(d, default=date_handler)


    def POST(self):
        web.header('Access-Control-Allow-Origin','*')
        web.header('Access-Control-Allow-Credentials','true')
        web.header('Content-Type', 'application/json')
        data = json.loads(web.data())
        errs = update_contrib_from_json("baio", data)
        """
        lines = web.data().split('\n')
        errs  = update_contrib_from_lines("baio", "gov-ru", lines)
        """
        if len(errs) ==  0:
            return json.dumps({"ok" : True})
        else:
            e = map(lambda x: {"line": x[0], "code" : x[1]}, errs)
            return json.dumps({"errors" : e})

if __name__ == "__main__":
    app.run()

