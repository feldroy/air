# Templating

Air loves Jinja!

A common pattern is to use a Jinja template as the project base and then use Air Tags for individual content.

## JinjaRenderer

```
JinjaRenderer(directory, context_processors=None, env=None)
```

Template renderer to make Jinja easier in Air.

Parameters:

| Name                 | Type                                            | Description   | Default                                                                                                                                                                                                          |
| -------------------- | ----------------------------------------------- | ------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `directory`          | \`str                                           | PathLike[str] | Sequence\[str                                                                                                                                                                                                    |
| `context_processors` | \`list\[Callable\[[Request], dict[str, Any]\]\] | None\`        | A list of Jinja-style context processors, functions that automatically injects variables or functions into the template context so they're available in every rendered template without passing them explicitly. |
| `env`                | \`Environment                                   | None\`        | The env is the central Jinja object that holds configuration, filters, globals, and template loading settings, and is responsible for compiling and rendering templates.                                         |

Example:

```
# Instantiate the render callable
jinja = JinjaRenderer('templates')

# Use for returning Jinja from views
@app.get('/')
async def home(request: Request):
    return jinja(
        request,
        'home.html',
        context={'id': 5}
     )

    # Can also pass in kwargs, which will be added to the context:
    return jinja(
        request,
        'home.html',
        name='Parmesan'
    )

    # Will render Air Tags sent into Jinja context
    return jinja(
        request,
        'home.html',
        content=air.Article(air.P('Cheddar'))
    )
```

Source code in `src/air/templating.py`

```
def __init__(
    self,
    directory: str | PathLike[str] | Sequence[str | PathLike[str]],
    context_processors: list[Callable[[StarletteRequest], dict[str, Any]]] | None = None,
    env: jinja2.Environment | None = None,
) -> None:
    """Initialize with template directory path"""
    self.templates = Jinja2Templates(directory=directory, context_processors=context_processors, env=env)
```

### __call__

```
__call__(request, name, context=None, **kwargs)
```

Render template with request and context. If an Air Tag is found in the context, try to render it.

Source code in `src/air/templating.py`

```
def __call__(
    self,
    request: Request,
    name: str,
    context: dict[Any, Any] | None = None,
    **kwargs: Any,
) -> _TemplateResponse:
    """Render template with request and context. If an Air Tag
    is found in the context, try to render it.
    """
    if context is None:
        context = {}
    if kwargs:
        context |= kwargs

    # Attempt to render any Tags in the context
    context = {k: _jinja_context_item(v) for k, v in context.items()}
    return self.templates.TemplateResponse(request=request, name=name, context=context)
```

## Renderer

```
Renderer(
    directory,
    context_processors=None,
    env=None,
    package=None,
)
```

Template/Tag renderer to make composing pluggable functions easier.

Parameters:

| Name                 | Type                                            | Description   | Default                                                                                                                                                                                                          |
| -------------------- | ----------------------------------------------- | ------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `directory`          | \`str                                           | PathLike[str] | Sequence\[str                                                                                                                                                                                                    |
| `context_processors` | \`list\[Callable\[[Request], dict[str, Any]\]\] | None\`        | A list of Jinja-style context processors, functions that automatically injects variables or functions into the template context so they're available in every rendered template without passing them explicitly. |
| `env`                | \`Environment                                   | None\`        | The env is the central Jinja object that holds configuration, filters, globals, and template loading settings, and is responsible for compiling and rendering templates.                                         |

Example:

```
import air

app = air.Air()

# Instantiate the render callable
render = air.Renderer('templates')

# Use for returning Jinja from views
@app.get('/')
async def home(request: Request):
    return render(
        name='home.html',
        request=request,
        context={'id': 5}
     )


    # Will render name of Air Tags
    return render(
        request,
        'components.home',
        context={'id': 5}
    )


    # Will render callables to HTML
    return render(
        air.layouts.mvpcss,
        air.Title("Test Page"),
        air.H1("Hello, World")
    )
```

Source code in `src/air/templating.py`

```
def __init__(
    self,
    directory: str | PathLike[str] | Sequence[str | PathLike[str]],
    context_processors: list[Callable[[StarletteRequest], dict[str, Any]]] | None = None,
    env: jinja2.Environment | None = None,
    package: str | None = None,
) -> None:
    """Initialize with template directory path"""
    self.templates = Jinja2Templates(directory=directory, context_processors=context_processors, env=env)
    self.package = package
```

### __call__

```
__call__(
    name, *children, request=None, context=None, **kwargs
)
```

Render template with request and context. If an Air Tag is found in the context, try to render it.

Source code in `src/air/templating.py`

```
def __call__(
    self,
    name: str | Callable,
    *children: Any,
    request: Request | None = None,
    context: dict[Any, Any] | None = None,
    **kwargs: Any,
) -> str:
    """Render template with request and context. If an Air Tag
    is found in the context, try to render it.
    """
    context = self._prepare_context(context, kwargs)

    if callable(name):
        assert not isinstance(name, str)
        result = name(**context)
        if isinstance(result, str):
            return result
        if hasattr(result, "render"):
            return result.render()
        msg = "Callable in name arg must a string or object with a render method."
        raise TypeError(msg)

    assert isinstance(name, str)

    if name.endswith((".html", ".jinja")):
        return self._render_template(name, request, context)

    if "." in name:
        return self._render_tag_callable(name, children, request, context)

    msg = "No callable or Jinja template found."
    raise RenderException(msg)
```
