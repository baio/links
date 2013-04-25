# -*- coding: utf-8 -*-
__author__ = 'baio'
import web
import simplejson as json
from es import elastic_search as es
from server_post_links import update_links
import shutil

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
        errs  = update_links(lines)
        if len(errs) ==  0:
            return json.dumps({"ok" : True})
        else:
            e = map(lambda x: {"line": x[0], "code" : x[1]}, errs)
            return json.dumps({"errors" : e})

if __name__ == "__main__":
    app.run()

