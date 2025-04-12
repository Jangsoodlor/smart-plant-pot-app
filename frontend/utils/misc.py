import re
from enum import Enum


def camel_to_title(x: str) -> str:
    def add_spacing(w: str) -> str:
        if len(w) == 0:
            return w
        if w[-1] == " ":
            return w
        return w + " "

    return "".join(
        [add_spacing(a.title()) for a in (re.split(r"(?=[A-Z][^A-Z])", x))]
    ).strip()


def camel_to_uppercase(x: str) -> str:
    def add_underscore(w: str) -> str:
        if len(w) == 0:
            return w
        if w[-1] == "_" or w[-1] == " ":
            return w
        return w + "_"

    return "".join(
        [add_underscore(a.upper().strip()) for a in (re.split(r"(?=[A-Z][^A-Z])", x))]
    ).strip("_")


class Units(Enum):
    LIGHT = "Lux"
    TEMPERATURE = "ºC"
    API_TEMPERATURE = "ºC"
    HUMIDITY = "%"
    PRECIPITATION = "mm"
    CLOUD_COVER = "%"

    @classmethod
    def append_unit(cls, key: str, val: float | int) -> str:
        try:
            return f"{val:.2f} {cls[camel_to_uppercase(key)].value}"
        except KeyError:
            return f"{val:.2f}"
