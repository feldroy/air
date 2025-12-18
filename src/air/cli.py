import logging
from datetime import datetime
from importlib.metadata import version
from pathlib import Path
from typing import Annotated

import typer
from cookiecutter.main import cookiecutter
from fastapi_cli.logging import setup_logging
from jinja2 import Environment, FileSystemLoader
from rich import print

logger = logging.getLogger(__name__)

try:
    import uvicorn
except ImportError:  # pragma: no cover
    uvicorn = None  # type: ignore[assignment]

template_path = Path(__file__).parent / "templates"

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
    """Start new Air project"""
    if path.exists():
        print(f"[bold red]ERROR: '{path}' already exists![/bold red]")
        print(f"[red]Air will not overwrite '{path}'.[/red]")
        raise typer.Abort
    if template is None:
        project_path = template_path / "init"
        cookiecutter(str(project_path), extra_context={"name": str(path)}, no_input=True)
    else:
        cookiecutter(template)
    print(f"Created new project at '{path}'")


@app.command()
def resource(
    name: Annotated[
        str,
        typer.Argument(help="Name of the new resource."),
    ],
    engine: Annotated[
        str,
        typer.Option(help="Choose which database engine, currently only supports asyncpg"),
    ] = "asyncpg",
    fields: Annotated[
        list[str] | None, typer.Argument(help="A set of 'name:type' pairs for defining fields in a resource")
    ] = None,
) -> None:
    """
    Creates a resource representing a database table.

    - Create the schema in db/
    - Create the initial migration in db/
    - Create a router file with CRUD views in apps/routes

    Supported types are:
        - Basic Python types like str, int, float, etc
        - "text" is a long character field
    """
    jinja_env = Environment(loader=FileSystemLoader(str(template_path / "resources"))) 

    # schema_path = Path() / "db" / "schema"


    if fields is None:
        fields = []

    if engine == "asyncpg":
        # Create route
        route_path = Path() / "app" / "routes" / f'{name}.py'
        try:
            route_path.touch()
        except FileNotFoundError:
            print("[red bold]Error: Not in an Air project.[/red bold]")
            raise typer.Abort from None
        template = jinja_env.get_template("app/routes/router.py")
        output = template.render(name=name)
        # print(output)
        route_path.write_text(output)
        print(f"Created router at {route_path}")

        # do migration
        types2pg = {"str": "VARCHAR(255)", "text": "TEXT"}
        field_dict = {}
        for field in fields:
            title, type = field.split(":")
            field_dict[title] = types2pg.get(type, "VARCHAR(255)")
        template = jinja_env.get_template("db/migrations/timestamp_initial.sql")
        output = template.render(name=name, fields=field_dict)
        migration_path = Path() / 'db' / 'migrations' / f'{timestamp_ymd_seconds()}_initial.py'
        migration_path.write_text(output)
        print(output)

        # migration_path / f"{timestamp_ymd_seconds()}_{name}.sql"
