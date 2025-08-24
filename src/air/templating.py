"""Air loves Jinja!

A common pattern is to use a Jinja template as the project base and then use Air Tags for individual content.
"""

from collections.abc import Mapping, Sequence
from os import PathLike
from typing import Any, Callable, cast, overload

import jinja2
from fastapi.templating import Jinja2Templates

from .requests import Request
from .tags import Tag


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
        context_processors: list[Callable[[Request], dict[str, Any]]] | None = None,
        env: jinja2.Environment | None = None,
    ):
        """Initialize with template directory path"""
        self.templates = Jinja2Templates(directory=directory, context_processors=context_processors, env=env)

    def __call__(
        self,
        request: Request,
        name: str,
        context: dict[Any, Any] | None = None,
        **kwargs,
    ):
        """Render template with request and context. If an Air Tag
        is found in the context, try to render it.
        """
        if context is None:
            context = {}
        if kwargs:
            context |= kwargs

        # Attempt to render any Tags in the contect
        for k, v in context.items():
            if isinstance(v, Tag) and hasattr(v, "render"):
                context[k] = v.render()
        return self.templates.TemplateResponse(request=request, name=name, context=context)
