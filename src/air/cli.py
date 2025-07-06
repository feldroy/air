from pathlib import Path

import typer
from typing_extensions import Annotated

from air.generator import StaticSiteGenerator
from air.plugins.markdown_plugin import MarkdownPlugin

app = typer.Typer()


@app.command()
def html(
    source_dir: Annotated[Path, typer.Argument()] = Path("input"),
    output_dir: Annotated[Path, typer.Argument()] = Path("public"),
) -> int:
    """Build a static site from source files."""
    print("Building site...")
    generator = StaticSiteGenerator(source_dir, output_dir)
    generator.register_plugin(MarkdownPlugin)
    generator.build()
    print(f"Site built from {source_dir}/ to {output_dir}/")
    return 0
