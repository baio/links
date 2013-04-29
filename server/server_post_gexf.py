__author__ = 'max'
from storage import mongo_storage as stg
from converters.gexf2nodes import get_nodes
from converters.contrib2gexf import merge_xml_elements
import shutil

def upload_gexf(gexf_xml):
    nodes = get_nodes(gexf_xml)
    stg.store_nodes(nodes)
    # 4. write new layout file
    edges = list(stg.get_edges())
    nodes = list(stg.get_nodes())
    shutil.copy("gephi/_layout.gexf", "gephi/layout.gexf")
    merge_xml_elements(edges, nodes, "gephi/layout.gexf")

