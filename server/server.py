# -*- coding: utf-8 -*-
__author__ = 'baio'
import web
import simplejson as json
from es import elastic_search as es
from server_post_links import update_links
from server_post_gexf import upload_gexf

render = web.template.render('../gephi/', cache=False)

urls = [
    '/names', 'names',
    '/tags', 'tags',
    '/links', 'links',
    '/gexf', 'gexf'
]

app = web.application(urls, globals())


class gexf:

    def GET(self):
        print "gexf download"
        web.header('Access-Control-Allow-Origin','*')
        web.header('Access-Control-Allow-Credentials','true')
        web.header('Content-Type', 'application/xml')
        return render.layout()

    def POST(self):
        print "gexf uload"
        web.header('Access-Control-Allow-Origin','*')
        web.header('Access-Control-Allow-Credentials','true')
        web.header('Content-Type', 'application/json')
        x = web.input(gexf_file={})
        xml = x['gexf_file'].file.read()
        upload_gexf(xml)
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

class links:

    def POST(self):
        web.header('Access-Control-Allow-Origin','*')
        web.header('Access-Control-Allow-Credentials','true')
        web.header('Content-Type', 'application/json')
        lines = web.data().split('\n')
        print lines
        errs  = update_links(lines)
        if len(errs) ==  0:
            return json.dumps({"ok" : True})
        else:
            e = map(lambda x: {"line": x[0], "code" : x[1]}, errs)
            return json.dumps({"errors" : e})

if __name__ == "__main__":
    app.run()

