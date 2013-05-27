__author__ = 'baio'
from dom.contrib.patch import patch
from es.elastic_search import append_names_tags

def contrib_patch(user_name, contrib_id, items):
    res_patch = patch(user_name, contrib_id, items)
    res = res_patch["data"]
    _items = []
    for i, item in enumerate(items):
        if len(res[i]["err"]) == 0 and item["_isRemoved"] == False:
            _items.append(item)
    names = sum(map(lambda x: [
       {"fname": x["name_1"].split(' ')[0], "lname": x["name_1"].split(' ')[1]},
       {"fname": x["name_2"].split(' ')[0], "lname": x["name_2"].split(' ')[1]}
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
    return res_patch


