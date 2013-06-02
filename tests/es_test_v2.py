# -*- coding: utf-8 -*-
__author__ = 'baio'

import unittest
from es import elastic_search_v2 as es

class TestContribElastic_v2(unittest.TestCase):

    def test_mset(self):
        return
        names = [(u"max pain", "max pain"), ("mikkey mauase", "mikkey mause"), ("hommer simpson", "hommer simpson")]
        es.mset("gov-ru[name]", "name", names)

    def test_mset_tag(self):
        return
        rels = [("test_sick", {"val": "test", "type": "sick"})]
        es.mset("gov-ru[person-rel]", "person-rel", rels, None)

    def test_get(self):
        res = es.get("gov-ru[name]", "name", "mix")
        print res

    def test_get_tag(self):
        res = es.get("gov-ru[person-rel]", "person-rel", "tezt", {"match" : {"type" : "sick"}})
        print res

if __name__ == '__main__':
    unittest.main()

