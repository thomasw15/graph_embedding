import networkx as nx

from graph_embedding.graph import Graph
from graph_embedding.helper import perpendicular, missing, point_toward

def edge_route1(arc1, arc2, graph: Graph):
    step1 = list(graph.nodes[arc1["start"]]["position"])
    step1[arc1["color"]] = graph.nodes[arc1["end"]]["position"][arc1["color"]]
    step2 = step1.copy()
    step2_color = missing(arc1["color"], arc2["color"])
    step2[step2_color] = graph.nodes[arc1["end"]]["position"][step2_color]
    arc1["anchor"] = False
    arc2["anchor"] = False
    return [graph.nodes[arc1["start"]]["position"], step1, step2, graph.nodes[arc1["end"]]["position"]]

def edge_route2(arc1, arc2, graph: Graph):
    if perpendicular(arc1, arc2):
        step1 = list(graph.nodes[arc1["start"]]["position"])
        step1[arc1["color"]] += arc1["orientation"] * 1
        step2 = step1.copy()
        step2_color = missing(arc1["color"], arc2["color"])
        step2[step2_color] = graph.nodes[arc1["end"]]["position"][step2_color]
        step3 = step2.copy()
        step3[arc1["color"]] = graph.nodes[arc1["end"]]["position"][arc1["color"]]
        arc1["anchor"] = True
        arc2["anchor"] = False
        return [graph.nodes[arc1["start"]]["position"], step1, step2, step3, graph.nodes[arc1["end"]]["position"]]
    else:
        step1 = list(graph.nodes[arc1["start"]]["position"])
        step1[arc1["color"]] += arc1["orientation"] * 1
        step2 = step1.copy()
        step2_color = missing(arc1["color"], arc2["color"])
        step2[step2_color] = graph.nodes[arc1["end"]]["position"][step2_color]
        step3 = step2.copy()
        step3_color = missing(arc1["color"], step2_color)
        step3[step3_color] = graph.nodes[arc1["end"]]["position"][step3_color]
        arc1["anchor"] = True
        arc2["anchor"] = False
        return [graph.nodes[arc1["start"]]["position"], step1, step2, step3, graph.nodes[arc1["end"]]["position"]]

def edge_route3(arc1, arc2, graph: Graph):
    step1 = list(graph.nodes[arc1["start"]]["position"])
    step1[arc1["color"]] += arc1["orientation"] * 1
    step2 = step1.copy()
    step2_color = missing(arc1["color"], arc2["color"])
    step2[step2_color] = graph.nodes[arc1["end"]]["position"][step2_color]
    step3 = step2.copy()
    step3_color = missing(arc1["color"], step2_color)
    step3[step3_color] = graph.nodes[arc1["end"]]["position"][step3_color]
    arc1["anchor"] = True
    arc2["anchor"] = False
    return [graph.nodes[arc1["start"]]["position"], step1, step2, step3, graph.nodes[arc1["end"]]["position"]]

def edge_route4(arc1, arc2, graph: Graph):
    if perpendicular(arc1, arc2):
        step1 = list(graph.nodes[arc1["start"]]["position"])
        step1[arc1["color"]] += arc1["orientation"] * 1
        step2 = step1.copy()
        step2[arc2["color"]] += arc2["orientation"] * 1
        step3 = step2.copy()
        step3_color = missing(arc1["color"], arc2["color"])
        step3[step3_color] = graph.nodes[arc1["end"]]["position"][step3_color]
        step4 = list(graph.nodes[arc1["end"]]["position"])
        step4[arc2["color"]] += arc2["orientation"] * 1
        arc1["anchor"] = True
        arc2["anchor"] = True
        return [graph.nodes[arc1["start"]]["position"], step1, step2, step3, step4, graph.nodes[arc1["end"]]["position"]]
    else:
        step1 = list(graph.nodes[arc1["start"]]["position"])
        step1[arc1["color"]] += arc1["orientation"] * 1
        step2 = step1.copy()
        step2_color = missing(arc1["color"], arc2["color"])
        step2[step2_color] = graph.nodes[arc1["end"]]["position"][step2_color]
        step3 = step2.copy()
        step3[arc2["color"]] += arc2["orientation"] * 1
        step4 = list(graph.nodes[arc1["end"]]["position"])
        step4[arc2["color"]] += arc2["orientation"] * 1
        arc1["anchor"] = True
        arc2["anchor"] = True
        return [graph.nodes[arc1["start"]]["position"], step1, step2, step3, step4, graph.nodes[arc1["end"]]["position"]]

def edge_routing(edge, graph: Graph):
    arc1, arc2 = edge["arcs"]
    if perpendicular(arc1, arc2) and point_toward(arc1, graph) and point_toward(arc2, graph):
        edge["route"] = edge_route1(arc1, arc2, graph)
    elif not point_toward(arc1, graph) and point_toward(arc2, graph):
        edge["route"] = edge_route2(arc1, arc2, graph)
    elif not point_toward(arc2, graph) and point_toward(arc1, graph):
        edge["route"] = list(reversed(edge_route2(arc2, arc1, graph)))
    elif not perpendicular(arc1, arc2) and point_toward(arc1, graph) and point_toward(arc2, graph):
        edge["route"] = edge_route3(arc1, arc2, graph)
    elif not point_toward(arc1, graph) and not point_toward(arc2, graph):
        edge["route"] = edge_route4(arc1, arc2, graph)

def edge_construction(graph: Graph):
    for _, _, edge_data in graph.edges(data=True):
        edge_routing(edge_data, graph)