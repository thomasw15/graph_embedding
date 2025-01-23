import networkx as nx

from graph_embedding.graph import Graph
from graph_embedding.edge_construction import edge_construction
from graph_embedding.crossing_removal import crossing_removal

def general_position_drawing(graph: Graph, vertex_positions):
    """
    Generate the 3D general position drawing of the graph.

    :param G: The graph object.
    :param vertex_positions: A dictionary mapping each vertex to its position in 3D space.
    :return: A dictionary containing 3D coordinates for each vertex and arc paths.
    """
    for v_id, features in graph.nodes(data = True):
        features["position"] = [0,0,0]
        for i in range(0,3):
            features["position"][i] = 3 * (vertex_positions[i].index(v_id) + 1)

    edge_construction(graph) 
    crossing_removal(graph)