"""Tools for handling requests."""

import json
from dataclasses import dataclass, field
from typing import Any, Final
from urllib.parse import urlsplit, urlunsplit

from starlette.datastructures import Headers as Headers
from starlette.requests import Request as _Request

# HTMX Header names as constants
HX_REQUEST: Final = "HX-Request"
HX_BOOSTED: Final = "HX-Boosted"
HX_CURRENT_URL: Final = "HX-Current-URL"
HX_HISTORY_RESTORE_REQUEST: Final = "HX-History-Restore-Request"
HX_PROMPT: Final = "HX-Prompt"
HX_TARGET: Final = "HX-Target"
HX_TRIGGER: Final = "HX-Trigger"
HX_TRIGGER_NAME: Final = "HX-Trigger-Name"

# Some servers send either of these for the triggering event payload
TRIGGERING_EVENT_ALIASES: Final[tuple[str, ...]] = ("Triggering-Event", "HX-Triggering-Event")


@dataclass(slots=True)
class HtmxDetails:
    """
    Attached to every Request served by Air; provides helpers for HTMX-aware handling.
    Derived values are computed once in `__post_init__`.
    """

    # fields
    headers: Headers
    url: str

    # Derived fields (formerly properties)
    is_hx_request: bool = field(init=False)
    boosted: bool = field(init=False)
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
    current_url: str | None = field(init=False)
    """The current URL in the browser that htmx made this request from, or `None` for non-htmx requests. Based on the `HX-Current-URL` header."""
    current_url_abs_path: str | None = field(init=False)
    """The absolute-path form of `current_url`, that is the URL without scheme or netloc, or None for non-htmx requests.

    This value will also be `None` if the scheme and netloc do not match the request. This could happen if the request is cross-origin, or if Air is not configured correctly.
    """
    history_restore_request: bool = field(init=False)
    """`True` if the request is for history restoration after a miss in the local history cache. Detected by checking if the `HX-History-Restore-Request` header equals `true`."""
    prompt: str | None = field(init=False)
    """The user response to `hx-prompt` if it was used, or `None`."""
    target: str | None = field(init=False)
    """The `id` of the target element if it exists, or `None`. Based on the `HX-Target` header."""
    trigger: str | None = field(init=False)
    """The `id` of the triggered element if it exists, or `None`. Based on the `HX-Trigger` header."""
    trigger_name: str | None = field(init=False)
    """The name of the triggered element if it exists, or `None`. Based on the `HX-Trigger-Name` header."""

    # TODO this requires an HTMX extension, evaluate if it makes sense to use it
    triggering_event: Any = field(init=False)

    def __post_init__(self) -> None:
        self.is_hx_request = self.headers.get(HX_REQUEST) == "true"
        self.boosted = self.headers.get(HX_BOOSTED) == "true"

        # Multi-line logic moved to helpers:
        self.current_url = self._get_current_url()
        self.current_url_abs_path = self._compute_current_url_abs_path(self.current_url)
        self.triggering_event = self._parse_triggering_event(self.headers)

        # Single-line field sets (stay inline):
        self.history_restore_request = self.headers.get(HX_HISTORY_RESTORE_REQUEST) == "true"
        self.prompt = self.headers.get(HX_PROMPT)
        self.target = self.headers.get(HX_TARGET)
        self.trigger = self.headers.get(HX_TRIGGER)
        self.trigger_name = self.headers.get(HX_TRIGGER_NAME)

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

    # ----------------- Private helpers -----------------

    def _get_current_url(self) -> str | None:
        return self.headers.get(HX_CURRENT_URL)

    def _compute_current_url_abs_path(self, url: str | None) -> str | None:
        if url is None:
            return None
        split = urlsplit(url)
        if split.scheme == self.url.scheme and split.netloc == self.url.netloc:
            return urlunsplit(split._replace(scheme="", netloc=""))
        return None

    def _parse_triggering_event(self, headers: Headers) -> Any:
        for name in TRIGGERING_EVENT_ALIASES:
            raw = headers.get(name)
            if raw is not None:
                try:
                    return json.loads(raw)
                except json.JSONDecodeError:
                    return None
        return None


class AirRequest(_Request):
    """A wrapper around `starlette.requests.Request` that includes the `HtmxDetails` object.

    !!! note

        AirRequest is available in Air 0.36.0+
    """

    @property
    def htmx(self) -> HtmxDetails:
        return HtmxDetails(headers=self.headers, url=self.url)


Request = AirRequest
