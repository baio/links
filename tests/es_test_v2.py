# -*- coding: utf-8 -*-
__author__ = 'baio'

import unittest
from es import elastic_search_v2 as es

class TestContribElastic_v2(unittest.TestCase):

    def test_mset(self):
        names = [(u"max", "max"), ("mikkey", "mikkey"), ("hommer", "hommer")]
        es.mset("name", "gov-ru", names)

if __name__ == '__main__':
    unittest.main()

