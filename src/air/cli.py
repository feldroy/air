"""Air CLI - Command-line interface for running Air applications."""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Annotated

import typer
import uvicorn

app = typer.Typer(
    name="air",
    help="Air CLI - Run Air applications",
    add_completion=False,
    no_args_is_help=True,
    rich_markup_mode="rich",
)


@app.command()
def run(
    path: Annotated[
        str,
        typer.Argument(
            help="Path to the Python file or module:app (e.g., main.py or main:app)"
        ),
    ] = "main:app",
    *,
    host: Annotated[
        str,
        typer.Option(help="Host to bind the server to"),
    ] = "127.0.0.1",
    port: Annotated[
        int,
        typer.Option(help="Port to bind the server to"),
    ] = 8000,
    reload: Annotated[
        bool,
        typer.Option(help="Enable auto-reload on code changes"),
    ] = True,
) -> None:
    """Run an Air application in development mode."""
    # Handle both "main.py" and "main:app" formats
    if path.endswith(".py"):
        # Convert main.py -> main:app
        file_path = Path(path).resolve()
        module = file_path.stem
        app_path = f"{module}:app"
        # Add the file's directory to sys.path so uvicorn can import it
        sys.path.insert(0, str(file_path.parent))
    elif ":" not in path:
        # Assume it's a module name without :app
        app_path = f"{path}:app"
        # Add current directory to sys.path
        sys.path.insert(0, str(Path.cwd()))
    else:
        app_path = path
        # Add current directory to sys.path
        sys.path.insert(0, str(Path.cwd()))

    uvicorn.run(
        app_path,
        host=host,
        port=port,
        reload=reload,
    )


@app.command()
def version() -> None:
    """Show the Air version."""
    from importlib.metadata import version as get_version  # noqa: PLC0415

    typer.echo(f"Air {get_version('air')}")


def main() -> None:
    """Entry point for the Air CLI."""
    app()


if __name__ == "__main__":
    main()
