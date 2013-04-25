__author__ = 'max'
from storage import mongo_storage as stg
from converters.gexf2nodes import get_nodes

def upload_gexf(gexf_xml):
    nodes = get_nodes(gexf_xml)
    stg.store_nodes(nodes)