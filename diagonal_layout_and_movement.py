import networkx as nx

from graph_embedding.graph import Graph
from graph_embedding.balanced_ordering import balanced_ordering
from graph_embedding.movement_special import movement_special
from graph_embedding.port_assignment import port_assignment
from graph_embedding.general_position_drawing import general_position_drawing

def diagonal_layout_and_movement(G: Graph):
    """
    Generate the diagonal layout and movement for the graph based on prior algorithms.

    :param G: The graph object.
    :return: A dictionary containing diagonal layouts and movement details.
    """
    # Step 1: Initialize balanced vertex orderings for X, Y, Z
    order = balanced_ordering(G)
    vertex_positions = [order, order, order]  #[X_order, Y_order, Z_order]

    # Step 2: Label arcs as movement or special based on table 2
    movement_special(G, order)  # Using X_order for arc classification

    # Step 3: Perform port assignment
    port_assignment(G, order)

    # Step 4: Move the end point of movement arcs accordingly
    arcs_of_G = G.get_arcs()
    for arc in arcs_of_G:
        arc_info = G.get_arc(arc[0],arc[1])
        if arc_info["movement"]:
            vertex_positions[arc_info["color"]].remove(arc_info["start"])
            vertex_positions[arc_info["color"]].insert(order.index(arc_info["end"]) + 1, arc_info["start"])

    # Generate general position drawing
    general_position_drawing(G, vertex_positions)