import networkx as nx
import copy

from graph_embedding.graph import Graph
from graph_embedding.helper import order_neighbor, vertex_type
from graph_embedding.table3 import table3
from graph_embedding.lovasz_3_coloring import lovasz_3_coloring

def clique(H, nodes, v):
    """
    Add cliques to the auxiliary graph H based on nodes connected to vertex v.

    :param H: Auxiliary graph.
    :param G: Original graph.
    :param nodes: List of nodes to form cliques.
    :param v: The reference vertex.
    """
    count = 0
    real_nodes = []

    for i in range(3):
        if nodes[i] is not False:
            count += 1
            real_nodes.append(nodes[i])
    if count == 2:
        v1 = (v, real_nodes[0])
        v2 = (v, real_nodes[1])
        if v1 not in list(H.neighbors(v2)):
            H.add_edge(v1, v2)
    elif count == 3:
        v1 = (v, real_nodes[0])
        v2 = (v, real_nodes[1])
        v3 = (v, real_nodes[2])
        if v1 not in list(H.neighbors(v2)):
            H.add_edge(v1, v2)
        if v1 not in list(H.neighbors(v3)):
            H.add_edge(v1, v3)
        if v3 not in list(H.neighbors(v2)):
            H.add_edge(v2, v3)

def arc_graph(G: Graph, order, arcs_of_G, vertices, edges):
    """
    Create an auxiliary graph H based on arc relationships in the original graph G.

    :param G: Original graph.
    :param order: Order of vertices.
    :param arcs_of_G: List of arcs in G.
    :param vertices: List of vertices in G.
    :param edges: List of edges in G.
    :return: The auxiliary graph H.
    """
    H = Graph()
    H.set_vertices(arcs_of_G)

    for v in vertices:
        ordered_v = order_neighbor(order, list(G.neighbors(v))+[v])
        type_v = vertex_type(v, ordered_v)
        nodes = table3(v, type_v, ordered_v)
        # Step a
        clique(H, nodes[:3], v)
        clique(H, nodes[3:], v)

        # Step d
        v_in_v = ordered_v.index(v)
        if type_v in [[6, 0], [5, 0]]:
            v1 = (v, ordered_v[v_in_v + 2])
            v2 = (ordered_v[v_in_v + 1], v)
            if v1 not in list(H.neighbors(v2)):
                H.add_edge(v1, v2)
        elif type_v in [[0, 6], [0, 5]]:
            v1 = (v, ordered_v[v_in_v - 2])
            v2 = (ordered_v[v_in_v - 1], v)
            if v1 not in list(H.neighbors(v2)):
                H.add_edge(v1, v2)

    # Step b
    for e in edges:
        arc1 = (e[0], e[1])
        arc2 = (e[1], e[0])
        arc1_info = G.get_arc(arc1[0],arc1[1])
        arc2_info = G.get_arc(arc2[0],arc2[1])
        if not arc1_info['special'] and not arc2_info['special']:
            v1 = arc1
            v2 = arc2
            if v1 not in list(H.neighbors(v2)):
                H.add_edge(v1, v2)

    # Step c
    for arc1 in arcs_of_G:
        arc1_info = G.get_arc(arc1[0],arc1[1])
        if arc1_info["movement"]:
            for arc2 in arcs_of_G:
                if arc2 != arc1:
                    arc2_info = G.get_arc(arc2[0],arc2[1])
                    if arc2_info["start"] == arc1_info["end"] and arc2_info["movement"]:
                        v1 = arc1
                        v2 = arc2
                        if v1 not in list(H.neighbors(v2)):
                            H.add_edge(v1, v2)
    
    return H

def clean_up(H: Graph, G: Graph, order):
    """
    Clean up the auxiliary graph H by considering vertex properties and simplifying the structure.

    :param H: Auxiliary graph.
    :return: A tuple of the cleaned-up graph and a mapping of merged vertices.
    """
    H_cleaned = copy.deepcopy(H)
    merged_vertices = {}
    layer1 = []
    layer2 = []
    G_vertices = list(G.nodes())

    for v in G_vertices:
        if G.degree(v) == 6:
            ordered_v = order_neighbor(order, list(G.neighbors(v))+[v])
            type_v = vertex_type(v, ordered_v)
            nodes = table3(v, type_v, ordered_v)
            if type_v[0] != type_v[1] and (v, nodes[2]) in list(H_cleaned.nodes()):
                layer1.append((v, nodes[2]))
                H_cleaned.remove_node((v, nodes[2]))

    for v in G_vertices:
        ordered_v = order_neighbor(order, list(G.neighbors(v))+[v])
        type_v = vertex_type(v, ordered_v)
        nodes = table3(v, type_v, ordered_v)
        if type_v == [0,5] or type_v == [0,6] or type_v == [5,0] or type_v == [6,0]: 
            v1 = nodes[0]
            ordered_v1 = order_neighbor(order, list(G.neighbors(v1))+[v1])
            type_v1 = vertex_type(v1, ordered_v1)
            v2 = nodes[1]
            ordered_v2 = order_neighbor(order, list(G.neighbors(v2))+[v2])
            type_v2 = vertex_type(v2, ordered_v2)
            if type_v1 == [1, 4] or type_v1 == [1, 5] or type_v1 == [4, 1] or type_v1 == [5, 1]:
                nodes_v1 = table3(v1, type_v1, ordered_v1)
                if (v1,nodes_v1[1]) in list(H_cleaned.nodes()):
                    merged_vertices[(v, v2)] = (v1, nodes_v1[1])
                    for neighbor in list(H_cleaned.neighbors((v1, nodes_v1[1]))):
                        if neighbor not in list(H_cleaned.neighbors((v, v2))):
                            H_cleaned.add_edge((v, v2), neighbor)
                    H_cleaned.remove_node((v1, nodes_v1[1]))
                if (v1, v) in list(H_cleaned.nodes()):
                    layer2.append((v1,v))
                    H_cleaned.remove_node((v1, v))
                if (v, v1) in list(H_cleaned.nodes()):
                    layer2.append((v,v1))
                    H_cleaned.remove_node((v, v1))
                if type_v2 == [1, 4] or type_v2 == [1, 5] or type_v2 == [4, 1] or type_v2 == [5, 1]:
                    if (v2,v) in list(H_cleaned.nodes()):
                        layer2.append((v2,v))
                        H_cleaned.remove_node((v2,v))
            else:
                if (v, v1) in list(H_cleaned.nodes()):
                    layer2.append((v, v1))
                    H_cleaned.remove_node((v, v1))
        elif type_v == [1, 4] or type_v == [1, 5] or type_v == [4, 1] or type_v == [5, 1]:
            vm1 = nodes[0]
            ordered_vm1 = order_neighbor(order, list(G.neighbors(vm1))+[vm1])
            type_vm1 = vertex_type(vm1, ordered_vm1)
            if type_vm1[0] >= type_vm1[1]:
                vm11 = ordered_vm1[ordered_vm1.index(vm1)+1]
            else:
                vm11 = ordered_vm1[ordered_vm1.index(vm1)-1]
            if not (type_vm1 == [0,5] or type_vm1 == [5,0]) and not vm11 == v:
                if (v, vm1) in list(H_cleaned.nodes()):
                    layer2.append((v,vm1))
                    H_cleaned.remove_node((v,vm1))
        elif type_v == [0,4] or type_v == [4,0]:
                if (v, nodes[0]) in list(H_cleaned.nodes()):
                    layer2.append((v, nodes[0]))
                    H_cleaned.remove_node((v, nodes[0]))
        
    return H_cleaned, merged_vertices, layer1, layer2

def transfer_coloring(H: Graph, H_cleaned, merged_vertices, cleaned_colors, layer1, layer2):
    """
    Transfer 3-coloring from H_cleaned to the original graph H using merged vertices information.

    :param H: Original graph.
    :param H_cleaned: Cleaned auxiliary graph.
    :param merged_vertices: Mapping of merged vertices in H_cleaned to their original counterparts in H.
    :param coloring_cleaned: 3-coloring of H_cleaned.
    :return: A dictionary mapping vertices in H to their colors.
    """
    colors = {v: None for v in H.nodes}

    # Assign colors for unmerged vertices
    for vertex in H_cleaned.nodes:
        colors[vertex] = cleaned_colors[vertex]

    # Assign colors for merged vertices
    for representative, original_vertices in merged_vertices.items():
        color = cleaned_colors[representative]
        colors[representative] = color
        colors[original_vertices] = color

    for vertex in layer2:
        neighbor_colors = {colors[neighbor] for neighbor in H.neighbors(vertex) if colors[neighbor] is not None}
        for color in range(0, 3):
            if color not in neighbor_colors:
                colors[vertex] = color
        if colors[vertex] is None:
            raise ValueError(f"Failed to assign color to vertex {vertex}.")

    for vertex in layer1:
        neighbor_colors = {colors[neighbor] for neighbor in H.neighbors(vertex) if colors[neighbor] is not None}
        for color in range(0, 3):
            if color not in neighbor_colors:
                colors[vertex] = color
        if colors[vertex] is None:
            raise ValueError(f"Failed to assign color to vertex {vertex}.")
            
    return colors

def port_assignment(G: Graph, order):
    """
    Assign ports to arcs in the graph based on vertex types and order.

    :param G: The graph object.
    :param order: The order of vertices.
    :return: None.
    """
    arcs_of_G = G.get_arcs()
    vertices = list(G.nodes)
    edges = list(G.edges)
    counter = 0

    for v in vertices:
        ordered_v = order_neighbor(order, list(G.neighbors(v))+[v])
        type_v = vertex_type(v, ordered_v)
        nodes = table3(v, type_v, ordered_v)
        neighbors_worked = 0

        if type_v[0] >= type_v[1]:
            for node in nodes[:3]:
                if node is not False:
                    arc = G.get_arc(v, node)
                    arc["orientation"] = -1
                    counter += 1
                    neighbors_worked += 1
            for node in nodes[3:]:
                if node is not False:
                    arc = G.get_arc(v, node)
                    arc["orientation"] = 1
                    counter += 1
                    neighbors_worked += 1
        else:
            for node in nodes[:3]:
                if node is not False:
                    arc = G.get_arc(v, node)
                    arc["orientation"] = 1
                    counter += 1
                    neighbors_worked += 1
            for node in nodes[3:]:
                if node is not False:
                    arc = G.get_arc(v, node)
                    arc["orientation"] = -1
                    counter += 1
                    neighbors_worked += 1
        if neighbors_worked != len(ordered_v)-1:
            raise ValueError(f"assigned orientation to {neighbors_worked} arcs but there are totally {len(ordered_v)-1}")
        
    if counter != len(arcs_of_G):
        raise ValueError(f"total number of arcs assigned orientation is {counter} and total number of arcs is {len(arcs_of_G)}")

    # Step 1: Create and clean up the auxiliary graph
    H = arc_graph(G, order, arcs_of_G, vertices, edges)
    H_cleaned, merged_vertices, layer1, layer2 = clean_up(H, G, order)

    # Step 2: Apply Lovasz's 3-coloring to the cleaned graph
    coloring_cleaned = lovasz_3_coloring(H_cleaned)

    # Step 3: Transfer coloring back to the original graph
    final_coloring = transfer_coloring(H, H_cleaned, merged_vertices, coloring_cleaned, layer1, layer2)

    # Step 4: Assign colors to ports
    for arc in arcs_of_G:
        arc_color = final_coloring[arc]
        arc_info = G.get_arc(arc[0],arc[1])
        arc_info["color"] = arc_color
