"""Weighted taxi-zone graph construction and visualization."""

from __future__ import annotations

from pathlib import Path
from textwrap import fill
from typing import Mapping, Sequence

import matplotlib.pyplot as plt
import networkx as nx

from .data_processing import TripRecord


def build_trip_graph(records: Sequence[TripRecord]) -> nx.Graph:
    """Build an undirected weighted graph of pickup/drop-off zone pairs.

    Nodes represent taxi zones. Edge weights count how many trips were observed
    between the two zones, matching the structure of the original assignment.
    """
    graph = nx.Graph()
    for trip in records:
        u, v = trip.pickup_zone_id, trip.dropoff_zone_id
        if graph.has_edge(u, v):
            graph[u][v]["weight"] += 1
        else:
            graph.add_edge(u, v, weight=1)
    return graph


def graph_summary(graph: nx.Graph, top_n: int = 5) -> dict[str, object]:
    """Return compact graph statistics and the most frequent connections."""
    ranked_edges = sorted(
        graph.edges(data=True),
        key=lambda edge: edge[2].get("weight", 1),
        reverse=True,
    )
    return {
        "nodes": graph.number_of_nodes(),
        "edges": graph.number_of_edges(),
        "total_trips_represented": int(
            sum(data.get("weight", 1) for _, _, data in graph.edges(data=True))
        ),
        "top_connections": [
            {"from": int(u), "to": int(v), "trips": int(data.get("weight", 1))}
            for u, v, data in ranked_edges[:top_n]
        ],
    }


def draw_trip_graph(
    graph: nx.Graph,
    output_path: str | Path,
    zone_lookup: Mapping[int, str] | None = None,
    max_edges: int = 40,
) -> None:
    """Save a readable visualization using the highest-weight connections."""
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)

    ranked = sorted(
        graph.edges(data=True),
        key=lambda edge: edge[2].get("weight", 1),
        reverse=True,
    )[:max_edges]

    display_graph = nx.Graph()
    for u, v, data in ranked:
        display_graph.add_edge(u, v, **data)

    if display_graph.number_of_nodes() == 0:
        return

    weights = [data.get("weight", 1) for _, _, data in display_graph.edges(data=True)]
    max_weight = max(weights)
    widths = [0.8 + 3.2 * (w / max_weight) for w in weights]

    labels = {
        node: fill(
            zone_lookup.get(node, str(node)) if zone_lookup else str(node),
            width=16,
        )
        for node in display_graph.nodes()
    }
    positions = nx.kamada_kawai_layout(display_graph, weight="weight")

    plt.figure(figsize=(13, 9))
    nx.draw_networkx_nodes(display_graph, positions, node_size=520, alpha=0.9)
    nx.draw_networkx_edges(display_graph, positions, width=widths, alpha=0.55)
    nx.draw_networkx_labels(display_graph, positions, labels=labels, font_size=7)
    plt.title("NYC Taxi Zone Network — Highest-Frequency Connections")
    plt.axis("off")
    plt.tight_layout()
    plt.savefig(output, dpi=180, bbox_inches="tight")
    plt.close()
