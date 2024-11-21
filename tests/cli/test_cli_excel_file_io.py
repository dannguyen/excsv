import pytest
from click.testing import CliRunner
from excsv.cli import cli
from io import BytesIO
from pathlib import Path
import os


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


def mock_csv_to_workbook(csv_reader):
    return BytesIO(b"Mock Excel Content")


@pytest.fixture(autouse=True)
def mock_csv_to_workbook_function(mocker):
    mocker.patch("excsv.cli.csv_to_workbook", new=mock_csv_to_workbook)


@pytest.mark.alpha
def test_excel_with_file_input_and_file_output(input_file):
    runner = CliRunner()
    with runner.isolated_filesystem():
        result = runner.invoke(
            cli,
            ["excel", str(input_file), "--output-path", "test.xlsx"],
        )
        assert result.exit_code == 0
        with open("test.xlsx", "rb") as f:
            content = f.read()
            assert content == b"Mock Excel Content"


# Test when input_path is a file
def test_excel_with_file_input(input_file):
    runner = CliRunner()
    with runner.isolated_filesystem():
        result = runner.invoke(
            cli,
            ["excel", str(input_file), "-o", "test.xlsx"],
        )
        assert result.exit_code == 0
        with open("test.xlsx", "rb") as f:
            content = f.read()
            assert content == b"Mock Excel Content"


# Test when input_path is stdin
def test_excel_with_stdin_input(mocker, input_file):
    runner = CliRunner()
    with runner.isolated_filesystem():

        with input_file.open("r") as infile:
            result = runner.invoke(
                cli,
                ["excel", "-o", "test.xlsx"],
                input=infile.read(),
            )
            assert result.exit_code == 0
            with open("test.xlsx", "rb") as f:
                content = f.read()
                assert content == b"Mock Excel Content"


# Test when output_path is a file
def test_excel_with_file_output(input_file):
    runner = CliRunner()
    with runner.isolated_filesystem():
        result = runner.invoke(
            cli,
            [
                "excel",
                str(input_file),
                "--output-path",
                "test.xlsx",
            ],
        )
        assert result.exit_code == 0

        with open("test.xlsx", "rb") as f:
            content = f.read()
            assert content == b"Mock Excel Content"


def test_excel_with_input_but_not_output_filename(mocker, input_file):
    runner = CliRunner()
    result = runner.invoke(cli, ["excel", str(input_file)])
    assert result.exit_code == 0
    with open(f"{input_file}.xlsx", "rb") as f:
        content = f.read()
        assert content == b"Mock Excel Content"


def test_excel_with_stdin_but_not_output_filename(mocker, tmp_path, input_file):
    runner = CliRunner()
    os.chdir(tmp_path)

    result = runner.invoke(cli, ["excel"], input="hello\nworld")
    assert result.exit_code == 0
    stdin_name = Path(tmp_path).joinpath("stdin.xlsx")
    with open(stdin_name, "rb") as f:
        content = f.read()
        assert content == b"Mock Excel Content"
