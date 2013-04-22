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
        return es.get_names(web.input().term)

class tags:
    def GET(self):
        return es.get_tags(web.input().term)

class links:
    def POST(self):
        data = web.data()
        print data
        stg.store(data)
        return json.dumps({"ok": True})


if __name__ == "__main__":
    app.run()

