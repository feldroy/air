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
