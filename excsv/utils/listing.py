from typing import List, NoReturn


def slice_input(input_data: List[List[str]], indices: List[int]) -> NoReturn:
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

    for row in zip(*input_data):
        yield list(row)
