import pytest
from click.testing import CliRunner
from excsv.cli import cli
from io import BytesIO


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


def mock_text_to_excel_book(csv_reader):
    return BytesIO(b"Mock Excel Content")


@pytest.fixture(autouse=True)
def mock_text_to_excel_book_function(mocker):
    mocker.patch("excsv.cli.text_to_excel_book", new=mock_text_to_excel_book)


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
            [
                "excel",
                str(input_file),
                 "-o", "test.xlsx"
            ],
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
            result = runner.invoke(cli, ["excel",  "-o", "test.xlsx"], input=infile.read(),)
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


# Test when output_path is stdout
@pytest.mark.skip("Excel stdout deprecated")
def test_excel_with_stdout_output(mocker, input_file):
    runner = CliRunner()
    result = runner.invoke(cli, ["excel", str(input_file)])
    assert result.exit_code == 0
    assert b"Mock Excel Content" in result.stdout_bytes
