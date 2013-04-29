__author__ = 'baio'
from es import elastic_search as es
from storage import mongo_storage as stg
from converters.line2bucket import parse_lines
from converters.contrib2gexf import merge_xml_elements
import shutil

def update_links(lines):
    bucks, errs  = parse_lines(lines)
    if len(errs) ==  0:
        # 1. store nodes to mongo/contrib
        stg.store(bucks)
        names = set([x[0] for x in bucks] + [x[1] for x in bucks])
        # 2. store names to es
        es.append_names(names)
        # 3. update mongo/storage
        stg.contribs2edges()
        # 4. write new layout file
        edges = list(stg.get_edges())
        nodes = list(stg.get_nodes())
        shutil.copy("gephi/_layout.gexf", "gephi/layout.gexf")
        merge_xml_elements(edges, nodes, "gephi/layout.gexf")
        return []
    else:
        return errs

