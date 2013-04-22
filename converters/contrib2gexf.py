# -*- coding: utf-8 -*-
__author__ = 'baio'
import xml.etree.ElementTree as ET
import codecs
import regex
import re

def parse_line(line, perv_url):
    if not line or len(line.strip()) == 0:
        raise ValueError("STR_EMPTY")
    line = line.strip()
    spt = line.split('-')
    if len(spt) == 3:
        name_1 = spt[0]
        name_2 = spt[1]
        attrs = spt[2]
        attrs_spt = attrs.split(',')
        if not (len(attrs_spt) == 2 or (len(attrs_spt) == 1 and perv_url)):
            raise ValueError("STR_ENTRY_EMPTY")
        if not regex.match("^^.[а-яА-Я\.]+^.$", attrs_spt[0]):
            raise ValueError("STR_TAG_FORMAT")
        link_types = attrs_spt[0].split('.')
        url = attrs_spt[1] if len(attrs_spt) == 2 else perv_url
        (name_1, name_2, link_types, url)
    else:
        raise ValueError("STR_FORMAT")


def get_edges(in_txt):
    with codecs.open(in_txt, "r", "utf-8") as f:
        for line in f.readlines():
            if line:
<<<<<<< HEAD:converters/contrib2gexf.py
                buck = parse_line(line, perv_url)
                perv_url = buck[3]
                yield buck

=======
                spt = line.split('-')
                if len(spt) == 3:
                    name_1 = spt[0]
                    name_2 = spt[1]
                    attrs = spt[2]
                    attrs_spt = attrs.split(',')
                    link_types = attrs_spt[0].split('.')
                    url = attrs_spt[1] if len(attrs_spt) == 2 else perv_url
                    perv_url = url
                    yield (name_1.strip('\r\n'), name_2.strip('\r\n'), [x.strip('\r\n') for x in link_types], url.strip('\r\n'))
>>>>>>> e23929cdd9b6e30c94b526183d86e35af95a6adf:contrib2gexf.py

def get_elements(in_txt):
    edges = list(get_edges(in_txt))
    print edges
    nodes = []
    for name in set([x[0] for x in edges] + [x[1] for x in edges]):
        nodes.append(name)
    return nodes, edges

<<<<<<< HEAD:converters/contrib2gexf.py
=======
def get_attr_rel_for(rel):
    return {
        u"брат" : "family_rel",
        u"муж" : "family_rel",
        u"двоюрод" : "family_rel",
        u"замуж" : "family_rel",
        u"сын" : "family_rel",
        u"друг" : "private_rel",
        u"кореш" : "private_rel",
        u"служба" : "prof_rel",
        u"лобби" : "prof_rel",
        u"партнер" : "prof_rel"

    }[rel];

>>>>>>> e23929cdd9b6e30c94b526183d86e35af95a6adf:contrib2gexf.py

def get_xml_elements(in_txt):
    nodes, edges = get_elements(in_txt)
    node_els = []
    edge_els = []
    for node in nodes:
        node_el = ET.Element("node")
        node_el.attrib["id"] = node.replace(" ", "_").strip()
        node_el.attrib["label"] = node.strip()
        node_els.append(node_el)
    for edge in edges:
        edge_el = ET.Element("edge")
        edge_el.attrib["source"] = edge[0].replace(" ", "_")
        edge_el.attrib["target"] = edge[1].replace(" ", "_")
        attrs_el = ET.Element("attvalues")
        edge_el.append(attrs_el)
        for rel in edge[2]:
            attr_val_el = ET.Element("attvalue")
            attrs_el.append(attr_val_el)
            attr_val_el.attrib["for"] = get_attr_rel_for(rel)
            attr_val_el.attrib["value"] = rel
        attr_val_el = ET.Element("attvalue")
        attrs_el.append(attr_val_el)
        attr_val_el.attrib["for"] = "url"
        attr_val_el.attrib["value"] = edge[3]
        edge_els.append(edge_el)
    return node_els, edge_els


def merge_xml_elements(in_txt, merge_xml):
    def ns_tag(tag):
        return str(ET.QName('http://www.gexf.net/1.2draft', tag) )

    nodes, edges = get_xml_elements(in_txt)
    ET.register_namespace("", "http://www.gexf.net/1.2draft")
    parser = ET.XMLParser(encoding="utf-8")
    xml = ET.parse(merge_xml, parser)
    xml_root = xml.getroot()
    xml_nodes = xml_root.find(ns_tag("graph")).find(ns_tag("nodes"))
    xml_edges = xml_root.find(ns_tag("graph")).find(ns_tag("edges"))
    for node in nodes:
        xml_nodes.append(node)
    for edge in edges:
        xml_edges.append(edge)
    xml.write("_" + merge_xml, "utf-8", xml_declaration=True)

<<<<<<< HEAD:converters/contrib2gexf.py
"""
if __name__ == '__main__':
    merge_xml_elements("contribs/baio_130418.txt", "template.gexf")
"""
=======
merge_xml_elements("contribs/baio_130418.txt", "template.gexf")
>>>>>>> e23929cdd9b6e30c94b526183d86e35af95a6adf:contrib2gexf.py



