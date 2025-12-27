"""Air CLI - Command-line interface for running Air applications."""

import sys
from importlib.metadata import version
from pathlib import Path
from typing import Annotated

import typer
import uvicorn
from rich.console import Console

app = typer.Typer(add_completion=False, rich_markup_mode="rich")
console = Console()

# Suppress uvicorn's startup noise, keep request logs
LOG_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "%(message)s",
        },
    },
    "handlers": {
        "default": {
            "class": "logging.StreamHandler",
            "formatter": "default",
            "stream": "ext://sys.stderr",
        },
    },
    "loggers": {
        "uvicorn.error": {"level": "WARNING", "handlers": ["default"]},
        "uvicorn.access": {"level": "INFO", "handlers": ["default"], "propagate": False},
    },
}


def _version_callback(value: bool) -> None:  # noqa: FBT001 - Typer callback signature
    if value:
        typer.echo(f"Air {version('air')}\nCrafted with care by Two Scoops authors pydanny and audreyfeldroy")
        raise typer.Exit


@app.callback(invoke_without_command=True)
def _callback(
    ctx: typer.Context,
    _: Annotated[
        bool | None,
        typer.Option("--version", "-v", help="Show version and exit.", callback=_version_callback),
    ] = None,
) -> None:
    """Air: Designed to give developers everywhere clarity and joy."""
    if ctx.invoked_subcommand is None:
        typer.echo(ctx.get_help())


@app.command()
def run(
    path: Annotated[
        str,
        typer.Argument(help="Path to the Python file or module:app (e.g., main.py or main:app)"),
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

    # Print startup banner
    url = f"http://{host}:{port}"
    console.print()
    console.print(f"  [bold cyan]Air[/bold cyan] v{version('air')}")
    console.print()
    console.print(f"  [dim]➜[/dim]  [bold]App:[/bold]     {app_path}")
    console.print(f"  [dim]➜[/dim]  [bold]Server:[/bold]  [link={url}]{url}[/link]")
    console.print()

    uvicorn.run(
        app_path,
        host=host,
        port=port,
        reload=reload,
        log_config=LOG_CONFIG,
    )


def main() -> None:
    """Entry point for the Air CLI."""
    app()


if __name__ == "__main__":
    main()
