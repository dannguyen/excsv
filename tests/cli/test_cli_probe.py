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
name,age,region
Alice,42,North
Bob,,North
Chaz,101,South
""".strip()
    )
    return p


def test_cli_transpose(input_file):
    runner = CliRunner()
    result = runner.invoke(cli, ["probe", str(input_file)])
    assert result.exit_code == 0
    assert "name,position,blanks,cardinality" in result.output, "Validate probe meta header names"
    assert "name,0,0,3" in result.output, "Validate that probe columnar indexing is 0-based"
    assert "age,1,1,3" in result.output, "Validate that empty column value is counted as blank and as 1 possible cardinality"
    assert "region,2,0,2" in result.output, "validate cardinality"
