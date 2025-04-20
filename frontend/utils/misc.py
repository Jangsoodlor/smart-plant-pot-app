import datetime


def snake_to_title(x: str) -> str:
    return x.replace("_", " ").title()


def snake_to_uppercase(x: str) -> str:
    return x.upper()


def parse_time(iso: str) -> str:
    """Parsed ISO time string to a more human-friendly format.

    :param iso: string of time in ISO format
    :return: string of time in DD/MM/YY HH:MM format.
    """
    dt = datetime.datetime.fromisoformat(iso.replace("Z", "+00:00"))
    return dt.strftime("%d/%m/%Y %H:%M")
