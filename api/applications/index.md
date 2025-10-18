# Applications

Instantiating Air applications.

## Air

```
Air(
    *,
    debug=False,
    routes=None,
    servers=None,
    dependencies=None,
    default_response_class=AirResponse,
    redirect_slashes=True,
    middleware=None,
    exception_handlers=None,
    on_startup=None,
    on_shutdown=None,
    lifespan=None,
    webhooks=None,
    deprecated=None,
    docs_url=None,
    redoc_url=None,
    openapi_url=None,
    path_separator="-",
    **extra,
)
```

Bases: `FastAPI`

FastAPI wrapper class with AirResponse as the default response class.

Parameters:

| Name                     | Type                              | Description                                                                                 | Default                                                                                                         |
| ------------------------ | --------------------------------- | ------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------- |
| `debug`                  | `bool`                            | Enables additional logging or diagnostic output.                                            | `False`                                                                                                         |
| `dependencies`           | \`Sequence[Depends]               | None\`                                                                                      | A list of global dependencies, they will be applied to each path operation, including in sub-routers.           |
| `middleware`             | \`Sequence[Middleware]            | None\`                                                                                      | List of middleware to be added when creating the application.                                                   |
| `default_response_class` | `type[Response]`                  | The default response class to be used.                                                      | `AirResponse`                                                                                                   |
| `redirect_slashes`       | `bool`                            | Whether to detect and redirect slashes in URLs when the client doesn't use the same format. | `True`                                                                                                          |
| `on_startup`             | \`Sequence\[Callable\[[], Any\]\] | None\`                                                                                      | A list of startup event handler functions.                                                                      |
| `on_shutdown`            | \`Sequence\[Callable\[[], Any\]\] | None\`                                                                                      | A list of shutdown event handler functions.                                                                     |
| `lifespan`               | \`Lifespan[AppType]               | None\`                                                                                      | A Lifespan context manager handler. This replaces startup and shutdown functions with a single context manager. |
| `path_separator`         | `Literal['/', '-']`               | An optional path separator, default to "-". valid option available ["/", "-"]               | `'-'`                                                                                                           |

Example:

```
import air

app = air.Air()
```

This preserves most FastAPI initialization parameters while setting

- AirResponse as the default response class.
- AirRoute as the default route class.

Source code in `src/air/applications.py`

````
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
        ExceptionHandlersType | None,
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
    path_separator: Annotated[Literal["/", "-"], Doc("An optional path separator.")] = "-",
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

    This preserves most FastAPI initialization parameters while setting:
        - AirResponse as the default response class.
        - AirRoute as the default route class.
    """
    self.path_separator = path_separator
    if exception_handlers is None:
        exception_handlers = {}
    exception_handlers |= DEFAULT_EXCEPTION_HANDLERS
    super().__init__(
        debug=debug,
        routes=routes,
        servers=servers,
        dependencies=dependencies,
        default_response_class=default_response_class,
        middleware=middleware,
        exception_handlers=exception_handlers,  # ty: ignore[invalid-argument-type]
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

    self.router.route_class = AirRoute
````

### get

```
get(
    path,
    *,
    response_model=None,
    status_code=None,
    tags=None,
    dependencies=None,
    summary=None,
    description=None,
    response_description="Successful Response",
    responses=None,
    deprecated=None,
    operation_id=None,
    response_model_include=None,
    response_model_exclude=None,
    response_model_by_alias=True,
    response_model_exclude_unset=False,
    response_model_exclude_defaults=False,
    response_model_exclude_none=False,
    include_in_schema=True,
    response_class=AirResponse,
    name=None,
    callbacks=None,
    openapi_extra=None,
    generate_unique_id_function=generate_unique_id,
)
```

Add a *path operation* using an HTTP GET operation.

##### Example

```
from air import Air

app = Air()


@app.get("/hello")
def hello_world():
    return air.H1("Hello, World!")
```

Source code in `src/air/applications.py`

````
def get(
    self,
    path: Annotated[
        str,
        Doc(
            """
            The URL path to be used for this *path operation*.

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
    ] = generate_unique_id,
) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """
    Add a *path operation* using an HTTP GET operation.

    ## Example

    ```python
    from air import Air

    app = Air()


    @app.get("/hello")
    def hello_world():
        return air.H1("Hello, World!")
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

        return super(Air, self).get(
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

### page

```
page(func)
```

Decorator that creates a GET route using the function name as the path.

If the name of the function is "index", then the route is "/".

Example:

```
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
```

Source code in `src/air/applications.py`

```
def page(self, func: FunctionType) -> FunctionType:
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
    page_path = compute_page_path(func.__name__, separator=self.path_separator)

    # Pin the route's response_class for belt-and-suspenders robustness
    return self.get(page_path)(func)
```

### post

```
post(
    path,
    *,
    response_model=None,
    status_code=None,
    tags=None,
    dependencies=None,
    summary=None,
    description=None,
    response_description="Successful Response",
    responses=None,
    deprecated=None,
    operation_id=None,
    response_model_include=None,
    response_model_exclude=None,
    response_model_by_alias=True,
    response_model_exclude_unset=False,
    response_model_exclude_defaults=False,
    response_model_exclude_none=False,
    include_in_schema=True,
    response_class=AirResponse,
    name=None,
    callbacks=None,
    openapi_extra=None,
    generate_unique_id_function=generate_unique_id,
)
```

Add a *path operation* using an HTTP POST operation.

Source code in `src/air/applications.py`

```
def post(
    self,
    path: Annotated[
        str,
        Doc(
            """
            The URL path to be used for this *path operation*.

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
    ] = generate_unique_id,
) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """
    Add a *path operation* using an HTTP POST operation.
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

        return super(Air, self).post(
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
