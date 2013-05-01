# -*- coding: utf-8 -*-
__author__ = 'baio'

import unittest
from dom.user.upload_lines import upload_lines
from dom.user.compile_graph import compile_graph
from dom.user.update_gexf_from_graph import update_gexf_from_graph

class TestDomUser(unittest.TestCase):

    @unittest.skip("demonstrating skipping")
    def test_upload(self):
        upload_lines("baio", "my-own", [u"елена скрынник-виктор христенко-брат.служба,http://goo.gl/ohEX4"])
        upload_lines("baio", "my-own", [u"елена скрынник-виктор христенко-брат.муж,http://goo.gl/ohEX4"])
        upload_lines("baio", "my-own", [u"ирина сакаева-лев григорьев-друг,http://goo.gl/ohEX4"])
        upload_lines("baio", "my-own-1", [u"ирина сакаева-лев григорьев-друг,http://goo.gl/ohEX4"])
        upload_lines("baio2", "my-own", [u"елена скрынник-виктор христенко-брат.служба,http://goo.gl/ohEX4"])


    @unittest.skip("demonstrating skipping")
    def test_compile(self):
        compile_graph("baio", ["my-own"], "grp1")

    def test_graph2gexf(self):
        update_gexf_from_graph("baio", "grp1")

if __name__ == '__main__':
    unittest.main()



