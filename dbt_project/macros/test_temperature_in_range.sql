{% test temperature_in_range(model, column_name, min_value=-50, max_value=60) %}

SELECT *
FROM {{ model }}
WHERE
    {{ column_name }} < {{ min_value }}
    OR {{ column_name }} > {{ max_value }}

{% endtest %}