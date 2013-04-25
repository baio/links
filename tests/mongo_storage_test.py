# -*- coding: utf-8 -*-
__author__ = 'baio'

import unittest
from storage import mongo_storage as stg
from converters.line2bucket import parse_line

class TestMongoStorage(unittest.TestCase):

    @unittest.skip("demonstrating skipping")
    def test_store_lines(self):
        buck = parse_line(u"елена скрынник-виктор христенко-брат.служба,http://goo.gl/ohEX4", None)
        stg.store([buck])

    @unittest.skip("demonstrating skipping")
    def test_contribs2edges(self):
        stg.contribs2edges()

    def test_get_bucks(self):
        print list(stg.get_bucks())

if __name__ == '__main__':
    #es._init("data")
    unittest.main()

