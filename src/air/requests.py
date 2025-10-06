"""Tools for handling requests."""

import json
from typing import Any
from urllib.parse import urlsplit, urlunsplit

from starlette.requests import Request as _Request


class HtmxDetails:
    """This class is attached to every Request served by Air, and provides tooling for using HTMX."""

    def __init__(self, request: _Request) -> None:
        self.request = request
        self.headers = request.headers

    def __bool__(self) -> bool:
        """`True` if the request was made with htmx, otherwise `False`. Detected by checking if the `HX-Request` header equals `true`.

        This method allows you to change content for requests made with htmx:

        Example:

            import air
            from random import randint

            app = air.Air()


            @app.page
            def index(request: air.Request):

                if request.htmx:
                    return air.H1(
                        "Click me: ", randint(1, 100),
                        id="number",
                        hx_get="/",
                        hx_swap="outerHTML"
                    )
                return air.layouts.mvpcss(
                    air.H1(
                        "Click me: ", randint(1, 100),
                        id="number",
                        hx_get="/",
                        hx_swap="outerHTML"
                    )
                )
        """

        return self.headers.get("HX-Request") == "true"

    def __str__(self) -> str:
        return str(self.__bool__())

    @property
    def boosted(self) -> bool:
        """`True` if the request came from an element with the `hx-boost` attribute. Detected by checking if the `HX-Boosted` header equals `true`.

        Example:

            import air
            from random import randint

            app = air.Air()


            @app.page
            def index(request: air.Request):

                if request.htmx.boosted:
                    # Do something here
        """
        return self.headers.get("HX-Boosted") == "true"

    @property
    def current_url(self) -> str | None:
        return self.headers.get("HX-Current-URL")

    @property
    def current_url_abs_path(self) -> str | None:
        url = self.current_url
        if url is not None:
            split = urlsplit(url)
            if split.scheme == self.request.url.scheme and split.netloc == self.request.url.netloc:
                url = urlunsplit(split._replace(scheme="", netloc=""))
            else:
                url = None
        return url

    @property
    def history_restore_request(self) -> bool:
        return self.headers.get("HX-History-Restore-Request") == "true"

    @property
    def prompt(self) -> str | None:
        return self.headers.get("HX-Prompt")

    @property
    def target(self) -> str | None:
        return self.headers.get("HX-Target")

    @property
    def trigger(self) -> str | None:
        return self.headers.get("HX-Trigger")

    @property
    def trigger_name(self) -> str | None:
        return self.headers.get("HX-Trigger-Name")

    @property
    def triggering_event(self) -> Any:
        value = self.headers.get("Triggering-Event")
        if value is not None:
            try:
                value = json.loads(value)
            except json.JSONDecodeError:
                value = None
        return value


class Request(_Request):
    @property
    def htmx(self) -> HtmxDetails:
        return HtmxDetails(self)
