import logging
from datetime import datetime
from importlib.metadata import version
from pathlib import Path
import tempfile
import shutil
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
    """Start new Air project"""
    if path.exists():
        print(f"[bold red]ERROR: '{path}' already exists![/bold red]")
        print(f"[red]Air will not overwrite '{path}'.[/red]")
        raise typer.Abort
    if template is None:
        project_template_path = templates_path / "init"
        cookiecutter(str(project_template_path), extra_context={"name": str(path)})
    else:
        cookiecutter(template)
    print(f"Created new project at '{path}'")


def copytree_no_overwrite(src: Path, dst: Path) -> None:
    src = Path(src)
    dst = Path(dst)

    for item in src.rglob("*"):
        target = dst / item.relative_to(src)

        if item.is_dir():
            target.mkdir(parents=True, exist_ok=True)
        else:
            if target.exists():
                # Skip existing files
                continue
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(item, target)    


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

    # schema_path = Path() / "db" / "schema"


    if fields is None:
        fields = []

    if engine == "asyncpg":
        # Save cookiecutter to tmp location
        # use shutil.copytree to bring it in

        resource_template_path = templates_path / "resources"

        # Create route
        try:
            (Path() / "app" / "routes" / "__init__.py").touch()
        except FileNotFoundError:
            print("[red bold]Error: Not in an Air project.[/red bold]")
            raise typer.Abort from None
        
        field_dict = {}
        for field in fields:
            title, type = field.split(":")
            field_dict[title] = PYTHON_TO_POSTGRES.get(type, "VARCHAR(255)")
                    
        with tempfile.TemporaryDirectory() as tmpdir:
            project_path = cookiecutter(
                template=str(resource_template_path),
                output_dir=tmpdir,
                no_input=True,
                extra_context={"name": name, "fields": field_dict, "project": "project"}
            )        

        copytree_no_overwrite(tmpdir, Path())
        print(f"New resource create at {Path().expanduser()}")

