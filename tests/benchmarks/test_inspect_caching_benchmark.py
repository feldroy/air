"""Benchmark inspect.signature and inspect.unwrap caching performance.

This benchmark measures the performance improvement from caching expensive
inspect module operations that are frequently called during route registration
and template rendering.
"""

import inspect
from collections.abc import Callable
from functools import wraps
from typing import Any

from pytest_benchmark.fixture import BenchmarkFixture

from air.utils import cached_signature, cached_unwrap


def sample_function(a: int, b: str, c: float = 1.0) -> str:
    """A sample function for signature inspection.

    Args:
        a: An integer parameter
        b: A string parameter
        c: A float parameter with default value

    Returns:
        A formatted string combining all parameters
    """
    return f"{a} {b} {c}"


def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
    """A sample decorator for unwrap testing.

    Args:
        func: The function to decorate

    Returns:
        The decorated wrapper function
    """

    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        return func(*args, **kwargs)

    return wrapper


@decorator
@decorator
@decorator
def decorated_function(x: int, y: str) -> int:
    """A multiply-decorated function for unwrap testing.

    Args:
        x: An integer parameter
        y: A string parameter (unused)

    Returns:
        The input integer x
    """
    return x


def test_signature_uncached_benchmark(benchmark: BenchmarkFixture) -> None:
    """Benchmark uncached inspect.signature calls."""

    def get_signature() -> inspect.Signature:
        return inspect.signature(sample_function)

    result = benchmark(get_signature)
    assert result is not None
    assert len(result.parameters) == 3


def test_signature_cached_benchmark(benchmark: BenchmarkFixture) -> None:
    """Benchmark cached signature calls.

    This should be significantly faster than uncached calls on subsequent
    invocations due to LRU caching.
    """

    # Warm up the cache
    cached_signature(sample_function)

    def get_cached_signature() -> inspect.Signature:
        return cached_signature(sample_function)

    result = benchmark(get_cached_signature)
    assert result is not None
    assert len(result.parameters) == 3


def test_unwrap_uncached_benchmark(benchmark: BenchmarkFixture) -> None:
    """Benchmark uncached inspect.unwrap calls."""

    def unwrap_func() -> Callable[..., Any]:
        return inspect.unwrap(decorated_function)

    result = benchmark(unwrap_func)
    assert result is not None
    assert result.__name__ == "decorated_function"


def test_unwrap_cached_benchmark(benchmark: BenchmarkFixture) -> None:
    """Benchmark cached unwrap calls.

    This should be significantly faster than uncached calls on subsequent
    invocations due to LRU caching.
    """

    # Warm up the cache
    cached_unwrap(decorated_function)

    def unwrap_cached_func() -> Callable[..., Any]:
        return cached_unwrap(decorated_function)

    result = benchmark(unwrap_cached_func)
    assert result is not None
    assert result.__name__ == "decorated_function"


def test_signature_with_existing_attribute_benchmark(benchmark: BenchmarkFixture) -> None:
    """Benchmark signature lookup when __signature__ is already set.

    This tests the optimization path where we check for an existing
    __signature__ attribute before calling inspect.signature.
    """

    # Create a function with pre-computed signature
    def func_with_sig(a: int, b: str) -> None:
        pass

    func_with_sig.__signature__ = inspect.signature(func_with_sig)

    def get_cached_signature_with_attr() -> inspect.Signature:
        return cached_signature(func_with_sig)

    result = benchmark(get_cached_signature_with_attr)
    assert result is not None
    assert len(result.parameters) == 2


def test_multiple_functions_cached_benchmark(benchmark: BenchmarkFixture) -> None:
    """Benchmark cached signature with multiple different functions.

    This simulates a more realistic scenario where we're inspecting
    multiple route handlers or template callables.
    """

    def func1(a: int) -> int:
        return a

    def func2(b: str) -> str:
        return b

    def func3(c: float) -> float:
        return c

    functions = [func1, func2, func3]

    # Warm up the cache for all functions
    for func in functions:
        cached_signature(func)

    def get_multiple_signatures() -> list[inspect.Signature]:
        return [cached_signature(f) for f in functions]

    results = benchmark(get_multiple_signatures)
    assert len(results) == 3
    assert all(r is not None for r in results)
