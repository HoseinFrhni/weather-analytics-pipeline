import logging
from ingestion.extract import fetch_all_cities
from ingestion.storage import save_raw_json, save_processed_parquet

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)

START_DATE = "2024-01-01"
END_DATE = "2024-12-31"


def main() -> None:
    results = fetch_all_cities(START_DATE, END_DATE)

    for payload in results:
        city = payload["_city"]
        save_raw_json(payload, city)
        save_processed_parquet(payload, city)


if __name__ == "__main__":
    main()