__author__ = 'baio'

from dom.user.update_contrib_from_lines import update_contrib_from_lines
from dom.user.compile_graph import compile_graph
from dom.user.update_gexf_from_graph import update_gexf_from_graph

def update_contrib(user, contrib, lines):
    errs = update_contrib_from_lines(user, contrib, lines)
    if len(errs) ==  0:
        compile_graph(user, [contrib], contrib)
        update_gexf_from_graph(user, contrib)
    return errs

