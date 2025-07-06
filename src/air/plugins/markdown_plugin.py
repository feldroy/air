import markdown

from air.generator import Plugin


class MarkdownPlugin(Plugin):
    def run(self) -> None:
        print("Running MarkdownPlugin...")
        print(f"Source dir: {self.generator.source_dir}")
        for path in self.generator.source_dir.rglob("*.md"):
            print(f"Converting {path} to HTML...")
            relative_path = path.relative_to(self.generator.source_dir)
            output_path = self.generator.output_dir / relative_path.with_suffix(".html")
            output_path.parent.mkdir(parents=True, exist_ok=True)

            with open(path, "r", encoding="utf-8") as f:
                content = f.read()

            html = markdown.markdown(content)

            with open(output_path, "w", encoding="utf-8") as f:
                f.write(html)
