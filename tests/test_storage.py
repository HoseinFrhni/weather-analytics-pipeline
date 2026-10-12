from ingestion.storage import save_processed_parquet


def test_save_processed_parquet(tmp_path, monkeypatch):
    import ingestion.storage as storage

    monkeypatch.setattr(storage, "PROCESSED_DIR", tmp_path)

    payload = {
        "hourly": {
            "time": ["2024-01-01T00:00", "2024-01-01T01:00"],
            "temperature_2m": [1.0, 2.0],
            "relative_humidity_2m": [80, 82],
            "precipitation": [0.0, 0.1],
            "wind_speed_10m": [5.0, 6.0],
        }
    }

    path = storage.save_processed_parquet(payload, "berlin")

    assert path.exists()
    assert path.suffix == ".parquet"