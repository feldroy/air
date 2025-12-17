import logging
from datetime import datetime
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
        project_path = Path(Path(__file__).parent / "templates/init")
        project_path.copy(path)
    print(f"Created new project at '{path}'")

    # check_call(["uv", "init", str(path)])  # TODO placeholder to be replaced by Cookiecutter


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
    project_path = Path()
    route_path = project_path / "app" / "routes"
    migration_path = project_path / "db" / "migrations"
    schema_path = project_path / "db" / "schema"
    if fields is None:
        fields = []

    if engine == "asyncpg":
        # Create route
        route_path = route_path / f"{name}.py"
        route_path.touch()
        # TODO
        route_path.write_text("""import air

router = air.AirRouter()
        """)

        # do migration
        migration = []
        migration.append("-- migrate:up")
        migration.append(f"-- PostgreSQL table creation script for {name}")
        migration.append(f"CREATE TABLE {name} (")
        migration.append("  id SERIAL PRIMARY KEY,")
        # TODO key:value pairs
        types2pg = {"str": "VARCHAR(255)", "text": "TEXT"}
        for field in fields:
            title, typ = field.split(":")
            migration.append(f"  {title} {types2pg.get(typ)},")
        migration.append("  created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),")
        migration.append("  updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()")
        migration.append(");")
        migration.append("\n")
        migration_path = migration_path / f"{timestamp_ymd_seconds()}_{name}.sql"
        text = "\n".join(migration)
        migration_path.touch()
        migration_path.write_text(text)
        print(f"Create migration at '{migration_path}'")
