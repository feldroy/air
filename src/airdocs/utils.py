from pathlib import Path

import air
from markdown import markdown


def make_link_from_mdpath(path: Path):
    return air.A(path.name[:-3], href=str(path)[6:-3])


def get_readme_content(path: Path):
    if path.exists():
        return path.read_text()
    return "README content not found."


def get_readme_as_html(path: Path):
    readme_content = get_readme_content(path)
    return markdown(readme_content)
