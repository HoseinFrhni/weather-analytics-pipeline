{{ config(materialized='table') }}

SELECT
    city,
    observation_date,
    EXTRACT(YEAR  FROM observation_date) AS year,
    EXTRACT(MONTH FROM observation_date) AS month,
    avg_temperature_c,
    min_temperature_c,
    max_temperature_c,
    avg_humidity_pct,
    total_precipitation_mm,
    avg_wind_speed_kmh,
    observation_count
FROM {{ ref('int_weather_daily') }}