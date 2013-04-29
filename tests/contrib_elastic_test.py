# -*- coding: utf-8 -*-
__author__ = 'baio'

import unittest
from es import elastic_search as es

class TestContribElastic(unittest.TestCase):

    @unittest.skip("demonstrating skipping")
    def test_names_similarity(self):
        res = list(es.get_similar_names([u"ебь гсей", u"еленна скрыник", u"елена скрынник"]))
        self.assertEquals(len(res), 3)
        self.assertEquals(res[0], False)
        self.assertEquals(res[1], u"елена скрынник")
        self.assertEquals(res[2], True)

    @unittest.skip("demonstrating skipping")
    def test_tags_in_list(self):
        res = list(es.check_tags([u"лобби", u"браат", u"двоюр"]))
        self.assertEquals(len(res), 3)
        self.assertEquals(res[0], True)
        self.assertEquals(res[1], False)
        self.assertEquals(res[2], False)

    @unittest.skip("demonstrating skipping")
    def test_names_append(self):
        res = es.append_names([u"виктор харитонин"])
        self.assertEquals(len(res), 1)
        self.assertEquals(res[0], True)


    def test_tags_and_names(self):
        names, tags = list(es.check_tags_and_names([u"ебь гсей", u"еленна скрыник", u"елена скрынник"], [u"лобби", u"браат", u"двоюр"]))

        self.assertEquals(len(names), 3)
        self.assertEquals(names[0], False)
        self.assertEquals(names[1], u"елена скрынник")
        self.assertEquals(names[2], True)

        self.assertEquals(len(tags), 3)
        self.assertEquals(tags[0], True)
        self.assertEquals(tags[1], False)
        self.assertEquals(tags[2], False)

if __name__ == '__main__':
    #es._init("data")
    unittest.main()

