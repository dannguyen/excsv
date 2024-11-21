from setuptools import setup
import os

VERSION = "0.1"


def get_long_description():
    with open(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "README.md"),
        encoding="utf8",
    ) as fp:
        return fp.read()


setup(
    name="csvskim",
    description="little utility for skimming CSV files from the command line",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    author="Dan Nguyen",
    url="https://github.com/dannguyen/csvskim",
    project_urls={
        "Issues": "https://github.dannguyen/dannguyen/csvskim/issues",
        "CI": "https://github.com/simonw/csvskim/actions",
        "Changelog": "https://github.com/dannguyen/csvskim/releases",
    },
    license="Apache License, Version 2.0",
    version=VERSION,
    packages=["csvskim"],
    entry_points="""
        [console_scripts]
        csvskim=csvskim.cli:cli
    """,
    install_requires=["click"],
#    extras_require={"test": ["pytest", "pytest-icdiff", "cogapp", "PyYAML", "ruff"]},
    extras_require={"test": ["pytest"]},
    python_requires=">=3.8",
)
