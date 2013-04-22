# -*- coding: utf-8 -*-
__author__ = 'baio'
import xml.etree.ElementTree as ET
import codecs
import regex
from es import elastic_search as es
import collections

_cryllic = u'абвгдеёжзийклмнопрстуфхцчшщъыьэюяабвгдеёжзийклмнопрстуфхцчшщъыьэюя'

def parse_lines(lines):
    perv_url = None
    res = []
    errors = []
    for idx, line in enumerate(lines):
        if line:
            try:
                buck = parse_line(line, perv_url)
                perv_url = buck[3]
                res.append(buck)
            except ValueError as e:
                errors.append((idx, e.message))
    return res, errors

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

        if not name_1 \
            or not name_2 \
            or not regex.match("^["+_cryllic+"\s]+$", name_1)\
            or not regex.match("^["+_cryllic+"\s]+$", name_2)\
            or len(name_1.split(' ')) != 2\
            or len(name_2.split(' ')) != 2:
                raise ValueError("STR_NAME_FORMAT")

        if name_1 == name_2:
            raise ValueError("STR_SAME_NAMES")

        if len(attrs_spt) == 2 and perv_url:
            raise ValueError("STR_TAG_FORMAT")
        if not regex.match("^(?!\.)["+_cryllic+"\.]+(?<!\.)$", attrs_spt[0]):
            raise ValueError("STR_TAG_FORMAT")

        link_types = attrs_spt[0].split('.')

        if filter(lambda x: not x, link_types):
            raise ValueError("STR_TAG_FORMAT")

        arr = collections.Counter(link_types)
        doubled_tags = set(i for i in arr if arr[i]>1)
        if len(doubled_tags) != 0:
            raise ValueError("STR_TAG_DOUBLED:" + ",".join(doubled_tags))

        url = attrs_spt[1] if len(attrs_spt) == 2 else perv_url

        if not regex.match("http://[\w\.]+/[\w]+$", url):
            raise ValueError("STR_LINK_FORMAT")

        sim_names = list(es.get_similar_names([name_1, name_2]))
        if isinstance(sim_names[0], basestring):
            raise ValueError(u"STR_SIMILAR_NAME:{},{}".format(name_1,sim_names[0]))
        if isinstance(sim_names[1], basestring):
            raise ValueError(u"STR_SIMILAR_NAME:{},{}".format(name_2,sim_names[1]))

        tags = filter(lambda x: not x[1], zip(link_types, es.check_tags(link_types)))
        if len(tags) != 0:
            raise ValueError(u"STR_TAG_NOT_FOUND:{}".format(",".join(map(lambda x: x[0], tags))))

        return (name_1, name_2, link_types, url)
    else:
        raise ValueError("STR_FORMAT")


def get_edges(in_txt):
    with codecs.open(in_txt, "r", "utf-8") as f:
        for line in f.readlines():
            if line:
                buck = parse_line(line, perv_url)
                perv_url = buck[3]
                yield buck

def get_elements(in_txt):
    edges = list(get_edges(in_txt))
    print edges
    nodes = []
    for name in set([x[0] for x in edges] + [x[1] for x in edges]):
        nodes.append(name)
    return nodes, edges

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

if __name__ == '__main__':
    merge_xml_elements("contribs/baio_130418.txt", "template.gexf")



