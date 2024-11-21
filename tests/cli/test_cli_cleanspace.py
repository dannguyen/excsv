import pytest
from click.testing import CliRunner
from excsv.cli import cli


@pytest.fixture
def input_file(tmp_path):
    d = tmp_path / "sub"
    d.mkdir()
    p = d / "input.csv"
    p.write_text(
        """
name ,"their
age"
Alice , 42
  Bob ," 9
 "
"Cha
Cha",101
""".strip()
    )
    return p


@pytest.mark.alpha
def test_cli_cleanspace(input_file):
    runner = CliRunner()
    result = runner.invoke(cli, ["cleanspace", str(input_file)])
    assert result.exit_code == 0
    assert "name,their age\n" in result.output, "cleanspace cleans/trims headers"
    assert (
        "\nAlice,42\n" in result.output
    ), "cleanspace trims leading/trailing whitespace from field values"
    assert (
        "\nBob,9\n" in result.output
    ), "cleanspace converts newlines and trims leading/trailing whitespace, within field values"
    assert (
        "\nCha Cha,101" in result.output
    ), "cleanspace converts each newline into a whitespace, within field values"
