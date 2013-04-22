# -*- coding: utf-8 -*-
__author__ = 'baio'
import web
from es import elastic_search as es
from storage import mongo_storage as stg
import simplejson as json

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
    def POST(self):
        data = web.data().split('\n')
        errs = stg.store(data)
        if len(errs) ==  0:
            return json.dumps({"ok": True})
        else:
            e = map(lambda x: {"line": x[0], "code" : x[1]}, errs)
            return json.dumps({"errors" : e})

if __name__ == "__main__":
    app.run()

