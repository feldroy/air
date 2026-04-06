"""Air CLI - Command-line interface for running Air applications."""

from __future__ import annotations

import importlib
import sys
from pathlib import Path
from typing import TYPE_CHECKING, Annotated

if TYPE_CHECKING:
    from air.checks import CheckMessage, CheckResult

import typer
import uvicorn
from rich.console import Console

import air

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
        typer.echo(f"Air {air.__version__}\nCrafted with care by Two Scoops authors pydanny and audreyfeldroy")
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


def _resolve_app_path(path: str) -> str:
    """Convert a user-supplied path to a ``module:attr`` import string.

    Handles ``main.py``, ``main``, and ``main:app`` formats.
    Adds the appropriate directory to ``sys.path`` so the module is importable.
    """
    if path.endswith(".py"):
        file_path = Path(path).resolve()
        module = file_path.stem
        app_path = f"{module}:app"
        sys.path.insert(0, str(file_path.parent))
    elif ":" not in path:
        app_path = f"{path}:app"
        sys.path.insert(0, str(Path.cwd()))
    else:
        app_path = path
        sys.path.insert(0, str(Path.cwd()))
    return app_path


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
    app_path = _resolve_app_path(path)

    # Print startup banner
    url = f"http://{host}:{port}"
    console.print()
    console.print(f"  [bold cyan]Air[/bold cyan] v{air.__version__}")
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


def _import_app(path: str) -> air.Air:
    """Import and return the Air application object from *path*.

    Raises:
        TypeError: If the imported object is not an Air instance.
    """
    app_path = _resolve_app_path(path)
    module_name, _, attr_name = app_path.partition(":")
    module = importlib.import_module(module_name)
    obj = getattr(module, attr_name)
    if not isinstance(obj, air.Air):
        msg = f"{app_path} is {type(obj).__name__}, not an Air application"
        raise TypeError(msg)
    return obj


@app.command()
def check(
    path: Annotated[
        str,
        typer.Argument(help="Path to the Python file or module:app (e.g., main.py or main:app)"),
    ] = "main:app",
) -> None:
    """Check an Air application for common issues."""  # noqa: DOC501
    from air.checks import run_checks  # noqa: PLC0415

    console.print()
    console.print(f"  [bold cyan]Air[/bold cyan] v{air.__version__}")
    console.print()

    try:
        air_app = _import_app(path)
    except Exception as exc:  # noqa: BLE001
        console.print(f"  [red]Could not import app:[/red] {exc}")
        raise typer.Exit(code=1) from None

    result = run_checks(air_app)
    _print_check_result(result)
    raise typer.Exit(code=0 if result.ok else 1)


def _print_check_result(result: CheckResult) -> None:
    """Pretty-print check results to the console."""

    if result.ok and not result.warnings:
        console.print(f"  [green]All checks passed[/green] ({result.route_count} routes)")
        console.print()
        return

    # Group messages by category
    by_category: dict[str, list[CheckMessage]] = {}
    for msg in result.messages:
        by_category.setdefault(msg.category, []).append(msg)

    for category, msgs in by_category.items():
        console.print(f"  [bold]{category.title()}[/bold]")
        for msg in msgs:
            color = "red" if msg.level == "error" else "yellow"
            console.print(f"    [{color}]{msg.subject}[/{color}]  {msg.message}")
        console.print()

    error_count = len(result.errors)
    warning_count = len(result.warnings)
    parts = []
    if error_count:
        parts.append(f"[red]{error_count} error{'s' if error_count != 1 else ''}[/red]")
    if warning_count:
        parts.append(f"[yellow]{warning_count} warning{'s' if warning_count != 1 else ''}[/yellow]")
    console.print(f"  {', '.join(parts)}")
    console.print()


def main() -> None:
    """Entry point for the Air CLI."""
    app()


if __name__ == "__main__":
    main()
