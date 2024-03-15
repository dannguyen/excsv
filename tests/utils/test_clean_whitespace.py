import pytest
import re
from excsv.utils.text import clean_whitespace


def test_clean_whitespace():
    val = """
hello
wor
 ld

"""
    assert clean_whitespace(val) == "hello wor  ld"
