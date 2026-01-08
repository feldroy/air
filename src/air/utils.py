from __future__ import annotations

import inspect
from functools import cache
from typing import TYPE_CHECKING, Any, Final, Literal

from fastapi.datastructures import Default
from fastapi.utils import generate_unique_id

from .responses import AirResponse, JSONResponse

if TYPE_CHECKING:
    from collections.abc import Callable


# Public default so apps/routers can import the same sentinel (meaning: special marker)
default_html_response: Final = Default(AirResponse)
default_json_response: Final = Default(JSONResponse)
default_generate_unique_id: Final = Default(generate_unique_id)


def compute_page_path(endpoint_name: str, separator: Literal["/", "-"] = "-") -> str:
    """index -> '/', otherwise '/name-with-dashes'.

    Returns:
        The computed path string for the endpoint.
    """
    return "/" if endpoint_name == "index" else f"/{endpoint_name.replace('_', separator)}"


@cache
def cached_signature(fn: Callable[..., Any]) -> inspect.Signature:
    """Get function signature with caching for performance.

    This cached version significantly improves performance when inspecting
    the same function multiple times, which commonly happens during route
    registration and template rendering.

    Args:
        fn: The function to inspect

    Returns:
        The function's signature object

    Example:

        from air.utils import cached_signature


        def my_func(a: int, b: str) -> None:
            pass


        sig = cached_signature(my_func)
        # Subsequent calls with same function use cached result
        sig2 = cached_signature(my_func)  # Fast!
    """
    if hasattr(fn, "__signature__"):
        sig = fn.__signature__
        if sig is not None and isinstance(sig, inspect.Signature):
            return sig

    return inspect.signature(fn)


@cache
def cached_unwrap(fn: Callable[..., Any]) -> Callable[..., Any]:
    """Unwrap decorated function with caching for performance.

    This cached version significantly improves performance when unwrapping
    the same decorated function multiple times, which commonly happens during
    route registration.

    Args:
        fn: The potentially decorated function to unwrap

    Returns:
        The unwrapped function

    Example:

        from collections.abc import Callable
        from functools import wraps
        from typing import Any

        from air.utils import cached_unwrap


        def decorator(f: Callable[..., Any]) -> Callable[..., Any]:
            @wraps(f)
            def wrapper(*args: Any, **kwargs: Any) -> Any:
                return f(*args, **kwargs)

            return wrapper


        @decorator
        def my_func() -> None:
            pass


        original = cached_unwrap(my_func)
        # Subsequent calls with same function use cached result
        original2 = cached_unwrap(my_func)  # Fast!
    """
    return inspect.unwrap(fn)
