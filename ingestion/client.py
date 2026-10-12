import os
import logging
from typing import Any

import requests
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

DEFAULT_BASE_URL = os.getenv(
    "OPEN_METEO_BASE_URL",
    "https://archive-api.open-meteo.com/v1/archive",
)
DEFAULT_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", "30"))


class OpenMeteoClient:
    def __init__(
        self,
        base_url: str = DEFAULT_BASE_URL,
        timeout: int = DEFAULT_TIMEOUT,
    ) -> None:
        self.base_url = base_url
        self.timeout = timeout
        self.session = requests.Session()

    def get(self, params: dict[str, Any]) -> dict[str, Any]:
        logger.info("Requesting %s with params=%s", self.base_url, params)

        try:
            response = self.session.get(
                self.base_url,
                params=params,
                timeout=self.timeout,
            )
            response.raise_for_status()
        except requests.RequestException as exc:
            logger.exception("Request failed: %s", exc)
            raise

        data = response.json()

        if "error" in data and data["error"]:
            raise ValueError(f"API error: {data.get('reason')}")

        return data