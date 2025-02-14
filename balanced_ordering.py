import networkx as nx
import math

from graph_embedding.graph import Graph
from graph_embedding.helper import order_neighbor, opposite, succ_index, pred_index, vertex_type

def move1(ordered, v, w):
    """
    Move vertex v to immediately after vertex w in the ordered list.

    :param ordered: The ordered list of vertices.
    :param v: The vertex to move.
    :param w: The reference vertex.
    """
    ordered.remove(v)
    ordered.insert(ordered.index(w) + 1, v)

def move1opp(ordered, v, w):
    """
    Move vertex v to immediately before vertex w in the ordered list.

    :param ordered: The ordered list of vertices.
    :param v: The vertex to move.
    :param w: The reference vertex.
    """
    ordered.remove(v)
    ordered.insert(ordered.index(w), v)

def move2(ordered, v, w, vi, wj):
    """
    Move vertex v to immediately before vertex vi and vertex w immediately after wj.

    :param ordered: The ordered list of vertices.
    :param v: The vertex to move.
    :param w: The vertex to move.
    :param vi: The reference vertex for v.
    :param wj: The reference vertex for w.
    """
    ordered.remove(v)
    ordered.insert(ordered.index(vi), v)
    ordered.remove(w)
    ordered.insert(ordered.index(wj) + 1, w)

def move3(ordered, v, w, vi):
    """
    Move vertex v to immediately after vi and vertex w to immediately before vi.

    :param ordered: The ordered list of vertices.
    :param v: The vertex to move.
    :param w: The vertex to move.
    :param vi: The reference vertex for both v and w.
    """
    ordered.remove(v)
    ordered.insert(ordered.index(vi) + 1, v)
    ordered.remove(w)
    ordered.insert(ordered.index(vi), w)

def move4(ordered, v, type):
    """
    Move vertex v forward by a calculated distance based on its type.

    :param ordered: The ordered list of vertices.
    :param v: The vertex to move.
    :param type: The type of the vertex [succ, pred].
    """
    i = math.floor(abs(type[0] - type[1]) / 2)
    target = ordered[ordered.index(v) + i]
    ordered.remove(v)
    ordered.insert(ordered.index(target) + 1, v)

def move4opp(ordered, v, type):
    """
    Move vertex v back by a calculated distance based on its type.

    :param ordered: The ordered list of vertices.
    :param v: The vertex to move.
    :param type: The type of the vertex [succ, pred].
    """
    i = math.floor(abs(type[0] - type[1]) / 2)
    target = ordered[ordered.index(v) - i]
    ordered.remove(v)
    ordered.insert(ordered.index(target), v)

def balanced_ordering(graph: Graph):
    """
    Perform a balanced ordering on the graph to minimize crossings.

    :param graph: The graph object.
    :return: The balanced order of vertices.
    """
    order = list(graph.nodes)
    check = list(graph.edges(data=False))
    degree = max(dict(graph.degree()).values())

    while check:
        edge = check[0]  # Get the first edge from the list
        v, w = edge

        # Retrieve neighbors and their ordered positions
        ordered_v = order_neighbor(order, list(graph.neighbors(v)) + [v])
        ordered_w = order_neighbor(order, list(graph.neighbors(w)) + [w])
        type_v = vertex_type(v, ordered_v)
        type_w = vertex_type(w, ordered_w)

        v_in_v = ordered_v.index(v)
        v_in_w = ordered_w.index(v)
        w_in_v = ordered_v.index(w)
        w_in_w = ordered_w.index(w)

        v_ind = order.index(v)
        w_ind = order.index(w)

        moved = False  # Flag to track if any movement occurs

        if opposite(v, w, type_v, type_w, order) and 1 <= succ_index(v, w, ordered_v) <= math.floor(abs(type_v[0] - type_v[1]) / 2):
            #print(f"executing move 1")
            move1(order, v, w)
            moved = True
        elif opposite(w, v, type_w, type_v, order) and 1 <= pred_index(v, w, ordered_v) <= math.floor(abs(type_w[0] - type_w[1]) / 2):
            #print(f"executing move 1opp")
            move1opp(order, v, w)
            moved = True
        elif opposite(v, w, type_v, type_w, order) and ordered_v.index(w) > v_in_v + 2:
            for vi in ordered_v[v_in_v:w_in_v]:
                for wj in ordered_w[:w_in_w]:
                    if v_ind < order.index(wj) < order.index(vi):
                        i = succ_index(v, vi, ordered_v)
                        j = pred_index(w, wj, ordered_w)
                        if 1 <= i <= math.floor((type_v[0] - type_v[1]) / 2) and 1 <= j <= math.floor((type_w[0] - type_w[1]) / 2):
                            #print(f"executing move 2")
                            move2(order, v, w, vi, wj)
                            moved = True
                            break
                if moved:
                    break
        elif opposite(w, v, type_w, type_v, order) and ordered_w.index(v) > w_in_w + 2:
            for wj in ordered_w[w_in_w:v_in_w]:
                for vi in ordered_v[:v_in_v]:
                    if w_ind < order.index(vi) < order.index(wj):
                        i = pred_index(v, vi, ordered_v)
                        j = succ_index(w, wj, ordered_w)
                        if 1 <= i <= math.floor((type_v[0] - type_v[1]) / 2) and 1 <= j <= math.floor((type_w[0] - type_w[1]) / 2):
                            #print(f"executing move 2opp")
                            move2(order, w, v, wj, vi)
                            moved = True
                            break
                if moved:
                    break
        elif opposite(v, w, type_v, type_w, order) and ordered_v.index(w) > v_in_v + 1:
            for vi in ordered_v[v_in_v + 1:w_in_v]:
                if vi in ordered_w:
                    i = succ_index(v, vi, ordered_v)
                    j = pred_index(w, vi, ordered_w)
                    if 1 <= i <= math.floor(abs(type_v[0] - type_v[1]) / 2 - 1) and 1 <= j <= math.floor(abs(type_w[0] - type_w[1]) / 2 - 1):
                        #print(f"executing move 3")
                        move3(order, v, w, vi)
                        moved = True
                        break
        elif opposite(w, v, type_w, type_v, order) and ordered_w.index(v) > w_in_w + 1:
            for wj in ordered_w[w_in_w + 1:v_in_w]:
                if wj in ordered_v:
                    j = succ_index(w, wj, ordered_w)
                    i = pred_index(v, wj, ordered_v)
                    if 1 <= i <= math.floor(abs(type_v[0] - type_v[1]) / 2 - 1) and 1 <= j <= math.floor(abs(type_w[0] - type_w[1]) / 2 - 1):
                        #print(f"executing move 3opp")
                        move3(order, w, v, wj)
                        moved = True
                        break
        elif len(ordered_v) - 1 == degree:
            if type_v[0] - type_v[1] == 0:
                unbalanced = False
            else:
                unbalanced = True
                if type_v[0] > type_v[1]:
                    for i in range(1, math.floor(abs((type_v[0] - type_v[1]) / 2)) + 1):
                        vi = ordered_v[v_in_v + i]
                        ordered_vi = order_neighbor(order, list(graph.neighbors(vi)) + [vi])
                        type_vi = vertex_type(vi, ordered_vi)
                        if type_vi[0] - type_vi[1] == 0:
                            unbalanced = False
                            break
                    if unbalanced:
                        #print(f"executing move 4 on {edge}")
                        move4(order, v, type_v)
                        moved = True
                else:
                    for i in range(1, math.floor(abs((type_v[0] - type_v[1]) / 2)) + 1):
                        vi = ordered_v[v_in_v - i]
                        ordered_vi = order_neighbor(order, list(graph.neighbors(vi)) + [vi])
                        type_vi = vertex_type(vi, ordered_vi)
                        if type_vi[0] - type_vi[1] == 0:
                            unbalanced = False
                            break
                    if unbalanced:
                        #print(f"executing move 4opp")
                        move4opp(order, v, type_v)
                        moved = True
        elif len(ordered_w) - 1 == degree:
            if (type_w[0] - type_w[1]) == 0:
                unbalanced = False
            else:
                unbalanced = True
                if type_w[0] > type_w[1]:
                    for i in range(1, math.floor(abs((type_w[0] - type_w[1]) / 2)) + 1):
                        wi = ordered_w[w_in_w + i]
                        ordered_wi = order_neighbor(order, list(graph.neighbors(wi)) + [wi])
                        type_wi = vertex_type(wi, ordered_wi)
                        if type_wi[0] - type_wi[1] == 0:
                            unbalanced = False
                            break
                    if unbalanced:
                        #print(f"executing move 4")
                        move4(order, w, type_w)
                        moved = True
                elif type_w[0] < type_w[1]:
                    for i in range(1, math.floor(abs((type_w[0] - type_w[1]) / 2)) + 1):
                        wi = ordered_w[w_in_w - i]
                        ordered_wi = order_neighbor(order, list(graph.neighbors(wi)) + [wi])
                        type_wi = vertex_type(wi, ordered_wi)
                        if type_wi[0] - type_wi[1] == 0:
                            unbalanced = False
                            break
                    if unbalanced:
                        #print(f"executing move 4opp")
                        move4opp(order, w, type_w)
                        moved = True

        if moved:
            # If a movement occurred, extend `check` with edges of affected neighbors
            for x in set(graph.neighbors(v)).union(set(graph.neighbors(w))):
                for e in graph.edges(x, data=False):
                    in_check = False
                    for e2 in check:
                        if ((e[0] == e2[0] and e[1] == e2[1]) or (e[1] == e2[0] and e[0] == e2[1])):
                            in_check = True
                    #if edge not in check:  # Check if the edge is already in `check`
                    if not in_check:
                        check.append(edge)
        else:
            # If no movement occurred, remove the edge from the check list
            check.remove(edge)
        #print(check)
    return order
