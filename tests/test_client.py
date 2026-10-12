from unittest.mock import MagicMock, patch

import pytest

from ingestion.client import OpenMeteoClient


def test_client_returns_json_on_success():
    client = OpenMeteoClient()

    fake_response = MagicMock()
    fake_response.json.return_value = {"hourly": {"time": ["2024-01-01T00:00"]}}
    fake_response.raise_for_status.return_value = None

    with patch.object(client.session, "get", return_value=fake_response):
        data = client.get({"latitude": 52.52, "longitude": 13.41})

    assert "hourly" in data


def test_client_raises_on_api_error():
    client = OpenMeteoClient()

    fake_response = MagicMock()
    fake_response.json.return_value = {"error": True, "reason": "bad request"}
    fake_response.raise_for_status.return_value = None

    with patch.object(client.session, "get", return_value=fake_response):
        with pytest.raises(ValueError):
            client.get({"latitude": 0, "longitude": 0})