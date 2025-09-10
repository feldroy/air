from __future__ import annotations

import inspect
from collections.abc import Callable
from functools import wraps
from typing import Any, Final, Protocol

from fastapi.datastructures import Default, DefaultPlaceholder
from fastapi.types import DecoratedCallable
from fastapi.utils import generate_unique_id

from .responses import AirResponse, JSONResponse, Response

# Public default so apps/routers can import the same sentinel (meaning: special marker)
default_html_response: Final[DefaultPlaceholder] = Default(AirResponse)
default_json_response = Default(JSONResponse)
default_generate_unique_id = Default(generate_unique_id)


class RegisterGet(Protocol):
    """Protocol (meaning: interface) for FastAPI/APIRouter.get returned registrar."""

    def __call__(
        self, path: str, /, *, response_class: type[Response] | DefaultPlaceholder, **kwargs: Any
    ) -> Callable[[Callable[..., Any]], Any]: ...


def coerce_response_class(rc: type[Response] | DefaultPlaceholder) -> type[Response]:
    """Resolve FastAPI's Default(...) placeholder to an actual Response class."""
    cls = getattr(rc, "value", rc)  # DefaultPlaceholder has .value; classes don't.
    assert isinstance(cls, type) and issubclass(cls, Response)
    return cls


def compute_page_path(func: Callable[..., Any]) -> str:
    """index -> '/', otherwise '/name-with-dashes'."""
    name = func.__name__
    return "/" if name == "index" else f"/{name.replace('_', '-')}"


def make_get_decorator(
    register: RegisterGet,
    path: str,
    /,
    *,
    response_class: type[Response] | DefaultPlaceholder = default_html_response,
    **kwargs: Any,
) -> Callable[[DecoratedCallable], DecoratedCallable]:
    """Return a decorator that wraps the handler and registers it as HTML by default."""

    def decorator(func: Callable[..., Any]) -> Any:
        @wraps(func)
        async def endpoint(*args: Any, **kw: Any) -> Any:
            result = func(*args, **kw)
            if inspect.isawaitable(result):
                result = await result
            if isinstance(result, Response):
                return result
            # Force HTML for non-Response results
            cls = coerce_response_class(response_class)
            return cls(result)

        return register(path, response_class=response_class, **kwargs)(endpoint)

    return decorator
