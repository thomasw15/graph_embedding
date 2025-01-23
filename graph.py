import networkx as nx

class Graph(nx.Graph):
    def __init__(self):
        """
        Initialize an empty graph using networkx.
        """
        super().__init__()
        self.default_vertex_attributes = {
            "position": None,
            "type": None,
        }
        self.default_edge_attributes = {
            "arcs": None,
            "route": None,
        }
        self.default_arc_attributes = {
            "color": None,
            "orientation": None,
            "movement": None,
            "special": None,
            "anchor": None,
        }

    def add_vertex(self, vertex_id, **attributes):
        """
        Add a vertex to the graph with preset attributes.

        :param vertex_id: Unique identifier for the new vertex.
        :param attributes: Optional attributes for the vertex.
        """
        vertex_attrs = {**self.default_vertex_attributes, **attributes}
        self.add_node(vertex_id, **vertex_attrs)

    def set_vertices(self, vertices):
        """
        Set the vertices of the graph to a given list of vertices.
        
        :param vertices: List of Vertex or other objects to set as vertices in the graph.
        """
        for v in vertices:
            self.add_vertex(v)
        # Reset edges since the graph structure may change
        self.edges = []
    
    def add_edge(self, start_id, end_id, **attributes):
        """
        Add an edge to the graph, setting up directed arcs as attributes.

        :param start_id: Unique identifier for the start vertex.
        :param end_id: Unique identifier for the end vertex.
        :param attributes: Optional attributes for the edge.
        """
        arc1 = {**self.default_arc_attributes, "start": start_id, "end": end_id}
        arc2 = {**self.default_arc_attributes, "start": end_id, "end": start_id}
        edge_attrs = {**self.default_edge_attributes, "arcs": [arc1, arc2], **attributes}
        super().add_edge(start_id, end_id, **edge_attrs)

    def get_arcs(self):
        """
        Retrieve all arcs (directed edges) from the graph.

        :return: List of arcs with attributes.
        """
        arcs = []
        edges = list(self.edges(data=True))
        for e in edges:
            arcs.append((e[0],e[1]))
            arcs.append((e[1],e[0]))
        return arcs

    def get_edges(self):
        """
        Retrieve all arcs (directed edges) from the graph.

        :return: List of arcs with attributes.
        """
        edges = list(self.edges(data=False))
        return edges

    def get_arc(self, start_id, end_id):
        """
        Retrieve the attributes of a specific directed arc.

        :param start_id: ID of the start vertex.
        :param end_id: ID of the end vertex.
        :return: Dictionary of arc attributes if the arc exists, otherwise None.
        """
        edge_data = self.get_edge_data(start_id, end_id)
        if edge_data and "arcs" in edge_data:
            for arc in edge_data["arcs"]:
                if arc["start"] == start_id and arc["end"] == end_id:
                    return arc
        return None

    def get_vertex(self, vertex_id):
        """
        Retrieve a vertex from the graph.
    
        :param vertex_id: The ID of the vertex to retrieve.
        :return: A dictionary of the vertex's attributes if it exists, otherwise None.
        """
        if vertex_id in self.nodes:
            return self.nodes[vertex_id]
        else: 
            raise ValueError(f"{vertex_id} is not a vertex of {self}")

    def set_default_attributes(self, vertex_attrs=None, edge_attrs=None, arc_attrs=None):
        """
        Set default attributes for vertices, edges, and arcs.

        :param vertex_attrs: Dictionary of default vertex attributes.
        :param edge_attrs: Dictionary of default edge attributes.
        :param arc_attrs: Dictionary of default arc attributes.
        """
        if vertex_attrs:
            self.default_vertex_attributes.update(vertex_attrs)
        if edge_attrs:
            self.default_edge_attributes.update(edge_attrs)
        if arc_attrs:
            self.default_arc_attributes.update(arc_attrs)

    def contracted_nodes(self, node1, node2):
        """
        Contract two nodes in the graph into a single node.
    
        :param node1: The first node to contract.
        :param node2: The second node to contract.
        :return: A new graph with the nodes contracted.
        """

        neighbors = list(self.neighbors(node2))
        for neighbor in neighbors:
            self.add_edge(node1,neighbor)
        self.remove_node(node2)
    
    def __repr__(self):
        """
        Representation of the graph showing its vertices and edges.
        """
        vertices = ", ".join(map(str, self.nodes))
        edges = list(self.edges)
        return f"Graph(Vertices: [{vertices}], Edges: {edges})"


