"""Tools for handling requests"""

import json
from typing import Any
from urllib.parse import urlsplit, urlunsplit

from starlette.requests import Request as _Request


class HtmxDetails:
    def __init__(self, request: _Request) -> None:
        self.request = request
        self.headers = request.headers

    def __bool__(self) -> bool:
        return self.is_htmx

    def __str__(self) -> str:
        return str(self.is_htmx)

    @property
    def is_htmx(self):
        return self.headers.get("HX-Request") == "true"

    @property
    def boosted(self) -> bool:
        return self.headers.get("HX-Boosted") == "true"

    @property
    def current_url(self) -> str | None:
        return self.headers.get("HX-Current-URL")

    @property
    def current_url_abs_path(self) -> str | None:
        url = self.current_url
        if url is not None:
            split = urlsplit(url)
            if split.scheme == self.request.scheme and split.netloc == self.request.get_host():
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
