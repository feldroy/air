Routing

If you need to knit several Python modules with their own Air views into one, that's where Routing is used. They allow the near seamless combination of multiple Air apps into one. Larger sites are often built from multiple routers.

Let's imagine we have an e-commerce store with a shopping cart app. Use instantiate a `router` object using `air.AirRouter()` just as we would with `air.App()`:

```
# cart.py
import air

router = air.AirRouter()


@router.page
def cart():
    return air.H1("I am a shopping cart")
```

Then in our main page we can load that and tie it into our main `app`.

```
import air
from cart import router as cart_router

app = air.Air()
app.include_router(cart_router)


@app.page
def index():
    return air.H1("Home page")
```

Note that the router allows sharing of sessions and other application states.

In addition, we can add links through the `.url()` method available on route functions, which generates URLs programmatically:

```
import air
from cart import router as cart_router, cart

app = air.Air()
app.include_router(cart_router)


@app.page
def index():
    return air.Div(air.H1("Home page"), air.A("View cart", href=cart.url()))
```

## Query Parameters

Air supports query parameters through FastAPI's `Query()` validator, which you can import as `air.Query()`:

```
import air

app = air.Air()


@app.get("/search")
def search(q: str = air.Query(""), page: int = air.Query(1)):
    return air.H1(f"Search: {q} (page {page})")


# Generate URLs with query parameters
@app.page
def index():
    return air.Div(
        air.A("Search", href=search.url(query_params={"q": "air", "page": 1}))
    )
```

The `.url()` method accepts a `query_params` argument for generating URLs with query strings. This works with both scalar values and lists:

```
@app.get("/filter")
def filter_items(
    tags: list[str] | None = air.Query(None),
):  # List parameters require explicit air.Query(None) for parsing
    return air.H1(f"Filtered by: {tags}")


# Generates: /filter?tags=python&tags=web
url = filter_items.url(query_params={"tags": ["python", "web"]})
```

______________________________________________________________________

Use routing if you want a single cohesive app where all routes share middlewares and error handling.

## AirRoute

```
AirRoute(*args, **kwargs)
```

Bases: `APIRoute`

Custom APIRoute that uses Air's custom AirRequest class.

Source code in `src/air/routing.py`

```
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
```

## AirRouter

```
AirRouter(
    *,
    prefix="",
    tags=None,
    dependencies=None,
    default_response_class=AirResponse,
    responses=None,
    callbacks=None,
    routes=None,
    redirect_slashes=True,
    default=None,
    dependency_overrides_provider=None,
    route_class=AirRoute,
    on_startup=None,
    on_shutdown=None,
    lifespan=None,
    deprecated=None,
    include_in_schema=True,
    generate_unique_id_function=default_generate_unique_id,
    path_separator="-",
)
```

Bases: `RouterMixin`

`AirRouter` class, used to group *path operations*, for example to structure an app in multiple files. It would then be included in the `App` app, or in another `AirRouter` (ultimately included in the app).

Example

````
```python
import air

app = air.Air()
router = air.AirRouter()


@router.get("/users/", tags=["users"])
async def read_users():
    return [{"username": "Rick"}, {"username": "Morty"}]


app.include_router(router)
````

```

Source code in `src/air/routing.py`

```

def __init__( self, \*, prefix: Annotated[str, Doc("An optional path prefix for the router.")] = "", tags: Annotated\[ list[str | Enum] | None, Doc( """ A list of tags to be applied to all the *path operations* in this router.

```
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
```

) -> None: self.path_separator = path_separator if default is None: default = default_404_router_handler(prefix or "router")

```
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
```

```

### delete

```

delete( path, \*, status_code=None, tags=None, dependencies=None, summary=None, description=None, response_description="Successful Response", responses=None, deprecated=None, operation_id=None, include_in_schema=True, response_class=AirResponse, name=None, callbacks=None, openapi_extra=None, generate_unique_id_function=generate_unique_id, )

```

Add a *path operation* using an HTTP DELETE operation.

Returns:

| Type | Description |
| --- | --- |
| `Callable[[Callable[..., Any]], Callable[..., Any]]` | A decorator function that registers the decorated function as a DELETE endpoint. |

Source code in `src/air/routing.py`

```

def delete( self, path: Annotated\[ str, Doc( """ The URL path to be used for this *path operation*.

```
        For example, in `http://example.com/items`, the path is `/items`.
        """
    ),
],
*,
status_code: Annotated[
    int | None,
    Doc(
        """
        The default status code to be used for the response.

        You could override the status code by returning a response directly.

        Read more about it in the
        [FastAPI docs for Response Status Code](https://fastapi.tiangolo.com/tutorial/response-status-code/).
        """
    ),
] = None,
tags: Annotated[
    list[str | Enum] | None,
    Doc(
        """
        A list of tags to be applied to the *path operation*.

        It will be added to the generated OpenAPI (e.g. visible at `/docs`).

        Read more about it in the
        [FastAPI docs for Path Operation Configuration](https://fastapi.tiangolo.com/tutorial/path-operation-configuration/#tags).
        """
    ),
] = None,
dependencies: Annotated[
    Sequence[params.Depends] | None,
    Doc(
        """
        A list of dependencies (using `Depends()`) to be applied to the
        *path operation*.

        Read more about it in the
        [FastAPI docs for Dependencies in path operation decorators](https://fastapi.tiangolo.com/tutorial/dependencies/dependencies-in-path-operation-decorators/).
        """
    ),
] = None,
summary: Annotated[
    str | None,
    Doc(
        """
        A summary for the *path operation*.

        It will be added to the generated OpenAPI (e.g. visible at `/docs`).

        Read more about it in the
        [FastAPI docs for Path Operation Configuration](https://fastapi.tiangolo.com/tutorial/path-operation-configuration/).
        """
    ),
] = None,
description: Annotated[
    str | None,
    Doc(
        """
        A description for the *path operation*.

        If not provided, it will be extracted automatically from the docstring
        of the *path operation function*.

        It can contain Markdown.

        It will be added to the generated OpenAPI (e.g. visible at `/docs`).

        Read more about it in the
        [FastAPI docs for Path Operation Configuration](https://fastapi.tiangolo.com/tutorial/path-operation-configuration/).
        """
    ),
] = None,
response_description: Annotated[
    str,
    Doc(
        """
        The description for the default response.

        It will be added to the generated OpenAPI (e.g. visible at `/docs`).
        """
    ),
] = "Successful Response",
responses: Annotated[
    dict[int | str, dict[str, Any]] | None,
    Doc(
        """
        Additional responses that could be returned by this *path operation*.

        It will be added to the generated OpenAPI (e.g. visible at `/docs`).
        """
    ),
] = None,
deprecated: Annotated[
    bool | None,
    Doc(
        """
        Mark this *path operation* as deprecated.

        It will be added to the generated OpenAPI (e.g. visible at `/docs`).
        """
    ),
] = None,
operation_id: Annotated[
    str | None,
    Doc(
        """
        Custom operation ID to be used by this *path operation*.

        By default, it is generated automatically.

        If you provide a custom operation ID, you need to make sure it is
        unique for the whole API.

        You can customize the
        operation ID generation with the parameter
        `generate_unique_id_function` in the `FastAPI` class.

        Read more about it in the
        [FastAPI docs about how to Generate Clients](https://fastapi.tiangolo.com/advanced/generate-clients/#custom-generate-unique-id-function).
        """
    ),
] = None,
include_in_schema: Annotated[
    bool,
    Doc(
        """
        Include this *path operation* in the generated OpenAPI schema.

        This affects the generated OpenAPI (e.g. visible at `/docs`).

        Read more about it in the
        [FastAPI docs for Query Parameters and String Validations](https://fastapi.tiangolo.com/tutorial/query-params-str-validations/#exclude-from-openapi).
        """
    ),
] = True,
response_class: Annotated[
    type[Response],
    Doc(
        """
        Response class to be used for this *path operation*.

        This will not be used if you return a response directly.

        Read more about it in the
        [FastAPI docs for Custom Response - HTML, Stream, File, others](https://fastapi.tiangolo.com/advanced/custom-response/#redirectresponse).
        """
    ),
] = AirResponse,
name: Annotated[
    str | None,
    Doc(
        """
        Name for this *path operation*. Only used internally.
        """
    ),
] = None,
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
openapi_extra: Annotated[
    dict[str, Any] | None,
    Doc(
        """
        Extra metadata to be included in the OpenAPI schema for this *path
        operation*.

        Read more about it in the
        [FastAPI docs for Path Operation Advanced Configuration](https://fastapi.tiangolo.com/advanced/path-operation-advanced-configuration/#custom-openapi-path-operation-schema).
        """
    ),
] = None,
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
] = generate_unique_id,
```

) -> Callable\[\[Callable[..., Any]\], Callable[..., Any]\]: """ Add a *path operation* using an HTTP DELETE operation.

```
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

    decorated = self._router.delete(
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
```

```

### get

```

get( path, \*, status_code=None, tags=None, dependencies=None, summary=None, description=None, response_description="Successful Response", responses=None, deprecated=None, operation_id=None, include_in_schema=True, response_class=AirResponse, name=None, callbacks=None, openapi_extra=None, generate_unique_id_function=generate_unique_id, )

```

Add a *path operation* using an HTTP GET operation.

Returns:

| Type | Description |
| --- | --- |
| `Callable[[Callable[..., Any]], Callable[..., Any]]` | A decorator function that registers the decorated function as a GET endpoint. |

##### Example

```

from air import Air, AirRouter

app = Air() router = AirRouter()

@app.get("/hello") def hello_world(): return air.H1("Hello, World!")

app.include_router(router)

```

Source code in `src/air/routing.py`

```

def get( self, path: Annotated\[ str, Doc( """ The URL path to be used for this *path operation*.

```
        For example, in `http://example.com/items`, the path is `/items`.
        """
    ),
],
*,
status_code: Annotated[
    int | None,
    Doc(
        """
        The default status code to be used for the response.

        You could override the status code by returning a response directly.

        Read more about it in the
        [FastAPI docs for Response Status Code](https://fastapi.tiangolo.com/tutorial/response-status-code/).
        """
    ),
] = None,
tags: Annotated[
    list[str | Enum] | None,
    Doc(
        """
        A list of tags to be applied to the *path operation*.

        It will be added to the generated OpenAPI (e.g. visible at `/docs`).

        Read more about it in the
        [FastAPI docs for Path Operation Configuration](https://fastapi.tiangolo.com/tutorial/path-operation-configuration/#tags).
        """
    ),
] = None,
dependencies: Annotated[
    Sequence[params.Depends] | None,
    Doc(
        """
        A list of dependencies (using `Depends()`) to be applied to the
        *path operation*.

        Read more about it in the
        [FastAPI docs for Dependencies in path operation decorators](https://fastapi.tiangolo.com/tutorial/dependencies/dependencies-in-path-operation-decorators/).
        """
    ),
] = None,
summary: Annotated[
    str | None,
    Doc(
        """
        A summary for the *path operation*.

        It will be added to the generated OpenAPI (e.g. visible at `/docs`).

        Read more about it in the
        [FastAPI docs for Path Operation Configuration](https://fastapi.tiangolo.com/tutorial/path-operation-configuration/).
        """
    ),
] = None,
description: Annotated[
    str | None,
    Doc(
        """
        A description for the *path operation*.

        If not provided, it will be extracted automatically from the docstring
        of the *path operation function*.

        It can contain Markdown.

        It will be added to the generated OpenAPI (e.g. visible at `/docs`).

        Read more about it in the
        [FastAPI docs for Path Operation Configuration](https://fastapi.tiangolo.com/tutorial/path-operation-configuration/).
        """
    ),
] = None,
response_description: Annotated[
    str,
    Doc(
        """
        The description for the default response.

        It will be added to the generated OpenAPI (e.g. visible at `/docs`).
        """
    ),
] = "Successful Response",
responses: Annotated[
    dict[int | str, dict[str, Any]] | None,
    Doc(
        """
        Additional responses that could be returned by this *path operation*.

        It will be added to the generated OpenAPI (e.g. visible at `/docs`).
        """
    ),
] = None,
deprecated: Annotated[
    bool | None,
    Doc(
        """
        Mark this *path operation* as deprecated.

        It will be added to the generated OpenAPI (e.g. visible at `/docs`).
        """
    ),
] = None,
operation_id: Annotated[
    str | None,
    Doc(
        """
        Custom operation ID to be used by this *path operation*.

        By default, it is generated automatically.

        If you provide a custom operation ID, you need to make sure it is
        unique for the whole API.

        You can customize the
        operation ID generation with the parameter
        `generate_unique_id_function` in the `FastAPI` class.

        Read more about it in the
        [FastAPI docs about how to Generate Clients](https://fastapi.tiangolo.com/advanced/generate-clients/#custom-generate-unique-id-function).
        """
    ),
] = None,
include_in_schema: Annotated[
    bool,
    Doc(
        """
        Include this *path operation* in the generated OpenAPI schema.

        This affects the generated OpenAPI (e.g. visible at `/docs`).

        Read more about it in the
        [FastAPI docs for Query Parameters and String Validations](https://fastapi.tiangolo.com/tutorial/query-params-str-validations/#exclude-parameters-from-openapi).
        """
    ),
] = True,
response_class: Annotated[
    type[Response],
    Doc(
        """
        Response class to be used for this *path operation*.

        This will not be used if you return a response directly.

        Read more about it in the
        [FastAPI docs for Custom Response - HTML, Stream, File, others](https://fastapi.tiangolo.com/advanced/custom-response/#redirectresponse).
        """
    ),
] = AirResponse,
name: Annotated[
    str | None,
    Doc(
        """
        Name for this *path operation*. Only used internally.
        """
    ),
] = None,
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
openapi_extra: Annotated[
    dict[str, Any] | None,
    Doc(
        """
        Extra metadata to be included in the OpenAPI schema for this *path
        operation*.

        Read more about it in the
        [FastAPI docs for Path Operation Advanced Configuration](https://fastapi.tiangolo.com/advanced/path-operation-advanced-configuration/#custom-openapi-path-operation-schema).
        """
    ),
] = None,
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
] = generate_unique_id,
```

) -> Callable\[\[Callable[..., Any]\], Callable[..., Any]\]: """ Add a *path operation* using an HTTP GET operation.

````
Returns:
    A decorator function that registers the decorated function as a GET endpoint.

## Example

```python
from air import Air, AirRouter

app = Air()
router = AirRouter()


@app.get("/hello")
def hello_world():
    return air.H1("Hello, World!")


app.include_router(router)
```
"""

def decorator[**P, R](func: Callable[P, MaybeAwaitable[R]]) -> RouteCallable:
    @wraps(func)
    async def endpoint(*args: P.args, **kw: P.kwargs) -> Response:
        result = func(*args, **kw)
        if inspect.isawaitable(result):
            result = await result
        if isinstance(result, Response):
            return result
        # Force HTML for non-Response results
        return response_class(result)

    decorated = self._router.get(
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
````

```

### patch

```

patch( path, \*, status_code=None, tags=None, dependencies=None, summary=None, description=None, response_description="Successful Response", responses=None, deprecated=None, operation_id=None, include_in_schema=True, response_class=AirResponse, name=None, callbacks=None, openapi_extra=None, generate_unique_id_function=generate_unique_id, )

```

Add a *path operation* using an HTTP PATCH operation.

Returns:

| Type | Description |
| --- | --- |
| `Callable[[Callable[..., Any]], Callable[..., Any]]` | A decorator function that registers the decorated function as a PATCH endpoint. |

Source code in `src/air/routing.py`

```

def patch( self, path: Annotated\[ str, Doc( """ The URL path to be used for this *path operation*.

```
        For example, in `http://example.com/items`, the path is `/items`.
        """
    ),
],
*,
status_code: Annotated[
    int | None,
    Doc(
        """
        The default status code to be used for the response.

        You could override the status code by returning a response directly.

        Read more about it in the
        [FastAPI docs for Response Status Code](https://fastapi.tiangolo.com/tutorial/response-status-code/).
        """
    ),
] = None,
tags: Annotated[
    list[str | Enum] | None,
    Doc(
        """
        A list of tags to be applied to the *path operation*.

        It will be added to the generated OpenAPI (e.g. visible at `/docs`).

        Read more about it in the
        [FastAPI docs for Path Operation Configuration](https://fastapi.tiangolo.com/tutorial/path-operation-configuration/#tags).
        """
    ),
] = None,
dependencies: Annotated[
    Sequence[Depends] | None,
    Doc(
        """
        A list of dependencies (using `Depends()`) to be applied to the
        *path operation*.

        Read more about it in the
        [FastAPI docs for Dependencies in path operation decorators](https://fastapi.tiangolo.com/tutorial/dependencies/dependencies-in-path-operation-decorators/).
        """
    ),
] = None,
summary: Annotated[
    str | None,
    Doc(
        """
        A summary for the *path operation*.

        It will be added to the generated OpenAPI (e.g. visible at `/docs`).

        Read more about it in the
        [FastAPI docs for Path Operation Configuration](https://fastapi.tiangolo.com/tutorial/path-operation-configuration/).
        """
    ),
] = None,
description: Annotated[
    str | None,
    Doc(
        """
        A description for the *path operation*.

        If not provided, it will be extracted automatically from the docstring
        of the *path operation function*.

        It can contain Markdown.

        It will be added to the generated OpenAPI (e.g. visible at `/docs`).

        Read more about it in the
        [FastAPI docs for Path Operation Configuration](https://fastapi.tiangolo.com/tutorial/path-operation-configuration/).
        """
    ),
] = None,
response_description: Annotated[
    str,
    Doc(
        """
        The description for the default response.

        It will be added to the generated OpenAPI (e.g. visible at `/docs`).
        """
    ),
] = "Successful Response",
responses: Annotated[
    dict[int | str, dict[str, Any]] | None,
    Doc(
        """
        Additional responses that could be returned by this *path operation*.

        It will be added to the generated OpenAPI (e.g. visible at `/docs`).
        """
    ),
] = None,
deprecated: Annotated[
    bool | None,
    Doc(
        """
        Mark this *path operation* as deprecated.

        It will be added to the generated OpenAPI (e.g. visible at `/docs`).
        """
    ),
] = None,
operation_id: Annotated[
    str | None,
    Doc(
        """
        Custom operation ID to be used by this *path operation*.

        By default, it is generated automatically.

        If you provide a custom operation ID, you need to make sure it is
        unique for the whole API.

        You can customize the
        operation ID generation with the parameter
        `generate_unique_id_function` in the `FastAPI` class.

        Read more about it in the
        [FastAPI docs about how to Generate Clients](https://fastapi.tiangolo.com/advanced/generate-clients/#custom-generate-unique-id-function).
        """
    ),
] = None,
include_in_schema: Annotated[
    bool,
    Doc(
        """
        Include this *path operation* in the generated OpenAPI schema.

        This affects the generated OpenAPI (e.g. visible at `/docs`).

        Read more about it in the
        [FastAPI docs for Query Parameters and String Validations](https://fastapi.tiangolo.com/tutorial/query-params-str-validations/#exclude-parameters-from-openapi).
        """
    ),
] = True,
response_class: Annotated[
    type[Response],
    Doc(
        """
        Response class to be used for this *path operation*.

        This will not be used if you return a response directly.

        Read more about it in the
        [FastAPI docs for Custom Response - HTML, Stream, File, others](https://fastapi.tiangolo.com/advanced/custom-response/#redirectresponse).
        """
    ),
] = AirResponse,
name: Annotated[
    str | None,
    Doc(
        """
        Name for this *path operation*. Only used internally.
        """
    ),
] = None,
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
openapi_extra: Annotated[
    dict[str, Any] | None,
    Doc(
        """
        Extra metadata to be included in the OpenAPI schema for this *path
        operation*.

        Read more about it in the
        [FastAPI docs for Path Operation Advanced Configuration](https://fastapi.tiangolo.com/advanced/path-operation-advanced-configuration/#custom-openapi-path-operation-schema).
        """
    ),
] = None,
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
] = generate_unique_id,
```

) -> Callable\[\[Callable[..., Any]\], Callable[..., Any]\]: """ Add a *path operation* using an HTTP PATCH operation.

```
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

    decorated = self._router.patch(
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
```

```

### post

```

post( path, \*, status_code=None, tags=None, dependencies=None, summary=None, description=None, response_description="Successful Response", responses=None, deprecated=None, operation_id=None, include_in_schema=True, response_class=AirResponse, name=None, callbacks=None, openapi_extra=None, generate_unique_id_function=generate_unique_id, )

```

Add a *path operation* using an HTTP POST operation.

Returns:

| Type | Description |
| --- | --- |
| `Callable[[Callable[..., Any]], Callable[..., Any]]` | A decorator function that registers the decorated function as a POST endpoint. |

Source code in `src/air/routing.py`

```

def post( self, path: Annotated\[ str, Doc( """ The URL path to be used for this *path operation*.

```
        For example, in `http://example.com/items`, the path is `/items`.
        """
    ),
],
*,
status_code: Annotated[
    int | None,
    Doc(
        """
        The default status code to be used for the response.

        You could override the status code by returning a response directly.

        Read more about it in the
        [FastAPI docs for Response Status Code](https://fastapi.tiangolo.com/tutorial/response-status-code/).
        """
    ),
] = None,
tags: Annotated[
    list[str | Enum] | None,
    Doc(
        """
        A list of tags to be applied to the *path operation*.

        It will be added to the generated OpenAPI (e.g. visible at `/docs`).

        Read more about it in the
        [FastAPI docs for Path Operation Configuration](https://fastapi.tiangolo.com/tutorial/path-operation-configuration/#tags).
        """
    ),
] = None,
dependencies: Annotated[
    Sequence[params.Depends] | None,
    Doc(
        """
        A list of dependencies (using `Depends()`) to be applied to the
        *path operation*.

        Read more about it in the
        [FastAPI docs for Dependencies in path operation decorators](https://fastapi.tiangolo.com/tutorial/dependencies/dependencies-in-path-operation-decorators/).
        """
    ),
] = None,
summary: Annotated[
    str | None,
    Doc(
        """
        A summary for the *path operation*.

        It will be added to the generated OpenAPI (e.g. visible at `/docs`).

        Read more about it in the
        [FastAPI docs for Path Operation Configuration](https://fastapi.tiangolo.com/tutorial/path-operation-configuration/).
        """
    ),
] = None,
description: Annotated[
    str | None,
    Doc(
        """
        A description for the *path operation*.

        If not provided, it will be extracted automatically from the docstring
        of the *path operation function*.

        It can contain Markdown.

        It will be added to the generated OpenAPI (e.g. visible at `/docs`).

        Read more about it in the
        [FastAPI docs for Path Operation Configuration](https://fastapi.tiangolo.com/tutorial/path-operation-configuration/).
        """
    ),
] = None,
response_description: Annotated[
    str,
    Doc(
        """
        The description for the default response.

        It will be added to the generated OpenAPI (e.g. visible at `/docs`).
        """
    ),
] = "Successful Response",
responses: Annotated[
    dict[int | str, dict[str, Any]] | None,
    Doc(
        """
        Additional responses that could be returned by this *path operation*.

        It will be added to the generated OpenAPI (e.g. visible at `/docs`).
        """
    ),
] = None,
deprecated: Annotated[
    bool | None,
    Doc(
        """
        Mark this *path operation* as deprecated.

        It will be added to the generated OpenAPI (e.g. visible at `/docs`).
        """
    ),
] = None,
operation_id: Annotated[
    str | None,
    Doc(
        """
        Custom operation ID to be used by this *path operation*.

        By default, it is generated automatically.

        If you provide a custom operation ID, you need to make sure it is
        unique for the whole API.

        You can customize the
        operation ID generation with the parameter
        `generate_unique_id_function` in the `FastAPI` class.

        Read more about it in the
        [FastAPI docs about how to Generate Clients](https://fastapi.tiangolo.com/advanced/generate-clients/#custom-generate-unique-id-function).
        """
    ),
] = None,
include_in_schema: Annotated[
    bool,
    Doc(
        """
        Include this *path operation* in the generated OpenAPI schema.

        This affects the generated OpenAPI (e.g. visible at `/docs`).

        Read more about it in the
        [FastAPI docs for Query Parameters and String Validations](https://fastapi.tiangolo.com/tutorial/query-params-str-validations/#exclude-parameters-from-openapi).
        """
    ),
] = True,
response_class: Annotated[
    type[Response],
    Doc(
        """
        Response class to be used for this *path operation*.

        This will not be used if you return a response directly.

        Read more about it in the
        [FastAPI docs for Custom Response - HTML, Stream, File, others](https://fastapi.tiangolo.com/advanced/custom-response/#redirectresponse).
        """
    ),
] = AirResponse,
name: Annotated[
    str | None,
    Doc(
        """
        Name for this *path operation*. Only used internally.
        """
    ),
] = None,
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
openapi_extra: Annotated[
    dict[str, Any] | None,
    Doc(
        """
        Extra metadata to be included in the OpenAPI schema for this *path
        operation*.

        Read more about it in the
        [FastAPI docs for Path Operation Advanced Configuration](https://fastapi.tiangolo.com/advanced/path-operation-advanced-configuration/#custom-openapi-path-operation-schema).
        """
    ),
] = None,
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
] = generate_unique_id,
```

) -> Callable\[\[Callable[..., Any]\], Callable[..., Any]\]: """ Add a *path operation* using an HTTP POST operation.

```
Returns:
    A decorator function that registers the decorated function as a POST endpoint.
"""

def decorator[**P, R](func: Callable[P, MaybeAwaitable[R]]) -> RouteCallable:
    @wraps(func)
    async def endpoint(*args: P.args, **kw: P.kwargs) -> Response:
        result = func(*args, **kw)
        if inspect.isawaitable(result):
            result = await result
        if isinstance(result, Response):
            return result
        # Force HTML for non-Response results
        return response_class(result)

    decorated = self._router.post(
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
```

```

### put

```

put( path, \*, status_code=None, tags=None, dependencies=None, summary=None, description=None, response_description="Successful Response", responses=None, deprecated=None, operation_id=None, include_in_schema=True, response_class=AirResponse, name=None, callbacks=None, openapi_extra=None, generate_unique_id_function=generate_unique_id, )

```

Add a *path operation* using an HTTP PUT operation.

Returns:

| Type | Description |
| --- | --- |
| `Callable[[Callable[..., Any]], Callable[..., Any]]` | A decorator function that registers the decorated function as a PUT endpoint. |

Source code in `src/air/routing.py`

```

def put( self, path: Annotated\[ str, Doc( """ The URL path to be used for this *path operation*.

```
        For example, in `http://example.com/items`, the path is `/items`.
        """
    ),
],
*,
status_code: Annotated[
    int | None,
    Doc(
        """
        The default status code to be used for the response.

        You could override the status code by returning a response directly.

        Read more about it in the
        [FastAPI docs for Response Status Code](https://fastapi.tiangolo.com/tutorial/response-status-code/).
        """
    ),
] = None,
tags: Annotated[
    list[str | Enum] | None,
    Doc(
        """
        A list of tags to be applied to the *path operation*.

        It will be added to the generated OpenAPI (e.g. visible at `/docs`).

        Read more about it in the
        [FastAPI docs for Path Operation Configuration](https://fastapi.tiangolo.com/tutorial/path-operation-configuration/#tags).
        """
    ),
] = None,
dependencies: Annotated[
    Sequence[Depends] | None,
    Doc(
        """
        A list of dependencies (using `Depends()`) to be applied to the
        *path operation*.

        Read more about it in the
        [FastAPI docs for Dependencies in path operation decorators](https://fastapi.tiangolo.com/tutorial/dependencies/dependencies-in-path-operation-decorators/).
        """
    ),
] = None,
summary: Annotated[
    str | None,
    Doc(
        """
        A summary for the *path operation*.

        It will be added to the generated OpenAPI (e.g. visible at `/docs`).

        Read more about it in the
        [FastAPI docs for Path Operation Configuration](https://fastapi.tiangolo.com/tutorial/path-operation-configuration/).
        """
    ),
] = None,
description: Annotated[
    str | None,
    Doc(
        """
        A description for the *path operation*.

        If not provided, it will be extracted automatically from the docstring
        of the *path operation function*.

        It can contain Markdown.

        It will be added to the generated OpenAPI (e.g. visible at `/docs`).

        Read more about it in the
        [FastAPI docs for Path Operation Configuration](https://fastapi.tiangolo.com/tutorial/path-operation-configuration/).
        """
    ),
] = None,
response_description: Annotated[
    str,
    Doc(
        """
        The description for the default response.

        It will be added to the generated OpenAPI (e.g. visible at `/docs`).
        """
    ),
] = "Successful Response",
responses: Annotated[
    dict[int | str, dict[str, Any]] | None,
    Doc(
        """
        Additional responses that could be returned by this *path operation*.

        It will be added to the generated OpenAPI (e.g. visible at `/docs`).
        """
    ),
] = None,
deprecated: Annotated[
    bool | None,
    Doc(
        """
        Mark this *path operation* as deprecated.

        It will be added to the generated OpenAPI (e.g. visible at `/docs`).
        """
    ),
] = None,
operation_id: Annotated[
    str | None,
    Doc(
        """
        Custom operation ID to be used by this *path operation*.

        By default, it is generated automatically.

        If you provide a custom operation ID, you need to make sure it is
        unique for the whole API.

        You can customize the
        operation ID generation with the parameter
        `generate_unique_id_function` in the `FastAPI` class.

        Read more about it in the
        [FastAPI docs about how to Generate Clients](https://fastapi.tiangolo.com/advanced/generate-clients/#custom-generate-unique-id-function).
        """
    ),
] = None,
include_in_schema: Annotated[
    bool,
    Doc(
        """
        Include this *path operation* in the generated OpenAPI schema.

        This affects the generated OpenAPI (e.g. visible at `/docs`).

        Read more about it in the
        [FastAPI docs for Query Parameters and String Validations](https://fastapi.tiangolo.com/tutorial/query-params-str-validations/#exclude-parameters-from-openapi).
        """
    ),
] = True,
response_class: Annotated[
    type[Response],
    Doc(
        """
        Response class to be used for this *path operation*.

        This will not be used if you return a response directly.

        Read more about it in the
        [FastAPI docs for Custom Response - HTML, Stream, File, others](https://fastapi.tiangolo.com/advanced/custom-response/#redirectresponse).
        """
    ),
] = AirResponse,
name: Annotated[
    str | None,
    Doc(
        """
        Name for this *path operation*. Only used internally.
        """
    ),
] = None,
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
openapi_extra: Annotated[
    dict[str, Any] | None,
    Doc(
        """
        Extra metadata to be included in the OpenAPI schema for this *path
        operation*.

        Read more about it in the
        [FastAPI docs for Path Operation Advanced Configuration](https://fastapi.tiangolo.com/advanced/path-operation-advanced-configuration/#custom-openapi-path-operation-schema).
        """
    ),
] = None,
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
] = generate_unique_id,
```

) -> Callable\[\[Callable[..., Any]\], Callable[..., Any]\]: """ Add a *path operation* using an HTTP PUT operation.

```
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

    decorated = self._router.put(
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
```

```

## RouteCallable

Bases: `Protocol`

Protocol for route functions.

This protocol represents the interface of functions after being decorated
by route decorators like @app.get(), @app.post(), or @app.page(). The decorator
adds a .url() method to the function, allowing programmatic URL generation.

Example

@app.get("/users/{user_id}")
def get_user(user_id: int) -> air.H1:
return air.H1(f"User {user_id}")

### The decorated function now has a .url() method

url = get_user.url(user_id=123) # Returns: "/users/123"

## RouterMixin

### get

```

get(\*args, \*\*kwargs)

```

Stub for type checking - implemented by subclasses.

Source code in `src/air/routing.py`

```

def get(self, \*args: Any, \*\*kwargs: Any) -> Any: """Stub for type checking - implemented by subclasses.""" raise NotImplementedError

```

### page

```

page(func)

```

Decorator that creates a GET route using the function name as the path.

Underscores in the function name are converted to dashes in the URL.
If the name of the function is "index", then the route is "/".

Returns:

| Type | Description |
| --- | --- |
| `RouteCallable` | The decorated function registered as a page route. |

Example:

```

import air

app = air.Air() router = air.AirRouter()

@app.page def index() -> air.H1: # route is "/" return air.H1("I am the home page")

@router.page def data() -> air.H1: # route is "/data" return air.H1("I am the data page")

@router.page def about_us() -> air.H1: # route is "/about-us" return air.H1("I am the about page")

app.include_router(router)

```

Source code in `src/air/routing.py`

```

def page(self, func: FunctionType) -> RouteCallable: """Decorator that creates a GET route using the function name as the path.

```
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
```

```

### url_path_for

```

url_path_for(name, /, \*\*params)

```

Stub for type checking - implemented by subclasses.

Source code in `src/air/routing.py`

```

def url_path_for(self, name: str, /, \*\*params: Any) -> str: """Stub for type checking - implemented by subclasses.""" raise NotImplementedError

```
```
