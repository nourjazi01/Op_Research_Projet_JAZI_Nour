from .graph import Graph


def export_to_dot(graph: Graph, path: str, title: str = "Flow Graph") -> None:
    """
    Exports original edges to Graphviz DOT format.

    Edge label:
    flow/capacity | cost
    """
    with open(path, "w", encoding="utf-8") as f:
        f.write("digraph G {\n")
        f.write('  rankdir=LR;\n')
        f.write(f'  label="{title}";\n')
        f.write('  labelloc="t";\n')
        f.write('  node [shape=circle];\n')

        for u, edge in graph.original_edges():
            label = f"{edge.flow}/{edge.capacity}"
            if edge.cost != 0:
                label += f" | c={edge.cost}"

            f.write(f'  "{u}" -> "{edge.to}" [label="{label}"];\n')

        f.write("}\n")
