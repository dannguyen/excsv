import pytest
from click.testing import CliRunner
from excsv.cli import cli


@pytest.fixture
def input_file(tmp_path):
    d = tmp_path / "sub"
    d.mkdir()
    p = d / "input.tsv"
    p.write_text(
        """
name,age
Alice,42
Bob,9
Chaz,101
""".strip()
    )
    return p


@pytest.fixture
def input_tsv_file(tmp_path):
    d = tmp_path / "sub"
    d.mkdir()
    p = d / "input.tsv"
    p.write_text(
        """
name\tage
Alice\t42
Bob\t9
Chaz\t101
""".strip()
    )
    return p


def test_cli_reads_different_delimiters(input_tsv_file):
    runner = CliRunner()
    result = runner.invoke(cli, ["cleanspace", "-d", "\t", str(input_tsv_file)])
    assert result.exit_code == 0
    assert "name,age" in result.output
    assert "Alice,42" in result.output


def test_cli_outputs_different_delimiters(input_file):
    runner = CliRunner()
    result = runner.invoke(cli, ["cleanspace", "-D", "\t", str(input_file)])
    assert result.exit_code == 0
    assert "name\tage" in result.output
    assert "Alice\t42" in result.output


def test_cli_inputs_outputs_different_delimiters(input_tsv_file):
    runner = CliRunner()
    result = runner.invoke(
        cli, ["cleanspace", "-D", "&", "-d", "\t", str(input_tsv_file)]
    )
    assert result.exit_code == 0
    assert "name&age" in result.output
    assert "Alice&42" in result.output
