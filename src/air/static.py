"""Static assets with content-based cache busting.

Computes content hashes at startup and serves files with hashed filenames.
Example: styles.css -> styles.a1b2c3d4.css

Usage:
    import air
    from air.static import Static

    app = air.Air()
    jinja = air.JinjaRenderer(directory="templates")

    # One line. Auto-mounts, auto-registers template function.
    Static("static", app=app, jinja=jinja)

    # Or use enable() for zero-config:
    from air.static import enable
    enable(app, jinja)  # If static/ exists, just works

    # Templates just work:
    {{ static('styles.css') }}  ->  /static/styles.a1b2c3d4.css
"""

from __future__ import annotations

import hashlib
from pathlib import Path
from typing import TYPE_CHECKING

from starlette.responses import FileResponse, Response

if TYPE_CHECKING:
    from starlette.types import Receive, Scope, Send

    from .applications import Air
    from .templating import JinjaRenderer


def enable(
    app: Air,
    jinja: JinjaRenderer,
    directory: str = "static",
    prefix: str = "/static",
) -> Static | None:
    """Enable static assets if the directory exists. Zero config.

    Args:
        app: The Air application to mount the static file handler on.
        jinja: The JinjaRenderer to register the static() template function with.
        directory: The directory containing static files. Defaults to "static".
        prefix: The URL prefix for static files. Defaults to "/static".

    Returns:
        The Static instance if the directory exists, None otherwise.

    Example:
        import air
        from air.static import enable

        app = air.Air()
        jinja = air.JinjaRenderer(directory="templates")
        enable(app, jinja)  # That's it. Discovers static/ automatically.
    """
    path = Path(directory)
    if not path.exists():
        return None

    return Static(directory, app=app, jinja=jinja, prefix=prefix)


class Static:
    """Static file server with content-based filename hashing.

    Computes SHA256 hashes of file contents at startup and serves files with
    hashed filenames for efficient browser caching with immutable cache headers.

    Args:
        directory: The directory containing static files.
        app: Optional Air application to auto-mount the static file handler.
        jinja: Optional JinjaRenderer to auto-register the static() template function.
        prefix: The URL prefix for static files. Defaults to "/static".
        hash_length: Number of hash characters to use. Defaults to 8.

    Example:
        app = air.Air()
        jinja = air.JinjaRenderer(directory="templates")

        # One line. Auto-mounts, auto-registers template function.
        Static("static", app=app, jinja=jinja)

        # Templates just work:
        {{ static('styles.css') }}  ->  /static/styles.a1b2c3d4.css
    """

    def __init__(
        self,
        directory: str,
        *,
        app: Air | None = None,
        jinja: JinjaRenderer | None = None,
        prefix: str = "/static",
        hash_length: int = 8,
    ) -> None:
        self.directory = Path(directory).resolve()
        self.prefix = prefix.rstrip("/")
        self.hash_length = hash_length

        # original path -> hashed path
        self.file_map: dict[str, str] = {}
        # hashed path -> original path
        self._reverse: dict[str, str] = {}

        self._hash_files()

        # Auto-wire if app/jinja provided
        if app is not None:
            app.mount(prefix, self, name="static")

        if jinja is not None:
            # Air's JinjaRenderer wraps Starlette's Jinja2Templates
            jinja.templates.env.globals["static"] = self.url

    def _hash_files(self) -> None:
        """Walk directory and compute hashes for all files."""
        if not self.directory.exists():
            return

        for file_path in self.directory.rglob("*"):
            if not file_path.is_file():
                continue

            relative = file_path.relative_to(self.directory).as_posix()
            content = file_path.read_bytes()
            hash_val = hashlib.sha256(content).hexdigest()[: self.hash_length]

            # Insert hash before extension: style.css -> style.a1b2c3d4.css
            p = Path(relative)
            if p.parent != Path():
                hashed = (p.parent / f"{p.stem}.{hash_val}{p.suffix}").as_posix()
            else:
                hashed = f"{p.stem}.{hash_val}{p.suffix}"

            self.file_map[relative] = hashed
            self._reverse[hashed] = relative

    def url(self, path: str) -> str:
        """Get the hashed URL for a static file.

        Args:
            path: The original file path (e.g., "styles.css" or "images/logo.png").

        Returns:
            The URL with the hashed filename (e.g., "/static/styles.a1b2c3d4.css").
        """
        path = path.lstrip("/")
        hashed = self.file_map.get(path, path)
        return f"{self.prefix}/{hashed}"

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        """ASGI app that serves static files."""
        if scope["type"] != "http":
            return

        path = scope["path"]
        if not path.startswith(self.prefix + "/"):
            await Response("Not Found", status_code=404)(scope, receive, send)
            return

        relative_path = path[len(self.prefix) + 1 :]

        # Check if this is a hashed filename
        original_path = self._reverse.get(relative_path)

        if original_path:
            # Hashed URL -> serve with immutable caching
            file_path = self.directory / original_path
            if file_path.exists():
                response = FileResponse(
                    file_path,
                    headers={"Cache-Control": "public, max-age=31536000, immutable"},
                )
                await response(scope, receive, send)
                return

        # Direct file request (unhashed) -> serve without aggressive caching
        file_path = self.directory / relative_path
        if file_path.exists() and file_path.is_file():
            await FileResponse(file_path)(scope, receive, send)
            return

        await Response("Not Found", status_code=404)(scope, receive, send)
