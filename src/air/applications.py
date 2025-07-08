from typing import (
    Any,
    Callable,
    Coroutine,
    Dict,
    List,
    Optional,
    Sequence,
    Type,
    TypeVar,
    Union,
)

from fastapi import FastAPI, routing
from fastapi.params import Depends
from starlette.middleware import Middleware
from starlette.requests import Request
from starlette.responses import Response
from starlette.routing import BaseRoute
from starlette.types import Lifespan
from typing_extensions import Annotated, Doc, deprecated

from .responses import AirResponse

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
            Optional[List[BaseRoute]],
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
            Optional[List[Dict[str, Union[str, Any]]]],
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
            Optional[Sequence[Depends]],
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
            Type[Response],
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
            Optional[Sequence[Middleware]],
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
            Optional[
                Dict[
                    Union[int, Type[Exception]],
                    Callable[[Request, Any], Coroutine[Any, Any, Response]],
                ]
            ],
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
            Optional[Sequence[Callable[[], Any]]],
            Doc(
                """
                A list of startup event handler functions.

                You should instead use the `lifespan` handlers.

                Read more in the [FastAPI docs for `lifespan`](https://fastapi.tiangolo.com/advanced/events/).
                """
            ),
        ] = None,
        on_shutdown: Annotated[
            Optional[Sequence[Callable[[], Any]]],
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
            Optional[Lifespan[AppType]],
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
            Optional[routing.APIRouter],
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
            Optional[bool],
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
        super().__init__(
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
            webhooks=webhooks,
            deprecated=deprecated,
            **extra,
        )

    def page(self, func):
        """Decorator that creates a GET route using the function name as the path.

        If the name of the function is "index", then the route is "/".

        Examples:

            import air

            app = Air()

            @app.page
            def index():
                return H1("I am the home page")
        """
        if func.__name__ == "index":
            route_name = "/"
        else:
            route_name = f"/{func.__name__}"
        return self.get(route_name)(func)
