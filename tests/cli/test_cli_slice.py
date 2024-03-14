import pytest
from pathlib import Path
from click.testing import CliRunner
from csvskim.cli import cli
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


@pytest.fixture
def output_file(tmp_path):
    return tmp_path / "output.csv"



def test_slice(input_file):
    runner = CliRunner()
    result = runner.invoke(cli, ['slice', '--input-path', str(input_file), '0', '2'])
    assert result.exit_code == 0
    assert 'name,age' in result.output, "slice always returns headers"
    assert 'Alice,42' in result.output, 'slice is 0-indexed'
    assert 'Chaz,101' in result.output, 'slice takes in multiple arguments for indices'
    assert 'Bob' not in result.output, 'slice does not return lines not specified in indices'


def test_slice_add_index_column():
    runner = CliRunner()

    with runner.isolated_filesystem():
        with open('test.csv', 'w') as f:
            writer = csv.writer(f)
            writer.writerow(['name', 'region'])
            writer.writerow(['Alice', 'North'])
            writer.writerow(['Bob', 'North'])
            writer.writerow(['Chaz', 'South'])

        result = runner.invoke(cli, ['slice', '--input-path', 'test.csv', '--add-index', '1', '2'])

        assert result.exit_code == 0
        assert '__INDEX__' in result.output
        assert 'Chaz' in result.output
