# -*- coding: utf-8 -*-
__author__ = 'baio'

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

