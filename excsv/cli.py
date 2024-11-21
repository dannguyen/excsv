#!/usr/bin/env python3

import click
import csv
from pathlib import Path
from typing import TextIO, List, Union
import sys

from .lib import transpose_list_of_lists, slice_input, text_to_excel_book


def resolve_absolute_path(path: Union[str, Path]) -> Path:
    return Path(path).expanduser().resolve()


@click.group()
@click.version_option()
def cli():
    pass


@cli.command()
@click.option(
    "--input-path",
    "-i",
    # type=Path,
    default="-",
    help=f"Set the path of the input CSV file. Default is stdin",
    required=False,
    show_default=False,
    type=click.File("r"),
)
@click.option(
    "--output-path",
    "-o",
    default="-",
    required=False,
    show_default=False,
    type=click.File("wb"),
    help=f"Set the path of the output Excel file. Default is sending bytes to stdout",
)
def excel(input_path, output_path):
    incsv = csv.reader(input_path)
    outbytes = text_to_excel_book(incsv)

    # with open(output_path, 'wb') as outfile:
    if output_path is sys.stdout:
        output_path.buffer.write(outbytes.getvalue())
    else:
        output_path.write(outbytes.getvalue())


@cli.command()
@click.option(
    "--input-path",
    "-i",
    # type=Path,
    default="-",
    help=f"Set the path of the input CSV file. Default is stdin",
    required=False,
    show_default=False,
    type=click.File("r"),
)
@click.option(
    "--output-path",
    "-o",
    default="-",
    required=False,
    show_default=False,
    type=click.File("w"),
    help=f"Set the path of the output file. Default is sending text to stdout",
)
@click.option(
    "--add-index",
    is_flag=True,
    show_default=True,
    default=False,
    help="Prepend a column named __INDEX__ that shows the row number",
)
@click.argument("indices", type=str, nargs=-1)
def slice(indices, input_path, output_path, add_index):
    # parse integers
    index_numbers = sorted([int(i) for i in indices])
    #    click.echo(index_numbers, err=True)
    out_csv = csv.writer(output_path)

    incsv = csv.reader(input_path)
    headers = next(incsv)

    if add_index is True:
        headers.insert(0, "__INDEX__")

    out_csv.writerow(headers)

    for i, line in slice_input(incsv, index_numbers):
        if add_index is True:
            line.insert(0, i)
        out_csv.writerow(line)


@cli.command()
@click.option(
    "--input-path",
    "-i",
    type=Path,
    help=f"Set the path of the input file",
)
def transpose(input_path):
    """
    Returns a transposed version of the CSV file
    """
    input_path = resolve_absolute_path(input_path)
    output_handle = sys.stdout

    input_data = []
    wcsv = csv.writer(output_handle)
    with open(input_path, "r") as infile:
        for row in transpose_list_of_lists(csv.reader(infile)):
            wcsv.writerow(row)


if __name__ == "__main__":
    cli()
