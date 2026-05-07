from collections import deque
from typing import Dict, Optional, Tuple, Set, List

from .graph import Graph


Parent = Dict[str, Tuple[str, int]]


def bfs_augmenting_path(graph: Graph, source: str, sink: str) -> Optional[Parent]:
    visited = {source}
    parent: Parent = {}
    queue = deque([source])

    while queue:
        u = queue.popleft()

        for i, edge in enumerate(graph.adj[u]):
            if edge.residual_capacity > 0 and edge.to not in visited:
                visited.add(edge.to)
                parent[edge.to] = (u, i)

                if edge.to == sink:
                    return parent

                queue.append(edge.to)

    return None


def path_bottleneck(graph: Graph, parent: Parent, source: str, sink: str) -> int:
    bottleneck = float("inf")
    v = sink

    while v != source:
        u, edge_index = parent[v]
        edge = graph.adj[u][edge_index]
        bottleneck = min(bottleneck, edge.residual_capacity)
        v = u

    return int(bottleneck)


def apply_augmentation(graph: Graph, parent: Parent, source: str, sink: str, amount: int) -> None:
    v = sink

    while v != source:
        u, edge_index = parent[v]
        graph.augment_edge(u, edge_index, amount)
        v = u


def max_flow(graph: Graph, source: str, sink: str) -> int:

    total = 0

    while True:
        parent = bfs_augmenting_path(graph, source, sink)

        if parent is None:
            break

        amount = path_bottleneck(graph, parent, source, sink)
        apply_augmentation(graph, parent, source, sink, amount)
        total += amount

    return total


def reachable_in_residual_graph(graph: Graph, source: str) -> Set[str]:
    visited = {source}
    queue = deque([source])

    while queue:
        u = queue.popleft()
        for edge in graph.adj[u]:
            if edge.residual_capacity > 0 and edge.to not in visited:
                visited.add(edge.to)
                queue.append(edge.to)

    return visited


def min_cut(graph: Graph, source: str) -> tuple[Set[str], Set[str], List[tuple[str, str, int]]]:
    
    s_set = reachable_in_residual_graph(graph, source)
    t_set = set(graph.nodes()) - s_set

    cut_edges = []
    for u, edge in graph.original_edges():
        if u in s_set and edge.to in t_set:
            cut_edges.append((u, edge.to, edge.capacity))

    return s_set, t_set, cut_edges
