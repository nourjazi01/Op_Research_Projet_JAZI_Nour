from dataclasses import dataclass
from typing import Dict, List, Any


@dataclass
class Edge:
    to: str
    rev: int
    capacity: int
    cost: int = 0
    flow: int = 0
    original: bool = True

    @property
    def residual_capacity(self) -> int:
        return self.capacity - self.flow


class Graph:
    """
    Directed graph represented as a residual graph.

    For each original edge u -> v, we add:
    - a forward edge with capacity c and cost cost
    - a reverse edge with capacity 0 and cost -cost

    The reverse edge is essential because it allows the algorithms
    to cancel part of a previous augmentation.
    """

    def __init__(self) -> None:
        self.adj: Dict[str, List[Edge]] = {}

    def add_node(self, node: str) -> None:
        if node not in self.adj:
            self.adj[node] = []

    def add_edge(self, u: str, v: str, capacity: int, cost: int = 0) -> None:
        if capacity < 0:
            raise ValueError("Capacity must be non-negative.")

        self.add_node(u)
        self.add_node(v)

        forward = Edge(
            to=v,
            rev=len(self.adj[v]),
            capacity=capacity,
            cost=cost,
            flow=0,
            original=True,
        )

        backward = Edge(
            to=u,
            rev=len(self.adj[u]),
            capacity=0,
            cost=-cost,
            flow=0,
            original=False,
        )

        self.adj[u].append(forward)
        self.adj[v].append(backward)

    def nodes(self) -> List[str]:
        return list(self.adj.keys())

    def get_reverse_edge(self, u: str, edge: Edge) -> Edge:
        return self.adj[edge.to][edge.rev]

    def augment_edge(self, u: str, edge_index: int, amount: int) -> None:
        edge = self.adj[u][edge_index]
        reverse = self.get_reverse_edge(u, edge)

        if amount < 0:
            raise ValueError("Augmentation amount must be non-negative.")
        if edge.residual_capacity < amount:
            raise ValueError("Not enough residual capacity.")

        edge.flow += amount
        reverse.flow -= amount

    def original_edges(self) -> List[tuple[str, Edge]]:
        result = []
        for u, edges in self.adj.items():
            for edge in edges:
                if edge.original:
                    result.append((u, edge))
        return result

    def total_cost(self) -> int:
        return sum(edge.flow * edge.cost for _, edge in self.original_edges())

    @staticmethod
    def from_json_data(data: Dict[str, Any]) -> "Graph":
        g = Graph()
        for e in data["edges"]:
            g.add_edge(
                str(e["from"]),
                str(e["to"]),
                int(e["capacity"]),
                int(e.get("cost", 0)),
            )
        return g
