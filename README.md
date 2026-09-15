# Data

The repository includes a **small synthetic demo dataset** so the project can be run immediately without redistributing the original course dataset.

## Expected trip columns

The analysis accepts a comma-delimited `.csv` or `.txt` file containing these NYC TLC-style columns:

- `tpep_pickup_datetime`
- `tpep_dropoff_datetime`
- `passenger_count`
- `trip_distance`
- `PULocationID`
- `DOLocationID`
- `fare_amount`
- `tip_amount`
- `total_amount`

Additional columns are allowed and ignored by the analysis.

## Zone lookup

The zone lookup must contain at least:

- `LocationID`
- `Zone`

To run the project with a larger dataset, pass custom file paths:

```bash
python run_analysis.py --trips path/to/trips.csv --zones path/to/taxi_zone_lookup.csv
```
