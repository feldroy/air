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
    redirect_slashes=True,
    middleware=None,
    exception_handlers=None,
    lifespan=None,
    path_separator="-",
    fastapi_app=None,
    **extra,
)
```

Bases: `RouterMixin`

Air web framework - HTML-first web apps powered by FastAPI.

Air uses composition, wrapping a FastAPI instance internally. This provides a clean, focused API for HTML applications while leveraging FastAPI's toolkit.

Parameters:

| Name                     | Type                   | Description                                                                                 | Default                                                                                                         |
| ------------------------ | ---------------------- | ------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------- |
| `debug`                  | `bool`                 | Enables additional logging or diagnostic output.                                            | `False`                                                                                                         |
| `dependencies`           | \`Sequence[Depends]    | None\`                                                                                      | A list of global dependencies, they will be applied to each path operation, including in sub-routers.           |
| `middleware`             | \`Sequence[Middleware] | None\`                                                                                      | List of middleware to be added when creating the application.                                                   |
| `default_response_class` |                        | The default response class to be used.                                                      | *required*                                                                                                      |
| `redirect_slashes`       | `bool`                 | Whether to detect and redirect slashes in URLs when the client doesn't use the same format. | `True`                                                                                                          |
| `on_startup`             |                        | A list of startup event handler functions.                                                  | *required*                                                                                                      |
| `on_shutdown`            |                        | A list of shutdown event handler functions.                                                 | *required*                                                                                                      |
| `lifespan`               | \`Lifespan[Any]        | None\`                                                                                      | A Lifespan context manager handler. This replaces startup and shutdown functions with a single context manager. |
| `path_separator`         | `Literal['/', '-']`    | An optional path separator, default to "-". valid option available ["/", "-"]               | `'-'`                                                                                                           |

Example:

```
import air

app = air.Air()

@app.get("/")
def index() -> air.H1:
    return air.H1("Hello, World!")
```

This preserves most FastAPI initialization parameters while setting

- AirResponse as the default response class.
- AirRoute as the default route class.

Source code in `src/air/applications.py`

````
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
````

### debug

```
debug
```

Debug mode status.

### dependency_overrides

```
dependency_overrides
```

Dependency overrides for testing.

### exception_handlers

```
exception_handlers
```

Exception handlers for this application.

### fastapi_app

```
fastapi_app
```

Access the underlying FastAPI app for advanced use cases.

Use this if you need FastAPI-specific features like:

- OpenAPI customization
- response_model for JSON endpoints
- WebSocket handling

Example:

```
@app.fastapi_app.get("/api/users", response_model=list[User])
async def api_get_users():
    return users
```

### router

```
router
```

The application router.

### routes

```
routes
```

The list of routes.

### state

```
state
```

Application state, shared across requests.

### __call__

```
__call__(scope, receive, send)
```

ASGI interface - delegates to internal FastAPI app.

Source code in `src/air/applications.py`

```
async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
    """ASGI interface - delegates to internal FastAPI app."""
    await self._app(scope, receive, send)
```

### add_middleware

```
add_middleware(middleware_class, **options)
```

Add middleware to the application.

Source code in `src/air/applications.py`

```
def add_middleware(
    self,
    middleware_class: type,
    **options: Any,
) -> None:
    """Add middleware to the application."""
    self._app.add_middleware(middleware_class, **options)
```

### delete

```
delete(
    path,
    *,
    status_code=None,
    tags=None,
    dependencies=None,
    summary=None,
    description=None,
    response_description="Successful Response",
    responses=None,
    deprecated=None,
    operation_id=None,
    include_in_schema=True,
    response_class=AirResponse,
    name=None,
    callbacks=None,
    openapi_extra=None,
    generate_unique_id_function=generate_unique_id,
)
```

Add a *path operation* using an HTTP DELETE operation.

Returns:

| Type                                                 | Description                                                                      |
| ---------------------------------------------------- | -------------------------------------------------------------------------------- |
| `Callable[[Callable[..., Any]], Callable[..., Any]]` | A decorator function that registers the decorated function as a DELETE endpoint. |

Source code in `src/air/applications.py`

```
def delete(
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
    Add a *path operation* using an HTTP DELETE operation.

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
            # Force HTML for non-Response results
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
```

### exception_handler

```
exception_handler(exc_class_or_status_code)
```

Add an exception handler to the application.

Returns:

| Type                                                 | Description                                       |
| ---------------------------------------------------- | ------------------------------------------------- |
| `Callable[[Callable[..., Any]], Callable[..., Any]]` | A decorator that registers the exception handler. |

Source code in `src/air/applications.py`

```
def exception_handler(
    self,
    exc_class_or_status_code: int | type[Exception],
) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """Add an exception handler to the application.

    Returns:
        A decorator that registers the exception handler.
    """
    return self._app.exception_handler(exc_class_or_status_code)
```

### get

```
get(
    path,
    *,
    status_code=None,
    tags=None,
    dependencies=None,
    summary=None,
    description=None,
    response_description="Successful Response",
    responses=None,
    deprecated=None,
    operation_id=None,
    include_in_schema=True,
    response_class=AirResponse,
    name=None,
    callbacks=None,
    openapi_extra=None,
    generate_unique_id_function=generate_unique_id,
)
```

Add a *path operation* using an HTTP GET operation.

Returns:

| Type                                                 | Description                                                                   |
| ---------------------------------------------------- | ----------------------------------------------------------------------------- |
| `Callable[[Callable[..., Any]], Callable[..., Any]]` | A decorator function that registers the decorated function as a GET endpoint. |

Example:

```
import air

app = air.Air()


@app.get("/hello")
def hello_world() -> air.H1:
    # Simple GET endpoint returning HTML.
    return air.H1("Hello, World!")


@app.get("/users/{user_id}")
def get_user(user_id: int) -> air.Div:
    # GET endpoint with path parameter.
    return air.Div(
        air.H2(f"User ID: {user_id}"),
        air.P("This is a user profile page"),
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
```

Source code in `src/air/applications.py`

```
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
    """Add a *path operation* using an HTTP GET operation.

    Returns:
        A decorator function that registers the decorated function as a GET endpoint.

    Example:

        import air

        app = air.Air()


        @app.get("/hello")
        def hello_world() -> air.H1:
            # Simple GET endpoint returning HTML.
            return air.H1("Hello, World!")


        @app.get("/users/{user_id}")
        def get_user(user_id: int) -> air.Div:
            # GET endpoint with path parameter.
            return air.Div(
                air.H2(f"User ID: {user_id}"),
                air.P("This is a user profile page"),
            )


        if __name__ == "__main__":
            import uvicorn

            uvicorn.run(app, host="0.0.0.0", port=8000)
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
```

### include_router

```
include_router(
    router,
    *,
    prefix="",
    tags=None,
    dependencies=None,
    responses=None,
    deprecated=None,
    include_in_schema=True,
    default_response_class=AirResponse,
    callbacks=None,
    generate_unique_id_function=generate_unique_id,
)
```

Include a router in this application.

Source code in `src/air/applications.py`

```
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
```

### middleware

```
middleware(middleware_type)
```

Add a middleware function using a decorator.

Returns:

| Type                                                 | Description                                         |
| ---------------------------------------------------- | --------------------------------------------------- |
| `Callable[[Callable[..., Any]], Callable[..., Any]]` | A decorator that registers the middleware function. |

Source code in `src/air/applications.py`

```
def middleware(self, middleware_type: str) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """Add a middleware function using a decorator.

    Returns:
        A decorator that registers the middleware function.
    """
    return self._app.middleware(middleware_type)
```

### mount

```
mount(path, app, name=None)
```

Mount a sub-application.

Source code in `src/air/applications.py`

```
def mount(
    self,
    path: str,
    app: Any,
    name: str | None = None,
) -> None:
    """Mount a sub-application."""
    self._app.mount(path, app, name=name)
```

### patch

```
patch(
    path,
    *,
    status_code=None,
    tags=None,
    dependencies=None,
    summary=None,
    description=None,
    response_description="Successful Response",
    responses=None,
    deprecated=None,
    operation_id=None,
    include_in_schema=True,
    response_class=AirResponse,
    name=None,
    callbacks=None,
    openapi_extra=None,
    generate_unique_id_function=generate_unique_id,
)
```

Add a *path operation* using an HTTP PATCH operation.

Returns:

| Type                                                 | Description                                                                     |
| ---------------------------------------------------- | ------------------------------------------------------------------------------- |
| `Callable[[Callable[..., Any]], Callable[..., Any]]` | A decorator function that registers the decorated function as a PATCH endpoint. |

Source code in `src/air/applications.py`

```
def patch(
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
    Add a *path operation* using an HTTP PATCH operation.

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
            # Force HTML for non-Response results
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
```

### post

```
post(
    path,
    *,
    status_code=None,
    tags=None,
    dependencies=None,
    summary=None,
    description=None,
    response_description="Successful Response",
    responses=None,
    deprecated=None,
    operation_id=None,
    include_in_schema=True,
    response_class=AirResponse,
    name=None,
    callbacks=None,
    openapi_extra=None,
    generate_unique_id_function=generate_unique_id,
)
```

Add a *path operation* using an HTTP POST operation.

Returns:

| Type                                                 | Description                                                                    |
| ---------------------------------------------------- | ------------------------------------------------------------------------------ |
| `Callable[[Callable[..., Any]], Callable[..., Any]]` | A decorator function that registers the decorated function as a POST endpoint. |

Example:

```
from pydantic import BaseModel

import air


class UserCreate(BaseModel):
    # User creation model.

    name: str
    email: str


app = air.Air()


@app.post("/submit")
def submit_form() -> air.Div:
    # Simple POST endpoint.
    return air.Div(
        air.H2("Form Submitted!"),
        air.P("Thank you for your submission"),
    )


@app.post("/users")
def create_user(user: UserCreate) -> air.Div:
    # POST endpoint with request body.
    return air.Div(
        air.H2("User Created"),
        air.P(f"Name: {user.name}"),
        air.P(f"Email: {user.email}"),
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
```

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
    """Add a *path operation* using an HTTP POST operation.

    Returns:
        A decorator function that registers the decorated function as a POST endpoint.

    Example:

        from pydantic import BaseModel

        import air


        class UserCreate(BaseModel):
            # User creation model.

            name: str
            email: str


        app = air.Air()


        @app.post("/submit")
        def submit_form() -> air.Div:
            # Simple POST endpoint.
            return air.Div(
                air.H2("Form Submitted!"),
                air.P("Thank you for your submission"),
            )


        @app.post("/users")
        def create_user(user: UserCreate) -> air.Div:
            # POST endpoint with request body.
            return air.Div(
                air.H2("User Created"),
                air.P(f"Name: {user.name}"),
                air.P(f"Email: {user.email}"),
            )


        if __name__ == "__main__":
            import uvicorn

            uvicorn.run(app, host="0.0.0.0", port=8000)
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
```

### put

```
put(
    path,
    *,
    status_code=None,
    tags=None,
    dependencies=None,
    summary=None,
    description=None,
    response_description="Successful Response",
    responses=None,
    deprecated=None,
    operation_id=None,
    include_in_schema=True,
    response_class=AirResponse,
    name=None,
    callbacks=None,
    openapi_extra=None,
    generate_unique_id_function=generate_unique_id,
)
```

Add a *path operation* using an HTTP PUT operation.

Returns:

| Type                                                 | Description                                                                   |
| ---------------------------------------------------- | ----------------------------------------------------------------------------- |
| `Callable[[Callable[..., Any]], Callable[..., Any]]` | A decorator function that registers the decorated function as a PUT endpoint. |

Source code in `src/air/applications.py`

```
def put(
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
            The description for the default response.

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
    """Add a *path operation* using an HTTP PUT operation.

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
            # Force HTML for non-Response results
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
```

### url_path_for

```
url_path_for(name, /, **path_params)
```

Generate a URL path for a named route.

Returns:

| Type  | Description                    |
| ----- | ------------------------------ |
| `str` | The generated URL path string. |

Source code in `src/air/applications.py`

```
def url_path_for(self, name: str, /, **path_params: Any) -> str:
    """Generate a URL path for a named route.

    Returns:
        The generated URL path string.
    """
    return str(self._app.url_path_for(name, **path_params))
```
