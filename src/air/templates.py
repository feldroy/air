from typing import Any

from fastapi import Request
from fastapi.templating import Jinja2Templates


class Jinja2Renderer:
    """Template renderer to make Jinja2 easier in Air.

    Args:
        directory: Template directory

    Example:
        >>> # Instantiate the render callable
        >>> jinja = TemplateRenderer('templates')
        >>>
        >>> # Use for returning Jinja2 from views
        >>> @app.get('/')
        >>> async def home(request: Request):
        >>> return jinja(
        ...     request,
        ...     'home.html',
        ...     context={'id': 5}
        ... )

    Can also pass in kwargs, which will be added to the context:

        >>> return jinja(
        ...     request,
        ...     'home.html',
        ...     name='Parmesan'
        ... )
    """

    def __init__(self, directory: str):
        """Initialize with template directory path"""
        self.templates = Jinja2Templates(directory=directory)

    def __call__(
        self,
        request: Request,
        name: str,
        context: dict[Any, Any] | None = None,
        **kwargs,
    ):
        """Render template with request and context"""
        if context is None:
            context = {}
        if kwargs:
            context = context | kwargs
        return self.templates.TemplateResponse(
            request=request, name=name, context=context
        )
