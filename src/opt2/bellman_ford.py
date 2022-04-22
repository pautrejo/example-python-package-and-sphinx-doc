import numpy as np 

def bf_negative_cycle(graph):
    """
    Description
    -------
    Get the shortest path using the Bellman-Ford algorithm.

    Parameters
    -------
    G : Networkx DiGraph
        The input graph.

    Returns
    -------
    list
        A list with the shortest path.

    References
    -------
    https://en.wikipedia.org/wiki/Bellman–Ford_algorithm
    https://nbviewer.org/github/rcroessmann/sharing_public/blob/master/arbitrage_identification.ipynb
    """

    # Remove nan edges
    n = len(graph.nodes()) + 1
    edges = [edge for edge in graph.edges().data() if ~np.isnan(edge[2]['weight'])]

    # Add a starting node and add edges with zero weight to all other nodes
    start_node_edges = [(n-1, i, {'weight': 0}) for i in range(n-1)]
    edges = edges + start_node_edges

    # Initialize node distances and predecessors
    d = np.ones(n) * np.inf
    d[n - 1] = 0  # Starting node has zero distance
    p = np.ones(n) * -1

    # Relax n times
    for i in range(n):  
        x = -1
        for e in edges:
            if d[int(e[0])] + e[2]['weight'] < d[int(e[1])]:
                d[int(e[1])] = d[int(e[0])] + e[2]['weight']
                p[int(e[1])] = int(e[0])
                x = int(e[1])
        if x == -1:  # If no relaxation possible, no negative cycle
            return None
        
    # Identify negative cycle
    for i in range(n):
        x = p[int(x)]
    cycle = []
    v = x
    while True:
        cycle.append(int(v))
        if v == x and len(cycle) > 1:
            break
        v = p[int(v)]
    return list(reversed(cycle))