"""Air loves Jinja!

A common pattern is to use a Jinja template as the project base and then use Air Tags for individual content.
"""

import importlib
import inspect
from collections.abc import Callable, Sequence
from os import PathLike
from types import ModuleType
from typing import Any

import jinja2
from fastapi.templating import Jinja2Templates
from starlette.requests import Request as StarletteRequest
from starlette.templating import _TemplateResponse

from .exceptions import RenderException
from .requests import Request
from .tags.models.base import BaseTag


def _jinja_context_item(item: Any) -> Any:
    """Prepare an item for processing by Jinja.

    BaseTag instances are converted to string.
    All other objects are handled by Jinja directly.
    """

    if isinstance(item, BaseTag):
        return str(item)
    return item


class JinjaRenderer:
    """Template renderer to make Jinja easier in Air.

    Args:
        directory: The template directory where Jinja templates for the project are stored.
        context_processors: A list of Jinja-style context processors, functions that automatically injects variables or functions into the template context so they're available in every rendered template without passing them explicitly.
        env: The env is the central Jinja object that holds configuration, filters, globals, and template loading settings, and is responsible for compiling and rendering templates.

    Example:

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

    """

    def __init__(
        self,
        directory: str | PathLike[str] | Sequence[str | PathLike[str]],
        context_processors: list[Callable[[StarletteRequest], dict[str, Any]]] | None = None,
        env: jinja2.Environment | None = None,
    ) -> None:
        """Initialize with template directory path"""
        self.templates = Jinja2Templates(directory=directory, context_processors=context_processors, env=env)

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


class Renderer:
    """Template/Tag renderer to make composing pluggable functions easier.

    Args:
        directory: The template directory where Jinja templates for the project are stored.
        context_processors: A list of Jinja-style context processors, functions that automatically injects variables or functions into the template context so they're available in every rendered template without passing them explicitly.
        env: The env is the central Jinja object that holds configuration, filters, globals, and template loading settings, and is responsible for compiling and rendering templates.

    Example:

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
    """

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

    def _prepare_context(self, context: dict[Any, Any] | None, kwargs: dict[Any, Any]) -> dict[Any, Any]:
        """Prepare and merge context dictionaries."""
        if context is None:
            context = {}
        if kwargs:
            context |= kwargs
        return context

    def _render_template(self, name: str, request: Request | None, context: dict[Any, Any]) -> _TemplateResponse:
        """Render Jinja template with Air Tag support."""
        context = {k: _jinja_context_item(v) for k, v in context.items()}
        return self.templates.TemplateResponse(request=request, name=name, context=context)

    def _render_tag_callable(self, name: str, args: tuple, request: Request | None, context: dict[Any, Any]) -> str:
        """Import and render a tag callable from module."""
        module_name, func_name = name.rsplit(".", 1)
        module = self._import_module(module_name)
        tag_callable = getattr(module, func_name)

        filtered_context = self._filter_context_for_callable(tag_callable, context, request)

        if filtered_context and args:
            return tag_callable(**filtered_context)
        return tag_callable(*args, **filtered_context)

    def _import_module(self, module_name: str) -> ModuleType:
        """Import module handling relative imports."""
        if module_name.startswith("."):
            return importlib.import_module(module_name, package=self.package)

        try:
            return importlib.import_module(module_name)
        except ModuleNotFoundError:
            return importlib.import_module(f".{module_name}", package=self.package)

    def _filter_context_for_callable(
        self, tag_callable: Callable, context: dict[Any, Any], request: Request | None
    ) -> dict[str, Any]:
        """Filter context to only include parameters expected by the callable."""
        sig = inspect.signature(tag_callable)
        filtered_context = {}

        for param_name in sig.parameters:
            if param_name in context:
                filtered_context[param_name] = context[param_name]

        if "request" in sig.parameters and request:
            filtered_context["request"] = request

        return filtered_context
