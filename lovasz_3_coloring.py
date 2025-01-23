import networkx as nx
import copy

from graph_embedding.graph import Graph

def lower_coloring(graph):
    # Ensure the graph has degree lower than 3
    max_degree = max(dict(graph.degree()).values())
    if max_degree >= 3:
        raise ValueError("Graph has degree higher than two.")
    vertices = list(graph.nodes)
    colors = {v: None for v in graph.nodes}

    a = vertices.pop(0)
    colors[a] = 0
    for v in vertices:
        neighbor_colors = {colors[neighbor] for neighbor in graph.neighbors(v) if colors[neighbor] is not None}
        for color in range(0, 3):
            if color not in neighbor_colors:
                colors[v] = color
        if colors[v] is None:
            raise ValueError(f"Failed to assign color to vertex {v}.")
    
    return colors

def lovasz_3_coloring(graph: Graph):
    """
    Implements Lovasz's algorithm for 3-coloring based on Brooks' theorem.

    :param graph: The graph to be colored.
    :return: A dictionary mapping each vertex to a color (0, 1, or 2).
    """
    # Ensure the graph does not contain K_(Delta + 1)
    max_degree = max(dict(graph.degree()).values())
    if max_degree < 3:
        colors = lower_coloring(graph)
        return colors

    # Check if the graph contains a complete subgraph K_(Delta + 1)
    for node in graph.nodes:
        if len(list(graph.neighbors(node))) == max_degree + 1:
            raise ValueError("Graph contains a K_(Delta + 1), which is not supported.")

    # Sequential ordering of vertices
    vertices = list(graph.nodes)
    # Initialize colors for vertices
    colors = {v: None for v in graph.nodes}
    points_picked = False

    if nx.is_connected(graph):
        for a in vertices:
            found = False
            for neighbor in graph.neighbors(a):
                for two_neighbor in graph.neighbors(neighbor):
                    if two_neighbor != a and not two_neighbor in graph.neighbors(a):
                        copied = copy.deepcopy(graph)
                        copied = nx.Graph(copied)
                        copied.remove_nodes_from([a,two_neighbor])
                        if nx.is_connected(copied):
                            points_picked = True
                            found = True
                            b = two_neighbor
                            v1 = neighbor
                            break
                    if found:
                        break
            if found:
                break
        
        if points_picked is False:
            if nx.is_biconnected(graph):
                for v0 in vertices:
                    if graph.degree(v0) == 3 and graph.degree(v0) < len(list(graph.nodes())):
                        a = v0
                        copied = copy.deepcopy(graph)
                        copied = nx.Graph(copied)
                        copied.remove_node(a)
                        if nx.is_biconnected(copied):
                            found = False
                            for neighbor in graph.neighbors(a):
                                for two_neighbor in graph.neighbors(neighbor):
                                    if two_neighbor != a and not two_neighbor in graph.neighbors(a):
                                        b = two_neighbor
                                        found = True
                                        points_picked = True
                                        neighbor = v1
                                        break
                                if found:
                                    break
                        else:
                            v1 = a
                            for a in graph.neighbors(v1):
                                for b in graph.neighbors(v1):
                                    if a != b:
                                        copied = copy.deepcopy(graph)
                                        copied = nx.Graph(copied)
                                        copied.remove_nodes_from([a,b])
                                        if nx.is_connected(copied):
                                            found = True
                                            points_picked = True
                                            break
                    if points_picked:
                        break
            else:
                for a in vertices:
                    copied = copy.deepcopy(graph)
                    copied = nx.Graph(copied)
                    copied.remove_node(a)
                    if not nx.is_connected(copied):
                        break
                components = nx.connected_components(copied)
                for generators in components:
                    subgraph = graph.subgraph(generators)
                    subgraph_color = lovasz_3_coloring(subgraph)
                    colors.update(subgraph_color)

                neighbor_colors = {colors[neighbor] for neighbor in graph.neighbors(a) if colors[neighbor] is not None}
                for color in range(0, 3):
                    if color not in neighbor_colors:
                        colors[a] = color
                        
                if colors[a] is None:
                    for vertex, color in subgraph_color.items():
                        subgraph_color[vertex] = (color + 1) % 3
                    colors.update(subgraph_color)
                neighbor_colors = {colors[neighbor] for neighbor in graph.neighbors(a) if colors[neighbor] is not None}
                for color in range(0, 3):
                    if color not in neighbor_colors:
                        colors[a] = color
                return colors
    else:
        components = nx.connected_components(graph)
        for generators in components:
            subgraph = graph.subgraph(generators)
            subgraph_color = lovasz_3_coloring(subgraph)
            colors.update(subgraph_color)
        return colors

    # Assign colors sequentially
    colors[a] = 0
    colors[b] = 0
    vertices.remove(a)
    vertices.remove(b)
    vertices.remove(v1)
    ordered_vertices = [v1]
    while len(vertices) > 0:
        for vi in ordered_vertices:
            found = False
            for vii in graph.neighbors(vi):
                if vii in vertices and not (vii in ordered_vertices):
                    ordered_vertices.append(vii)
                    vertices.remove(vii)
                    break
            if found:
                break
    if len(vertices) > 0:
        raise ValueError(f"Failed to order all vertices {vertices} are the vertices not added.")
    ordered_vertices.reverse()
    for vertex in ordered_vertices:
        neighbor_colors = {colors[neighbor] for neighbor in graph.neighbors(vertex) if colors[neighbor] is not None}
        for color in range(0, 3):
            if color not in neighbor_colors:
                colors[vertex] = color
        if colors[vertex] is None:
            raise ValueError(f"Failed to assign color to vertex {vertex}.")
    
    return colors
