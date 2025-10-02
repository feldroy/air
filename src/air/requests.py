"""Tools for handling requests"""

from starlette.requests import Request as _Request


class Request(_Request):
    @property
    def htmx(self) -> bool:
        return self.headers.get("hx-request", "").lower() == "true"
