import networkx as nx

from graph_embedding.graph import Graph


def perpendicular(arc1, arc2):
    """
    Check if two arcs are perpendicular based on their colors.

    :param arc1: Dictionary representing the first arc.
    :param arc2: Dictionary representing the second arc.
    :return: True if the arcs are perpendicular, otherwise False.
    """
    return arc1["color"] != arc2["color"]

def point_toward(arc, graph: Graph):
    """
    Determine if an arc points in the positive direction.

    :param arc: Dictionary representing the arc.
    :param graph: The graph containing the vertices.
    :return: True if the arc points in the positive direction, otherwise False.
    """
    start_position = graph.nodes[arc["start"]]["position"]
    end_position = graph.nodes[arc["end"]]["position"]
    color = arc["color"]
    if arc["orientation"] == 1:
        return end_position[color] > start_position[color]
    elif arc["orientation"] == -1:
        return end_position[color] < start_position[color]
    return False

def missing(a, b):
    """
    Find the missing element in a set of {0, 1, 2}.

    :param a: First element.
    :param b: Second element.
    :return: The missing element.
    """
    elements = {0, 1, 2}
    return (elements - {a, b}).pop()

def sign(x):
    """
    Return the sign of a number: -1 for negative, 1 for positive, 0 for zero.
    """
    return (x > 0) - (x < 0)

def vertex_type(vertex, ordered):
    """
    Calculate the type of a vertex based on its position in the order.

    :param vertex: The vertex to calculate the type for.
    :param ordered: The ordered list of vertices.
    :return: A list [succ, pred], where succ is the position from the start, and pred from the end.
    """
    succ = len(ordered) - 1 - ordered.index(vertex)
    pred = ordered.index(vertex)
    return [succ, pred]

def order_neighbor(order, neighbor):
    """
    Order the neighbors of a vertex based on their position in the given order.

    :param order: The current order of vertices.
    :param neighbor: The list of neighbors to order.
    :return: A sorted list of neighbors based on their position in the order.
    """
    return sorted(neighbor, key=lambda x: order.index(x))

def succ_index(v, w, ordered_v):
    """
    Find the successor index of vertex w relative to vertex v in the ordered list.

    :param v: The reference vertex.
    :param w: The target vertex.
    :param ordered_v: The ordered list of vertices.
    :return: The index difference of w from v in the ordered list.
    """
    if w not in ordered_v:
        raise ValueError(f"{w} is not a neighbor of {v}")
    val = ordered_v.index(w) - ordered_v.index(v)
    if val <= 0:
        raise ValueError(f"{w} is on the left of {v}")
    return  val
    

def pred_index(v, w, ordered_v):
    """
    Find the predecessor index of vertex w relative to vertex v in the ordered list.

    :param v: The reference vertex.
    :param w: The target vertex.
    :param ordered_v: The ordered list of vertices.
    :return: The index difference of v from w in the ordered list.
    """
    if w not in ordered_v:
        raise ValueError(f"{w} is not a neighbor of {v}")
    val = ordered_v.index(v) - ordered_v.index(w)
    if val <= 0:
        raise ValueError(f"{w} is on the right of {v}")
    return  val

def opposite(v, w, type_v, type_w, order):
    """
    Check if two vertices are opposite in terms of type and order.

    :param v: The first vertex.
    :param w: The second vertex.
    :param type_v: The type of the first vertex [succ, pred].
    :param type_w: The type of the second vertex [succ, pred].
    :param order: The ordered list of vertices.
    :return: True if the vertices are opposite, otherwise False.
    """
    return (order.index(w) > order.index(v) and
            (type_v[0] - type_v[1]) > 0 and
            (type_w[0] - type_w[1]) < 0)