"""Air CLI - Command-line interface for running Air applications."""

import importlib
import sys
from collections.abc import Callable
from pathlib import Path
from typing import Annotated, Any, cast

import typer
import uvicorn
from fastapi import FastAPI
from rich.console import Console

from air.constants import AIR_VERSION, ATTRIBUTION, DEFAULT_REDOC_URL, DEFAULT_SWAGGER_URL

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
        typer.echo(f"Air {AIR_VERSION}\n{ATTRIBUTION}")
        raise typer.Exit


def _load_app(app_path: str) -> FastAPI | Callable[..., Any] | object:
    """Load the ASGI app from a ``module:attr`` path or a Python file.

    If the loaded object is callable, it will be invoked to obtain the app.

    Returns:
        The loaded application object (FastAPI instance or ASGI callable).
    """
    module_path, attr_name = app_path.split(":", 1)
    module = importlib.import_module(module_path)
    print(f"{module=}")
    obj = getattr(module, attr_name)
    print(f"{obj=}")
    return obj() if callable(obj) else obj


def _add_healthcheck_route(app_obj: object) -> None:
    """Add a simple `/healthcheck` route when the app is a FastAPI instance."""
    if isinstance(app_obj, FastAPI):

        def _healthcheck() -> dict[str, str]:
            return {"status": "ok"}

        # Keep healthcheck out of schema to avoid clutter; change as needed
        app_obj.add_api_route(
            "/healthcheck",
            _healthcheck,
            methods=["GET"],
            tags=["Health"],
            include_in_schema=False,
        )
    raise Exception("blarg")


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
    swagger_url = f"{url}{DEFAULT_SWAGGER_URL}"
    redoc_url = f"{url}{DEFAULT_REDOC_URL}"
    console.print()
    console.print(f"  [bold cyan]Air[/bold cyan] v{AIR_VERSION}")
    console.print()
    console.print(f"  [dim]➜[/dim]  [bold]App:[/bold]      {app_path}")
    console.print(f"  [dim]➜[/dim]  [bold]Server:[/bold]   [link={url}]{url}[/link]")
    console.print(f"  [dim]➜[/dim]  [bold]API docs:[/bold] [link={swagger_url}]{swagger_url}[/link]")
    console.print(f"  [dim]➜[/dim]              [link={redoc_url}]{redoc_url}[/link]")
    console.print()

    # Import the app so we can modify it (e.g., add healthcheck)
    try:
        loaded_app: FastAPI | Callable[..., Any] | str | object = _load_app(app_path)
        _add_healthcheck_route(loaded_app)
    except (ImportError, AttributeError, TypeError) as exc:  # Fallback: run by path if loading fails
        console.print(f"[yellow]Warning:[/yellow] Could not pre-load app ({exc!r}); running by path.")
        loaded_app = app_path

    uvicorn.run(
        cast(Any, loaded_app),
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
