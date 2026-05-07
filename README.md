# Operations Research Project

## Author
Nour JAZI

---

# Project Overview

This project implements several classical flow algorithms studied in Operations Research:

- Ford-Fulkerson / Edmonds-Karp for maximum flow
- Minimum cut
- Minimum cost flow using:
  - Bellman-Ford
  - Dijkstra with reduced costs and potentials
- Negative cycle detection
- Most vital arc detection
- Graph visualization with Graphviz

No external flow library such as NetworkX is used.

---

# Project Structure

```text
Op_Research_Projet_JAZI_Nour/
│
├── README.md
├── OR_project_report_JAZI_Nour.tex
├── examples/
├── outputs/
└── src/
```

---

# How to Run

## Maximum Flow

```bash
python -m src.main maxflow examples/maxflow_example.json
```

## Minimum Cost Flow (Bellman-Ford)

```bash
python -m src.main mincost-bf examples/mincost_example.json
```

## Minimum Cost Flow (Dijkstra + Potentials)

```bash
python -m src.main mincost-dijkstra examples/mincost_example.json
```

## Negative Cycle Detection

```bash
python -m src.main negcycle examples/mincost_example.json
```

## Most Vital Arc

```bash
python -m src.main vital examples/teacher_maxflow.json
```

---

# Teacher Test Examples

## Maximum Flow

```bash
python -m src.main maxflow examples/teacher_maxflow.json
```

## Minimum Cost Flow

```bash
python -m src.main mincost-bf examples/teacher_mincost.json
```

```bash
python -m src.main mincost-dijkstra examples/teacher_mincost.json
```

---

# Graphviz

The program generates `.dot` files inside the `outputs/` folder.

To generate PNG images:

```bash
dot -Tpng outputs/teacher_maxflow_maxflow_result.dot -o outputs/teacher_maxflow.png
```

```bash
dot -Tpng outputs/teacher_mincost_mincost_dijkstra_result.dot -o outputs/teacher_mincost_dijkstra.png
```

---

# Main Concepts

The project is based on the residual graph structure:

- forward residual edges
- backward residual edges
- residual capacities
- residual costs

This structure is used by all implemented algorithms.

---

# Results

The implementation successfully computes:

- maximum flow values,
- minimum cuts,
- minimum cost flows,
- negative cycle detection,
- most vital arcs.

Graphviz visualizations are included in the report.