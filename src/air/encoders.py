import air
from starlette.templating import _TemplateResponse
from fastapi import encoders
from fastapi.templating import Jinja2Templates
from typing import Dict, Type, Callable, Any

def render_template_response_to_string(request: air.Request, template_name: str, context: dict, templates: Jinja2Templates) -> str:
    template = templates.get_template(template_name)
    content = template.render({"request": request, **context})
    return content

ENCODERS_BY_TYPE: Dict[Type[Any], Callable[[Any], Any]] = {
    _TemplateResponse: render_template_response_to_string
}

