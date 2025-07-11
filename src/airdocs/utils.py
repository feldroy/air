from markdown import markdown
from pathlib import Path
import air


def get_readme_content():
    readme_path = Path(air.__path__[0]).parent.parent / "README.md"
    if readme_path.exists():
        return readme_path.read_text()
    return "README content not found."

def get_readme_as_html():
    readme_content = get_readme_content()
    return markdown(readme_content)
