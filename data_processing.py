"""Data loading and descriptive analysis for NYC taxi trip records."""

from __future__ import annotations

import csv
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from statistics import fmean
from typing import Iterable, Mapping, Sequence

MILES_TO_KM = 1.609344


@dataclass(frozen=True)
class TripRecord:
    pickup_datetime: datetime
    dropoff_datetime: datetime
    passenger_count: int
    trip_distance_miles: float
    pickup_zone_id: int
    dropoff_zone_id: int
    fare_amount: float
    tip_amount: float
    total_amount: float


REQUIRED_TRIP_COLUMNS = {
    "tpep_pickup_datetime",
    "tpep_dropoff_datetime",
    "passenger_count",
    "trip_distance",
    "PULocationID",
    "DOLocationID",
    "fare_amount",
    "tip_amount",
    "total_amount",
}


def _parse_datetime(value: str) -> datetime:
    """Parse common NYC TLC datetime formats."""
    value = value.strip()
    for fmt in (
        "%Y-%m-%dT%H:%M:%S.%f",
        "%Y-%m-%dT%H:%M:%S",
        "%Y-%m-%d %H:%M:%S",
    ):
        try:
            return datetime.strptime(value, fmt)
        except ValueError:
            pass
    raise ValueError(f"Unsupported datetime format: {value!r}")


def load_trip_records(file_path: str | Path) -> list[TripRecord]:
    """Load comma-delimited taxi trip data into typed records.

    The source may have a .csv or .txt extension as long as it contains a
    header row with the expected NYC TLC column names.
    """
    path = Path(file_path)
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None:
            raise ValueError("Trip file does not contain a header row.")

        missing = REQUIRED_TRIP_COLUMNS.difference(reader.fieldnames)
        if missing:
            raise ValueError(
                "Trip file is missing required columns: "
                + ", ".join(sorted(missing))
            )

        records: list[TripRecord] = []
        for row_number, row in enumerate(reader, start=2):
            try:
                records.append(
                    TripRecord(
                        pickup_datetime=_parse_datetime(row["tpep_pickup_datetime"]),
                        dropoff_datetime=_parse_datetime(row["tpep_dropoff_datetime"]),
                        passenger_count=int(float(row["passenger_count"])),
                        trip_distance_miles=float(row["trip_distance"]),
                        pickup_zone_id=int(float(row["PULocationID"])),
                        dropoff_zone_id=int(float(row["DOLocationID"])),
                        fare_amount=float(row["fare_amount"]),
                        tip_amount=float(row["tip_amount"]),
                        total_amount=float(row["total_amount"]),
                    )
                )
            except (TypeError, ValueError, KeyError) as exc:
                raise ValueError(f"Invalid trip data on row {row_number}: {exc}") from exc

    if not records:
        raise ValueError("Trip file contains no data rows.")
    return records


def load_zone_lookup(file_path: str | Path) -> dict[int, str]:
    """Load a NYC taxi-zone lookup file keyed by LocationID."""
    path = Path(file_path)
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None:
            raise ValueError("Zone lookup does not contain a header row.")

        required = {"LocationID", "Zone"}
        missing = required.difference(reader.fieldnames)
        if missing:
            raise ValueError(
                "Zone lookup is missing required columns: "
                + ", ".join(sorted(missing))
            )

        lookup: dict[int, str] = {}
        for row in reader:
            lookup[int(row["LocationID"])] = row["Zone"].strip()
    return lookup


def summarize(values: Sequence[float | int]) -> dict[str, float]:
    """Return minimum, maximum and arithmetic mean for numeric values."""
    if not values:
        raise ValueError("Cannot summarize an empty sequence.")
    return {
        "min": float(min(values)),
        "max": float(max(values)),
        "average": float(fmean(values)),
    }


def descriptive_statistics(records: Sequence[TripRecord]) -> dict[str, dict[str, float]]:
    """Compute the statistics requested in the original assignment."""
    return {
        "passenger_count": summarize([r.passenger_count for r in records]),
        "fare_amount_usd": summarize([r.fare_amount for r in records]),
        "tip_amount_usd": summarize([r.tip_amount for r in records]),
        "total_amount_usd": summarize([r.total_amount for r in records]),
    }


def calculate_speeds_kmh(records: Iterable[TripRecord]) -> list[float]:
    """Calculate valid trip speeds in km/h.

    NYC TLC trip distance is expressed in miles, so miles/hour is converted to
    km/h. Trips with non-positive duration are ignored instead of creating a
    misleading zero or infinite speed.
    """
    speeds: list[float] = []
    for trip in records:
        duration_hours = (
            trip.dropoff_datetime - trip.pickup_datetime
        ).total_seconds() / 3600.0
        if duration_hours <= 0:
            continue
        mph = trip.trip_distance_miles / duration_hours
        speeds.append(mph * MILES_TO_KM)
    return speeds


def count_pickups_by_zone(
    records: Iterable[TripRecord],
    zone_lookup: Mapping[int, str],
    selected_zone_ids: Sequence[int],
) -> dict[str, int]:
    """Count trips originating from selected pickup zones."""
    counts = {
        zone_lookup.get(zone_id, f"Zone {zone_id}"): 0
        for zone_id in selected_zone_ids
    }
    selected = set(selected_zone_ids)

    for trip in records:
        if trip.pickup_zone_id in selected:
            name = zone_lookup.get(trip.pickup_zone_id, f"Zone {trip.pickup_zone_id}")
            counts[name] += 1
    return counts
