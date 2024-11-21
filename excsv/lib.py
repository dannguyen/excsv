import csv
from typing import Union, Dict, List, TextIO, NoReturn, Iterator


def transpose_list_of_lists(input_data:List[List[str]]) -> List[List[str]]:
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



def slice_input(input_data:Iterator, indices:List[int]) -> NoReturn:

    for i, row in enumerate(input_data):
        if i in indices:
            yield i, row


