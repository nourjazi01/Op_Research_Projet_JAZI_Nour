from copy import deepcopy
from .max_flow import max_flow


def most_vital_arc(graph, source, sink):
    """
    Most vital arc:
    edge whose removal decreases max flow the most.
    """

    original_flow = max_flow(deepcopy(graph), source, sink)

    best_edge = None
    best_reduction = -1

    for u, edge in graph.original_edges():

        g_copy = deepcopy(graph)

        # remove edge
        for e in g_copy.adj[u]:
            if e.to == edge.to and e.capacity == edge.capacity:
                e.capacity = 0

        new_flow = max_flow(g_copy, source, sink)

        reduction = original_flow - new_flow

        if reduction > best_reduction:
            best_reduction = reduction
            best_edge = (u, edge.to)

    return best_edge, best_reduction