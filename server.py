# -*- coding: utf-8 -*-
__author__ = 'baio'
import web
from es import elastic_search as es
from storage import mongo_storage as stg
from converters.line2bucket import parse_lines
import simplejson as json
from converters.contrib2gexf import merge_xml_elements

render = web.template.render('gephi/', cache=False)

urls = [
    '/names', 'names',
    '/tags', 'tags',
    '/links', 'links'
]

app = web.application(urls, globals())


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

class links:

    def GET(self):
        web.header('Access-Control-Allow-Origin','*')
        web.header('Access-Control-Allow-Credentials','true')
        web.header('Content-Type', 'application/xml')
        return render.layout()

    def POST(self):
        web.header('Access-Control-Allow-Origin','*')
        web.header('Access-Control-Allow-Credentials','true')
        web.header('Content-Type', 'application/json')
        lines = web.data().split('\n')
        bucks, errs  = parse_lines(lines)
        if len(errs) ==  0:
            stg.store(bucks)
            names = set([x[0] for x in bucks] + [x[1] for x in bucks])
            es.append_names(names)
            merge_xml_elements(bucks, "gephi/layout.gexf")
            return json.dumps({"ok": True})
        else:
            e = map(lambda x: {"line": x[0], "code" : x[1]}, errs)
            return json.dumps({"errors" : e})

if __name__ == "__main__":
    app.run()

