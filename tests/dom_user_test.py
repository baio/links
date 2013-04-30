# -*- coding: utf-8 -*-
__author__ = 'baio'

import unittest
from dom.user_contrib import upload

class TestDomUser(unittest.TestCase):

    def test_upload(self):
        upload("baio", "my-own", [u"елена скрынник-виктор христенко-брат.служба,http://goo.gl/ohEX4"])
        upload("baio", "my-own", [u"елена скрынник-виктор христенко-брат.муж,http://goo.gl/ohEX4"])
        upload("baio", "my-own", [u"ирина сакаева-лев григорьев-друг,http://goo.gl/ohEX4"])
        upload("baio", "my-own-1", [u"ирина сакаева-лев григорьев-друг,http://goo.gl/ohEX4"])
        upload("baio2", "my-own", [u"елена скрынник-виктор христенко-брат.служба,http://goo.gl/ohEX4"])

if __name__ == '__main__':
    unittest.main()



