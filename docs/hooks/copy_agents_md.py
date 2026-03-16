"""MkDocs hook: copy AGENTS.md to the site root so it's served as raw markdown."""

import shutil
from pathlib import Path


def on_post_build(config, **kwargs):
    src = Path(config["docs_dir"]).parent / "AGENTS.md"
    dst = Path(config["site_dir"]) / "AGENTS.md"
    if src.exists():
        shutil.copy2(src, dst)
