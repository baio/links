# -*- coding: utf-8 -*-
__author__ = 'baio'
import web
from es import elastic_search as es
from storage import mongo_storage as stg
from converters.line2bucket import parse_lines
import simplejson as json
from converters.contrib2gexf import merge_xml_elements

urls = [
    '/names', 'names',
    '/tags', 'tags',
    '/links', 'links'
]

app = web.application(urls, globals())

class names:
    def GET(self):
        return es.get_names_json(web.input().term)

class tags:
    def GET(self):
        return es.get_tags_json(web.input().term)

class links:

    def GET(self):
        raise web.seeother("/static/layout.gexf")

    def POST(self):
        lines = web.data().split('\n')
        bucks, errs  = parse_lines(lines)
        if len(errs) ==  0:
            stg.store(bucks)
            names = set([x[0] for x in bucks] + [x[1] for x in bucks])
            es.append_names(names)
            merge_xml_elements(bucks, "static/layout.gexf")
            return json.dumps({"ok": True})
        else:
            e = map(lambda x: {"line": x[0], "code" : x[1]}, errs)
            return json.dumps({"errors" : e})

if __name__ == "__main__":
    app.run()

