import re

def camel_to_title(x):
    return "".join([a.title() + " " for a in (re.split(r"(?=[A-Z][^A-Z])", x))]).strip()

