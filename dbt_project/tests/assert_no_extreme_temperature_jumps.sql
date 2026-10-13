-- Check for unrealistically large temperature changes between consecutive days
-- for the same city (more than 20°C jump is suspicious).

WITH daily_with_lag AS (
    SELECT
        city,
        observation_date,
        avg_temperature_c,
        LAG(avg_temperature_c) OVER (
            PARTITION BY city
            ORDER BY observation_date
        ) AS prev_temp
    FROM {{ ref('int_weather_daily') }}
)

SELECT *
FROM daily_with_lag
WHERE prev_temp IS NOT NULL
  AND ABS(avg_temperature_c - prev_temp) > 20