import pytest
from pathlib import Path
from click.testing import CliRunner
from excsv.cli import cli
import csv


@pytest.fixture
def input_file(tmp_path):
    d = tmp_path / "sub"
    d.mkdir()
    p = d / "input.csv"
    p.write_text(
        """
name,age
Alice,42
Bob,9
Chaz,101
""".strip()
    )
    return p


def test_slice(input_file):
    runner = CliRunner()
    result = runner.invoke(cli, ["slice", "--input-path", str(input_file), "0", "2"])
    assert result.exit_code == 0
    assert "name,age" in result.output, "slice always returns headers"
    assert "Alice,42" in result.output, "slice is 0-indexed"
    assert "Chaz,101" in result.output, "slice takes in multiple arguments for indices"
    assert (
        "Bob" not in result.output
    ), "slice does not return lines not specified in indices"


def test_slice_add_index_column(input_file):
    runner = CliRunner()
    result = runner.invoke(
        cli, ["slice", "--input-path", str(input_file), "0", "2", "--add-index"]
    )
    assert result.exit_code == 0
    assert "__INDEX__,name,age" in result.output
    assert "2,Chaz,101" in result.output


def test_slice_with_file_input(input_file):
    runner = CliRunner()
    result = runner.invoke(
        cli,
        ["slice", "--input-path", str(input_file), "1", "2"],
        catch_exceptions=False,
    )
    assert result.exit_code == 0
    assert "Bob" in result.output
    assert "9" in result.output


def test_slice_with_stdin_input(input_file):
    runner = CliRunner()
    with input_file.open("r") as infile:
        result = runner.invoke(
            cli,
            ["slice", "--add-index", "1", "2"],
            input=infile.read(),
            catch_exceptions=False,
        )
    assert result.exit_code == 0
    assert "__INDEX__" in result.output
    assert "Bob" in result.output
    assert "9" in result.output


# @pytest.fixture
# def output_file(tmp_path):
#     return tmp_path / "output.csv"
