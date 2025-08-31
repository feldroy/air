"""
Instantiating Air applications.
"""

from collections.abc import Callable, Coroutine, Sequence
from typing import (
    Annotated,
    Any,
    Final,
    TypeVar,
)

from fastapi import APIRouter, FastAPI, routing
from fastapi.params import Depends
from starlette.middleware import Middleware
from starlette.requests import Request
from starlette.responses import Response
from starlette.routing import BaseRoute
from starlette.types import Lifespan
from typing_extensions import Doc, deprecated

from air.links import RouteLink

from .layouts import mvpcss
from .responses import AirResponse
from .tags import H1, P, Title

AppType = TypeVar("AppType", bound="FastAPI")


class Air(FastAPI):
    """FastAPI wrapper class with AirResponse as the default response class.

    Args:
        debug: Enables additional logging or diagnostic output.
        dependencies: A list of global dependencies, they will be applied to each *path operation*,
                including in sub-routers.
        middleware: List of middleware to be added when creating the application.
        default_response_class: The default response class to be used.
        redirect_slashes: Whether to detect and redirect slashes in URLs when the client doesn't
                use the same format.
        on_startup: A list of startup event handler functions.
        on_shutdown: A list of shutdown event handler functions.
        lifespan: A `Lifespan` context manager handler. This replaces `startup` and
                `shutdown` functions with a single context manager.
    Example:

        import air

        app = air.Air()
    """

    def __init__(
        self: AppType,
        *,
        debug: Annotated[
            bool,
            Doc(
                """
                Boolean indicating if debug tracebacks should be returned on server
                errors.

                Read more in the
                [Starlette docs for Applications](https://www.starlette.io/applications/#instantiating-the-application).
                """
            ),
        ] = False,
        routes: Annotated[
            list[BaseRoute] | None,
            Doc(
                """
                **Note**: you probably shouldn't use this parameter, it is inherited
                from Starlette and supported for compatibility.

                ---

                A list of routes to serve incoming HTTP and WebSocket requests.
                """
            ),
            deprecated(
                """
                You normally wouldn't use this parameter with FastAPI, it is inherited
                from Starlette and supported for compatibility.

                In FastAPI, you normally would use the *path operation methods*,
                like `app.get()`, `app.post()`, etc.
                """
            ),
        ] = None,
        servers: Annotated[
            list[dict[str, str | Any]] | None,
            Doc(
                """
                A `list` of `dict`s with connectivity information to a target server.

                You would use it, for example, if your application is served from
                different domains and you want to use the same Swagger UI in the
                browser to interact with each of them (instead of having multiple
                browser tabs open). Or if you want to leave fixed the possible URLs.

                If the servers `list` is not provided, or is an empty `list`, the
                default value would be a `dict` with a `url` value of `/`.

                Each item in the `list` is a `dict` containing:

                * `url`: A URL to the target host. This URL supports Server Variables
                and MAY be relative, to indicate that the host location is relative
                to the location where the OpenAPI document is being served. Variable
                substitutions will be made when a variable is named in `{`brackets`}`.
                * `description`: An optional string describing the host designated by
                the URL. [CommonMark syntax](https://commonmark.org/) MAY be used for
                rich text representation.
                * `variables`: A `dict` between a variable name and its value. The value
                    is used for substitution in the server's URL template.

                Read more in the
                [FastAPI docs for Behind a Proxy](https://fastapi.tiangolo.com/advanced/behind-a-proxy/#additional-servers).

                **Example**

                ```python
                from fastapi import FastAPI

                app = FastAPI(
                    servers=[
                        {"url": "https://stag.example.com", "description": "Staging environment"},
                        {"url": "https://prod.example.com", "description": "Production environment"},
                    ]
                )
                ```
                """
            ),
        ] = None,
        dependencies: Annotated[
            Sequence[Depends] | None,
            Doc(
                """
                A list of global dependencies, they will be applied to each
                *path operation*, including in sub-routers.

                Read more about it in the
                [FastAPI docs for Global Dependencies](https://fastapi.tiangolo.com/tutorial/dependencies/global-dependencies/).

                **Example**

                ```python
                from fastapi import Depends, FastAPI

                from .dependencies import func_dep_1, func_dep_2

                app = FastAPI(dependencies=[Depends(func_dep_1), Depends(func_dep_2)])
                ```
                """
            ),
        ] = None,
        default_response_class: Annotated[
            type[Response],
            Doc(
                """
                The default response class to be used.
                Read more in the
                [FastAPI docs for Custom Response - HTML, Stream, File, others](https://fastapi.tiangolo.com/advanced/custom-response/#default-response-class).
                **Analogy**
                ```python
                from fastapi import FastAPI
                from air import AirResponse
                app = FastAPI(default_response_class=AirResponse)
                ```
                """
            ),
        ] = AirResponse,
        redirect_slashes: Annotated[
            bool,
            Doc(
                """
                Whether to detect and redirect slashes in URLs when the client doesn't
                use the same format.

                **Example**

                ```python
                from fastapi import FastAPI

                app = FastAPI(redirect_slashes=True)  # the default

                @app.get("/items/")
                async def read_items():
                    return [{"item_id": "Foo"}]
                ```

                With this app, if a client goes to `/items` (without a trailing slash),
                they will be automatically redirected with an HTTP status code of 307
                to `/items/`.
                """
            ),
        ] = True,
        middleware: Annotated[
            Sequence[Middleware] | None,
            Doc(
                """
                List of middleware to be added when creating the application.

                In FastAPI you would normally do this with `app.add_middleware()`
                instead.

                Read more in the
                [FastAPI docs for Middleware](https://fastapi.tiangolo.com/tutorial/middleware/).
                """
            ),
        ] = None,
        exception_handlers: Annotated[
            dict[int | type[Exception], Callable[[Request, Any], Coroutine[Any, Any, Response]]] | None,
            Doc(
                """
                A dictionary with handlers for exceptions.

                In FastAPI, you would normally use the decorator
                `@app.exception_handler()`.

                Read more in the
                [FastAPI docs for Handling Errors](https://fastapi.tiangolo.com/tutorial/handling-errors/).
                """
            ),
        ] = None,
        on_startup: Annotated[
            Sequence[Callable[[], Any]] | None,
            Doc(
                """
                A list of startup event handler functions.

                You should instead use the `lifespan` handlers.

                Read more in the [FastAPI docs for `lifespan`](https://fastapi.tiangolo.com/advanced/events/).
                """
            ),
        ] = None,
        on_shutdown: Annotated[
            Sequence[Callable[[], Any]] | None,
            Doc(
                """
                A list of shutdown event handler functions.

                You should instead use the `lifespan` handlers.

                Read more in the
                [FastAPI docs for `lifespan`](https://fastapi.tiangolo.com/advanced/events/).
                """
            ),
        ] = None,
        lifespan: Annotated[
            Lifespan[AppType] | None,
            Doc(
                """
                A `Lifespan` context manager handler. This replaces `startup` and
                `shutdown` functions with a single context manager.

                Read more in the
                [FastAPI docs for `lifespan`](https://fastapi.tiangolo.com/advanced/events/).
                """
            ),
        ] = None,
        webhooks: Annotated[
            routing.APIRouter | None,
            Doc(
                """
                Add OpenAPI webhooks. This is similar to `callbacks` but it doesn't
                depend on specific *path operations*.

                It will be added to the generated OpenAPI (e.g. visible at `/docs`).

                **Note**: This is available since OpenAPI 3.1.0, FastAPI 0.99.0.

                Read more about it in the
                [FastAPI docs for OpenAPI Webhooks](https://fastapi.tiangolo.com/advanced/openapi-webhooks/).
                """
            ),
        ] = None,
        deprecated: Annotated[
            bool | None,
            Doc(
                """
                Mark all *path operations* as deprecated. You probably don't need it,
                but it's available.

                It will be added to the generated OpenAPI (e.g. visible at `/docs`).

                Read more about it in the
                [FastAPI docs for Path Operation Configuration](https://fastapi.tiangolo.com/tutorial/path-operation-configuration/).
                """
            ),
        ] = None,
        docs_url: Annotated[
            str | None,
            Doc(
                """
                The path at which to serve the Swagger UI documentation.

                Set to `None` to disable it.
                """
            ),
        ] = None,
        redoc_url: Annotated[
            str | None,
            Doc(
                """
                The path at which to serve the ReDoc documentation.

                Set to `None` to disable it.
                """
            ),
        ] = None,
        openapi_url: Annotated[
            str | None,
            Doc(
                """
                The URL where the OpenAPI schema will be served from.

                Set to `None` to disable it.
                """
            ),
        ] = None,
        **extra: Annotated[
            Any,
            Doc(
                """
                Extra keyword arguments to be stored in the app, not used by FastAPI
                anywhere.
                """
            ),
        ],
    ) -> None:
        """Initialize Air app with AirResponse as default response class.

        This preserves all FastAPI initialization parameters while setting
        AirResponse as the default response class.
        """
        if exception_handlers is None:
            exception_handlers = {}
        exception_handlers |= DEFAULT_EXCEPTION_HANDLERS
        super().__init__(  # ty: ignore [invalid-super-argument]
            debug=debug,
            routes=routes,
            servers=servers,
            dependencies=dependencies,
            default_response_class=default_response_class,
            middleware=middleware,
            exception_handlers=exception_handlers,
            on_startup=on_startup,
            on_shutdown=on_shutdown,
            lifespan=lifespan,
            docs_url=docs_url,
            redoc_url=redoc_url,
            openapi_url=openapi_url,
            webhooks=webhooks,
            deprecated=deprecated,
            **extra,
        )

        # bind .url to all endpoints once the app is fully wired
        self.add_event_handler("startup", self._attach_route_links)

    def page(self, func):
        """Decorator that creates a GET route using the function name as the path.

        If the name of the function is "index", then the route is "/".

        Example:

            import air

            app = Air()

            @app.page
            def index(): # routes is "/"
                return H1("I am the home page")

            @app.page
            def data(): # route is "/data"
                return H1("I am the home page")

            @app.page
            def about_us(): # routes is "/about-us"
                return H1("I am the about page")
        """
        route_name = "/" if func.__name__ == "index" else f"/{func.__name__}".replace("_", "-")
        return self.get(route_name)(func)

    # when including routers, also (re)bind .url so prefixes are respected
    def include_router(self, router: APIRouter, *args, **kwargs) -> None:
        super().include_router(router, *args, **kwargs)
        self._attach_route_links()

    # one-time binder used by startup/include_router/tests ---
    def _attach_route_links(self) -> None:
        for r in self.router.routes:
            if isinstance(r, routing.APIRoute) and r.name and callable(r.endpoint):
                ep = r.endpoint
                # don't overwrite if user already attached something custom
                if not hasattr(ep, "url"):
                    try:
                        ep.url = RouteLink(self, r.name)
                    except Exception:
                        pass

    def bind_urls(self) -> None:
        """Manually attach `.url` to endpoints (useful for unit tests)."""
        self._attach_url_descriptors()


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
