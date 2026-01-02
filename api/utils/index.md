Utils

## cached_signature

```
cached_signature(fn)
```

Get function signature with caching for performance.

This cached version significantly improves performance when inspecting the same function multiple times, which commonly happens during route registration and template rendering.

Parameters:

| Name | Type                 | Description             | Default    |
| ---- | -------------------- | ----------------------- | ---------- |
| `fn` | `Callable[..., Any]` | The function to inspect | *required* |

Returns:

| Type        | Description                     |
| ----------- | ------------------------------- |
| `Signature` | The function's signature object |

Example:

```
from air.utils import cached_signature


def my_func(a: int, b: str) -> None:
    pass


sig = cached_signature(my_func)
# Subsequent calls with same function use cached result
sig2 = cached_signature(my_func)  # Fast!
```

Source code in `src/air/utils.py`

```
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
```

## cached_unwrap

```
cached_unwrap(fn)
```

Unwrap decorated function with caching for performance.

This cached version significantly improves performance when unwrapping the same decorated function multiple times, which commonly happens during route registration.

Parameters:

| Name | Type                 | Description                                  | Default    |
| ---- | -------------------- | -------------------------------------------- | ---------- |
| `fn` | `Callable[..., Any]` | The potentially decorated function to unwrap | *required* |

Returns:

| Type                 | Description            |
| -------------------- | ---------------------- |
| `Callable[..., Any]` | The unwrapped function |

Example:

```
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
```

Source code in `src/air/utils.py`

```
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
```

## compute_page_path

```
compute_page_path(endpoint_name, separator='-')
```

index -> '/', otherwise '/name-with-dashes'.

Returns:

| Type  | Description                                |
| ----- | ------------------------------------------ |
| `str` | The computed path string for the endpoint. |

Source code in `src/air/utils.py`

```
def compute_page_path(endpoint_name: str, separator: Literal["/", "-"] = "-") -> str:
    """index -> '/', otherwise '/name-with-dashes'.

    Returns:
        The computed path string for the endpoint.
    """
    return "/" if endpoint_name == "index" else f"/{endpoint_name.replace('_', separator)}"
```
