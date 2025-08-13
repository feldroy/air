from types import BuiltinFunctionType
from typing import (
    Any,
    Callable,
    Coroutine,
    Dict,
    List,
    Optional,
    Self, Sequence,
    Type,
    TypeVar,
    Literal,
    Protocol,
    TYPE_CHECKING,
    runtime_checkable,
)

from fastapi import FastAPI, routing
from fastapi.params import Depends
from starlette.middleware import Middleware
from starlette.requests import Request
from starlette.responses import Response
from starlette.routing import BaseRoute
from starlette.types import Lifespan
from typing_extensions import Annotated, Doc, deprecated

from .layouts import mvpcss
from .responses import AirResponse
from .tags import H1, P, Title

AppType = TypeVar("AppType", bound="FastAPI")


class Air(FastAPI):
    """FastAPI wrapper class with AirResponse as the default response class.

    Extra (optional) MCP integration (requires `air[mcp]` which installs fastapi-mcp):
      - Pass `mcp=True` to auto-mount MCP over HTTP at "/mcp".
      - Or pass a dict with options, e.g.:
            mcp={"name": "Air MCP", "description": "Tools", "transport": "http", "mount_path": "/mcp"}
      - Or call `app.enable_mcp(...)` later.

    Docs: quickstart (how to mount), customization (name/filters), deploy separate app, refresh.  # noqa: E501
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
            Optional[List[Dict[str, str | Any]]],
            Doc("A list of dicts with connectivity information to a target server."),
        ] = None,
        dependencies: Annotated[
            Optional[Sequence[Depends]],
            Doc(
                """
                A list of global dependencies, they will be applied to each
                *path operation*, including in sub-routers.
                """
            ),
        ] = None,
        default_response_class: Annotated[
            Type[Response],
            Doc(
                """
                The default response class to be used.
                Read more in the
                [FastAPI docs for Custom Response - HTML, Stream, File, others](https://fastapi.tiangolo.com/advanced/custom-response/#default-response-class).  # noqa: E501
                """
            ),
        ] = AirResponse,
        redirect_slashes: Annotated[
            bool,
            Doc(
                """
                Whether to detect and redirect slashes in URLs when the client doesn't
                use the same format.
                """
            ),
        ] = True,
        middleware: Annotated[
            Optional[Sequence[Middleware]],
            Doc("List of middleware to be added when creating the application."),
        ] = None,
        exception_handlers: Annotated[
            Optional[
                Dict[int | Type[Exception], Callable[[Request, Any], Coroutine[Any, Any, Response]]]
            ],
            Doc("A dictionary with handlers for exceptions."),
        ] = None,
        on_startup: Annotated[
            Optional[Sequence[Callable[[], Any]]],
            Doc("A list of startup event handler functions."),
        ] = None,
        on_shutdown: Annotated[
            Optional[Sequence[Callable[[], Any]]],
            Doc("A list of shutdown event handler functions."),
        ] = None,
        lifespan: Annotated[
            Optional[Lifespan[AppType]],
            Doc("A `Lifespan` context manager handler."),
        ] = None,
        webhooks: Annotated[
            Optional[routing.APIRouter],
            Doc("Add OpenAPI webhooks."),
        ] = None,
        deprecated: Annotated[
            Optional[bool],
            Doc("Mark all *path operations* as deprecated."),
        ] = None,
        docs_url: Annotated[
            Optional[str],
            Doc("Path at which to serve the Swagger UI documentation."),
        ] = None,
        redoc_url: Annotated[
            Optional[str],
            Doc("Path at which to serve the ReDoc documentation."),
        ] = None,
        openapi_url: Annotated[
            Optional[str],
            Doc("URL where the OpenAPI schema will be served from."),
        ] = None,
        # ---- New: optional MCP autoconfig ------------------------------------
        with_mcp: Annotated[
            bool,
            Doc("Enable built-in MCP server (requires fastapi-mcp)."),
        ] = False,
        # ----------------------------------------------------------------------
        **extra: Annotated[Any, Doc("Extra keyword arguments stored in the app.")],
    ) -> None:
        """Initialize Air app with AirResponse as default response class."""
        DEFAULT_EXCEPTION_HANDLERS: dict[int, BuiltinFunctionType] = {
            404: default_404_exception_handler,
            500: default_500_exception_handler,
        }
        if exception_handlers is None:
            exception_handlers = {}
        exception_handlers = DEFAULT_EXCEPTION_HANDLERS | exception_handlers
        super().__init__(  # ty: ignore[invalid-super-argument]
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

        # Internal MCP state
        self._mcp: Optional["FastApiMCP"] = None
        self._mcp_mount_path: str = "/mcp"
        self._mcp_transport: Literal["http", "sse"] = "http"

        # Auto-enable MCP if requested and available
        if with_mcp:
            try:
                from fastapi_mcp import FastApiMCP
            except ImportError:
                raise ImportError(
                    "MCP requested, but 'fastapi-mcp' is not installed. "
                    "Install with: uv pip install 'air[mcp]' or uv add 'air[mcp]'."
                )
            # Create an MCP server based on this app
            self._mcp = FastApiMCP(self)
            # Mount the MCP server directly to your app
            self._mcp.mount_http()

    # ------------------ MCP helpers ------------------
    @property
    def mcp_enabled(self) -> bool:
        """True if the MCP server is set up and mounted."""
        return self._mcp is not None

    def mcp_mount(self,
                  *,
                  transport: Literal["http", "sse"] = "http",
                  mount_path: str = "/mcp",
                  ) -> None:
        """Rescan app routes and update MCP tools after new endpoints are added."""
        if not self._mcp:
            raise RuntimeError("MCP is not enabled.")
        self._mcp
        self._mcp_transport = transport
        self._mcp_mount_path = mount_path
        # Mount using selected transport and path.
        if transport == "http":
            # Recommended by the docs (Streamable HTTP).  # recommended = preferred
            self._mcp.mount_http(mount_path=mount_path)  # uses the app passed to FastApiMCP(...)
        else:
            self._mcp.mount_sse(mount_path=mount_path)

    def mcp_refresh(self) -> None:
        """Rescan app routes and update MCP tools after new endpoints are added."""
        if not self._mcp:
            raise RuntimeError("MCP is not enabled.")
        # Refresh the MCP server to include the new endpoint
        self._mcp.setup_server()

    def mcp_client_config(self, *, url: Optional[str] = None) -> Dict[str, Any]:
        """Return a minimal client config JSON for common MCP clients.

        If `url` is not provided, defaults to "http://localhost:8000{mount_path}".
        """
        if not self._mcp:
            raise RuntimeError("MCP is not enabled.")
        return {
            "mcpServers": {
                "air": {
                    "url": url or f"http://localhost:8000{self._mcp_mount_path}",
                }
            }
        }

    # -------------------------------------------------

    def page(self, func: Callable[..., Any]) -> Callable[..., Any]:
        """Decorator that creates a GET route using the function name as the path.

        If the name of the function is "index", the route is "/".
        """
        route_name: str = "/" if func.__name__ == "index" else f"/{func.__name__}"
        return self.get(route_name)(func)


def default_404_exception_handler(request: Request, exc: Exception) -> AirResponse:
    return AirResponse(
        mvpcss(
            Title("404 Not Found"),
            H1("404 Not Found"),
            P("The requested resource was not found on this server."),
            P(f"URL: {request.url}"),
            htmx=False,
        ),
        status_code=404,
    )


def default_500_exception_handler(request: Request, exc: Exception) -> AirResponse:
    return AirResponse(
        mvpcss(
            Title("500 Internal Server Error"),
            H1("500 Internal Server Error"),
            P("An internal server error occurred."),
            htmx=False,
        ),
        status_code=500,
    )
