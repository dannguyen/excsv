import pytest
from click.testing import CliRunner
from excsv.cli import cli

def test_help_option():
    runner = CliRunner()
    result = runner.invoke(cli, ['--help'])
    assert result.exit_code == 0
    assert 'Usage:' in result.output
    assert '--help ' in result.output



def test_cli_version():
    runner = CliRunner()
    result = runner.invoke(cli, ['--version'])
    assert result.exit_code == 0
    assert "version" in result.output
