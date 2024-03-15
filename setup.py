from setuptools import setup
import os

VERSION = "0.1.1"


def get_long_description():
    with open(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "README.md"),
        encoding="utf8",
    ) as fp:
        return fp.read()


setup(
    name="excsv",
    description="little utility for skimming CSV files from the command line",
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
    packages=["excsv"],
    entry_points="""
        [console_scripts]
        excsv=excsv.cli:cli
    """,
    install_requires=["click"],
    #    extras_require={"test": ["pytest", "pytest-icdiff", "cogapp", "PyYAML", "ruff"]},
    extras_require={"test": ["pytest", "pytest-mock"]},
    python_requires=">=3.8",
)
