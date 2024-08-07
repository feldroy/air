from air.generator import StaticSiteGenerator
from air.plugins.markdown_plugin import MarkdownPlugin
from air.plugins.fasthtml_plugin import FastHTMLPlugin


def main() -> int:
    print("Building site...")
    generator = StaticSiteGenerator("input", "public")
    generator.register_plugin(MarkdownPlugin)
    generator.register_plugin(FastHTMLPlugin)
    generator.build()
    print("Site built from input/ to public/")
    return 0
