__author__ = 'baio'
from dom.contrib.patch import patch
#from es.elastic_search import append_names_tags
import es.elastic_search_v2 as es
import utils.array as utils_array

def contrib_patch(user_name, contrib_id, items):
    res_patch = patch(user_name, contrib_id, items)
    res = res_patch["data"]
    _items = []
    for i, item in enumerate(items):
        if len(res[i]["err"]) == 0 and item["_isRemoved"] == False:
            _items.append(item)
    def map_names(item):
        spt = item["name_1"].strip().lower().split(' ')
        name_1 = spt[1] + ' ' + spt[0]
        spt = item["name_2"].strip().lower().split(' ')
        name_2 = spt[1] + ' ' + spt[0]
        return [(name_1, name_1), (name_2, name_2)]
    def map_rels(item):
        res = []
        t = item["private_rel"]
        if t:
            t = t.strip().lower()
            if t: res.append(("private_rel_" + t, {"val" : t, "type": "private_rel"}))
        t = item["prof_rel"].strip().lower()
        if t:
            t = t.strip().lower()
            if t: res.append(("prof_rel_" + t, {"val" : t, "type": "prof_rel"}))
        t = item["family_rel"].strip().lower()
        if t:
            t = t.strip().lower()
            if t: res.append(("family_rel_" + t, {"val" : t, "type": "family_rel"}))
        return res
    names = utils_array.unique(sum(map(map_names, items), []), lambda x: x[0])
    tags = utils_array.unique(sum(map(map_rels, items), []), lambda x: x[0])

    es.mset("gov-ru[name]", "name", names)
    es.mset("gov-ru[person-rel]", "person-rel", tags, None)
    """
    names = sum(map(lambda x: [
       {"fname": x["name_1"].split(' ')[1], "lname": x["name_1"].split(' ')[0]},
       {"fname": x["name_2"].split(' ')[1], "lname": x["name_2"].split(' ')[0]}
        ]
        , items), [])
    tags = sum(map(lambda x:[
       {"name": x["private_rel"], "type": "private"},
       {"name": x["prof_rel"], "type": "prof"},
       {"name": x["family_rel"], "type": "family"}
       ], items), [])
    tags = filter(lambda x: x["name"], tags)
    #TODO append only unique items
    if len(names) > 0 and len(tags) > 0:
        append_names_tags(names, tags)
    """
    return res_patch


