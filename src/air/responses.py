"""Air uses custom response classes to improve the developer experience."""

import importlib
from typing import Any

from fastapi import Response
from starlette.responses import (
    FileResponse as FileResponse,  # noqa
    HTMLResponse as HTMLResponse,  # noqa
    JSONResponse as JSONResponse,  # noqa
    PlainTextResponse as PlainTextResponse,  # noqa
    RedirectResponse as RedirectResponse,  # noqa
    StreamingResponse as StreamingResponse,  # noqa
)
from starlette.types import Send

from .tags import Tag


def dict_to_airtag(d):
    children_raw = d.get("_children", ())
    children = tuple(dict_to_airtag(c) if isinstance(c, dict) else c for c in children_raw)
    module = importlib.import_module(d["_module"])
    obj = getattr(module, d["_name"])
    return obj(*children, **d.get("_attrs", {}))


class AirResponse(Response):
    """Response class to handle air.tags.Tags or HTML (from Jinja2)."""

    media_type = "text/html; charset=utf-8"

    def render(self, content: Any) -> bytes:
        """Render Tag elements to bytes of HTML."""
        if isinstance(content, str):
            return content.encode("utf-8")
        if isinstance(content, dict):
            content = dict_to_airtag(content)
        return content.render().encode("utf-8")


class TagResponse(Response):
    """Response class to handle air.tags.Tags."""

    media_type = "text/html; charset=utf-8"

    def render(self, content: Any) -> bytes:
        """Render Tag elements to bytes of HTML."""
        if isinstance(content, dict):
            content = dict_to_airtag(content)
        return content.render().encode("utf-8")


class SSEResponse(StreamingResponse):
    """Response class for Server Sent Events

    Example:

        # For tags
        import random
        from asyncio import sleep

        import air

        app = air.Air()


        @app.page
        def index():
            return air.layouts.mvpcss(
                air.Script(src="https://unpkg.com/htmx-ext-sse@2.2.1/sse.js"),
                air.Title("Server Sent Event Demo"),
                air.H1("Server Sent Event Demo"),
                air.P("Lottery number generator"),
                air.Section(
                    hx_ext="sse",
                    sse_connect="/lottery-numbers",
                    hx_swap="beforeend show:bottom",
                    sse_swap="message",
                ),
            )

        async def lottery_generator():
            while True:
                lottery_numbers = ", ".join([str(random.randint(1, 40)) for x in range(6)])
                # Tags work seamlessly
                yield air.Aside(lottery_numbers)
                # As do strings. Non-strings are cast to strings via the str built-in
                yield "Hello, world"
                await sleep(1)


        @app.get("/lottery-numbers")
        async def get():
            return air.SSEResponse(lottery_generator())
    """

    media_type = "text/event-stream"

    async def stream_response(self, send: Send) -> None:
        await send({
            "type": "http.response.start",
            "status": self.status_code,
            "headers": self.raw_headers,
        })
        async for chunk in self.body_iterator:
            if not isinstance(chunk, (bytes, memoryview)):
                if isinstance(chunk, Tag) or hasattr(chunk, "render"):
                    # If a tag or has a "render" method, call that and create lines
                    lines = [t for t in chunk.render().splitlines()]
                else:
                    # Anything else, cast to str and run splitlines
                    lines = [t for t in str(chunk).splitlines()]
                formatted = [f"data: {t}" for t in lines]
                data = "\n".join(formatted)
                chunk = f"event: message\n{data}\n\n"
                chunk = chunk.encode(self.charset)
            await send({"type": "http.response.body", "body": chunk, "more_body": True})

        await send({"type": "http.response.body", "body": b"", "more_body": False})
