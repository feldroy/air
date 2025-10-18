# Exceptions

## default_404_exception_handler

```
default_404_exception_handler(request, exc)
```

Default 404 exception handler. Can be overloaded.

Source code in `src/air/exception_handlers.py`

```
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
```

## default_404_router_handler

```
default_404_router_handler(router_name)
```

Build an ASGI app that delegates the 404 to the default_404_exception_handler.

Source code in `src/air/exception_handlers.py`

```
def default_404_router_handler(router_name: str) -> ASGIApp:
    """Build an ASGI app that delegates the 404 to the default_404_exception_handler."""

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
```

## default_500_exception_handler

```
default_500_exception_handler(request, exc)
```

Default 500 exception handler. Can be overloaded.

Source code in `src/air/exception_handlers.py`

```
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
```
