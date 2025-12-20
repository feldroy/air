import logging
from datetime import datetime
from importlib.metadata import version
from pathlib import Path
from typing import Annotated

import typer
from cookiecutter.main import cookiecutter
from fastapi_cli.logging import setup_logging
from rich import print

logger = logging.getLogger(__name__)

try:
    import uvicorn
except ImportError:  # pragma: no cover
    uvicorn = None  # type: ignore[assignment]

templates_path = Path(__file__).parent / "templates"

PYTHON_TO_POSTGRES = {
    "int": "INTEGER",
    "float": "DOUBLE PRECISION",
    "bool": "BOOLEAN",
    "str": "VARCHAR(255)",
    "bytes": "BYTEA",
    "date": "DATE",
    "time": "TIME",
    "datetime": "TIMESTAMP",
    "uuid": "UUID",
    "dict": "JSONB",
    "list": "JSONB",
    "tuple": "JSONB",
    "object": "TEXT",
    "text": "TEXT",
}

app = typer.Typer(rich_markup_mode="rich", context_settings={"help_option_names": ["-h", "--help"]})


def version_callback(value: int) -> None:
    if value:
        print(f"Air version: [green]{version('air')}[/green]")
        raise typer.Exit


def timestamp_ymd_seconds() -> str:
    now = datetime.now()
    seconds_of_day = now.hour * 3600 + now.minute * 60 + now.second
    return f"{now:%Y%m%d}{seconds_of_day}"


@app.callback()
def callback(
    version: Annotated[
        bool | None,
        typer.Option("--version", help="Show the version and exit.", callback=version_callback),
    ] = None,
    verbose: int = typer.Option(0, help="Enable verbose output"),
) -> None:
    """
    Air CLI - The [bold]air[/bold] command line app. ☁️

    Manage your [bold]Air[/bold] projects.

    """

    log_level = logging.DEBUG if verbose else logging.INFO

    setup_logging(level=log_level)


@app.command()
def init(
    path: Annotated[
        Path,
        typer.Argument(help="Path for where the new project will be built."),
    ],
    template: Annotated[str | None, typer.Option(help="The Cookiecutter-style path to a project template.")] = None,
) -> None:
    """Start new Air project

    Args:
        path: Location on the server where the project will be

    Raises:
        Abort: If the route name doesn't exist or if the provided parameters
            don't match the route's path parameters.

    """
    if path.exists():
        print(f"[bold red]ERROR: '{path}' already exists![/bold red]")
        print(f"[red]Air will not overwrite '{path}'.[/red]")
        raise typer.Abort

    if template is None:
        project_template_path = templates_path / "init"
        cookiecutter(str(project_template_path), extra_context={"name": path.name})
    else:
        cookiecutter(template)
    print(f"Created project {path.name} at '{path}'")
