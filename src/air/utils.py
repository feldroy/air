from __future__ import annotations

import inspect
import re
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


def slugify(value: str, *, fallback: str = "post", max_length: int = 80) -> str:
    """Create a URL-safe slug from arbitrary text.

    Reusable across Air apps: lowercases, replaces non-alphanumerics with
    a single hyphen, trims leading/trailing hyphens, and caps length.

    Args:
        value: Source text.
        fallback: Returned when the normalized text is empty.
        max_length: Maximum slug length; truncated and re-trimmed.

    Returns:
        URL-safe slug.
    """

    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return slug[:max_length].strip("-") or fallback


def header_get(headers: Any, name: str) -> str | None:
    """Case-insensitive header lookup tolerant of Worker and dict-like mappings."""

    try:
        getter = getattr(headers, "get", None)
        if callable(getter):
            value = getter(name)
            if value is not None:
                return str(value)
            alt = name.lower() if name[:1].isupper() else name
            if alt != name:
                value = getter(alt)
                if value is not None:
                    return str(value)
        if hasattr(headers, "items"):
            lower = name.lower()
            for key, val in headers.items():
                if str(key).lower() == lower:
                    return str(val)
    except Exception:  # noqa: BLE001 - tolerate arbitrary Worker/JS header mappings
        return None
    return None


def parse_cache_control_directives(value: str | None) -> set[str]:
    """Tokenize a Cache-Control header into lower-cased directives."""

    if not value:
        return set()
    return {token.strip().lower() for token in value.split(",") if token.strip()}


def is_public_without_no_store(headers: Any) -> bool:
    """Whether Cache-Control contains public without no-store."""

    raw = header_get(headers, "Cache-Control")
    directives = parse_cache_control_directives(raw)
    return "public" in directives and "no-store" not in directives
