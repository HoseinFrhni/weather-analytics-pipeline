import duckdb

DB_PATH = "data/warehouse.duckdb"


def main() -> None:
    con = duckdb.connect(DB_PATH)

    print("=== Sample rows ===")
    for row in con.execute("""
        SELECT * FROM raw_weather LIMIT 5
    """).fetchall():
        print(row)

    print("\n=== Row count per city ===")
    for row in con.execute("""
        SELECT city, COUNT(*) AS rows
        FROM raw_weather
        GROUP BY city
        ORDER BY city
    """).fetchall():
        print(row)

    print("\n=== Daily aggregates (first 10) ===")
    for row in con.execute("""
        SELECT
            city,
            DATE_TRUNC('day', CAST(time AS TIMESTAMP)) AS day,
            ROUND(AVG(temperature_2m), 2) AS avg_temp,
            ROUND(SUM(precipitation), 2) AS total_precipitation,
            ROUND(AVG(relative_humidity_2m), 2) AS avg_humidity
        FROM raw_weather
        GROUP BY city, day
        ORDER BY city, day
        LIMIT 10
    """).fetchall():
        print(row)

    con.close()


if __name__ == "__main__":
    main()