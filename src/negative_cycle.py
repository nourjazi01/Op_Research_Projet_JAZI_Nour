from typing import Optional

from .graph import Graph


def find_negative_cycle(graph: Graph) -> Optional[list[str]]:
    """
    Detects a negative cycle in the residual graph using Bellman-Ford.

    We initialize all distances to 0 so that we can detect a negative cycle
    anywhere in the graph, not only cycles reachable from one source.
    """
    nodes = graph.nodes()
    dist = {node: 0 for node in nodes}
    parent: dict[str, tuple[str, int]] = {}

    last_updated = None

    for _ in range(len(nodes)):
        last_updated = None

        for u in nodes:
            for i, edge in enumerate(graph.adj[u]):
                if edge.residual_capacity <= 0:
                    continue

                v = edge.to

                if dist[v] > dist[u] + edge.cost:
                    dist[v] = dist[u] + edge.cost
                    parent[v] = (u, i)
                    last_updated = v

    if last_updated is None:
        return None

    # Move inside the cycle.
    x = last_updated
    for _ in range(len(nodes)):
        x = parent[x][0]

    cycle = []
    current = x
    seen = set()

    while current not in seen:
        seen.add(current)
        cycle.append(current)
        current = parent[current][0]

    cycle.append(current)
    cycle.reverse()

    return cycle
