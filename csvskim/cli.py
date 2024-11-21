#!/usr/bin/env python3

import click
import csv
from pathlib import Path
from typing import TextIO, List
import sys

from .lib import transpose_list_of_lists, slice_input

@click.group()
@click.version_option()
def cli():
    pass



@cli.command()
@click.option(
    '--input-path',
    '-i',
    type=Path,
    help=f"Set the path of the input file",
)
@click.option(
    "--add-index",
    is_flag=True,
    show_default=True,
    default=False,
    help="Prepend a column named __INDEX__ that shows the row number",
)
@click.argument("indices", type=str, nargs=-1)
def slice(indices, input_path, add_index):
    # parse integers
    index_numbers = sorted([int(i) for i in indices])
    click.echo(index_numbers, err=True)
    output_handle = sys.stdout
    out_csv = csv.writer(output_handle)

    input_path = Path(input_path).expanduser().resolve()
    with open(input_path, 'r') as infile:
        incsv = csv.reader(infile)
        headers = next(incsv)

        if add_index is True:
            headers.insert(0, '__INDEX__')

        out_csv.writerow(headers)
        for i, line in slice_input(incsv, index_numbers):
            if add_index is True:
                line.insert(0, i)
            out_csv.writerow(line)



@cli.command()
@click.option(
    '--input-path',
    '-i',
    type=Path,
    help=f"Set the path of the input file",
)
def transpose(input_path):
    """
    Returns a transposed version of the CSV file
    """
    input_path = Path(input_path).expanduser().resolve()
    output_handle = sys.stdout

    input_data = []
    wcsv = csv.writer(output_handle)
    with open(input_path, 'r') as infile:
        for row in transpose_list_of_lists(csv.reader(infile)):
            wcsv.writerow(row)


if __name__ == '__main__':
    cli()

