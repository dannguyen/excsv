import pytest
from pathlib import Path
import click
import csv

from click.testing import CliRunner
from excsv.cli import cli


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
Dan,2000
Egon,3000
Fran,5555
""".strip()
    )
    return p


def test_slice(input_file):
    runner = CliRunner()
    result = runner.invoke(cli, ["slice", str(input_file), "-i", "0", "--index", "2"])
    assert result.exit_code == 0
    assert "name,age" in result.output, "slice always returns headers"
    assert "Alice,42" in result.output, "slice is 0-indexed"
    assert "Chaz,101" in result.output, "slice takes in multiple arguments for index"
    assert (
        "Bob" not in result.output
    ), "slice does not return lines not specified in index"


def test_slice_with_range(input_file):
    runner = CliRunner()
    result = runner.invoke(cli, ["slice",  "--index", "1-2",  str(input_file),])
    assert result.exit_code == 0
    assert "Bob,9" in result.output
    assert "Chaz,101" in result.output


def test_slice_with_multiple_ranges(input_file):
    runner = CliRunner()
    result = runner.invoke(cli, ["slice", "-i", "4-5", "-i", "0-2", str(input_file)])
    assert result.exit_code == 0
    assert "Bob,9" in result.output
    assert "Chaz,101" in result.output
    assert "Egon,3000" in result.output
    assert "Fran,5555" in result.output
    assert "Dan,2000" not in result.output


def test_slice_with_mix_of_num_and_ranges(input_file):
    runner = CliRunner()
    result = runner.invoke(cli, ["slice", "-i" , "4" , "-i", "0-1", str(input_file),])
    assert result.exit_code == 0
    assert "Alice,42" in result.output, "slice is 0-indexed"
    assert "Bob,9" in result.output
    assert "Egon,3000" in result.output
    assert "Chaz,101" not in result.output
    assert "Dan,2000" not in result.output



def test_slice_with_file_input(input_file):
    runner = CliRunner()
    result = runner.invoke(
        cli,
        ["slice", str(input_file), "-i", "0", "-i", "2",],
        catch_exceptions=False,
    )
    assert result.exit_code == 0
    assert "Alice,42" in result.output
    assert "Chaz,101" in result.output



def test_slice_with_stdin_input(input_file):
    runner = CliRunner()
    with input_file.open("r") as infile:
        result = runner.invoke(
            cli,
            ["slice", "-i", "1", "-i", "2",],
            input=infile.read(),
            catch_exceptions=False,
        )
    assert result.exit_code == 0
    assert "Bob" in result.output
    assert "9" in result.output




@pytest.mark.skip("Deprecated with new input_path handling")
def test_slice_raises_error_when_no_index_argument_is_passed(input_file):
    runner = CliRunner()
    result = runner.invoke(cli, ['slice', '--input-path', str(input_file)])
    assert result.exit_code == 2  # Expecting a failure exit code
    assert "You must provide at least one value for index argument." in result.output


def test_slice_raises_error_when_invalid_index_argument(input_file):
    runner = CliRunner()
    result = runner.invoke(cli, ['slice', "-i", "42,233" ,  str(input_file)])
    assert result.exit_code == 2
    assert "Invalid --index value: 42,233" in  result.output
