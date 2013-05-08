__author__ = 'baio'
from dom.contrib.patch import patch
from es.elastic_search import append_names_tags

def contrib_patch(user_name, contrib_id, items):
    _res = patch(user_name, contrib_id, items)
    res = zip(_res, items)
    res = filter(lambda x: len(x[0]["err"]) == 0, res)
    names = sum(map(lambda x: [
       {"fname": x[1]["name_1"].split(' ')[0], "lname": x[1]["name_1"].split(' ')[1]},
       {"fname": x[1]["name_2"].split(' ')[0], "lname": x[1]["name_2"].split(' ')[1]}
        ]
        , res), [])
    tags = sum(map(lambda x:[
       {"name": x[1]["private_rel"], "type": "private"},
       {"name": x[1]["prof_rel"], "type": "prof"},
       {"name": x[1]["family_rel"], "type": "family"}
       ], res), [])
    tags = filter(lambda x: x["name"] is not None, tags)
    #TODO append only unique items
    append_names_tags(names, tags)
    return _res


