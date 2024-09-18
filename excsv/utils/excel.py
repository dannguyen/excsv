import csv
from io import BytesIO
import openpyxl
from openpyxl.styles import Alignment, Font
from openpyxl.styles import Color, PatternFill, Font, Border
from openpyxl.utils import get_column_letter
# from openpyxl.utils.dataframe import dataframe_to_rows
from typing import BinaryIO, TextIO



HEADER_FILL = PatternFill(patternType="solid", fgColor=Color(rgb="00222222"))


def init_workbook(
    frozen_row: int = 1,
    frozen_col: int = 2,
) -> openpyxl.Workbook:
    """
    Create workbook
    Add workbook features, e.g. freeze rows and so forth
    """
    wb = openpyxl.Workbook(write_only=False)
    # TK: we want to use write_only, but write_only means you have to
    #  add features to workbook before you write data
    # can't write data and then freeze rows, for instance

    sheet = wb.create_sheet()

    return wb


def add_data_to_workbook(wb: openpyxl.Workbook, input_csv: csv.reader):
    sheet = wb.active
    for row in input_csv:
        sheet.append(row)


def add_features_to_workbook(
    wb: openpyxl.Workbook,
    frozen_row: int = 1,
    frozen_col: int = 2,
    auto_filter: bool = True,
) -> None:
    """
    Add Workbook features, such as frozen row/column and autofilters
    """

    sheet = wb.active

    frozen_row_actual_num = frozen_row + 1
    frozen_col_letter = openpyxl.utils.cell.get_column_letter(frozen_col)
    sheet.freeze_panes = f"{frozen_col_letter}{frozen_row_actual_num}"

    if auto_filter is True:
        sheet.auto_filter.ref = sheet.dimensions



def add_styles_to_workbook(wb: openpyxl.Workbook, max_cell_width=70, min_cell_width=10) -> None:
    """
    Set typefaces
    Bold and colorize the headers
    Set maxwidth

    todo: add params to let user configure look and feel
    for now, just apply default styles

    tk todo: this is really inefficient. Data and styling should be done in one loop, not in separate loops
    """
    sheet = wb.active



    # Set column width to: min_cell_width and no bigger than max_cell_width
    # tk: this is very inefficient
    for ix, col in enumerate(sheet.columns):
        if ix == 0:
            continue
        column = col[0].column_letter  # Get the column name

        biggest_cell = min_cell_width

        for cell in col:
            try:
                if len(str(cell.value)) > biggest_cell:
                    biggest_cell = len(str(cell.value))
            except:
                pass
        adjusted_width = biggest_cell + 2
        adjusted_width = min(adjusted_width, max_cell_width)
        sheet.column_dimensions[column].width = adjusted_width


    # Set cell-by-cell styles
    for row_idx, row in enumerate(sheet.iter_rows(), start=1):
        for col_idx, cell in enumerate(row, start=1):

            cell = sheet.cell(row=row_idx, column=col_idx,)

            # Set default cell to wrap text, and be aligned at the top and left
            cell.alignment = Alignment(
                wrap_text=True, vertical="top", horizontal="left"
            )

            # set header styles
            if row_idx == 1:
                cell.alignment = Alignment(
                    wrap_text=True, vertical="center", horizontal="left"
                )
                cell.font = Font(bold=True, size="14", color="FFFFFF")
                cell.fill = HEADER_FILL

            # set first column styles
            if col_idx == 1 and row_idx != 1:
                # Make first column bold, and set fill to gray
                cell.font = Font(bold=True)
                cell.fill = PatternFill(patternType="solid", fgColor=Color(rgb="00EEEEEE"))





# note to self: why does this return BinaryIO? Was it just for testing?
def csv_to_workbook(
    input_csv: csv.reader,
    frozen_row: int = 1,
    frozen_col: int = 2,
) -> BinaryIO:
    # Create a workbook and select the active worksheet
    wb = init_workbook()
    add_data_to_workbook(wb, input_csv)
    add_features_to_workbook(wb, frozen_row, frozen_col)
    add_styles_to_workbook(wb)
    excel_bytes = BytesIO()
    wb.save(excel_bytes)

    # Seek to the start of the BytesIO object so it can be read from the beginning
    excel_bytes.seek(0)

    # Return the BytesIO object
    return excel_bytes
