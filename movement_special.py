import networkx as nx

from graph_embedding.graph import Graph
from graph_embedding.helper import order_neighbor, vertex_type
def movement_special(graph: Graph, order):
    """
    Label arcs with movement or special attributes based on vertex types.

    :param graph: The graph object.
    :param order: The order of vertices.
    """
    for v in graph.nodes:
        ordered_v = order_neighbor(order, list(graph.neighbors(v)) + [v])
        type_v = vertex_type(v, ordered_v)
        v_in_v = ordered_v.index(v)

        if type_v == [4, 0]:
            arc = graph.get_arc(v, ordered_v[v_in_v + 1])
            arc["movement"] = True
        elif type_v == [0, 4]:
            arc = graph.get_arc(v, ordered_v[v_in_v - 1])
            arc["movement"] = True
        elif type_v == [4, 1]:
            arc = graph.get_arc(v, ordered_v[v_in_v + 1])
            arc["movement"] = True
        elif type_v == [1, 4]:
            arc = graph.get_arc(v, ordered_v[v_in_v - 1])
            arc["movement"] = True
        elif type_v == [5, 0]:
            arc = graph.get_arc(v, ordered_v[v_in_v + 1])
            arc["movement"] = True
            arc = graph.get_arc(v, ordered_v[v_in_v + 2])
            arc["movement"] = True
        elif type_v == [0, 5]:
            arc = graph.get_arc(v, ordered_v[v_in_v - 1])
            arc["movement"] = True
            arc = graph.get_arc(v, ordered_v[v_in_v - 2])
            arc["movement"] = True
        elif type_v == [4, 2]:
            arc = graph.get_arc(v, ordered_v[v_in_v + 1])
            arc["special"] = True
        elif type_v == [2, 4]:
            arc = graph.get_arc(v, ordered_v[v_in_v - 1])
            arc["special"] = True
        elif type_v == [5, 1]:
            arc = graph.get_arc(v, ordered_v[v_in_v + 1])
            arc["movement"] = True
            arc = graph.get_arc(v, ordered_v[v_in_v + 2])
            arc["special"] = True
        elif type_v == [1, 5]:
            arc = graph.get_arc(v, ordered_v[v_in_v - 1])
            arc["movement"] = True
            arc = graph.get_arc(v, ordered_v[v_in_v - 2])
            arc["special"] = True
        elif type_v == [6, 0]:
            arc = graph.get_arc(v, ordered_v[v_in_v + 1])
            arc["movement"] = True
            arc = graph.get_arc(v, ordered_v[v_in_v + 2])
            arc["movement"] = True
            arc = graph.get_arc(v, ordered_v[v_in_v + 3])
            arc["special"] = True
        elif type_v == [0, 6]:
            arc = graph.get_arc(v, ordered_v[v_in_v - 1])
            arc["movement"] = True
            arc = graph.get_arc(v, ordered_v[v_in_v - 2])
            arc["movement"] = True
            arc = graph.get_arc(v, ordered_v[v_in_v - 3])
            arc["special"] = True
