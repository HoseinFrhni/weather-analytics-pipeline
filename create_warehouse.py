from pathlib import Path
import duckdb

DB_PATH = Path("data/warehouse.duckdb")
DB_PATH.parent.mkdir(parents=True, exist_ok=True)

con = duckdb.connect(str(DB_PATH))

con.execute("""
    CREATE OR REPLACE VIEW raw_weather AS
    SELECT *
    FROM 'data/processed/weather/city=*/*.parquet'
""")

result = con.execute("SELECT COUNT(*) FROM raw_weather").fetchone()
print(f"Total rows in raw_weather view: {result[0]}")

result = con.execute("""
    SELECT city, COUNT(*) 
    FROM raw_weather 
    GROUP BY city 
    ORDER BY city
""").fetchall()

for row in result:
    print(row)

con.close()