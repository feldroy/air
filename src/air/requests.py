"""Tools for handling requests"""

from starlette.requests import Request as _Request


class Request(_Request):
    """Requests are what views process."""