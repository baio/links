# -*- coding: utf-8 -*-
__author__ = 'baio'

import unittest
from storage import mongo_storage as stg
from converters.line2bucket import parse_line

class TestMongoStorage(unittest.TestCase):

    def test_store_lines(self):
        buck = parse_line(u"елена скрынник-виктор христенко-брат.служба,http://goo.gl/ohEX4", None)
        stg.store([buck])

if __name__ == '__main__':
    #es._init("data")
    unittest.main()

