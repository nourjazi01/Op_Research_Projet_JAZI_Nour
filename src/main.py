import json
import sys
from pathlib import Path

from .graph import Graph
from .max_flow import max_flow, min_cut
from .min_cost_flow import min_cost_flow_bellman_ford, min_cost_flow_dijkstra
from .negative_cycle import find_negative_cycle
from .graphviz_export import export_to_dot
from .vital_arc import most_vital_arc


def load_graph(path: str) -> tuple[Graph, dict]:
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    return Graph.from_json_data(data), data


def output_dot_path(input_file: str, suffix: str) -> str:
    """
    Creates a clear output filename based on the input example name.

    Example:
    examples/teacher_maxflow.json + maxflow
    => outputs/teacher_maxflow_maxflow_result.dot
    """
    Path("outputs").mkdir(exist_ok=True)
    name = Path(input_file).stem
    return f"outputs/{name}_{suffix}_result.dot"


def print_flows(graph: Graph) -> None:
    print("\nFlow on original edges:")
    for u, edge in graph.original_edges():
        cost_part = f", cost={edge.cost}" if edge.cost != 0 else ""
        print(f"  {u} -> {edge.to}: {edge.flow}/{edge.capacity}{cost_part}")


def run_maxflow(input_file: str) -> None:
    graph, data = load_graph(input_file)
    source = str(data["source"])
    sink = str(data["sink"])

    value = max_flow(graph, source, sink)
    s_set, t_set, cut_edges = min_cut(graph, source)

    print("=== Maximum Flow ===")
    print(f"Input file: {input_file}")
    print(f"Maximum flow value: {value}")
    print_flows(graph)

    print("\nMinimum cut:")
    print(f"  S = {sorted(s_set)}")
    print(f"  T = {sorted(t_set)}")
    print("  Cut edges:")
    for u, v, capacity in cut_edges:
        print(f"    {u} -> {v}, capacity={capacity}")

    dot_path = output_dot_path(input_file, "maxflow")
    export_to_dot(graph, dot_path, "Maximum Flow Result")
    print(f"\nDOT file created: {dot_path}")


def run_mincost_bf(input_file: str) -> None:
    graph, data = load_graph(input_file)
    source = str(data["source"])
    sink = str(data["sink"])
    demand = int(data["demand"])

    sent, cost = min_cost_flow_bellman_ford(graph, source, sink, demand)
    cycle = find_negative_cycle(graph)

    print("=== Minimum Cost Flow: Bellman-Ford ===")
    print(f"Input file: {input_file}")
    print(f"Sent flow: {sent}")
    print(f"Total cost: {cost}")
    print_flows(graph)

    print("\nNegative cycle in residual graph:")
    print("  None" if cycle is None else f"  {cycle}")

    dot_path = output_dot_path(input_file, "mincost_bf")
    export_to_dot(graph, dot_path, "Minimum Cost Flow BF Result")
    print(f"\nDOT file created: {dot_path}")


def run_mincost_dijkstra(input_file: str) -> None:
    graph, data = load_graph(input_file)
    source = str(data["source"])
    sink = str(data["sink"])
    demand = int(data["demand"])

    sent, cost = min_cost_flow_dijkstra(graph, source, sink, demand)
    cycle = find_negative_cycle(graph)

    print("=== Minimum Cost Flow: Dijkstra + Potentials ===")
    print(f"Input file: {input_file}")
    print(f"Sent flow: {sent}")
    print(f"Total cost: {cost}")
    print_flows(graph)

    print("\nNegative cycle in residual graph:")
    print("  None" if cycle is None else f"  {cycle}")

    dot_path = output_dot_path(input_file, "mincost_dijkstra")
    export_to_dot(graph, dot_path, "Minimum Cost Flow Dijkstra Result")
    print(f"\nDOT file created: {dot_path}")


def run_negative_cycle(input_file: str) -> None:
    graph, _ = load_graph(input_file)
    cycle = find_negative_cycle(graph)

    print("=== Negative Cycle Detection ===")
    print(f"Input file: {input_file}")
    if cycle is None:
        print("No negative cycle found.")
    else:
        print(f"Negative cycle found: {cycle}")


def run_vital_arc(input_file):
    graph, data = load_graph(input_file)

    source = str(data["source"])
    sink = str(data["sink"])

    edge, reduction = most_vital_arc(graph, source, sink)

    print("=== Most Vital Arc ===")
    print(f"Arc: {edge}")
    print(f"Flow reduction: {reduction}")


def main() -> None:
    if len(sys.argv) != 3:
        print("Usage:")
        print("  python -m src.main maxflow examples/maxflow_example.json")
        print("  python -m src.main mincost-bf examples/mincost_example.json")
        print("  python -m src.main mincost-dijkstra examples/mincost_example.json")
        print("  python -m src.main negcycle examples/mincost_example.json")
        sys.exit(1)

    command = sys.argv[1]
    input_file = sys.argv[2]

    if command == "maxflow":
        run_maxflow(input_file)
    elif command == "mincost-bf":
        run_mincost_bf(input_file)
    elif command == "mincost-dijkstra":
        run_mincost_dijkstra(input_file)
    elif command == "negcycle":
        run_negative_cycle(input_file)
    elif command == "vital":
        run_vital_arc(input_file)
    else:
        raise ValueError(f"Unknown command: {command}")


if __name__ == "__main__":
    main()
