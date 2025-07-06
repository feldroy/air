import re
import shutil
from pathlib import Path
from typing import List

from jinja2 import Environment, FileSystemLoader, select_autoescape


class Plugin:
    """Base class for static site generator plugins"""

    def __init__(self, generator) -> None:
        """Initialize plugin with generator instance"""
        self.generator = generator

    def run(self) -> None:
        """Execute plugin functionality"""
        pass


class StaticSiteGenerator:
    """Generates static sites from HTML templates"""

    def __init__(self, source_dir: Path, output_dir: Path) -> None:
        """Initialize generator with source and output directories"""
        self.source_dir = source_dir
        self.output_dir = output_dir
        self.env = Environment(
            loader=FileSystemLoader(str(self.source_dir)),
            autoescape=select_autoescape(["html"]),
        )
        self.plugins: List[Plugin] = []

    def register_plugin(self, plugin: type) -> None:
        """Register a plugin class with the generator"""
        plugin_instance = plugin(self)
        self.plugins.append(plugin_instance)

    def build(self) -> None:
        """Build the static site by rendering templates"""
        if self.output_dir.exists():
            shutil.rmtree(self.output_dir)
        self.output_dir.mkdir(parents=True)

        base_pattern = re.compile(r"^base.*\.html$")

        for path in self.source_dir.rglob("*.html"):
            relative_path = path.relative_to(self.source_dir)
            output_path = self.output_dir / relative_path

            # Skip rendering templates that start with "base"
            if base_pattern.match(path.name):
                continue

            output_path.parent.mkdir(parents=True, exist_ok=True)

            with open(output_path, "w", encoding="utf-8") as f:
                template = self.env.get_template(str(relative_path))
                f.write(template.render())

        for plugin in self.plugins:
            plugin.run()
