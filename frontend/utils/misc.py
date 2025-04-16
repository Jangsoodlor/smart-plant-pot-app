import datetime
import re


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


def parse_time(iso: str):
    dt = datetime.datetime.fromisoformat(iso.replace("Z", "+00:00"))
    return dt.strftime("%d/%m/%Y %H:%M")
