import logging
from dataclasses import dataclass
from ingestion.client import OpenMeteoClient, logger


@dataclass(frozen=True)
class City:
    name: str
    latitude: float
    longitude: float


CITIES = [
    City(name="berlin", latitude=52.52, longitude=13.41),
    City(name="amsterdam", latitude=52.37, longitude=4.90),
    City(name="tehran", latitude=35.69, longitude=51.39),
]

HOURLY_VARIABLES = [
    "temperature_2m",
    "relative_humidity_2m",
    "precipitation",
    "wind_speed_10m",
]


def fetch_city_weather(
        client: OpenMeteoClient,
        city: City,
        start_date: str,
        end_date: str,
) -> dict:
    params = {
        "latitude": city.latitude,
        "longitude": city.longitude,
        "start_date": start_date,
        "end_date": end_date,
        "hourly": HOURLY_VARIABLES,
        "timezone": "UTC",
    }

    logger.info("Fetching weather for %s", city.name)
    payload = client.get(params)
    payload["_city"] = city.name
    return payload


def fetch_all_cities(
        start_date: str,
        end_date: str,
        client: OpenMeteoClient | None = None,
) -> list[dict]:
    client = client or OpenMeteoClient()
    results = []
    for city in CITIES:
        data = fetch_city_weather(client,city,start_date,end_date)
        results.append(data)

    return results


