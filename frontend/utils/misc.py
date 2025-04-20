import datetime


def snake_to_title(x: str) -> str:
    return x.replace("_", " ").title()


def snake_to_uppercase(x: str) -> str:
    return x.upper()


def parse_time(iso: str):
    dt = datetime.datetime.fromisoformat(iso.replace("Z", "+00:00"))
    return dt.strftime("%d/%m/%Y %H:%M")
