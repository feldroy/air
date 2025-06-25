from fastapi import Request
from fastapi.templating import Jinja2Templates
from typing import Any


class Jinja2Renderer:
    """Template renderer to make Jinja2 easier in Air.

    Args:
        directory: Template directory

    Example:
        >>> # Instantiate the render callable
        >>> render = TemplateRenderer('templates')
        >>>
        >>> # Use for returning Jinja2 from views
        >>> @app.get('/')
        >>> async def home(request: Request):
        >>> return render(
        ...     request,
        ...     'home.html',
        ...     context={'id': 5}
        ... )
    """

    def __init__(self, directory: str):
        self.templates = Jinja2Templates(directory=directory)

    def __call__(
        self, request: Request, name: str, context: dict[Any, Any] | None = None
    ):
        if context is None:
            context = {}
        return self.templates.TemplateResponse(
            request=request, name=name, context=context
        )
