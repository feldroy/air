"""
Instantiating Air applications.
"""

from collections.abc import Callable, Sequence
from enum import Enum
from typing import Annotated, Any, Literal
from warnings import deprecated

from fastapi import FastAPI, routing
from fastapi.params import Depends
from fastapi.utils import generate_unique_id
from starlette.middleware import Middleware
from starlette.responses import Response
from starlette.routing import BaseRoute
from starlette.types import Lifespan, Receive, Scope, Send
from typing_extensions import Doc

from .exception_handlers import DEFAULT_EXCEPTION_HANDLERS, ExceptionHandlersType
from .responses import AirResponse
from .routing import AirRoute, AirRouter, RouterMixin


class Air(RouterMixin):
    """Air web framework - HTML-first web apps powered by FastAPI.

    Air uses composition, wrapping a FastAPI instance internally. This provides a clean, focused
        API for HTML applications while leveraging FastAPI's toolkit.

    Args:
        debug: Enables additional logging or diagnostic output.
        dependencies: A list of global dependencies, they will be applied to each *path operation*,
                including in sub-routers.
        middleware: List of middleware to be added when creating the application.
        redirect_slashes: Whether to detect and redirect slashes in URLs when the client doesn't
                use the same format.
        lifespan: A `Lifespan` context manager handler. This replaces `startup` and
                `shutdown` functions with a single context manager.
        path_separator: An optional path separator, default to "-". valid option available ["/", "-"]

    Example:

        import air

        app = air.Air()

        @app.get("/")
        def index() -> air.H1:
            return air.H1("Hello, World!")
    """

    def __init__(
        self,
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
                "You normally wouldn't use this parameter with Air. "
                "Use the path operation methods like app.get(), app.post(), etc."
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
                        {
                            "url": "https://stag.example.com",
                            "description": "Staging environment",
                        },
                        {
                            "url": "https://prod.example.com",
                            "description": "Production environment",
                        },
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
        redirect_slashes: Annotated[
            bool,
            Doc(
                """
                Whether to detect and redirect slashes in URLs when the client doesn't
                use the same format.

                **Example**

                ```python
                import air

                app = Air(redirect_slashes=True)  # the default


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
            ExceptionHandlersType | None,
            Doc(
                """
                A dictionary with handlers for exceptions.

                In FastAPI and Air, you would normally use the decorator
                `@app.exception_handler()`.

                Read more in the
                [FastAPI docs for Handling Errors](https://fastapi.tiangolo.com/tutorial/handling-errors/).
                """
            ),
        ] = None,
        lifespan: Annotated[
            Lifespan[Any] | None,
            Doc(
                """
                A `Lifespan` context manager handler. This replaces `startup` and
                `shutdown` functions with a single context manager.

                Read more in the
                [FastAPI docs for `lifespan`](https://fastapi.tiangolo.com/advanced/events/).
                """
            ),
        ] = None,
        path_separator: Annotated[
            Literal["/", "-"],
            Doc("An optional path separator."),
        ] = "-",
        fastapi_app: Annotated[
            FastAPI | None,
            Doc("""
                For those occasions when the FastAPI app needs more customization
                than Air parameters allow.

                Example:

                    # This example turns on OpenAPI docs while continuing mostly normal Air behaviors.
                    # Go to 127.0.0.1:8000/docs or 127.0.0.1:8000/redoc
                    import air
                    from fastapi import FastAPI

                    fastapi_app = FastAPI(default_response_class=air.AirResponse)
                    app = air.Air(fastapi_app=fastapi_app)


                    @app.page
                    def index():
                        "project home page"
                        return air.H1('Hello world')


                    @app.page
                    def about():
                        "This is the about page"
                        return air.Div('About Air')
                """),
        ] = None,
        **extra: Annotated[
            Any,
            Doc(
                """
                Extra keyword arguments to be stored in the app, not used by Air
                anywhere.
                """
            ),
        ],
    ) -> None:
        """Initialize Air app with composition over FastAPI.

        This preserves most FastAPI initialization parameters while setting:
            - AirResponse as the default response class.
            - AirRoute as the default route class.
        """
        self.path_separator = path_separator
        if exception_handlers is None:
            exception_handlers = {}
        exception_handlers |= DEFAULT_EXCEPTION_HANDLERS

        # Create internal FastAPI instance
        if fastapi_app is None:
            self._app = FastAPI(
                debug=debug,
                routes=routes,
                servers=servers,
                dependencies=dependencies,
                default_response_class=AirResponse,
                middleware=middleware,
                exception_handlers=exception_handlers,  # type: ignore[arg-type]
                on_startup=None,
                on_shutdown=None,
                lifespan=lifespan,
                docs_url=None,
                redoc_url=None,
                openapi_url=None,
                webhooks=None,
                deprecated=None,
                redirect_slashes=redirect_slashes,
                **extra,
            )
        else:
            self._app = fastapi_app

        # Use Air's custom route class
        self._app.router.route_class = AirRoute

    # =========================================================================
    # ASGI Interface
    # =========================================================================

    @property
    def _target(self) -> FastAPI:
        return self._app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        """ASGI interface - delegates to internal FastAPI app."""
        await self._app(scope, receive, send)

    # =========================================================================
    # FastAPI Proxies - expose commonly needed functionality
    # =========================================================================

    @property
    def state(self) -> Any:
        """Application state, shared across requests."""
        return self._app.state

    @property
    def router(self) -> routing.APIRouter:
        """The application router."""
        return self._app.router

    @property
    def routes(self) -> list[BaseRoute]:
        """The list of routes."""
        return self._app.routes

    @property
    def debug(self) -> bool:
        """Debug mode status."""
        return self._app.debug

    @debug.setter
    def debug(self, value: bool) -> None:
        self._app.debug = value

    @property
    def dependency_overrides(self) -> dict[Callable[..., Any], Callable[..., Any]]:
        """Dependency overrides for testing."""
        return self._app.dependency_overrides

    @property
    def exception_handlers(self) -> dict[Any, Callable[..., Any]]:
        """Exception handlers for this application."""
        return self._app.exception_handlers

    def url_path_for(self, name: str, /, **path_params: Any) -> str:
        """Generate a URL path for a named route.

        Returns:
            The generated URL path string.
        """
        return str(self._app.url_path_for(name, **path_params))

    def add_middleware(
        self,
        middleware_class: type,
        **options: Any,
    ) -> None:
        """Add middleware to the application."""
        self._app.add_middleware(middleware_class, **options)

    def include_router(
        self,
        router: AirRouter | routing.APIRouter,
        *,
        prefix: str = "",
        tags: list[str | Enum] | None = None,
        dependencies: Sequence[Depends] | None = None,
        responses: dict[int | str, dict[str, Any]] | None = None,
        deprecated: bool | None = None,
        include_in_schema: bool = True,
        default_response_class: type[Response] = AirResponse,
        callbacks: list[BaseRoute] | None = None,
        generate_unique_id_function: Callable[[routing.APIRoute], str] = generate_unique_id,
    ) -> None:
        """Include a router in this application."""
        # Extract internal APIRouter from AirRouter for type compatibility
        actual_router: routing.APIRouter = router._router if isinstance(router, AirRouter) else router
        self._app.include_router(
            actual_router,
            prefix=prefix,
            tags=tags,
            dependencies=dependencies,
            responses=responses,
            deprecated=deprecated,
            include_in_schema=include_in_schema,
            default_response_class=default_response_class,
            callbacks=callbacks,
            generate_unique_id_function=generate_unique_id_function,
        )

    def exception_handler(
        self,
        exc_class_or_status_code: int | type[Exception],
    ) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
        """Add an exception handler to the application.

        Returns:
            A decorator that registers the exception handler.
        """
        return self._app.exception_handler(exc_class_or_status_code)

    def middleware(self, middleware_type: str) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
        """Add a middleware function using a decorator.

        Returns:
            A decorator that registers the middleware function.
        """
        return self._app.middleware(middleware_type)

    def mount(
        self,
        path: str,
        app: Any,
        name: str | None = None,
    ) -> None:
        """Mount a sub-application."""
        self._app.mount(path, app, name=name)

    @property
    def fastapi_app(self) -> FastAPI:
        """Access the underlying FastAPI app for advanced use cases.

        Use this if you need FastAPI-specific features like:
        - OpenAPI customization
        - response_model for JSON endpoints
        - WebSocket handling

        Example:

            @app.fastapi_app.get("/api/users", response_model=list[User])
            async def api_get_users():
                return users
        """
        return self._app
