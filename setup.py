from setuptools import setup, find_packages
import os

VERSION = "0.1.4.1"


def get_long_description():
    with open(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "README.md"),
        encoding="utf8",
    ) as fp:
        return fp.read()


setup(
    name="excsv",
    description="A command-line utility for converting CSV files into Excel sheets.",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    author="Dan Nguyen",
    url="https://github.com/dannguyen/excsv",
    project_urls={
        "Issues": "https://github.dannguyen/dannguyen/excsv/issues",
        "CI": "https://github.com/dannguyen/excsv/actions",
        "Changelog": "https://github.com/dannguyen/excsv/releases",
    },
    license="Apache License, Version 2.0",
    version=VERSION,
    packages=find_packages(exclude=["tests", "tests.*"]),
    entry_points="""
        [console_scripts]
        excsv=excsv.cli:cli
    """,
    install_requires=[
        "click>=8.1",
        "hyperloglog",
        "rich_click",
        "openpyxl",
        "click-default-group>=1.2.3",
        "setuptools",
        "pip",
        "pyreadline3; sys_platform == 'win32'",
    ],
    extras_require={
        "test": [
            "pytest",
            "pytest-mock",
            "black>=24.2.0",
            "types-click",
        ]
    },
    python_requires=">=3.8",
)
