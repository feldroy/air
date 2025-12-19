"""Air uses custom response classes to improve the developer experience."""

from collections.abc import Mapping
from typing import override

from fastapi import status
from starlette.background import BackgroundTask
from starlette.datastructures import URL
from starlette.responses import (
    FileResponse as FileResponse,
    HTMLResponse as HTMLResponse,
    JSONResponse as JSONResponse,
    PlainTextResponse as PlainTextResponse,
    RedirectResponse as StarletteRedirectResponse,
    Response as Response,
    StreamingResponse as StreamingResponse,
)
from starlette.types import Send

from .tags import BaseTag


class AirResponse(HTMLResponse):
    """Response class to handle air.tags.Tags or HTML (from Jinja2)."""

    @override
    def render(self, tag: BaseTag | str) -> bytes | memoryview:  # ty: ignore[invalid-method-override]
        """Render Tag elements to bytes of HTML.

        Returns:
            Rendered HTML as bytes or memoryview.
        """
        return super().render(str(tag))


TagResponse = AirResponse
"""Alias for the `AirResponse` Response class; use it if it improves clarity."""


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
                lottery_numbers = ", ".join(
                    [str(random.randint(1, 40)) for x in range(6)]
                )
                # Tags work seamlessly
                yield air.Aside(lottery_numbers)
                # As do strings. Non-strings are cast to strings via the
                # str built-in
                yield "Hello, world"
                await sleep(1)


        @app.get("/lottery-numbers")
        async def get():
            return air.SSEResponse(lottery_generator())
    """

    media_type = "text/event-stream"

    async def stream_response(self, send: Send) -> None:
        await send(
            {
                "type": "http.response.start",
                "status": self.status_code,
                "headers": self.raw_headers,
            },
        )
        async for chunk in self.body_iterator:
            if not isinstance(chunk, bytes | memoryview):
                lines = list(str(chunk).splitlines())
                formatted = [f"data: {t}" for t in lines]
                data = "\n".join(formatted)
                chunk = f"event: message\n{data}\n\n"
                chunk = chunk.encode(self.charset)
            await send({"type": "http.response.body", "body": chunk, "more_body": True})

        await send({"type": "http.response.body", "body": b"", "more_body": False})


class RedirectResponse(StarletteRedirectResponse):
    """Response class for HTTP redirects.

    Use `air.RedirectResponse` to redirect users to a different URL.

    Example:
        ```python
        import air

        app = air.Air()


        @app.get("/old-page")
        def old_page():
            # Permanent redirect (301) - browsers cache this
            return air.RedirectResponse(url="/new-page", status_code=301)


        @app.page
        def legacy():
            # Using @app.page works too - redirects from /legacy
            return air.RedirectResponse(url="/", status_code=301)
        ```

    Args:
        url: The target URL to redirect to.
        status_code: HTTP status code for the redirect. Defaults to 307 (Temporary Redirect).
            Common values:
            - 301: Permanent redirect (SEO-friendly, browsers cache)
            - 302: Temporary redirect (traditional)
            - 307: Temporary redirect (preserves HTTP method, default)
            - 303: See Other (use after POST to redirect to GET)
        headers: Optional additional headers to include in the response.
        background: Optional background task to run after the response is sent.
    """

    def __init__(
        self,
        url: str | URL,
        status_code: int = status.HTTP_307_TEMPORARY_REDIRECT,
        headers: Mapping[str, str] | None = None,
        background: BackgroundTask | None = None,
    ) -> None:
        super().__init__(url=url, status_code=status_code, headers=headers, background=background)
