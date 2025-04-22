from enum import Enum
from .misc import snake_to_uppercase


class Units(Enum):
    """Collections of units of various attributes.."""

    LIGHT = "Lux"
    TEMPERATURE = "ºC"
    API_TEMPERATURE = "ºC"
    HUMIDITY = "%"
    PRECIPITATION = "mm"
    CLOUD_COVER = "%"

    @classmethod
    def get_unit(cls, key: str) -> str:
        """Get a unit of an attribute based on key."""
        try:
            return f"{cls[snake_to_uppercase(key)].value}"
        except KeyError:
            return ""
