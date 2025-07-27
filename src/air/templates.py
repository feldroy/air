from typing import Any

from fastapi.templating import Jinja2Templates

from .requests import Request
from .tags import Tag


class JinjaRenderer:
    """Template renderer to make Jinja easier in Air.

    Args:
        directory: Template directory

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
        """Render template with request and context. If an Air Tag
        is found in the context, try to render it.
        """
        if context is None:
            context = {}
        if kwargs:
            context = context | kwargs

        # Attempt to render any Tags in the contect
        for k, v in context.items():
            if isinstance(v, Tag) and hasattr(v, "render"):
                context[k] = v.render()
        return self.templates.TemplateResponse(
            request=request, name=name, context=context
        )


class Jinja2Renderer:
    "Deprecated: Use air.templates.JinjaRenderer instead"

    def __init__(self, directory: str):
        raise DeprecationWarning("Use air.templates.JinjaRenderer instead")
