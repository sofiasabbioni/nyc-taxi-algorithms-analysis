"""Sorting algorithms implemented from scratch for the algorithms assignment."""

from __future__ import annotations

from time import perf_counter
from typing import Callable, Iterable, TypeVar

T = TypeVar("T")


def bubble_sort(values: Iterable[T]) -> list[T]:
    """Return a new list sorted with Bubble Sort: O(n^2) time, O(n) copy space."""
    result = list(values)
    n = len(result)
    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            if result[j] > result[j + 1]:
                result[j], result[j + 1] = result[j + 1], result[j]
                swapped = True
        if not swapped:
            break
    return result


def merge_sort(values: Iterable[T]) -> list[T]:
    """Return a new list sorted with Merge Sort: O(n log n) time."""
    items = list(values)
    if len(items) <= 1:
        return items

    middle = len(items) // 2
    left = merge_sort(items[:middle])
    right = merge_sort(items[middle:])

    merged: list[T] = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1

    merged.extend(left[i:])
    merged.extend(right[j:])
    return merged


def quick_sort(values: Iterable[T]) -> list[T]:
    """Return a new list sorted with a three-way Quick Sort partition."""
    items = list(values)
    if len(items) <= 1:
        return items

    pivot = items[len(items) // 2]
    lower = [x for x in items if x < pivot]
    equal = [x for x in items if x == pivot]
    higher = [x for x in items if x > pivot]
    return quick_sort(lower) + equal + quick_sort(higher)


ALGORITHMS: dict[str, Callable[[Iterable[float]], list[float]]] = {
    "bubble": bubble_sort,
    "merge": merge_sort,
    "quick": quick_sort,
}


def benchmark_sorting(values: Iterable[float]) -> dict[str, dict[str, float | bool]]:
    """Benchmark each custom algorithm on the same input and verify correctness."""
    original = list(values)
    expected = sorted(original)
    results: dict[str, dict[str, float | bool]] = {}

    for name, algorithm in ALGORITHMS.items():
        start = perf_counter()
        output = algorithm(original)
        elapsed = perf_counter() - start
        results[name] = {
            "seconds": elapsed,
            "correct": output == expected,
        }
    return results
