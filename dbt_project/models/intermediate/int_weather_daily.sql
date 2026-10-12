{{ config(materialized='view') }}

SELECT
    city,
    CAST(observed_at AS DATE)             AS observation_date,
    ROUND(AVG(temperature_c), 2)          AS avg_temperature_c,
    ROUND(MIN(temperature_c), 2)          AS min_temperature_c,
    ROUND(MAX(temperature_c), 2)          AS max_temperature_c,
    ROUND(AVG(humidity_pct), 2)           AS avg_humidity_pct,
    ROUND(SUM(precipitation_mm), 2)       AS total_precipitation_mm,
    ROUND(AVG(wind_speed_kmh), 2)         AS avg_wind_speed_kmh,
    COUNT(*)                              AS observation_count
FROM {{ ref('stg_weather') }}
GROUP BY city, observation_date