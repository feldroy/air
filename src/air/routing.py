"""Use routing if you want a single cohesive app where all routes share middlewares and error handling."""

import inspect
from collections.abc import Callable, Sequence
from enum import Enum
from functools import wraps
from types import FunctionType
from typing import (
    Annotated,
    Any,
    Literal,
    Protocol,
    TypedDict,
    Unpack,
    get_type_hints,
    override,
)
from urllib.parse import urlencode
from warnings import deprecated as warnings_deprecated

import fastapi.encoders
from fastapi import params
from fastapi.params import Depends
from fastapi.routing import APIRoute, APIRouter
from starlette.responses import Response
from starlette.routing import (
    BaseRoute,
)
from starlette.types import ASGIApp, Lifespan
from typing_extensions import Doc

from .exception_handlers import default_404_router_handler
from .requests import AirRequest
from .responses import AirResponse
from .tags.models.base import BaseTag
from .utils import cached_signature, cached_unwrap, compute_page_path, default_generate_unique_id

# Register BaseTag in FastAPI's encoder so jsonable_encoder calls str(tag)
# instead of vars(tag). This eliminates the need for endpoint wrappers.
fastapi.encoders.ENCODERS_BY_TYPE[BaseTag] = str
fastapi.encoders.encoders_by_class_tuples = fastapi.encoders.generate_encoders_by_class_tuples(
    fastapi.encoders.ENCODERS_BY_TYPE
)


class RouteCallable(Protocol):
    """Protocol for route functions.

    This protocol represents the interface of functions after being decorated
    by route decorators like @app.get(), @app.post(), or @app.page(). The decorator
    adds a .url() method to the function, allowing programmatic URL generation.

    Example:
        @app.get("/users/{user_id}")
        def get_user(user_id: int) -> air.H1:
            return air.H1(f"User {user_id}")

        # The decorated function now has a .url() method
        url = get_user.url(user_id=123)  # Returns: "/users/123"
    """

    __call__: Callable[..., Any]
    __name__: str

    def url(self, **path_params: Any) -> str:
        return ""


# Type alias matching FastAPI's IncEx for response_model include/exclude
_IncEx = set[int] | set[str] | dict[int, Any] | dict[str, Any]


class RouteKwargs(TypedDict, total=False):
    """Keyword arguments for Air's HTTP method decorators (get, post, etc.).

    These are forwarded directly to FastAPI's path operation methods.
    Every field is optional; omitted fields use FastAPI's defaults.

    Reference: https://fastapi.tiangolo.com/reference/apirouter/
    """

    status_code: int | None
    tags: list[str | Enum] | None
    dependencies: Sequence[Depends] | None
    summary: str | None
    description: str | None
    response_description: str
    responses: dict[int | str, dict[str, Any]] | None
    deprecated: bool | None
    operation_id: str | None
    response_model_include: _IncEx | None
    response_model_exclude: _IncEx | None
    response_model_by_alias: bool
    response_model_exclude_unset: bool
    response_model_exclude_defaults: bool
    response_model_exclude_none: bool
    include_in_schema: bool
    response_class: type[Response]
    name: str | None
    callbacks: list[BaseRoute] | None
    openapi_extra: dict[str, Any] | None
    generate_unique_id_function: Callable[[APIRoute], str]


class AirRoute(APIRoute):
    """Custom APIRoute that uses Air's custom AirRequest class."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Initialize AirRoute and resolve string annotations from PEP 563."""

        endpoint = kwargs.get("endpoint") or (args[1] if len(args) > 1 else None)

        if endpoint is not None:
            original = cached_unwrap(endpoint)
            resolved_hints = get_type_hints(original, include_extras=True)
            sig = cached_signature(endpoint)
            endpoint.__signature__ = sig.replace(
                parameters=[
                    param.replace(annotation=resolved_hints.get(name, param.annotation))
                    for name, param in sig.parameters.items()
                ],
                return_annotation=resolved_hints.get("return", sig.return_annotation),
            )

        super().__init__(*args, **kwargs)

    @override
    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Any) -> Response:
            request = AirRequest(request.scope, request.receive)
            return await original_route_handler(request)

        return custom_route_handler


class RouterMixin:
    path_separator: Literal["/", "-"]

    @property
    def _target(self) -> Any:
        """The underlying FastAPI or APIRouter instance."""
        raise NotImplementedError

    def url_path_for(self, name: str, /, **params: Any) -> str:
        """Stub for type checking - implemented by subclasses."""
        raise NotImplementedError

    def _wrap_endpoint(
        self,
        func: Callable[..., Any],
        response_class: type[Response],
    ) -> Callable[..., Any]:
        """Wrap func to convert non-Response returns using response_class.

        Preserves the original sync/async nature so FastAPI dispatches
        sync handlers to a threadpool instead of blocking the event
        loop (#1067).

        Returns:
            A wrapped endpoint function with the same sync/async signature.
        """
        if inspect.iscoroutinefunction(func):

            @wraps(func)
            async def endpoint(*args: Any, **kw: Any) -> Response:
                result = await func(*args, **kw)
                if isinstance(result, Response):
                    return result
                return response_class(result)

        else:

            @wraps(func)
            def endpoint(*args: Any, **kw: Any) -> Response:
                result = func(*args, **kw)
                if isinstance(result, Response):
                    return result
                return response_class(result)

        return endpoint

    # =========================================================================
    # Route Decorators
    # =========================================================================

    def get(self, path: str, **kwargs: Unpack[RouteKwargs]) -> Callable[[Callable[..., Any]], RouteCallable]:
        """Register a GET route. The decorated function can return Air tags
        (``air.H1("Hello")``), strings, or Response objects. Tags and strings
        are automatically rendered as HTML responses. Sync handlers run in a
        threadpool; async handlers run on the event loop.

        The decorated function gains a ``.url()`` method for reverse URL
        generation: ``my_handler.url(user_id=42)`` returns ``"/users/42"``.

        Accepts all FastAPI path operation kwargs (``status_code``, ``tags``,
        ``dependencies``, etc.) via ``**kwargs``.

        Example::

            @app.get("/users/{user_id}")
            def user_profile(user_id: int) -> air.Div:
                return air.Div(air.H1(f"User {user_id}"))


            user_profile.url(user_id=42)  # "/users/42"
        """
        return self._route("get", path, **kwargs)

    def post(self, path: str, **kwargs: Unpack[RouteKwargs]) -> Callable[[Callable[..., Any]], RouteCallable]:
        """Register a POST route. The decorated function can return Air tags,
        strings, or Response objects. Tags and strings are automatically
        rendered as HTML responses. Sync handlers run in a threadpool; async
        handlers run on the event loop.

        For form handling, use ``await request.form()`` or Air's
        ``AirForm.from_request(request)`` to access submitted data. Return a
        ``RedirectResponse`` after successful processing to follow the
        Post/Redirect/Get pattern.

        The decorated function gains a ``.url()`` method for reverse URL
        generation, useful as a form ``action``::

            @app.post("/submit")
            async def submit(request: air.Request) -> air.Div:
                form_data = await request.form()
                return air.Div(air.P("Received!"))


            air.Form(..., method="post", action=submit.url())
        """
        return self._route("post", path, **kwargs)

    def put(self, path: str, **kwargs: Unpack[RouteKwargs]) -> Callable[[Callable[..., Any]], RouteCallable]:
        """Register a PUT route. The decorated function can return Air tags,
        strings, or Response objects. Tags and strings are automatically
        rendered as HTML responses. Sync handlers run in a threadpool; async
        handlers run on the event loop.

        The decorated function gains a ``.url()`` method for reverse URL
        generation: ``update_user.url(user_id=42)`` returns ``"/users/42"``.

        Accepts all FastAPI path operation kwargs (``status_code``, ``tags``,
        ``dependencies``, etc.) via ``**kwargs``.

        Example::

            @app.put("/users/{user_id}")
            def update_user(user_id: int, user: UserUpdate) -> air.Div:
                return air.Div(air.P(f"Updated user {user_id}"))
        """
        return self._route("put", path, **kwargs)

    def patch(self, path: str, **kwargs: Unpack[RouteKwargs]) -> Callable[[Callable[..., Any]], RouteCallable]:
        """Register a PATCH route. The decorated function can return Air tags,
        strings, or Response objects. Tags and strings are automatically
        rendered as HTML responses. Sync handlers run in a threadpool; async
        handlers run on the event loop.

        Commonly used with HTMX for partial page updates, where the handler
        returns an HTML fragment rather than a full page.

        The decorated function gains a ``.url()`` method for reverse URL
        generation. Accepts all FastAPI path operation kwargs via ``**kwargs``.

        Example::

            @app.patch("/users/{user_id}")
            def patch_user(user_id: int) -> air.Span:
                return air.Span(f"Updated field for user {user_id}")
        """
        return self._route("patch", path, **kwargs)

    def delete(self, path: str, **kwargs: Unpack[RouteKwargs]) -> Callable[[Callable[..., Any]], RouteCallable]:
        """Register a DELETE route. The decorated function can return Air tags,
        strings, or Response objects. Tags and strings are automatically
        rendered as HTML responses. Sync handlers run in a threadpool; async
        handlers run on the event loop.

        The decorated function gains a ``.url()`` method for reverse URL
        generation. Accepts all FastAPI path operation kwargs via ``**kwargs``.

        Example::

            @app.delete("/items/{item_id}")
            def delete_item(item_id: int) -> air.H1:
                return air.H1(f"Deleted item {item_id}")
        """
        return self._route("delete", path, **kwargs)

    def _route(self, method: str, path: str, **kwargs: Any) -> Callable[[Callable[..., Any]], RouteCallable]:
        """Shared implementation for all HTTP method decorators.

        Returns:
            A decorator that registers the function as a route.
        """
        name = kwargs.get("name")
        response_class = kwargs.pop("response_class", AirResponse)

        def decorator(func: Callable[..., Any]) -> RouteCallable:
            endpoint = self._wrap_endpoint(func, response_class)
            register = getattr(self._target, method)
            decorated = register(path, response_model=None, response_class=response_class, **kwargs)(endpoint)
            decorated.url = self._url_helper(name or getattr(func, "__name__", "unknown"))
            return decorated

        return decorator

    def page(self, func: FunctionType) -> RouteCallable:
        """Decorator that creates a GET route using the function name as the path.

        Underscores in the function name are converted to dashes in the URL.
        If the name of the function is "index", then the route is "/".

        Returns:
            The decorated function registered as a page route.

        Example:

            import air

            app = air.Air()
            router = air.AirRouter()


            @app.page
            def index() -> air.H1:  # route is "/"
                return air.H1("I am the home page")


            @router.page
            def data() -> air.H1:  # route is "/data"
                return air.H1("I am the data page")


            @router.page
            def about_us() -> air.H1:  # route is "/about-us"
                return air.H1("I am the about page")


            app.include_router(router)
        """
        page_path = compute_page_path(func.__name__, separator=self.path_separator)

        # Pin the route's response_class for belt-and-suspenders robustness
        return self.get(page_path)(func)

    def _url_helper(self, name: str) -> Callable[..., str]:
        """Helper function to generate URLs for route operations.

        Creates a callable that generates URLs for a specific route by wrapping
        Starlette's `url_path_for` method.

        Args:
            name: The route operation name (usually the function name or custom name).

        Returns:
            A function that accepts **params (path parameters) and optional
            `query_params` to return the generated URL string.

        Raises:
            NoMatchFound: If the route name doesn't exist or if the provided parameters
                don't match the route's path parameters.

        Example:
            @app.get("/users/{user_id}")
            def get_user(user_id: int):
                return air.H1(f"User {user_id}")

            # The .url() method is created by this helper
            url = get_user.url(user_id=123)  # Returns: "/users/123"
            url_with_query = get_user.url(user_id=123, query_params={"page": 2})
            # Returns: "/users/123?page=2"
        """  # noqa: DOC502

        def helper_function(**params: Any) -> str:
            query_params = params.pop("query_params", None)
            path = self.url_path_for(name, **params)

            if query_params is None:
                return path

            query_string = urlencode(query_params, doseq=True)
            if not query_string:
                return path
            return f"{path}?{query_string}"

        return helper_function


class AirRouter(RouterMixin):
    """
    `AirRouter` class, used to group *path operations*, for example to structure
    an app in multiple files. It would then be included in the `App` app, or
    in another `AirRouter` (ultimately included in the app).

    Example

        ```python
        import air

        app = air.Air()
        router = air.AirRouter()


        @router.get("/users/", tags=["users"])
        async def read_users():
            return [{"username": "Rick"}, {"username": "Morty"}]


        app.include_router(router)
        ```
    """

    def __init__(
        self,
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
            Sequence[params.Depends] | None,
            Doc(
                """
                A list of dependencies (using `Depends()`) to be applied to all the
                *path operations* in this router.

                Read more about it in the
                [FastAPI docs for Bigger Applications - Multiple Files](https://fastapi.tiangolo.com/tutorial/bigger-applications/#include-an-apirouter-with-a-custom-prefix-tags-responses-and-dependencies).
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
                """
            ),
        ] = AirResponse,
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
        callbacks: Annotated[
            list[BaseRoute] | None,
            Doc(
                """
                OpenAPI callbacks that should apply to all *path operations* in this
                router.

                It will be added to the generated OpenAPI (e.g. visible at `/docs`).

                Read more about it in the
                [FastAPI docs for OpenAPI Callbacks](https://fastapi.tiangolo.com/advanced/openapi-callbacks/).
                """
            ),
        ] = None,
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
            warnings_deprecated(
                """
                You normally wouldn't use this parameter with FastAPI, it is inherited
                from Starlette and supported for compatibility.

                In FastAPI, you normally would use the *path operation methods*,
                like `router.get()`, `router.post()`, etc.
                """
            ),
        ] = None,
        redirect_slashes: Annotated[
            bool,
            Doc(
                """
                Whether to detect and redirect slashes in URLs when the client doesn't
                use the same format.
                """
            ),
        ] = True,
        default: Annotated[
            ASGIApp | None,
            Doc(
                """
                Default function handler for this router. Used to handle
                404 Not Found errors.
                """
            ),
        ] = None,
        dependency_overrides_provider: Annotated[
            Any | None,
            Doc(
                """
                Only used internally by FastAPI to handle dependency overrides.

                You shouldn't need to use it. It normally points to the `FastAPI` app
                object.
                """
            ),
        ] = None,
        route_class: Annotated[
            type[AirRoute],
            Doc(
                """
                Custom route (*path operation*) class to be used by this router.

                Read more about it in the
                [FastAPI docs for Custom Request and APIRoute class](https://fastapi.tiangolo.com/how-to/custom-request-and-route/#custom-apiroute-class-in-a-router).
                """
            ),
        ] = AirRoute,
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
        # the generic to Lifespan[AppType] is the type of the top level application
        # which the router cannot know statically, so we use typing.Any
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
        deprecated: Annotated[
            bool | None,
            Doc(
                """
                Mark all *path operations* in this router as deprecated.

                It will be added to the generated OpenAPI (e.g. visible at `/docs`).

                Read more about it in the
                [FastAPI docs for Path Operation Configuration](https://fastapi.tiangolo.com/tutorial/path-operation-configuration/).
                """
            ),
        ] = None,
        include_in_schema: Annotated[
            bool,
            Doc(
                """
                To include (or not) all the *path operations* in this router in the
                generated OpenAPI.

                This affects the generated OpenAPI (e.g. visible at `/docs`).

                Read more about it in the
                [FastAPI docs for Query Parameters and String Validations](https://fastapi.tiangolo.com/tutorial/query-params-str-validations/#exclude-parameters-from-openapi).
                """
            ),
        ] = True,
        generate_unique_id_function: Annotated[
            Callable[[APIRoute], str],
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
        path_separator: Annotated[Literal["/", "-"], Doc("An optional path separator.")] = "-",
    ) -> None:
        self.path_separator = path_separator
        if default is None:
            default = default_404_router_handler(prefix or "router")

        # Validate prefix before creating router
        if prefix:
            assert prefix.startswith("/"), "A path prefix must start with '/'"
            assert not prefix.endswith("/"), "A path prefix must not end with '/' except for the root path"

        # Create internal router using composition
        self._router = APIRouter(
            prefix=prefix,
            tags=tags,
            dependencies=dependencies,
            default_response_class=default_response_class,
            responses=responses,
            callbacks=callbacks,
            routes=routes,
            redirect_slashes=redirect_slashes,
            default=default,
            dependency_overrides_provider=dependency_overrides_provider,
            route_class=route_class,
            on_startup=on_startup,
            on_shutdown=on_shutdown,
            lifespan=lifespan,
            deprecated=deprecated,
            include_in_schema=include_in_schema,
            generate_unique_id_function=generate_unique_id_function,
        )

    @property
    def _target(self) -> APIRouter:
        return self._router

    # =========================================================================
    # Proxy Properties - expose APIRouter attributes for include_router() compatibility
    # =========================================================================

    @property
    def routes(self) -> list[BaseRoute]:
        return self._router.routes

    @property
    def prefix(self) -> str:
        return self._router.prefix

    @property
    def tags(self) -> list[str | Enum] | None:
        return self._router.tags

    @property
    def dependencies(self) -> Sequence[params.Depends] | None:
        return self._router.dependencies

    @property
    def responses(self) -> dict[int | str, dict[str, Any]] | None:
        return self._router.responses

    @property
    def callbacks(self) -> list[BaseRoute] | None:
        return self._router.callbacks

    @property
    def deprecated(self) -> bool | None:
        return self._router.deprecated

    @property
    def include_in_schema(self) -> bool:
        return self._router.include_in_schema

    @property
    def default_response_class(self) -> type[Response]:
        return self._router.default_response_class

    @property
    def default(self) -> ASGIApp | None:
        return self._router.default

    @property
    def redirect_slashes(self) -> bool:
        return self._router.redirect_slashes

    @property
    def route_class(self) -> type[APIRoute]:
        return self._router.route_class

    @property
    def on_startup(self) -> list[Callable[[], Any]]:
        return self._router.on_startup

    @property
    def on_shutdown(self) -> list[Callable[[], Any]]:
        return self._router.on_shutdown

    @property
    def lifespan_context(self) -> Any:
        return self._router.lifespan_context

    @property
    def dependency_overrides_provider(self) -> Any | None:
        return self._router.dependency_overrides_provider

    @property
    def generate_unique_id_function(self) -> Callable[[APIRoute], str]:
        return self._router.generate_unique_id_function

    async def __call__(self, scope: Any, receive: Any, send: Any) -> None:
        await self._router(scope, receive, send)

    def url_path_for(self, name: str, /, **path_params: Any) -> str:
        return str(self._router.url_path_for(name, **path_params))
