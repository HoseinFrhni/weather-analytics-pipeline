-- This test checks that each city has exactly 24 observations per day.
-- If any row is returned, it means there is a day with a wrong count.

SELECT
    city,
    observation_date,
    observation_count
FROM {{ ref('int_weather_daily') }}
WHERE observation_count != 24