import logging
from importlib.metadata import version
from pathlib import Path
from typing import Annotated

import typer
from fastapi_cli.logging import setup_logging
from rich import print

logger = logging.getLogger(__name__)

try:
    import uvicorn
except ImportError:  # pragma: no cover
    uvicorn = None  # type: ignore[assignment]


app = typer.Typer(rich_markup_mode="rich", context_settings={"help_option_names": ["-h", "--help"]})


def version_callback(value: bool) -> None:
    if value:
        print(f"Air version: [green]{version('air')}[/green]")
        raise typer.Exit


@app.callback()
def callback(
    version: Annotated[
        bool | None,
        typer.Option("--version", help="Show the version and exit.", callback=version_callback),
    ] = None,
    verbose: bool = typer.Option(False, help="Enable verbose output"),
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
        typer.Argument(help="The path for where the new project will be built."),
    ],
    template: Annotated[str | None, typer.Option(help="The Cookiecutter-style path to a project template.")] = None,
) -> None:
    """Start new Air project"""
    if path.exists():
        print(f"[bold red]ERROR: '{path}' already exists![/bold red]")
        print(f"[red]Air will not overwrite '{path}'.[/red]")
        raise typer.Abort
    if template is None:
        project_path = Path(Path(__file__).parent / "templates/init")
        project_path.copy(path)
    print(f"Created new project at '{path}'")

    # check_call(["uv", "init", str(path)])  # TODO placeholder to be replaced by Cookiecutter


@app.command()
def resource(name: str) -> None:
    """
    Creates a resource representing a database table.

    - Create the schema in db/
    - Create the initial migration in db/
    - Create a router file with CRUD views in apps/routes
    """

