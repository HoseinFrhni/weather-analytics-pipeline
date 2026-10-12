import json
import logging
from datetime import datetime, timezone
from pathlib import Path

import pyarrow as pa
import pyarrow.parquet as pq

logger = logging.getLogger(__name__)

RAW_DIR = Path("data/raw/weather")
PROCESSED_DIR = Path("data/processed/weather")


def save_raw_json(payload: dict, city: str) -> Path:
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    target_dir = RAW_DIR / f"city={city}"
    target_dir.mkdir(parents=True, exist_ok=True)

    file_path = target_dir / f"{today}.json"

    with file_path.open("w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)

    logger.info("Saved raw JSON: %s", file_path)
    return file_path


def save_processed_parquet(payload: dict, city: str) -> Path:
    hourly = payload.get("hourly") or {}
    times = hourly.get("time") or []

    if not times:
        raise ValueError(f"No hourly data for city={city}")

    columns = {"time": times, "city": [city] * len(times)}

    for key, values in hourly.items():
        if key == "time":
            continue
        columns[key] = values

    table = pa.table(columns)

    target_dir = PROCESSED_DIR / f"city={city}"
    target_dir.mkdir(parents=True, exist_ok=True)

    file_path = target_dir / "weather.parquet"
    pq.write_table(table, file_path)

    logger.info("Saved processed Parquet: %s", file_path)
    return file_path