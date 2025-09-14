from collections.abc import Callable
from typing import Final

from starlette.requests import Request

from .layouts import mvpcss
from .responses import AirResponse
from .tags import H1, P, Title


def default_404_exception_handler(request: Request, exc: Exception) -> AirResponse:
    """Default 404 exception handler. Can be overloaded."""
    return AirResponse(
        mvpcss(
            Title("404 Not Found"),
            H1("404 Not Found"),
            P("The requested resource was not found on this server."),
            P(f"URL: {request.url}"),
        ),
        status_code=404,
    )


def default_500_exception_handler(request: Request, exc: Exception) -> AirResponse:
    """Default 500 exception handler. Can be overloaded."""
    return AirResponse(
        mvpcss(
            Title("500 Internal Server Error"),
            H1("500 Internal Server Error"),
            P("An internal server error occurred."),
        ),
        status_code=500,
    )


DEFAULT_EXCEPTION_HANDLERS: Final[dict[int, Callable[[Request, Exception], AirResponse]]] = {
    404: default_404_exception_handler,
    500: default_500_exception_handler,
}
