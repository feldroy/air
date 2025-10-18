Routing

If you need to knit several Python modules with their own Air views into one, that's where Routing is used. They allow the near seamless combination of multiple Air apps into one. Larger sites are often built from multiple routers.

Let's imagine we have an e-commerce store with a shopping cart app. Use instantiate a `router` object using `air.AirRouter()` just as we would with `air.App()`:

```
# cart.py
import air

router = air.AirRouter()

@router.page
def cart():
    return air.H1('I am a shopping cart')
```

Then in our main page we can load that and tie it into our main `app`.

```
import air
from cart import router as cart_router

app = air.Air()
app.include_router(cart_router)

@app.page
def index():
    return air.H1('Home page')
```

Note that the router allows sharing of sessions and other application states.

______________________________________________________________________

Use routing if you want a single cohesive app where all routes share middlewares and error handling.

## AirRoute

Bases: `APIRoute`

Custom APIRoute that uses Air's custom AirRequest class.

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

Bases: `APIRouter`

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
    deprecated(
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
    Callable[[AirRoute], str],
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

) -> None: self.path_separator = path_separator if default is None: default = default_404_router_handler super().__init__( prefix=prefix, tags=tags, dependencies=dependencies, default_response_class=default_response_class, responses=responses, callbacks=callbacks, routes=routes, redirect_slashes=redirect_slashes, default=default, dependency_overrides_provider=dependency_overrides_provider, route_class=route_class, on_startup=on_startup, on_shutdown=on_shutdown, lifespan=lifespan, deprecated=deprecated, include_in_schema=include_in_schema, generate_unique_id_function=generate_unique_id_function, ) if prefix: assert prefix.startswith("/"), "A path prefix must start with '/'" assert not prefix.endswith("/"), "A path prefix must not end with '/' except for the root path"

```

### get

```

get( path, \*, response_model=None, status_code=None, tags=None, dependencies=None, summary=None, description=None, response_description="Successful Response", responses=None, deprecated=None, operation_id=None, response_model_include=None, response_model_exclude=None, response_model_by_alias=True, response_model_exclude_unset=False, response_model_exclude_defaults=False, response_model_exclude_none=False, include_in_schema=True, response_class=AirResponse, name=None, callbacks=None, openapi_extra=None, generate_unique_id_function=generate_unique_id, )

```

Add a *path operation* using an HTTP GET operation.

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
response_model: Annotated[
    Any,
    Doc(
        """
        The type to use for the response.

        It could be any valid Pydantic *field* type. So, it doesn't have to
        be a Pydantic model, it could be other things, like a `list`, `dict`,
        etc.

        It will be used for:

        * Documentation: the generated OpenAPI (and the UI at `/docs`) will
            show it as the response (JSON Schema).
        * Serialization: you could return an arbitrary object and the
            `response_model` would be used to serialize that object into the
            corresponding JSON.
        * Filtering: the JSON sent to the client will only contain the data
            (fields) defined in the `response_model`. If you returned an object
            that contains an attribute `password` but the `response_model` does
            not include that field, the JSON sent to the client would not have
            that `password`.
        * Validation: whatever you return will be serialized with the
            `response_model`, converting any data as necessary to generate the
            corresponding JSON. But if the data in the object returned is not
            valid, that would mean a violation of the contract with the client,
            so it's an error from the API developer. So, FastAPI will raise an
            error and return a 500 error code (Internal Server Error).

        Read more about it in the
        [FastAPI docs for Response Model](https://fastapi.tiangolo.com/tutorial/response-model/).
        """
    ),
] = None,
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
response_model_include: Annotated[
    IncEx | None,
    Doc(
        """
        Configuration passed to Pydantic to include only certain fields in the
        response data.

        Read more about it in the
        [FastAPI docs for Response Model - Return Type](https://fastapi.tiangolo.com/tutorial/response-model/#response_model_include-and-response_model_exclude).
        """
    ),
] = None,
response_model_exclude: Annotated[
    IncEx | None,
    Doc(
        """
        Configuration passed to Pydantic to exclude certain fields in the
        response data.

        Read more about it in the
        [FastAPI docs for Response Model - Return Type](https://fastapi.tiangolo.com/tutorial/response-model/#response_model_include-and-response_model_exclude).
        """
    ),
] = None,
response_model_by_alias: Annotated[
    bool,
    Doc(
        """
        Configuration passed to Pydantic to define if the response model
        should be serialized by alias when an alias is used.

        Read more about it in the
        [FastAPI docs for Response Model - Return Type](https://fastapi.tiangolo.com/tutorial/response-model/#response_model_include-and-response_model_exclude).
        """
    ),
] = True,
response_model_exclude_unset: Annotated[
    bool,
    Doc(
        """
        Configuration passed to Pydantic to define if the response data
        should have all the fields, including the ones that were not set and
        have their default values. This is different from
        `response_model_exclude_defaults` in that if the fields are set,
        they will be included in the response, even if the value is the same
        as the default.

        When `True`, default values are omitted from the response.

        Read more about it in the
        [FastAPI docs for Response Model - Return Type](https://fastapi.tiangolo.com/tutorial/response-model/#use-the-response_model_exclude_unset-parameter).
        """
    ),
] = False,
response_model_exclude_defaults: Annotated[
    bool,
    Doc(
        """
        Configuration passed to Pydantic to define if the response data
        should have all the fields, including the ones that have the same value
        as the default. This is different from `response_model_exclude_unset`
        in that if the fields are set but contain the same default values,
        they will be excluded from the response.

        When `True`, default values are omitted from the response.

        Read more about it in the
        [FastAPI docs for Response Model - Return Type](https://fastapi.tiangolo.com/tutorial/response-model/#use-the-response_model_exclude_unset-parameter).
        """
    ),
] = False,
response_model_exclude_none: Annotated[
    bool,
    Doc(
        """
        Configuration passed to Pydantic to define if the response data should
        exclude fields set to `None`.

        This is much simpler (less smart) than `response_model_exclude_unset`
        and `response_model_exclude_defaults`. You probably want to use one of
        those two instead of this one, as those allow returning `None` values
        when it makes sense.

        Read more about it in the
        [FastAPI docs for Response Model - Return Type](https://fastapi.tiangolo.com/tutorial/response-model/#response_model_exclude_none).
        """
    ),
] = False,
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
    Callable[[AirRoute], str],
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

def decorator[**P, R](func: Callable[P, MaybeAwaitable[R]]) -> Callable[..., Any]:
    @wraps(func)
    async def endpoint(*args: P.args, **kw: P.kwargs) -> Response:
        result = func(*args, **kw)
        if inspect.isawaitable(result):
            result = await result
        if isinstance(result, Response):
            return result
        # Force HTML for non-Response results
        return response_class(result)

    return super(AirRouter, self).get(
        path,
        response_model=response_model,
        status_code=status_code,
        tags=tags,
        dependencies=dependencies,
        summary=summary,
        description=description,
        response_description=response_description,
        responses=responses,
        deprecated=deprecated,
        operation_id=operation_id,
        response_model_include=response_model_include,
        response_model_exclude=response_model_exclude,
        response_model_by_alias=response_model_by_alias,
        response_model_exclude_unset=response_model_exclude_unset,
        response_model_exclude_defaults=response_model_exclude_defaults,
        response_model_exclude_none=response_model_exclude_none,
        include_in_schema=include_in_schema,
        response_class=response_class,
        name=name,
        callbacks=callbacks,
        openapi_extra=openapi_extra,
        generate_unique_id_function=generate_unique_id_function,
    )(endpoint)

return decorator
````

```

### page

```

page(func)

```

Decorator that creates a GET route using the function name as the path.

If the name of the function is "index", then the route is "/".

Example:

```

import air

app = air.Air() router = air.AirRouter()

@router.page def index(): # routes is "/" return H1("I am the home page")

@router.page def data(): # route is "/data" return H1("I am the home page")

@router.page def about_us(): # routes is "/about-us" return H1("I am the about page")

app.include_router(router)

```

Source code in `src/air/routing.py`

```

def page(self, func: FunctionType) -> FunctionType: """Decorator that creates a GET route using the function name as the path.

```
If the name of the function is "index", then the route is "/".

Example:

    import air

    app = air.Air()
    router = air.AirRouter()

    @router.page
    def index(): # routes is "/"
        return H1("I am the home page")

    @router.page
    def data(): # route is "/data"
        return H1("I am the home page")

    @router.page
    def about_us(): # routes is "/about-us"
        return H1("I am the about page")

    app.include_router(router)
"""
page_path = compute_page_path(func.__name__, separator=self.path_separator)

# Pin the route's response_class for belt-and-suspenders robustness
return self.get(page_path)(func)
```

```

### post

```

post( path, \*, response_model=None, status_code=None, tags=None, dependencies=None, summary=None, description=None, response_description="Successful Response", responses=None, deprecated=None, operation_id=None, response_model_include=None, response_model_exclude=None, response_model_by_alias=True, response_model_exclude_unset=False, response_model_exclude_defaults=False, response_model_exclude_none=False, include_in_schema=True, response_class=AirResponse, name=None, callbacks=None, openapi_extra=None, generate_unique_id_function=generate_unique_id, )

```

Add a *path operation* using an HTTP POST operation.

Source code in `src/air/routing.py`

```

def post( self, path: Annotated\[ str, Doc( """ The URL path to be used for this *path operation*.

```
        For example, in `http://example.com/items`, the path is `/items`.
        """
    ),
],
*,
response_model: Annotated[
    Any,
    Doc(
        """
        The type to use for the response.

        It could be any valid Pydantic *field* type. So, it doesn't have to
        be a Pydantic model, it could be other things, like a `list`, `dict`,
        etc.

        It will be used for:

        * Documentation: the generated OpenAPI (and the UI at `/docs`) will
            show it as the response (JSON Schema).
        * Serialization: you could return an arbitrary object and the
            `response_model` would be used to serialize that object into the
            corresponding JSON.
        * Filtering: the JSON sent to the client will only contain the data
            (fields) defined in the `response_model`. If you returned an object
            that contains an attribute `password` but the `response_model` does
            not include that field, the JSON sent to the client would not have
            that `password`.
        * Validation: whatever you return will be serialized with the
            `response_model`, converting any data as necessary to generate the
            corresponding JSON. But if the data in the object returned is not
            valid, that would mean a violation of the contract with the client,
            so it's an error from the API developer. So, FastAPI will raise an
            error and return a 500 error code (Internal Server Error).

        Read more about it in the
        [FastAPI docs for Response Model](https://fastapi.tiangolo.com/tutorial/response-model/).
        """
    ),
] = None,
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
response_model_include: Annotated[
    IncEx | None,
    Doc(
        """
        Configuration passed to Pydantic to include only certain fields in the
        response data.

        Read more about it in the
        [FastAPI docs for Response Model - Return Type](https://fastapi.tiangolo.com/tutorial/response-model/#response_model_include-and-response_model_exclude).
        """
    ),
] = None,
response_model_exclude: Annotated[
    IncEx | None,
    Doc(
        """
        Configuration passed to Pydantic to exclude certain fields in the
        response data.

        Read more about it in the
        [FastAPI docs for Response Model - Return Type](https://fastapi.tiangolo.com/tutorial/response-model/#response_model_include-and-response_model_exclude).
        """
    ),
] = None,
response_model_by_alias: Annotated[
    bool,
    Doc(
        """
        Configuration passed to Pydantic to define if the response model
        should be serialized by alias when an alias is used.

        Read more about it in the
        [FastAPI docs for Response Model - Return Type](https://fastapi.tiangolo.com/tutorial/response-model/#response_model_include-and-response_model_exclude).
        """
    ),
] = True,
response_model_exclude_unset: Annotated[
    bool,
    Doc(
        """
        Configuration passed to Pydantic to define if the response data
        should have all the fields, including the ones that were not set and
        have their default values. This is different from
        `response_model_exclude_defaults` in that if the fields are set,
        they will be included in the response, even if the value is the same
        as the default.

        When `True`, default values are omitted from the response.

        Read more about it in the
        [FastAPI docs for Response Model - Return Type](https://fastapi.tiangolo.com/tutorial/response-model/#use-the-response_model_exclude_unset-parameter).
        """
    ),
] = False,
response_model_exclude_defaults: Annotated[
    bool,
    Doc(
        """
        Configuration passed to Pydantic to define if the response data
        should have all the fields, including the ones that have the same value
        as the default. This is different from `response_model_exclude_unset`
        in that if the fields are set but contain the same default values,
        they will be excluded from the response.

        When `True`, default values are omitted from the response.

        Read more about it in the
        [FastAPI docs for Response Model - Return Type](https://fastapi.tiangolo.com/tutorial/response-model/#use-the-response_model_exclude_unset-parameter).
        """
    ),
] = False,
response_model_exclude_none: Annotated[
    bool,
    Doc(
        """
        Configuration passed to Pydantic to define if the response data should
        exclude fields set to `None`.

        This is much simpler (less smart) than `response_model_exclude_unset`
        and `response_model_exclude_defaults`. You probably want to use one of
        those two instead of this one, as those allow returning `None` values
        when it makes sense.

        Read more about it in the
        [FastAPI docs for Response Model - Return Type](https://fastapi.tiangolo.com/tutorial/response-model/#response_model_exclude_none).
        """
    ),
] = False,
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
    Callable[[AirRoute], str],
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

) -> Callable\[\[Callable[..., Any]\], Callable[..., Any]\]: """ Add a *path operation* using an HTTP POST operation. """

```
def decorator[**P, R](func: Callable[P, MaybeAwaitable[R]]) -> Callable[..., Any]:
    @wraps(func)
    async def endpoint(*args: P.args, **kw: P.kwargs) -> Response:
        result = func(*args, **kw)
        if inspect.isawaitable(result):
            result = await result
        if isinstance(result, Response):
            return result
        # Force HTML for non-Response results
        return response_class(result)

    return super(AirRouter, self).post(
        path,
        response_model=response_model,
        status_code=status_code,
        tags=tags,
        dependencies=dependencies,
        summary=summary,
        description=description,
        response_description=response_description,
        responses=responses,
        deprecated=deprecated,
        operation_id=operation_id,
        response_model_include=response_model_include,
        response_model_exclude=response_model_exclude,
        response_model_by_alias=response_model_by_alias,
        response_model_exclude_unset=response_model_exclude_unset,
        response_model_exclude_defaults=response_model_exclude_defaults,
        response_model_exclude_none=response_model_exclude_none,
        include_in_schema=include_in_schema,
        response_class=response_class,
        name=name,
        callbacks=callbacks,
        openapi_extra=openapi_extra,
        generate_unique_id_function=generate_unique_id_function,
    )(endpoint)

return decorator
```

```
```
