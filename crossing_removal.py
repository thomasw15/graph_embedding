import networkx as nx

from graph_embedding.graph import Graph
from graph_embedding.edge_construction import edge_routing

def overlap_vertices(edge1, edge2):
    """
    Determine the overlap between vertices of two edges.

    :param edge1: The first edge with arc data.
    :param edge2: The second edge with arc data.
    :param graph: The graph object.
    :return: List of indices [i, j] indicating overlap or False if no overlap.
    """
    if edge1["arcs"][0]["start"] == edge2["arcs"][0]["start"]:
        return [0, 0]
    elif edge1["arcs"][0]["start"] == edge2["arcs"][1]["start"]:
        return [0, 1]
    elif edge1["arcs"][1]["start"] == edge2["arcs"][0]["start"]:
        return [1, 0]
    elif edge1["arcs"][1]["start"] == edge2["arcs"][1]["start"]:
        return [1, 1]
    else:
        return False

def segment_cross(s1, s2):
    """
    Check if two segments cross in 3D space.

    :param s1: The first segment as a list of two points.
    :param s2: The second segment as a list of two points.
    :return: True if the segments cross, otherwise False.
    """
    [x1, y1, z1] = s1[0]
    [x2, y2, z2] = s1[1]
    [x3, y3, z3] = s2[0]
    [x4, y4, z4] = s2[1]

    if x1 == x2 and y3 == y4 and z1 == z3:  # Segment1 along x, Segment2 along y
        return min(x1, x2) <= x3 <= max(x1, x2) and min(y3, y4) <= y1 <= max(y3, y4)
    elif y1 == y2 and z3 == z4 and x1 == x3:  # Segment1 along y, Segment2 along z
        return min(y1, y2) <= y3 <= max(y1, y2) and min(z3, z4) <= z1 <= max(z3, z4)
    elif z1 == z2 and x3 == x4 and y1 == y3:  # Segment1 along z, Segment2 along x
        return min(z1, z2) <= z3 <= max(z1, z2) and min(x3, x4) <= x1 <= max(x3, x4)
    return False

def cross_check(edge1, edge2, graph: Graph):
    """
    Check if two edges cross based on their routes and anchors.

    :param edge1: The first edge with route and arc data.
    :param edge2: The second edge with route and arc data.
    :param graph: The graph object.
    :return: Crossing type or False if no crossing.
    """
    overlap = overlap_vertices(edge1, edge2)
    if not overlap:
        return False

    arc1 = edge1["arcs"][overlap[0]]
    arc2 = edge2["arcs"][overlap[1]]

    if overlap[0] == 0:
        route1 = edge1["route"]
    else:
        route1 = list(reversed(edge1["route"]))

    if overlap[1] == 0:
        route2 = edge2["route"]
    else:
        route2 = list(reversed(edge2["route"]))

    if arc1["anchor"] and arc2["anchor"]:
        # Check case 1
        s1 = [route1[1], route1[2]]
        s2 = [route2[1], route2[2]]
        if segment_cross(s1, s2):
            return 1
        # Check case 2b
        s1 = [route1[2], route1[3]]
        s2 = [route2[1], route2[2]]
        if segment_cross(s1, s2):
            return 2.2
        # Check case 3
        s1 = [route1[2], route1[3]]
        s2 = [route2[2], route2[3]]
        if segment_cross(s1, s2):
            return 3

    elif arc1["anchor"] and not arc2["anchor"]:
        # Check case 2a
        s1 = [route1[2], route1[3]]
        s2 = [route2[0], route2[1]]
        if segment_cross(s1, s2):
            return 2.1
        # Check case 3
        s1 = [route1[2], route1[3]]
        s2 = [route2[1], route2[2]]
        if segment_cross(s1, s2):
            return 3

    elif not arc1["anchor"] and arc2["anchor"]:
        # Check case 2b
        s1 = [route1[1], route1[2]]
        s2 = [route2[1], route2[2]]
        if segment_cross(s1, s2):
            return 2.2
        # Check case 3
        s1 = [route1[1], route1[2]]
        s2 = [route2[2], route2[3]]
        if segment_cross(s1, s2):
            return 3

    elif not arc1["anchor"] and not arc2["anchor"]:
        # Check case 3
        s1 = [route1[1], route1[2]]
        s2 = [route2[1], route2[2]]
        if segment_cross(s1, s2):
            return 3

def crossing_removal(graph):
    """
    Remove crossings in the graph through two phases.

    :param graph: The graph object with edges and arcs.
    """
    # Phase 1
    vertices_to_check = list(graph.nodes)

    while vertices_to_check:
        v = vertices_to_check[0]
        neighbors = list(graph.neighbors(v))
        action_taken = False

        for i, u in enumerate(neighbors):
            for w in neighbors[i+1:]:
                vu = graph.get_edge_data(v, u)
                vw = graph.get_edge_data(v, w)

                if vu and vw:
                    cross = cross_check(vu, vw, graph)

                    if cross in [2.2, 3]:
                        arc1 = vu["arcs"][0]  # Assume this arc relates to v -> u
                        arc2 = vw["arcs"][0]  # Assume this arc relates to v -> w

                        # Swap color and orientation
                        arc1["color"], arc2["color"] = arc2["color"], arc1["color"]
                        arc1["orientation"], arc2["orientation"] = arc2["orientation"], arc1["orientation"]

                        edge_routing(vu, graph)
                        edge_routing(vw, graph)

                        # Revisit neighbors
                        vertices_to_check.extend([u, w])
                        action_taken = True

        if not action_taken:
            vertices_to_check.pop(0)

    # Phase 2
    for v in graph.nodes:
        neighbors = list(graph.neighbors(v))

        for i, u in enumerate(neighbors):
            for w in neighbors[i+1:]:
                vu = graph.get_edge_data(v, u)
                vw = graph.get_edge_data(v, w)

                if vu and vw:
                    cross = cross_check(vu, vw, graph)

                    if cross in [1, 2.1]:
                        arc1 = vu["arcs"][0]  # Assume this arc relates to v -> u
                        arc2 = vw["arcs"][0]  # Assume this arc relates to v -> w

                        # Swap color and orientation
                        arc1["color"], arc2["color"] = arc2["color"], arc1["color"]
                        arc1["orientation"], arc2["orientation"] = arc2["orientation"], arc1["orientation"]

                        edge_routing(vu, graph)
                        edge_routing(vw, graph)
