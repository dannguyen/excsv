import re


def clean_whitespace(txt: str):
    """
    Normalizes all whitespace as space characters, e.g. '\\r' and '\\n' are converted to ' '
    Converts newline characters into space characters
    Strips whitespace from left and right
    """
    return re.sub(r"[\s\r\n]", " ", txt).strip()
