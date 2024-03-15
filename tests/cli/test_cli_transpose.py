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
name,age
Alice,42
Bob,9
Chaz,101
""".strip()
    )
    return p


def test_cli_transpose(input_file):
    runner = CliRunner()
    result = runner.invoke(cli, ["transpose", str(input_file)])
    assert result.exit_code == 0
    assert (
        "name,Alice,Bob,Chaz" in result.output
    ), "transpose result first row is the first header and its values"
    assert "age,42,9,101" in result.output
