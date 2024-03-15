import csv
from io import BytesIO
import openpyxl
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, numbers
from openpyxl.utils.dataframe import dataframe_to_rows
from openpyxl.worksheet.views import Pane

from typing import Dict, Iterator, List, NoReturn, Union
from typing import BinaryIO, TextIO


def slice_input(input_data: Iterator, indices: List[int]) -> NoReturn:
    for i, row in enumerate(input_data):
        if i in indices:
            yield i, row


def transpose_list_of_lists(input_data: List[List[str]]) -> List[List[str]]:
    """
    Converts:
        [                         to:      [
            ["name", "region"],               ["name", "Alice", "Bob", "Chaz"],
            ["Alice", "North"],               ["region", "North", "North", "South"],
            ["Bob",  "North"],             ]
            ["Chaz", "South"],

        ]
    """
    return [list(row) for row in zip(*input_data)]


def text_to_excel_book(
    input_csv: csv.reader,
    frozen_row: int = 1,
    frozen_col: int = 2,
) -> BinaryIO:
    # Create a workbook and select the active worksheet
    wb = Workbook()
    sheet = wb.active

    # Simulate reading from a stream (e.g., a file or network stream)
    # Here, csv_stream is expected to be an iterable of CSV lines

    for row in input_csv:
        # Append each row from the CSV to the Excel sheet
        sheet.append(row)

    frozen_row_actual_num = frozen_row + 1
    frozen_col_letter = openpyxl.utils.cell.get_column_letter(frozen_col)
    sheet.freeze_panes = f"{frozen_col_letter}{frozen_row_actual_num}"
    sheet.auto_filter.ref = sheet.dimensions

    excel_bytes = BytesIO()
    wb.save(excel_bytes)

    # Seek to the start of the BytesIO object so it can be read from the beginning
    excel_bytes.seek(0)

    # Return the BytesIO object
    return excel_bytes
