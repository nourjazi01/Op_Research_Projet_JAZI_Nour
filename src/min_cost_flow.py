from typing import Dict

from .graph import Graph
from .shortest_paths import (
    bellman_ford_shortest_path,
    dijkstra_with_potentials,
    reconstruct_path,
)


def bottleneck_on_path(graph: Graph, path: list[tuple[str, int]]) -> int:
    return min(graph.adj[u][edge_index].residual_capacity for u, edge_index in path)


def augment_path(graph: Graph, path: list[tuple[str, int]], amount: int) -> None:
    for u, edge_index in path:
        graph.augment_edge(u, edge_index, amount)


def min_cost_flow_bellman_ford(
    graph: Graph,
    source: str,
    sink: str,
    demand: int,
) -> tuple[int, int]:

    sent = 0

    while sent < demand:
        dist, parent = bellman_ford_shortest_path(graph, source)

        if dist[sink] == float("inf"):
            raise ValueError("Not enough capacity to send the required demand.")

        path = reconstruct_path(parent, source, sink)
        if path is None:
            raise ValueError("No augmenting path found.")

        amount = min(demand - sent, bottleneck_on_path(graph, path))
        augment_path(graph, path, amount)
        sent += amount

    return sent, graph.total_cost()


def initialize_potentials_with_bellman_ford(graph: Graph, source: str) -> Dict[str, float]:

    dist, _ = bellman_ford_shortest_path(graph, source)

    potentials = {}
    for node in graph.nodes():
        potentials[node] = 0 if dist[node] == float("inf") else dist[node]

    return potentials


def min_cost_flow_dijkstra(
    graph: Graph,
    source: str,
    sink: str,
    demand: int,
) -> tuple[int, int]:

    sent = 0
    potentials = initialize_potentials_with_bellman_ford(graph, source)

    while sent < demand:
        dist, parent = dijkstra_with_potentials(graph, source, potentials)

        if dist[sink] == float("inf"):
            raise ValueError("Not enough capacity to send the required demand.")

        path = reconstruct_path(parent, source, sink)
        if path is None:
            raise ValueError("No augmenting path found.")

        amount = min(demand - sent, bottleneck_on_path(graph, path))
        augment_path(graph, path, amount)
        sent += amount

        # Update potentials only for reachable nodes.
        for node in graph.nodes():
            if dist[node] < float("inf"):
                potentials[node] += dist[node]

    return sent, graph.total_cost()
