#!/usr/bin/env python3

from functools import wraps
from hyperloglog import HyperLogLog
from click_default_group import DefaultGroup
from rich_click import RichGroup
from rich.console import Console

error_console = Console(stderr=True,  style="cyan")

# Custom echo function that checks quiet flag from context
def verbose_echo(message, **kwargs):
    ctx = click.get_current_context()
    if ctx.obj and ctx.obj.get('quiet') is not True:
        error_console.print(message)
#        click.secho(message, err=True, **kwargs)

def load_quiet_option(func):
    """Decorator to add a quiet option to a command."""
    @click.option('--quiet', '-q', is_flag=True, help="Silence verbose stderr output.")
    @wraps(func)
    def wrapper(*args, **kwargs):
        quiet = kwargs.pop('quiet', False)
        ctx = click.get_current_context()
        ctx.ensure_object(dict)
        ctx.obj['quiet'] = quiet
        return func(*args, **kwargs)
    return wrapper



class DefaultRichGroup(DefaultGroup, RichGroup):
    """Make `click-default-group` work with `rick-click`."""



import rich_click as click

import csv
import re
from pathlib import Path
from typing import TextIO, List, Union
import sys

from .utils.excel import text_to_excel_book
from .utils.infer import infer_column_types
from .utils.listing import slice_input, transpose_list_of_lists
from .utils.text import clean_whitespace


def callback_tab_to_str(ctx, param, value):
    if value is not None:
        return value.encode().decode("unicode-escape")
    return value


def init_csv_reader(infile: TextIO, delimiter: str) -> csv.reader:
    return csv.reader(infile, delimiter=delimiter)

def init_csv_dict_reader(infile: TextIO, delimiter: str) -> csv.DictReader:
    return csv.DictReader(infile, delimiter=delimiter)



def init_csv_writer(outfile: TextIO, delimiter: str) -> csv.writer:
    return csv.writer(outfile, delimiter=delimiter)


def init_csv_dict_writer(
    outfile: TextIO, delimiter: str, fieldnames: List[str]
) -> csv.DictWriter:
    return csv.DictWriter(outfile, delimiter=delimiter, fieldnames=fieldnames)



def load_arg_input_file(fn):
    return click.argument(
        "input_file", nargs=1, type=click.File("r"), default="-", required=False
    )(fn)

def load_option_delimiter_in(fn):
    return click.option(
        "--delimiter",
        "-d",
        default=",",
        help=f"The field delimiter in the input CSV data.",
        required=False,
        show_default=True,
        type=str,
        callback=callback_tab_to_str,
    )(fn)


def load_option_delimiter_out(fn):
    return click.option(
        "--out-delimiter",
        "-D",
        default=",",
        help=f"The field delimiter in the output CSV data.",
        required=False,
        show_default=True,
        type=click.STRING,
        callback=callback_tab_to_str,
    )(fn)


def load_option_output_path(output_type="text"):
    def decorator(fn):
        if output_type == "bytes":
            mode = "wb"
        else:
            mode = "w"

        return click.option(
            "--output-path",
            "-o",
            default='-',
            help=f"Set the path of the output file. Default is sending {output_type} to stdout.",
            required=False,
            show_default=False,
            type=click.File(mode),
        )(fn)

    return decorator


## not yet implemented
# def load_option_line_numbers(fn):
#     return click.option(
#     "--line-numbers",
#     "-l",
#     default=0,
#     type=int,
#     help="Prepend a column named __line_number__ to each row that indicates the row number in the output data. Starts at 0 by default",
# )(fn)


@click.version_option()
@click.group(cls=DefaultRichGroup, default="excel", default_if_no_args=True)
def cli():
    pass


@cli.command()
@load_option_delimiter_in
@load_option_delimiter_out
@load_arg_input_file
@load_option_output_path()
def cleanspace(input_file, output_path, delimiter, out_delimiter):
    """
    Normalizes all whitespace as space characters, e.g. '\\r' and '\\n' are converted to ' '
    Converts all newlines into single space
    Strips whitespace from left and right
    Affects headers and data
    """
    incsv = init_csv_reader(input_file, delimiter=delimiter)
    out_csv = init_csv_writer(output_path, delimiter=out_delimiter)
    for row in incsv:
        for i, val in enumerate(row):
            row[i] = clean_whitespace(val)

        out_csv.writerow(row)


@cli.command()
@load_option_delimiter_in
@load_arg_input_file
@load_quiet_option
@click.option(
        "--output-path",
        "-o",
        help=f"Set the path of the output Excel file",
        required=True,
#        type=click.File('wb'),
        type=click.Path(dir_okay=False, path_type=Path, resolve_path=True)
)
def excel(input_file, output_path, delimiter):
    """
    Convert a CSV into a friendly readable Excel file
    """
    incsv = init_csv_reader(input_file, delimiter=delimiter)
    outbytes = text_to_excel_book(incsv)

    with open(output_path, 'wb') as wfile:
        wfile.write(outbytes.getvalue())

    verbose_echo(f"Wrote Excel file to:")
    verbose_echo(click.format_filename(output_path))

@cli.command()
@load_option_delimiter_in
@load_option_delimiter_out
@load_arg_input_file
@load_option_output_path()
def infer(input_file, output_path, delimiter, out_delimiter):
    """
    Infer the data types for each column
    """

    incsv = init_csv_dict_reader(input_file, delimiter=delimiter)

    inferred = infer_column_types(incsv)
    outs = [["fieldname", "datatype"]]
    for key, val in inferred.items():
        outs.append([key, val])

    out_csv = init_csv_writer(output_path, delimiter=out_delimiter)
    for row in outs:
        out_csv.writerow(row)




@cli.command()
@load_option_delimiter_in
@load_option_delimiter_out
@load_arg_input_file
@load_option_output_path()
def probe(input_file, output_path, delimiter, out_delimiter):

    incsv = init_csv_dict_reader(input_file, delimiter=delimiter)
    row_count = 0
    headers = incsv.fieldnames
    # col_count = len(headers)

    column_metadata = {
        header: {"name": header, "position": i,  "blanks": 0, "cardinality": HyperLogLog(0.01),}
        for i, header in enumerate(headers)
    }

    # Process each row
    for row in incsv:
        row_count += 1

        for header, value in row.items():
            column_metadata[header]["cardinality"].add(value)
            if value in ["", ]:  # Define other criteria for blank or N/A as needed
                column_metadata[header]["blanks"] += 1



    # error_console.print(f"Number of rows: {row_count}")
    # error_console.print(f"Number of columns: {col_count}")

    out_data = []
    for col in column_metadata.values():
        col['cardinality'] = len(col['cardinality'])
        out_data.append(col)


    out_headers = out_data[0].keys()
    outcsv = init_csv_dict_writer(output_path, delimiter=out_delimiter, fieldnames=out_headers)
    outcsv.writeheader()
    outcsv.writerows(out_data)





@cli.command()
@load_option_delimiter_in
@load_option_delimiter_out
@load_arg_input_file
@load_option_output_path()
@click.option(
    "--index",
    "-i",
    show_default=True,
    default=[
        "0",
    ],
    multiple=True,
    help="0-based row numbers to include in slice, can be either integer or integer range e.g. 1,42,6-20",
)
def slice(index, input_file, output_path, delimiter, out_delimiter):
    """
    Select specific lines from a CSV to output.

    index option accepts integer values, e.g.
        excsv slice -i 1 input.csv

    You can also pass in hyphenated ranges, e.g.
        excsv slice -i 4-10 input.csv

        is equivalent to:
        excsv slice -i 4 -i 5 -i 6 -i 7 -i 8 -i 9 -i 10  input.csv
    """

    # parse indices
    index_numbers = []
    for ival in index:
        if re.match(r"^\d+$", ival):
            index_numbers.append(int(ival))
        elif rx := re.match(r"^(\d+)-(\d+)$", ival):
            _a, _b = (int(i) for i in rx.groups())
            index_numbers.extend(list(range(_a, _b + 1)))
        else:
            raise click.UsageError(f"Invalid --index value: {ival}")

    index_numbers.sort()  # = sorted([int(i) for i in indices])

    incsv = init_csv_reader(input_file, delimiter=delimiter)
    headers = next(incsv)

    out_csv = init_csv_writer(output_path, delimiter=out_delimiter)

    out_csv.writerow(headers)

    for i, line in slice_input(incsv, index_numbers):
        out_csv.writerow(line)


if __name__ == "__main__":
    cli()


@cli.command()
@load_option_delimiter_in
@load_option_delimiter_out
@load_arg_input_file
@load_option_output_path()
def transpose(input_file, output_path, delimiter, out_delimiter):
    """
    Returns a transposed version of the CSV file
    """
    incsv = init_csv_reader(input_file, delimiter=delimiter)
    out_csv = init_csv_writer(output_path, delimiter=out_delimiter)


    """
    Converts:
        [                         to:      [
            ["name", "region"],               ["name", "Alice", "Bob", "Chaz"],
            ["Alice", "North"],               ["region", "North", "North", "South"],
            ["Bob",  "North"],             ]
            ["Chaz", "South"],

        ]
    """

    for row in zip(*incsv):
        out_csv.writerow(row)





@cli.command()
@load_arg_input_file
@load_option_delimiter_in
@load_option_delimiter_out
@load_option_output_path()
def testread(input_file, delimiter, out_delimiter, output_path):

    incsv = init_csv_reader(input_file, delimiter=delimiter)

    data = list(incsv)

    output_path.write(f"Number of rows: {len(data)}\n")
    output_path.write(f"Number of cols: {len(data[0])}\n")


if __name__ == "__main__":
    cli()
