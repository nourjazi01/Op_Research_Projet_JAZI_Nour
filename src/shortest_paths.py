import heapq
from typing import Dict, Tuple, Optional

from .graph import Graph


Parent = Dict[str, Tuple[str, int]]


def bellman_ford_shortest_path(graph: Graph, source: str) -> tuple[Dict[str, float], Parent]:
    """
    Bellman-Ford on the residual graph.
    Only edges with positive residual capacity are considered.
    Works with negative costs if there is no negative cycle reachable from source.
    """
    nodes = graph.nodes()
    dist = {node: float("inf") for node in nodes}
    parent: Parent = {}

    dist[source] = 0

    for _ in range(len(nodes) - 1):
        changed = False

        for u in nodes:
            if dist[u] == float("inf"):
                continue

            for i, edge in enumerate(graph.adj[u]):
                if edge.residual_capacity <= 0:
                    continue

                v = edge.to
                new_dist = dist[u] + edge.cost

                if new_dist < dist[v]:
                    dist[v] = new_dist
                    parent[v] = (u, i)
                    changed = True

        if not changed:
            break

    return dist, parent


def dijkstra_with_potentials(
    graph: Graph,
    source: str,
    potentials: Dict[str, float],
) -> tuple[Dict[str, float], Parent]:
    """
    Dijkstra on reduced costs:
    cR(u, v) = c(u, v) + potential[u] - potential[v]

    If potentials are valid, all reduced costs are non-negative.
    """
    dist = {node: float("inf") for node in graph.nodes()}
    parent: Parent = {}

    dist[source] = 0
    pq = [(0, source)]

    while pq:
        current_dist, u = heapq.heappop(pq)

        if current_dist != dist[u]:
            continue

        for i, edge in enumerate(graph.adj[u]):
            if edge.residual_capacity <= 0:
                continue

            reduced_cost = edge.cost + potentials[u] - potentials[edge.to]

            # Small numerical tolerance in case floats appear.
            if reduced_cost < -1e-9:
                raise ValueError(
                    f"Negative reduced cost found on edge {u}->{edge.to}: {reduced_cost}"
                )

            new_dist = dist[u] + reduced_cost

            if new_dist < dist[edge.to]:
                dist[edge.to] = new_dist
                parent[edge.to] = (u, i)
                heapq.heappush(pq, (new_dist, edge.to))

    return dist, parent


def reconstruct_path(parent: Parent, source: str, sink: str) -> Optional[list[tuple[str, int]]]:
    if sink not in parent:
        return None

    path = []
    v = sink

    while v != source:
        u, edge_index = parent[v]
        path.append((u, edge_index))
        v = u

    path.reverse()
    return path
