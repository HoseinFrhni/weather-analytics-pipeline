{{ config(materialized='view') }}

SELECT
    CAST(time AS TIMESTAMP) AS observed_at,
    city,
    temperature_2m        AS temperature_c,
    relative_humidity_2m  AS humidity_pct,
    precipitation         AS precipitation_mm,
    wind_speed_10m        AS wind_speed_kmh
FROM read_parquet(
    'data/processed/weather/city=*/*.parquet',
    hive_partitioning = true
)