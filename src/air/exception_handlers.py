from collections.abc import Callable
from typing import Final

from starlette.requests import Request
from starlette.types import ASGIApp, Receive, Scope, Send

from .exceptions import HTTPException
from .layouts import mvpcss
from .responses import AirResponse
from .tags import H1, P, Title


def default_404_router_handler(router_name: str) -> ASGIApp:
    """Build an ASGI app that delegates the 404 to the default_404_exception_handler.

    Example:

        import air

        app = air.Air()
        router = air.AirRouter()


        @router.get("/example")
        def index():
            return air.AirResponse(air.P("I am an example route."), status_code=404)


        app.include_router(router)
    """

    async def app(scope: Scope, receive: Receive, send: Send) -> None:
        # Create a Request so router handler can render URL and other context.
        request: Request = Request(scope, receive=receive)

        # Use a concrete HTTPException (status 404). Your handler accepts Exception.
        exc: HTTPException = HTTPException(
            status_code=404,
            detail=f"Not Found in router '{router_name}'",
        )

        # Delegate to the project's default 404 renderer (AirResponse).
        response = default_404_exception_handler(request, exc)

        # AirResponse is a Starlette-compatible Response, so call it as ASGI.
        await response(scope, receive, send)

    return app


def default_404_exception_handler(request: Request, exc: Exception) -> AirResponse:
    """Default 404 exception handler. Can be overloaded.

    Example:

        import air

        app = air.Air()


        @app.get("/")
        def index():
            return air.AirResponse(air.P("404 Not Found"), status_code=404)
    """
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
    """Default 500 exception handler. Can be overloaded.

    Example:

        import air

        app = air.Air()


        @app.get("/")
        def index():
            return air.AirResponse(air.P("500 Internal Server Error"), status_code=500)
    """
    return AirResponse(
        mvpcss(
            Title("500 Internal Server Error"),
            H1("500 Internal Server Error"),
            P("An internal server error occurred."),
        ),
        status_code=500,
    )


type ExceptionHandlersType = dict[int, Callable[[Request, Exception], AirResponse]]
DEFAULT_EXCEPTION_HANDLERS: Final[ExceptionHandlersType] = {
    404: default_404_exception_handler,
    500: default_500_exception_handler,
}
