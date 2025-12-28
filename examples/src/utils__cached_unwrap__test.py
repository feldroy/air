from collections.abc import Callable
from functools import wraps
from typing import Any

from air.utils import cached_unwrap


def test_cached_unwrap() -> None:
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

    # Verify both unwrapped functions are the same
    assert original == original2
    assert original.__name__ == "my_func"
    # The unwrapped function should be different from the decorated one
    assert original != my_func
