"""
Instantiating Air applications.
"""

import inspect
from collections.abc import Callable, Coroutine, Sequence
from enum import Enum
from typing import (
    Annotated,
    Any,
    Final,
    Self,
)

from fastapi import FastAPI, routing
from fastapi.datastructures import Default, DefaultPlaceholder
from fastapi.params import Depends
from fastapi.types import IncEx
from fastapi.utils import generate_unique_id
from starlette.middleware import Middleware
from starlette.requests import Request
from starlette.responses import Response
from starlette.routing import BaseRoute
from starlette.types import Lifespan
from typing_extensions import Doc, deprecated

from air.urls import UrlDescriptor

from .layouts import mvpcss
from .responses import AirResponse
from .tags import H1, P, Title

default_generate_unique_id = Default(generate_unique_id)
default_response_model = Default(None)


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
        self: Self,
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
            Lifespan[Self] | None,
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

        # bind .url to all endpoints once the app is fully wired to cover plugins or third-party
        # code that add routes by touching app.router directly and bypassing add_api_route.
        self.add_event_handler("startup", self._attach_url_descriptors)

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

    def add_api_route(
        self,
        path: str,
        endpoint: Callable[..., Any],
        *,
        response_model: Any = default_response_model,
        status_code: int | None = None,
        tags: list[str | Enum] | None = None,
        dependencies: Sequence[Depends] | None = None,
        summary: str | None = None,
        description: str | None = None,
        response_description: str = "Successful Response",
        responses: dict[int | str, dict[str, Any]] | None = None,
        deprecated: bool | None = None,
        methods: list[str] | None = None,
        operation_id: str | None = None,
        response_model_include: IncEx | None = None,
        response_model_exclude: IncEx | None = None,
        response_model_by_alias: bool = True,
        response_model_exclude_unset: bool = False,
        response_model_exclude_defaults: bool = False,
        response_model_exclude_none: bool = False,
        include_in_schema: bool = True,
        response_class: type[Response] | DefaultPlaceholder = AirResponse,
        name: str | None = None,
        openapi_extra: dict[str, Any] | None = None,
        generate_unique_id_function: Callable[[routing.APIRoute], str] = default_generate_unique_id,
    ) -> None:
        route_name = name or getattr(endpoint, "__name__", None) or path
        self._attach_url_descriptor_to_route(route_name, endpoint)

        super().add_api_route(
            path,
            endpoint=endpoint,
            response_model=response_model,
            status_code=status_code,
            tags=tags,
            dependencies=dependencies,
            summary=summary,
            description=description,
            response_description=response_description,
            responses=responses,
            deprecated=deprecated,
            methods=methods,
            operation_id=operation_id,
            response_model_include=response_model_include,
            response_model_exclude=response_model_exclude,
            response_model_by_alias=response_model_by_alias,
            response_model_exclude_unset=response_model_exclude_unset,
            response_model_exclude_defaults=response_model_exclude_defaults,
            response_model_exclude_none=response_model_exclude_none,
            include_in_schema=include_in_schema,
            response_class=response_class,
            name=route_name,
            openapi_extra=openapi_extra,
            generate_unique_id_function=generate_unique_id_function,
        )

    def include_router(
        self,
        router: Annotated[routing.APIRouter, Doc("The `APIRouter` to include.")],
        *,
        prefix: Annotated[str, Doc("An optional path prefix for the router.")] = "",
        tags: Annotated[
            list[str | Enum] | None,
            Doc(
                """
                A list of tags to be applied to all the *path operations* in this
                router.

                It will be added to the generated OpenAPI (e.g. visible at `/docs`).

                Read more about it in the
                [FastAPI docs for Path Operation Configuration](https://fastapi.tiangolo.com/tutorial/path-operation-configuration/).
                """
            ),
        ] = None,
        dependencies: Annotated[
            Sequence[Depends] | None,
            Doc(
                """
                A list of dependencies (using `Depends()`) to be applied to all the
                *path operations* in this router.

                Read more about it in the
                [FastAPI docs for Bigger Applications - Multiple Files](https://fastapi.tiangolo.com/tutorial/bigger-applications/#include-an-apirouter-with-a-custom-prefix-tags-responses-and-dependencies).

                **Example**

                    ```python
                    from fastapi import Depends, FastAPI

                    from .dependencies import get_token_header
                    from .internal import admin

                    app = FastAPI()

                    app.include_router(
                        admin.router,
                        dependencies=[Depends(get_token_header)],
                    )
                    ```
                """
            ),
        ] = None,
        responses: Annotated[
            dict[int | str, dict[str, Any]] | None,
            Doc(
                """
                Additional responses to be shown in OpenAPI.

                It will be added to the generated OpenAPI (e.g. visible at `/docs`).

                Read more about it in the
                [FastAPI docs for Additional Responses in OpenAPI](https://fastapi.tiangolo.com/advanced/additional-responses/).

                And in the
                [FastAPI docs for Bigger Applications](https://fastapi.tiangolo.com/tutorial/bigger-applications/#include-an-apirouter-with-a-custom-prefix-tags-responses-and-dependencies).
                """
            ),
        ] = None,
        deprecated: Annotated[
            bool | None,
            Doc(
                """
                Mark all the *path operations* in this router as deprecated.

                It will be added to the generated OpenAPI (e.g. visible at `/docs`).

                **Example**

                ```python
                from fastapi import FastAPI

                from .internal import old_api

                app = FastAPI()

                app.include_router(
                    old_api.router,
                    deprecated=True,
                )
                ```
                """
            ),
        ] = None,
        include_in_schema: Annotated[
            bool,
            Doc(
                """
                Include (or not) all the *path operations* in this router in the
                generated OpenAPI schema.

                This affects the generated OpenAPI (e.g. visible at `/docs`).

                **Example**

                ```python
                from fastapi import FastAPI

                from .internal import old_api

                app = FastAPI()

                app.include_router(
                    old_api.router,
                    include_in_schema=False,
                )
                ```
                """
            ),
        ] = True,
        default_response_class: Annotated[
            type[Response],
            Doc(
                """
                Default response class to be used for the *path operations* in this
                router.

                Read more in the
                [FastAPI docs for Custom Response - HTML, Stream, File, others](https://fastapi.tiangolo.com/advanced/custom-response/#default-response-class).

                **Example**

                ```python
                from fastapi import FastAPI
                from fastapi.responses import ORJSONResponse

                from .internal import old_api

                app = FastAPI()

                app.include_router(
                    old_api.router,
                    default_response_class=ORJSONResponse,
                )
                ```
                """
            ),
        ] = AirResponse,
        callbacks: Annotated[
            list[BaseRoute] | None,
            Doc(
                """
                List of *path operations* that will be used as OpenAPI callbacks.

                This is only for OpenAPI documentation, the callbacks won't be used
                directly.

                It will be added to the generated OpenAPI (e.g. visible at `/docs`).

                Read more about it in the
                [FastAPI docs for OpenAPI Callbacks](https://fastapi.tiangolo.com/advanced/openapi-callbacks/).
                """
            ),
        ] = None,
        generate_unique_id_function: Annotated[
            Callable[[routing.APIRoute], str],
            Doc(
                """
                Customize the function used to generate unique IDs for the *path
                operations* shown in the generated OpenAPI.

                This is particularly useful when automatically generating clients or
                SDKs for your API.

                Read more about it in the
                [FastAPI docs about how to Generate Clients](https://fastapi.tiangolo.com/advanced/generate-clients/#custom-generate-unique-id-function).
                """
            ),
        ] = default_generate_unique_id,
    ) -> None:
        """
        Include an `APIRouter` in the same app.

        Read more about it in the
        [FastAPI docs for Bigger Applications](https://fastapi.tiangolo.com/tutorial/bigger-applications/).

        ## Example

        ```python
        from fastapi import FastAPI

        from .users import users_router

        app = FastAPI()

        app.include_router(users_router)
        ```
        """
        super().include_router(
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

        # when including routers, also (re)bind .url so prefixes are respected
        self._attach_url_descriptors()

    def _attach_url_descriptors(self) -> None:
        """
        Bind reverse-URL helpers to all registered HTTP endpoints.

        Walks `self.router.routes` and, for each `APIRoute` that has a `name` and a
        callable `endpoint`, ensures the endpoint has a `.url(**params) -> str`
        attribute (via `UrlDescriptor`).
        """
        for route in self.router.routes:
            if isinstance(route, routing.APIRoute) and route.name and callable(route.endpoint):
                self._attach_url_descriptor_to_route(route.name, route.endpoint)

    def _attach_url_descriptor_to_route(self, route_name: str, endpoint: Callable[..., Any]) -> None:
        """
        Attach a `.url` callable to a single endpoint, if possible.

        Adds `endpoint.url = UrlDescriptor(self, route_name)` so handlers can build
        links like `handler.url(id=123, ref="home")`. If `.url` already exists, returns immediately.
        """
        attr = "url"
        if hasattr(endpoint, attr):
            return  # already attached
        if inspect.isfunction(endpoint) or inspect.ismethod(endpoint) or hasattr(endpoint, "__dict__"):
            setattr(endpoint, attr, UrlDescriptor(self, route_name))
        else:
            # We can't attach an attribute (e.g. callable instance with __slots__)
            # better to have some warning logs here ...
            pass

    def bind_urls(self) -> None:
        """
        Manually attach `.url` to endpoints (useful for unit tests)

        ## Example

            ```python
            def create_app():
                import air

                app = air.Air()

                @app.get("/{id}", name="item")
                def item(id: int): ...

                return app


            def test_urls():
                app = create_app()
                # no server startup here, so manually attach .url:
                app.bind_urls()

                assert item.url(id=123) == "/123"
            ```
        """
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
