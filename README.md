# NYC Taxi Algorithms Analysis

Group academic project applying **data analysis, sorting algorithms and graph theory** to NYC taxi trip data using Python.

> **Portfolio note:** This project was originally developed as a group assignment during the first year of my Bachelor's degree. I later reorganized and refactored the code for this portfolio repository, improving readability, correctness, modularity and reproducibility while preserving the original learning objectives.

## Project Overview

The original assignment used NYC taxi trip data to combine introductory data analysis with core algorithms and graph concepts. The project covers:

- loading and structuring taxi trip data;
- computing minimum, maximum and average values for key trip variables;
- calculating trip speed in **km/h**;
- counting departures from selected NYC taxi zones;
- implementing **Bubble Sort, Merge Sort and Quick Sort from scratch**;
- benchmarking execution time and verifying sorting correctness;
- building a weighted graph of pickup and drop-off locations, where edge weights represent trip frequency.

## Skills Demonstrated

- Python programming
- Data parsing and validation
- Descriptive statistics
- Algorithm implementation
- Time-complexity reasoning
- Performance benchmarking
- Graph modelling with NetworkX
- Data visualization with Matplotlib
- Code refactoring and modular design

## Repository Structure

```text
nyc-taxi-algorithms-analysis/
├── README.md
├── run_analysis.py
├── requirements.txt
├── data/
│   ├── README.md
│   ├── sample_taxi_trips.csv
│   └── sample_zone_lookup.csv
├── src/
│   ├── __init__.py
│   ├── data_processing.py
│   ├── sorting_algorithms.py
│   ├── graph_analysis.py
│   └── main.py
├── tests/
│   └── test_algorithms.py
└── outputs/
    ├── analysis_summary.json
    └── taxi_zone_network.png
```

## Sorting Algorithms

| Algorithm | Typical Time Complexity | Main Idea |
|---|---:|---|
| Bubble Sort | O(n²) | Repeatedly swaps adjacent out-of-order values |
| Merge Sort | O(n log n) | Divide-and-conquer with ordered merging |
| Quick Sort | O(n log n) average | Partitions values around a pivot |

All three algorithms are implemented directly in `src/sorting_algorithms.py`. The benchmark runs each algorithm on the **same input values** and checks the result against Python's built-in sorted output for correctness.

## Graph Analysis

Taxi zones are represented as nodes and observed trips as edges. Repeated trips between the same pair of zones increase the edge weight. The visualization focuses on the highest-frequency connections so that the network remains readable.

The assignment originally modelled the network as an **undirected weighted graph**, which is preserved here for consistency with the original project.

![Sample taxi-zone network](outputs/taxi_zone_network.png)

## Run the Project

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Run with the included demo data

```bash
python run_analysis.py
```

The script prints the analysis to the terminal and generates:

- `outputs/analysis_summary.json`
- `outputs/taxi_zone_network.png`

### 3. Run the tests

```bash
python -m unittest discover -s tests -v
```

### 4. Run with another NYC TLC-style dataset

```bash
python run_analysis.py \
  --trips path/to/trips.csv \
  --zones path/to/taxi_zone_lookup.csv \
  --benchmark-size 2000
```

`--benchmark-size` limits the number of observations used for the sorting benchmark because Bubble Sort becomes intentionally slow on large inputs.

## Demo Data

The small dataset included in `data/` is **synthetic** and exists only to make the repository immediately reproducible. It follows the field structure used by the original NYC taxi dataset. The original course dataset and group presentation are not redistributed in this portfolio version.

## What Was Improved in the Portfolio Version

Compared with the original first-year submission, this version:

- separates data processing, algorithms and graph logic into modules;
- fixes the Quick Sort integration and makes all three sorting implementations executable;
- avoids overwriting Python built-in names such as `list`, `tuple` and `dict`;
- validates input columns and reports clear errors;
- converts taxi distance from miles to kilometres before reporting km/h;
- uses the taxi-zone lookup dynamically instead of hard-coding labels inside the counting logic;
- benchmarks algorithms without mutating the original input;
- checks that each custom sorting algorithm produces the correct result;
- creates reproducible JSON and image outputs;
- includes documentation and a runnable demo dataset.

## Academic Context

**Group academic project — Algorithms course, first year of Bachelor's studies.**

This repository is intended to demonstrate both the concepts learned in the original assignment and the improvement in my programming practices since completing it.
