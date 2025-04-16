from enum import Enum
from .misc import camel_to_uppercase


class Units(Enum):
    LIGHT = "Lux"
    TEMPERATURE = "ºC"
    API_TEMPERATURE = "ºC"
    HUMIDITY = "%"
    PRECIPITATION = "mm"
    CLOUD_COVER = "%"

    @classmethod
    def get_unit(cls, key: str) -> str:
        try:
            return f"{cls[camel_to_uppercase(key)].value}"
        except KeyError:
            return ""
