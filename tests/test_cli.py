"""Tests for the Air CLI."""

from typer.testing import CliRunner

from air.cli import app

runner = CliRunner()


def test_cli_help() -> None:
    """Test that --help works."""
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "Air CLI" in result.output
    assert "run" in result.output
    assert "version" in result.output


def test_cli_version() -> None:
    """Test the version command."""
    result = runner.invoke(app, ["version"])
    assert result.exit_code == 0
    assert "Air" in result.output


def test_cli_run_help() -> None:
    """Test that run --help works."""
    result = runner.invoke(app, ["run", "--help"])
    assert result.exit_code == 0
    assert "Run an Air application" in result.output
    assert "--host" in result.output
    assert "--port" in result.output
    assert "--reload" in result.output
