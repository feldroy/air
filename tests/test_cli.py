"""Tests for the Air CLI."""

import re

from typer.testing import CliRunner

from air.cli import app

runner = CliRunner()


def strip_ansi(text: str) -> str:
    """Remove ANSI escape codes from text."""
    return re.sub(r"\x1b\[[0-9;]*m", "", text)


def test_cli_help() -> None:
    """Test that --help works."""
    result = runner.invoke(app, ["--help"], color=False)
    assert result.exit_code == 0
    output = strip_ansi(result.output)
    assert "Air CLI" in output
    assert "run" in output
    assert "version" in output


def test_cli_version() -> None:
    """Test the version command."""
    result = runner.invoke(app, ["version"], color=False)
    assert result.exit_code == 0
    assert "Air" in result.output


def test_cli_run_help() -> None:
    """Test that run --help works."""
    result = runner.invoke(app, ["run", "--help"], color=False)
    assert result.exit_code == 0
    output = strip_ansi(result.output)
    assert "Run an Air application" in output
    assert "--host" in output
    assert "--port" in output
    assert "--reload" in output
