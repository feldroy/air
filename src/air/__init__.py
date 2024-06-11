from air.generator import StaticSiteGenerator
from air.plugins.markdown_plugin import MarkdownPlugin


def main() -> int:
    print("Hello from air!")
    generator = StaticSiteGenerator("source", "output")
    generator.register_plugin(MarkdownPlugin)
    generator.build()
    return 0
