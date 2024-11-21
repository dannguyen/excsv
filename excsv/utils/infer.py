import csv
from typing import List, Union, Dict, TextIO


def infer_data_type(value: str) -> Union[type(int), type(float), type(str)]:
    """
    infer the data type of a value
    """

    try:
        int(value)
        return int
    except ValueError:
        try:
            float(value)
            return float
        except ValueError:
            return str


def common_type(types: List[type]) -> type:
    """
    determine the most specific common type among a list of types
    """
    if str in types:
        return str
    elif float in types:
        return float
    elif int in types:
        return int
    return str  # Default to string if no values are present


def infer_column_types(input_data: List[Dict[str, str]]) -> Dict[str, type]:
    column_types = {}

    for row in input_data:
        for column, value in row.items():
            inferred_type = infer_data_type(value)

            # If this is the first time we're seeing this column, initialize its type list
            if column not in column_types:
                column_types[column] = [inferred_type]
            else:
                # Otherwise, add the inferred type to the list if it's not already present
                if inferred_type not in column_types[column]:
                    column_types[column].append(inferred_type)

    # Determine the most specific common type for each column
    for column, types in column_types.items():
        column_types[column] = common_type(types)

    return {column: typ.__name__ for column, typ in column_types.items()}
