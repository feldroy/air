import importlib
from typing import Any
from fastapi import Response


def dict_to_ft_component(d):
    children_raw = d.get("_children", ())
    children = tuple(
        dict_to_ft_component(c) if isinstance(c, dict) else c for c in children_raw
    )
    module = importlib.import_module(d["_module"])
    obj = getattr(module, d["_name"])
    return obj(*children, **d.get("_attrs", {}))


class TagResponse(Response):
    """Custom response class to handle air.tags.Tags."""

    media_type = "text/html; charset=utf-8"

    def render(self, content: Any) -> bytes:
        """Render Tag elements to bytes of HTML."""
        if isinstance(content, dict):
            content = dict_to_ft_component(content)
        return content.render().encode("utf-8")
