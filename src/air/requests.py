"""Tools for handling requests"""

from starlette.requests import Request as _Request


class Request(_Request):
    @property
    def htmx(self):
        return self.headers["hx_request"] is not None and self.headers["hx_request"].lower() == "true"
