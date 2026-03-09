"""Static assets with content-based cache busting.

Computes content hashes at startup and serves files with hashed filenames.
Example: styles.css -> styles.a1b2c3d4.css

Zero-config: Air auto-detects ``static/`` and rewrites URLs in HTML responses.

    # Just write normal paths in templates or Air tags:
    <link href="/static/styles.css">
    air.Link(href="/static/styles.css")

    # Air automatically rewrites to:
    <link href="/static/styles.a1b2c3d4.css">
"""

from __future__ import annotations

import hashlib
import re
from pathlib import Path
from typing import TYPE_CHECKING, Any

from starlette.responses import FileResponse, Response

if TYPE_CHECKING:
    from starlette.types import ASGIApp, Receive, Scope, Send

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


class StaticRewriteMiddleware:
    """ASGI middleware that rewrites static file paths in HTML responses.

    Automatically transforms ``/static/styles.css`` to ``/static/styles.a1b2c3d4.css``
    in HTML responses. Works with Jinja templates, Air tags, and hardcoded HTML.
    """

    def __init__(self, app: ASGIApp, *, static: Static) -> None:
        self.app = app
        self.static = static
        escaped = re.escape(static.prefix)
        self._pattern = re.compile(escaped + r"/([^\"'>\s)#?]+)")

    def _replace(self, match: re.Match[str]) -> str:
        path = match.group(1)
        if path in self.static.file_map:
            return f"{self.static.prefix}/{self.static.file_map[path]}"
        return match.group(0)

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        response_start: dict[str, Any] | None = None
        body_parts: list[bytes] = []
        is_html = False

        async def send_wrapper(message: dict[str, Any]) -> None:
            nonlocal response_start, is_html

            if message["type"] == "http.response.start":
                response_start = message
                headers = dict(message.get("headers", []))
                content_type = headers.get(b"content-type", b"").decode("latin-1")
                is_html = "text/html" in content_type
                if not is_html:
                    await send(message)
                return

            if message["type"] == "http.response.body":
                if not is_html:
                    await send(message)
                    return

                body = message.get("body", b"")
                more_body = message.get("more_body", False)
                body_parts.append(body)

                if not more_body:
                    full_body = b"".join(body_parts)
                    try:
                        text = full_body.decode("utf-8")
                        text = self._pattern.sub(self._replace, text)
                        full_body = text.encode("utf-8")
                    except UnicodeDecodeError:
                        pass

                    assert response_start is not None
                    new_headers = [
                        (k, str(len(full_body)).encode("latin-1")) if k == b"content-length" else (k, v)
                        for k, v in response_start.get("headers", [])
                    ]
                    response_start["headers"] = new_headers
                    await send(response_start)
                    await send({"type": "http.response.body", "body": full_body})
                return

        await self.app(scope, receive, send_wrapper)
