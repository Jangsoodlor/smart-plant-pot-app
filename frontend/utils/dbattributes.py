from enum import Enum

from .api_fetcher import APIFetcher


class DBAttributes(Enum):
    """Attributes of each table. Extracted as ENUM to avoid multiple calls to API."""

    SENSOR_ATTR = APIFetcher.get_attributes("sensor")
    WEATHER_ATTR = APIFetcher.get_attributes("weather")
