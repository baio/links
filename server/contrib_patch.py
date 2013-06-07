__author__ = 'baio'
from dom.contrib.patch import patch
from dom.contrib.get_scheme import get_scheme
import es.elastic_search_v2 as es
import utils.array as utils_array


def contrib_patch(user_name, contrib_id, items):
    res_patch = patch(user_name, contrib_id, items)
    res = res_patch["data"]
    _items = []

    for i, item in enumerate(items):
        if len(res[i]["err"]) == 0 and item["_isRemoved"] == False:
            _items.append(item)

    def map_field(field_val, scheme):
        if isinstance(field_val, list):
            for v in field_val:
                yield map_field(v, scheme)
        else:
            type = field_val["type"] if "type" in field_val else (scheme["default_type"] if type(scheme["type"]) is list else scheme["type"])
            val = field_val["val"] if "val" in field_val else field_val
            yield  (scheme["index"], type , type + "|" + val, {"val" : val})

    scheme = get_scheme(user_name, contrib_id)
    for key in scheme:
        field_scheme = scheme[key]
        field = utils_array.unique(
            sum(map(lambda i: list(map_field(i[key], field_scheme)), items), []), lambda x: x[0])
        es.bset(field)

    return res_patch


