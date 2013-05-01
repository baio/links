# -*- coding: utf-8 -*-
__author__ = 'baio'

import unittest
from dom.user_contrib import upload
from dom.user_compile_graph import compile_graph
from dom.user_graph2gexf import graph2gexf

class TestDomUser(unittest.TestCase):

    @unittest.skip("demonstrating skipping")
    def test_upload(self):
        upload("baio", "my-own", [u"елена скрынник-виктор христенко-брат.служба,http://goo.gl/ohEX4"])
        upload("baio", "my-own", [u"елена скрынник-виктор христенко-брат.муж,http://goo.gl/ohEX4"])
        upload("baio", "my-own", [u"ирина сакаева-лев григорьев-друг,http://goo.gl/ohEX4"])
        upload("baio", "my-own-1", [u"ирина сакаева-лев григорьев-друг,http://goo.gl/ohEX4"])
        upload("baio2", "my-own", [u"елена скрынник-виктор христенко-брат.служба,http://goo.gl/ohEX4"])
        compile_graph("baio", ["my-own"], "grp1")

    @unittest.skip("demonstrating skipping")
    def test_compile(self):
        compile_graph("baio", ["my-own"], "grp1")

    def test_graph2gexf(self):
        graph2gexf("baio", "grp1")

if __name__ == '__main__':
    unittest.main()



