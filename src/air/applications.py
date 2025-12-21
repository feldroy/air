"""
Instantiating Air applications.
"""

import inspect
from collections.abc import Callable, Sequence
from enum import Enum
from functools import wraps
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
from .routing import AirRoute, AirRouter, RouteCallable, RouterMixin
from .types import MaybeAwaitable


class Air(RouterMixin):
    """Air web framework - HTML-first web apps powered by FastAPI.

    Air uses composition, wrapping a FastAPI instance internally. This provides a clean, focused
        API for HTML applications while leveraging FastAPI's toolkit.

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

                app = FastAPI(dependencies=[Depends(func_dep_1), Depends(func_dep_2)])"""
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
                TODO: Update for Air

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
            Doc("""
                TODO: Update for Air
                List of middleware to be added when creating the application.

                In FastAPI you would normally do this with `app.add_middleware()`
                instead.

                Read more in the
                [FastAPI docs for Middleware](https://fastapi.tiangolo.com/tutorial/middleware/).
                """),
        ] = None,
        exception_handlers: Annotated[
            ExceptionHandlersType | None,
            Doc(
                """
                TODO: Update for Air
                A dictionary with handlers for exceptions.

                In FastAPI, you would normally use the decorator
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
                TODO: Update for Air
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
                TODO: Update for Air
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
            Doc("The path to serve Swagger UI documentation. Set None to disable."),
        ] = None,
        redoc_url: Annotated[
            str | None,
            Doc("The path to serve ReDoc documentation. Set None to disable."),
        ] = None,
        openapi_url: Annotated[
            str | None,
            Doc("The URL where the OpenAPI schema will be served. Set  None to disable."),
        ] = None,
        path_separator: Annotated[
            Literal["/", "-"],
            Doc("An optional path separator."),
        ] = "-",
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

        # Merge default exception handlers
        if exception_handlers is None:
            exception_handlers = {}
        exception_handlers = {**exception_handlers, **DEFAULT_EXCEPTION_HANDLERS}

        # Create internal FastAPI instance
        self._app = FastAPI(
            debug=debug,
            routes=routes,
            servers=servers,
            dependencies=dependencies,
            default_response_class=default_response_class,
            middleware=middleware,
            exception_handlers=exception_handlers,  # type: ignore[arg-type]
            on_startup=None,
            on_shutdown=None,
            lifespan=lifespan,
            docs_url=docs_url,
            redoc_url=redoc_url,
            openapi_url=openapi_url,
            webhooks=webhooks,
            deprecated=deprecated,
            redirect_slashes=redirect_slashes,
            **extra,
        )

        # Use Air's custom route class
        self._app.router.route_class = AirRoute

    # =========================================================================
    # ASGI Interface
    # =========================================================================

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
        self._app.include_router(
            router,
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

    # =========================================================================
    # Route Decorators - Clean API without response_model clutter
    # =========================================================================

    def get(
        self,
        path: Annotated[
            str,
            Doc("The URL path for this path operation."),
        ],
        *,
        status_code: Annotated[
            int | None,
            Doc("The default status code for the response."),
        ] = None,
        tags: Annotated[
            list[str | Enum] | None,
            Doc("Tags for OpenAPI documentation."),
        ] = None,
        dependencies: Annotated[
            Sequence[Depends] | None,
            Doc("Dependencies for this path operation."),
        ] = None,
        summary: Annotated[
            str | None,
            Doc("Summary for OpenAPI documentation."),
        ] = None,
        description: Annotated[
            str | None,
            Doc("Description for OpenAPI documentation."),
        ] = None,
        response_description: Annotated[
            str,
            Doc("Description for the default response."),
        ] = "Successful Response",
        responses: Annotated[
            dict[int | str, dict[str, Any]] | None,
            Doc("Additional responses for OpenAPI."),
        ] = None,
        deprecated: Annotated[
            bool | None,
            Doc("Mark this path operation as deprecated."),
        ] = None,
        operation_id: Annotated[
            str | None,
            Doc("Custom operation ID for OpenAPI."),
        ] = None,
        include_in_schema: Annotated[
            bool,
            Doc("Include in OpenAPI schema."),
        ] = True,
        response_class: Annotated[
            type[Response],
            Doc("Response class for this path operation."),
        ] = AirResponse,
        name: Annotated[
            str | None,
            Doc("Name for this path operation."),
        ] = None,
        callbacks: Annotated[
            list[BaseRoute] | None,
            Doc("OpenAPI callbacks."),
        ] = None,
        openapi_extra: Annotated[
            dict[str, Any] | None,
            Doc("Extra OpenAPI metadata."),
        ] = None,
        generate_unique_id_function: Annotated[
            Callable[[routing.APIRoute], str],
            Doc("Function to generate unique IDs for OpenAPI."),
        ] = generate_unique_id,
    ) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
        """Add a GET path operation.

        Returns:
            A decorator function that registers the decorated function as a GET endpoint.

        Example:

            import air

            app = air.Air()

            @app.get("/hello")
            def hello_world() -> air.H1:
                return air.H1("Hello, World!")

            @app.get("/users/{user_id}")
            def get_user(user_id: int) -> air.Div:
                return air.Div(
                    air.H2(f"User ID: {user_id}"),
                    air.P("User profile page"),
                )
        """

        def decorator[**P, R](func: Callable[P, MaybeAwaitable[R]]) -> RouteCallable:
            @wraps(func)
            async def endpoint(*args: P.args, **kw: P.kwargs) -> Response:
                result = func(*args, **kw)
                if inspect.isawaitable(result):
                    result = await result
                if isinstance(result, Response):
                    return result
                return response_class(result)

            decorated = self._app.get(
                path,
                response_model=None,
                status_code=status_code,
                tags=tags,
                dependencies=dependencies,
                summary=summary,
                description=description,
                response_description=response_description,
                responses=responses,
                deprecated=deprecated,
                operation_id=operation_id,
                response_model_include=None,
                response_model_exclude=None,
                response_model_by_alias=True,
                response_model_exclude_unset=False,
                response_model_exclude_defaults=False,
                response_model_exclude_none=False,
                include_in_schema=include_in_schema,
                response_class=response_class,
                name=name,
                callbacks=callbacks,
                openapi_extra=openapi_extra,
                generate_unique_id_function=generate_unique_id_function,
            )(endpoint)

            decorated.url = self._url_helper(name or endpoint.__name__)
            return decorated

        return decorator

    def post(
        self,
        path: Annotated[
            str,
            Doc("The URL path for this path operation."),
        ],
        *,
        status_code: Annotated[
            int | None,
            Doc("The default status code for the response."),
        ] = None,
        tags: Annotated[
            list[str | Enum] | None,
            Doc("Tags for OpenAPI documentation."),
        ] = None,
        dependencies: Annotated[
            Sequence[Depends] | None,
            Doc("Dependencies for this path operation."),
        ] = None,
        summary: Annotated[
            str | None,
            Doc("Summary for OpenAPI documentation."),
        ] = None,
        description: Annotated[
            str | None,
            Doc("Description for OpenAPI documentation."),
        ] = None,
        response_description: Annotated[
            str,
            Doc("Description for the default response."),
        ] = "Successful Response",
        responses: Annotated[
            dict[int | str, dict[str, Any]] | None,
            Doc("Additional responses for OpenAPI."),
        ] = None,
        deprecated: Annotated[
            bool | None,
            Doc("Mark this path operation as deprecated."),
        ] = None,
        operation_id: Annotated[
            str | None,
            Doc("Custom operation ID for OpenAPI."),
        ] = None,
        include_in_schema: Annotated[
            bool,
            Doc("Include in OpenAPI schema."),
        ] = True,
        response_class: Annotated[
            type[Response],
            Doc("Response class for this path operation."),
        ] = AirResponse,
        name: Annotated[
            str | None,
            Doc("Name for this path operation."),
        ] = None,
        callbacks: Annotated[
            list[BaseRoute] | None,
            Doc("OpenAPI callbacks."),
        ] = None,
        openapi_extra: Annotated[
            dict[str, Any] | None,
            Doc("Extra OpenAPI metadata."),
        ] = None,
        generate_unique_id_function: Annotated[
            Callable[[routing.APIRoute], str],
            Doc("Function to generate unique IDs for OpenAPI."),
        ] = generate_unique_id,
    ) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
        """Add a POST path operation.

        Returns:
            A decorator function that registers the decorated function as a POST endpoint.

        Example:

            from pydantic import BaseModel
            import air

            class UserCreate(BaseModel):
                name: str
                email: str

            app = air.Air()

            @app.post("/users")
            def create_user(user: UserCreate) -> air.Div:
                return air.Div(
                    air.H2("User Created"),
                    air.P(f"Name: {user.name}"),
                )
        """

        def decorator[**P, R](func: Callable[P, MaybeAwaitable[R]]) -> RouteCallable:
            @wraps(func)
            async def endpoint(*args: P.args, **kw: P.kwargs) -> Response:
                result = func(*args, **kw)
                if inspect.isawaitable(result):
                    result = await result
                if isinstance(result, Response):
                    return result
                return response_class(result)

            decorated = self._app.post(
                path,
                response_model=None,
                status_code=status_code,
                tags=tags,
                dependencies=dependencies,
                summary=summary,
                description=description,
                response_description=response_description,
                responses=responses,
                deprecated=deprecated,
                operation_id=operation_id,
                response_model_include=None,
                response_model_exclude=None,
                response_model_by_alias=True,
                response_model_exclude_unset=False,
                response_model_exclude_defaults=False,
                response_model_exclude_none=False,
                include_in_schema=include_in_schema,
                response_class=response_class,
                name=name,
                callbacks=callbacks,
                openapi_extra=openapi_extra,
                generate_unique_id_function=generate_unique_id_function,
            )(endpoint)

            decorated.url = self._url_helper(name or endpoint.__name__)
            return decorated

        return decorator

    def patch(
        self,
        path: Annotated[
            str,
            Doc("The URL path for this path operation."),
        ],
        *,
        status_code: Annotated[
            int | None,
            Doc("The default status code for the response."),
        ] = None,
        tags: Annotated[
            list[str | Enum] | None,
            Doc("Tags for OpenAPI documentation."),
        ] = None,
        dependencies: Annotated[
            Sequence[Depends] | None,
            Doc("Dependencies for this path operation."),
        ] = None,
        summary: Annotated[
            str | None,
            Doc("Summary for OpenAPI documentation."),
        ] = None,
        description: Annotated[
            str | None,
            Doc("Description for OpenAPI documentation."),
        ] = None,
        response_description: Annotated[
            str,
            Doc("Description for the default response."),
        ] = "Successful Response",
        responses: Annotated[
            dict[int | str, dict[str, Any]] | None,
            Doc("Additional responses for OpenAPI."),
        ] = None,
        deprecated: Annotated[
            bool | None,
            Doc("Mark this path operation as deprecated."),
        ] = None,
        operation_id: Annotated[
            str | None,
            Doc("Custom operation ID for OpenAPI."),
        ] = None,
        include_in_schema: Annotated[
            bool,
            Doc("Include in OpenAPI schema."),
        ] = True,
        response_class: Annotated[
            type[Response],
            Doc("Response class for this path operation."),
        ] = AirResponse,
        name: Annotated[
            str | None,
            Doc("Name for this path operation."),
        ] = None,
        callbacks: Annotated[
            list[BaseRoute] | None,
            Doc("OpenAPI callbacks."),
        ] = None,
        openapi_extra: Annotated[
            dict[str, Any] | None,
            Doc("Extra OpenAPI metadata."),
        ] = None,
        generate_unique_id_function: Annotated[
            Callable[[routing.APIRoute], str],
            Doc("Function to generate unique IDs for OpenAPI."),
        ] = generate_unique_id,
    ) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
        """Add a PATCH path operation.

        Returns:
            A decorator function that registers the decorated function as a PATCH endpoint.
        """

        def decorator[**P, R](func: Callable[P, MaybeAwaitable[R]]) -> RouteCallable:
            @wraps(func)
            async def endpoint(*args: P.args, **kw: P.kwargs) -> Response:
                result = func(*args, **kw)
                if inspect.isawaitable(result):
                    result = await result
                if isinstance(result, Response):
                    return result
                return response_class(result)

            decorated = self._app.patch(
                path,
                response_model=None,
                status_code=status_code,
                tags=tags,
                dependencies=dependencies,
                summary=summary,
                description=description,
                response_description=response_description,
                responses=responses,
                deprecated=deprecated,
                operation_id=operation_id,
                response_model_include=None,
                response_model_exclude=None,
                response_model_by_alias=True,
                response_model_exclude_unset=False,
                response_model_exclude_defaults=False,
                response_model_exclude_none=False,
                include_in_schema=include_in_schema,
                response_class=response_class,
                name=name,
                callbacks=callbacks,
                openapi_extra=openapi_extra,
                generate_unique_id_function=generate_unique_id_function,
            )(endpoint)

            decorated.url = self._url_helper(name or endpoint.__name__)
            return decorated

        return decorator

    def put(
        self,
        path: Annotated[
            str,
            Doc("The URL path for this path operation."),
        ],
        *,
        status_code: Annotated[
            int | None,
            Doc("The default status code for the response."),
        ] = None,
        tags: Annotated[
            list[str | Enum] | None,
            Doc("Tags for OpenAPI documentation."),
        ] = None,
        dependencies: Annotated[
            Sequence[Depends] | None,
            Doc("Dependencies for this path operation."),
        ] = None,
        summary: Annotated[
            str | None,
            Doc("Summary for OpenAPI documentation."),
        ] = None,
        description: Annotated[
            str | None,
            Doc("Description for OpenAPI documentation."),
        ] = None,
        response_description: Annotated[
            str,
            Doc("Description for the default response."),
        ] = "Successful Response",
        responses: Annotated[
            dict[int | str, dict[str, Any]] | None,
            Doc("Additional responses for OpenAPI."),
        ] = None,
        deprecated: Annotated[
            bool | None,
            Doc("Mark this path operation as deprecated."),
        ] = None,
        operation_id: Annotated[
            str | None,
            Doc("Custom operation ID for OpenAPI."),
        ] = None,
        include_in_schema: Annotated[
            bool,
            Doc("Include in OpenAPI schema."),
        ] = True,
        response_class: Annotated[
            type[Response],
            Doc("Response class for this path operation."),
        ] = AirResponse,
        name: Annotated[
            str | None,
            Doc("Name for this path operation."),
        ] = None,
        callbacks: Annotated[
            list[BaseRoute] | None,
            Doc("OpenAPI callbacks."),
        ] = None,
        openapi_extra: Annotated[
            dict[str, Any] | None,
            Doc("Extra OpenAPI metadata."),
        ] = None,
        generate_unique_id_function: Annotated[
            Callable[[routing.APIRoute], str],
            Doc("Function to generate unique IDs for OpenAPI."),
        ] = generate_unique_id,
    ) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
        """Add a PUT path operation.

        Returns:
            A decorator function that registers the decorated function as a PUT endpoint.
        """

        def decorator[**P, R](func: Callable[P, MaybeAwaitable[R]]) -> RouteCallable:
            @wraps(func)
            async def endpoint(*args: P.args, **kw: P.kwargs) -> Response:
                result = func(*args, **kw)
                if inspect.isawaitable(result):
                    result = await result
                if isinstance(result, Response):
                    return result
                return response_class(result)

            decorated = self._app.put(
                path,
                response_model=None,
                status_code=status_code,
                tags=tags,
                dependencies=dependencies,
                summary=summary,
                description=description,
                response_description=response_description,
                responses=responses,
                deprecated=deprecated,
                operation_id=operation_id,
                response_model_include=None,
                response_model_exclude=None,
                response_model_by_alias=True,
                response_model_exclude_unset=False,
                response_model_exclude_defaults=False,
                response_model_exclude_none=False,
                include_in_schema=include_in_schema,
                response_class=response_class,
                name=name,
                callbacks=callbacks,
                openapi_extra=openapi_extra,
                generate_unique_id_function=generate_unique_id_function,
            )(endpoint)

            decorated.url = self._url_helper(name or endpoint.__name__)
            return decorated

        return decorator

    def delete(
        self,
        path: Annotated[
            str,
            Doc("The URL path for this path operation."),
        ],
        *,
        status_code: Annotated[
            int | None,
            Doc("The default status code for the response."),
        ] = None,
        tags: Annotated[
            list[str | Enum] | None,
            Doc("Tags for OpenAPI documentation."),
        ] = None,
        dependencies: Annotated[
            Sequence[Depends] | None,
            Doc("Dependencies for this path operation."),
        ] = None,
        summary: Annotated[
            str | None,
            Doc("Summary for OpenAPI documentation."),
        ] = None,
        description: Annotated[
            str | None,
            Doc("Description for OpenAPI documentation."),
        ] = None,
        response_description: Annotated[
            str,
            Doc("Description for the default response."),
        ] = "Successful Response",
        responses: Annotated[
            dict[int | str, dict[str, Any]] | None,
            Doc("Additional responses for OpenAPI."),
        ] = None,
        deprecated: Annotated[
            bool | None,
            Doc("Mark this path operation as deprecated."),
        ] = None,
        operation_id: Annotated[
            str | None,
            Doc("Custom operation ID for OpenAPI."),
        ] = None,
        include_in_schema: Annotated[
            bool,
            Doc("Include in OpenAPI schema."),
        ] = True,
        response_class: Annotated[
            type[Response],
            Doc("Response class for this path operation."),
        ] = AirResponse,
        name: Annotated[
            str | None,
            Doc("Name for this path operation."),
        ] = None,
        callbacks: Annotated[
            list[BaseRoute] | None,
            Doc("OpenAPI callbacks."),
        ] = None,
        openapi_extra: Annotated[
            dict[str, Any] | None,
            Doc("Extra OpenAPI metadata."),
        ] = None,
        generate_unique_id_function: Annotated[
            Callable[[routing.APIRoute], str],
            Doc("Function to generate unique IDs for OpenAPI."),
        ] = generate_unique_id,
    ) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
        """Add a DELETE path operation.

        Returns:
            A decorator function that registers the decorated function as a DELETE endpoint.
        """

        def decorator[**P, R](func: Callable[P, MaybeAwaitable[R]]) -> RouteCallable:
            @wraps(func)
            async def endpoint(*args: P.args, **kw: P.kwargs) -> Response:
                result = func(*args, **kw)
                if inspect.isawaitable(result):
                    result = await result
                if isinstance(result, Response):
                    return result
                return response_class(result)

            decorated = self._app.delete(
                path,
                response_model=None,
                status_code=status_code,
                tags=tags,
                dependencies=dependencies,
                summary=summary,
                description=description,
                response_description=response_description,
                responses=responses,
                deprecated=deprecated,
                operation_id=operation_id,
                response_model_include=None,
                response_model_exclude=None,
                response_model_by_alias=True,
                response_model_exclude_unset=False,
                response_model_exclude_defaults=False,
                response_model_exclude_none=False,
                include_in_schema=include_in_schema,
                response_class=response_class,
                name=name,
                callbacks=callbacks,
                openapi_extra=openapi_extra,
                generate_unique_id_function=generate_unique_id_function,
            )(endpoint)

            decorated.url = self._url_helper(name or endpoint.__name__)
            return decorated

        return decorator
