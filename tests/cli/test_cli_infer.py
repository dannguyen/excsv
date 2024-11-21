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
name,age,improv rate
Alice,42,12
Bob,9,1.9
Chaz,101,3.14
""".strip()
    )
    return p


@pytest.mark.alpha
def test_cli_infer(input_file):
    """
    tk tk this is very basic and naive implementation
    """
    runner = CliRunner()
    result = runner.invoke(cli, ["infer", str(input_file)])
    assert result.exit_code == 0
    assert "fieldname,datatype\n" in result.output, "infer outputs the headers fieldname and datatype"
    assert "name,str" in result.output
    assert "age,int" in result.output
    assert "improv rate,float" in result.output
