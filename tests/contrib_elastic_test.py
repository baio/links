# -*- coding: utf-8 -*-
__author__ = 'baio'

import unittest
from es import elastic_search as es

class TestContribElastic(unittest.TestCase):

    def test_names_similarity(self):
        res = list(es.get_similar_names([u"fhirwehfieryhfl", u"ленна скрыник", u"елена скрынник"]))
        self.assertEquals(len(res), 3)
        self.assertEquals(res[0], False)
        self.assertEquals(res[1], u"елена скрынник")
        self.assertEquals(res[2], True)

    def test_tags_in_list(self):
        res = list(es.check_tags([u"лобби", u"браат", u"двоюр"]))
        self.assertEquals(len(res), 3)
        self.assertEquals(res[0], True)
        self.assertEquals(res[1], False)
        self.assertEquals(res[2], False)

    def test_names_append(self):
        res = es.append_names([u"виктор харитонин"])
        self.assertEquals(len(res), 1)
        self.assertEquals(res[0], True)

if __name__ == '__main__':
    es._init("data")
    #unittest.main()

