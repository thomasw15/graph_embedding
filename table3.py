def table3(v, type_v, ordered_v):
    """
    Determine the port assignment table for a given vertex.

    :param v: The vertex.
    :param type_v: The type of the vertex as [succ, pred].
    :param ordered_v: The ordered neighbors of the vertex.
    :return: List of assigned nodes for the vertex.
    """
    nodes = [False, False, False, False, False, False]
    v_in_v = ordered_v.index(v)

    #### start from here
    if type_v[0] < 4 and type_v[1] < 4:
        if type_v[0] >= type_v[1]:
            for i in range(0, type_v[0]):
                nodes[3 + i] = ordered_v[v_in_v + i + 1]
            for i in range(0, type_v[1]):
                nodes[3 - i - 1] = ordered_v[v_in_v - i - 1]
        if type_v[0] < type_v[1]:
            for i in range(0, type_v[0]):
                nodes[3 + i] = ordered_v[v_in_v - i - 1]
            for i in range(0, type_v[1]):
                nodes[3 - i - 1] = ordered_v[v_in_v + i + 1]

    if type_v == [4, 0]:
        nodes = [ordered_v[v_in_v + 1], False, False, ordered_v[v_in_v + 2], ordered_v[v_in_v + 3], ordered_v[v_in_v + 4]]
    if type_v == [0, 4]:
        nodes = [ordered_v[v_in_v - 1], False, False, ordered_v[v_in_v - 2], ordered_v[v_in_v - 3], ordered_v[v_in_v - 4]]
    if type_v == [4, 1]:
        nodes = [ordered_v[v_in_v - 1], ordered_v[v_in_v + 1], False, ordered_v[v_in_v + 2], ordered_v[v_in_v + 3], ordered_v[v_in_v + 4]]
    if type_v == [1, 4]:
        nodes = [ordered_v[v_in_v + 1], ordered_v[v_in_v - 1], False, ordered_v[v_in_v - 2], ordered_v[v_in_v - 3], ordered_v[v_in_v - 4]]
    if type_v == [4, 2]:
        nodes = [ordered_v[v_in_v - 2], ordered_v[v_in_v - 1], ordered_v[v_in_v + 1], ordered_v[v_in_v + 2], ordered_v[v_in_v + 3], ordered_v[v_in_v + 4]]
    if type_v == [2, 4]:
        nodes = [ordered_v[v_in_v + 2], ordered_v[v_in_v + 1], ordered_v[v_in_v - 1], ordered_v[v_in_v - 2], ordered_v[v_in_v - 3], ordered_v[v_in_v - 4]]
    if type_v == [5, 0]:
        nodes = [ordered_v[v_in_v + 1], ordered_v[v_in_v + 2], False, ordered_v[v_in_v + 3], ordered_v[v_in_v + 4], ordered_v[v_in_v + 5]]
    if type_v == [0, 5]:
        nodes = [ordered_v[v_in_v - 1], ordered_v[v_in_v - 2], False, ordered_v[v_in_v - 3], ordered_v[v_in_v - 4], ordered_v[v_in_v - 5]]
    if type_v == [5, 1]:
        nodes = [ordered_v[v_in_v - 1], ordered_v[v_in_v + 1], ordered_v[v_in_v + 2], ordered_v[v_in_v + 3], ordered_v[v_in_v + 4], ordered_v[v_in_v + 5]]
    if type_v == [1, 5]:
        nodes = [ordered_v[v_in_v + 1], ordered_v[v_in_v - 1], ordered_v[v_in_v - 2], ordered_v[v_in_v - 3], ordered_v[v_in_v - 4], ordered_v[v_in_v - 5]]
    if type_v == [6, 0]:
        nodes = [ordered_v[v_in_v + 1], ordered_v[v_in_v + 2], ordered_v[v_in_v + 3], ordered_v[v_in_v + 4], ordered_v[v_in_v + 5], ordered_v[v_in_v + 6]]
    if type_v == [0, 6]:
        nodes = [ordered_v[v_in_v - 1], ordered_v[v_in_v - 2], ordered_v[v_in_v - 3], ordered_v[v_in_v - 4], ordered_v[v_in_v - 5], ordered_v[v_in_v - 6]]

    return nodes