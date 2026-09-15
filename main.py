"""Command-line entry point for the NYC Taxi Algorithms Analysis project."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from .data_processing import (
    calculate_speeds_kmh,
    count_pickups_by_zone,
    descriptive_statistics,
    load_trip_records,
    load_zone_lookup,
    summarize,
)
from .graph_analysis import build_trip_graph, draw_trip_graph, graph_summary
from .sorting_algorithms import benchmark_sorting

TARGET_ZONE_IDS = [1, 132, 74, 43]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Analyze NYC taxi trips using custom sorting algorithms and graph analysis."
    )
    parser.add_argument(
        "--trips",
        default="data/sample_taxi_trips.csv",
        help="Path to the taxi trip CSV/TXT file.",
    )
    parser.add_argument(
        "--zones",
        default="data/sample_zone_lookup.csv",
        help="Path to the taxi-zone lookup CSV file.",
    )
    parser.add_argument(
        "--benchmark-size",
        type=int,
        default=2000,
        help="Maximum number of observations per sorting benchmark.",
    )
    parser.add_argument(
        "--output-dir",
        default="outputs",
        help="Directory for generated JSON and graph outputs.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    records = load_trip_records(args.trips)
    zones = load_zone_lookup(args.zones)

    speeds = calculate_speeds_kmh(records)
    if not speeds:
        raise ValueError("No valid trip speeds could be calculated.")

    stats = descriptive_statistics(records)
    stats["speed_kmh"] = summarize(speeds)

    pickup_counts = count_pickups_by_zone(records, zones, TARGET_ZONE_IDS)

    benchmark_size = min(max(args.benchmark_size, 1), len(records))
    metric_values = {
        "passenger_count": [float(r.passenger_count) for r in records[:benchmark_size]],
        "fare_amount": [r.fare_amount for r in records[:benchmark_size]],
        "tip_amount": [r.tip_amount for r in records[:benchmark_size]],
        "total_amount": [r.total_amount for r in records[:benchmark_size]],
        "speed_kmh": speeds[:benchmark_size],
    }
    sorting_benchmarks = {
        metric: benchmark_sorting(values)
        for metric, values in metric_values.items()
        if values
    }

    graph = build_trip_graph(records)
    graph_stats = graph_summary(graph)
    graph_path = output_dir / "taxi_zone_network.png"
    draw_trip_graph(graph, graph_path, zone_lookup=zones)

    result = {
        "records_loaded": len(records),
        "descriptive_statistics": stats,
        "selected_pickup_zone_counts": pickup_counts,
        "sorting_benchmarks": sorting_benchmarks,
        "graph": graph_stats,
    }

    summary_path = output_dir / "analysis_summary.json"
    summary_path.write_text(json.dumps(result, indent=2), encoding="utf-8")

    print(json.dumps(result, indent=2))
    print(f"\nSaved summary to: {summary_path}")
    print(f"Saved network visualization to: {graph_path}")


if __name__ == "__main__":
    main()
