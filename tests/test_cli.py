from pathlib import Path
from shutil import rmtree
from typer.testing import CliRunner

from air.cli import app


runner = CliRunner()


def _mysite_cleanup():
    if Path('mysite').exists():
        rmtree(Path('mysite'))


def test_init_success():
    _mysite_cleanup()
    result = runner.invoke(app, ["init", "mysite", "--defaults"])
    assert result.exit_code == 0
    assert result.output == "Created project mysite at [32m'mysite/'[0m\n"
    _mysite_cleanup()