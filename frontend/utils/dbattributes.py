from enum import Enum

from .api_fetcher import APIFetcher


class DBAttributes(Enum):
    SENSOR_ATTR = APIFetcher.get_attributes("sensor")
    WEATHER_ATTR = APIFetcher.get_attributes("weather")
