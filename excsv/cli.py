#!/usr/bin/env python3

import click
import csv
import re
from pathlib import Path
from typing import TextIO, List, Union
import sys

from .utils.excel import text_to_excel_book
from .utils.infer import infer_column_types
from .utils.listing import slice_input, transpose_list_of_lists
from .utils.text import clean_whitespace




def load_arg_input_file(fn):
    return click.argument('input_file', nargs=1, type=click.File("r"), default="-", required=False)(fn)


def init_csv_reader(infile:TextIO, delimiter:str, dict_mode:bool=False) -> Union[csv.reader, csv.DictReader]:
    if dict_mode is True:
        return csv.DictReader(infile, delimiter=delimiter)
    else:
        return csv.reader(infile, delimiter=delimiter)

def init_csv_writer(outfile:TextIO, delimiter:str) -> csv.writer:
    return csv.writer(outfile, delimiter=delimiter)

def init_csv_dict_writer(outfile:TextIO, delimiter:str, fieldnames:List[str]) -> csv.DictWriter:
    return csv.DictWriter(outfile, delimiter=delimiter, fieldnames=fieldnames)

def load_option_delimiter_in(fn):
    return click.option(
    "--delimiter",
    "-d",
    default=",",
    help=f"The field delimiter in the input CSV data.",
    required=False,
    show_default=True,
    type=str
)(fn)

def load_option_delimiter_out(fn):
    return click.option(
    "--out-delimiter",
    "-D",
    default=",",
    help=f"The field delimiter in the output CSV data.",
    required=False,
    show_default=True,
    type=str
)(fn)


def load_option_output_path(output_type='text'):
    def decorator(fn):
        if output_type == 'bytes':
            mode = 'wb'
        else:
            mode = "w"

        return click.option(
            "--output-path",
            "-o",
            default="-",
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





@click.group()
@click.version_option()
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
@load_option_output_path(output_type='bytes')
def excel(input_file, output_path, delimiter):
    """
    Convert a CSV into a friendly readable Excel file
    """
    incsv = init_csv_reader(input_file, delimiter=delimiter)
    outbytes = text_to_excel_book(incsv)

    # with open(output_path, 'wb') as outfile:
    if output_path is sys.stdout:
        output_path.buffer.write(outbytes.getvalue())
    else:
        output_path.write(outbytes.getvalue())



@cli.command()
@load_option_delimiter_in
@load_option_delimiter_out
@load_arg_input_file
@load_option_output_path()
def infer(input_file, output_path, delimiter, out_delimiter):
    """
    Infer the data types for each column
    """

    incsv = init_csv_reader(input_file, dict_mode=True, delimiter=delimiter)

    inferred = infer_column_types(incsv)
    outs = [['fieldname', 'datatype']]
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
@click.option(
    "--index",
    "-i",
    show_default=True,
    default=['0',],
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
        if re.match(r'^\d+$', ival):
            index_numbers.append(int(ival))
        elif (rx := re.match(r'^(\d+)-(\d+)$', ival)):
            _a, _b = (int(i) for i in rx.groups())
            index_numbers.extend(list(range(_a, _b+1)))
        else:
            raise click.UsageError(f"Invalid --index value: {ival}")


    index_numbers.sort() #= sorted([int(i) for i in indices])


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
    for row in transpose_list_of_lists(incsv):
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




