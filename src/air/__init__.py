from air.generator import StaticSiteGenerator
from air.plugins.markdown_plugin import MarkdownPlugin


def main() -> int:
    print("Building site...")
    generator = StaticSiteGenerator("templates", "output")
    generator.register_plugin(MarkdownPlugin)
    generator.build()
    print("Site built from templates/ to output/")
    return 0
