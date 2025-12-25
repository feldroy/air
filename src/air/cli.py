"""Air CLI - Command-line interface for running Air applications."""

from __future__ import annotations

from typing import Annotated

import typer

app = typer.Typer(
    name="air",
    help="Air CLI - Run Air applications",
    add_completion=False,
    no_args_is_help=True,
    rich_markup_mode="rich",
)


def _check_uvicorn() -> None:
    """Check if uvicorn is available and provide helpful error if not."""
    try:
        import uvicorn  # noqa: F401
    except ImportError:
        typer.echo(
            'To use the "air run" command, please install "air[standard]":\n\n'
            '    pip install "air[standard]"\n\n'
            "or:\n\n"
            '    uv add "air[standard]"'
        )
        raise typer.Exit(code=1)


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
    """Run an Air application in development mode.

    Examples:

        air run

        air run main.py

        air run main:app --port 8080

        air run myapp.py --host 0.0.0.0 --port 5000

    """
    _check_uvicorn()
    import uvicorn

    # Handle both "main.py" and "main:app" formats
    if path.endswith(".py"):
        # Convert main.py -> main:app
        module = path[:-3].replace("/", ".").replace("\\", ".")
        app_path = f"{module}:app"
    elif ":" not in path:
        # Assume it's a module name without :app
        app_path = f"{path}:app"
    else:
        app_path = path

    uvicorn.run(
        app_path,
        host=host,
        port=port,
        reload=reload,
    )


def main() -> None:
    """Entry point for the Air CLI."""
    app()


if __name__ == "__main__":
    main()
