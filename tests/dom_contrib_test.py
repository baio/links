# -*- coding: utf-8 -*-
__author__ = 'baio'

import unittest
from dom.contrib.create import create
from dom.contrib.update import update
from dom.contrib.merge import merge

class TestDomContrib(unittest.TestCase):

    @unittest.skip("demonstrating skipping")
    def test_create(self):
        create("baio-1", "contrib-1", "url")

    @unittest.skip("demonstrating skipping")
    def test_update(self):
        update("baio-1", "contrib-1", "contrib-2", "url-2")

    @unittest.skip("demonstrating skipping")
    def test_merge_create(self):
        data = [
            {"_id": None, "name_1": "name-1", "name_2": "name-2", "family_rel": u"брат", u"private_rel": "друг"},
            {"_id": None, "name_1": "name-1", "name_2": "name-3", "family_rel": u"муж"}
        ]
        merge("baio-1", "contrib-1", data)

    #@unittest.skip("demonstrating skipping")
    def test_merge_update(self):
        data = [
            {"_id": None, "name_1": "name-5", "name_2": "name-2", "family_rel": u"брат", u"private_rel": "друг"},
            {"_id": "name-1_name-2", "name_1": "name-1", "name_2": "name-2", "family_rel": u"муж", u"private_rel": "друг"},
            {"_id": "name-2_name-3", "name_1": "name_1", "name_2": "name_3", "family_rel": u"муж"}
        ]
        merge("baio-1", "contrib-1", data)

if __name__ == '__main__':
    unittest.main()



