# -*- coding: utf-8 -*-
__author__ = 'baio'

import unittest
from storage import  mongo_storage as mongo
from converters.contrib2gexf import merge_xml_elements

class TestServer2nodes(unittest.TestCase):

    def test_gen_gexf(self):
        edges = list(mongo.get_edges())
        nodes = list(mongo.get_nodes())
        merge_xml_elements(edges, nodes, "gephi/layout.gexf")

if __name__ == '__main__':
    unittest.main()


