import inspect
from collections.abc import Callable
from functools import wraps
from typing import Any

from air.utils import (
    cached_signature,
    cached_unwrap,
    compute_page_path,
    header_get,
    is_public_without_no_store,
    parse_cache_control_directives,
    slugify,
)


def test_compute_page_path_returns_root_for_index_endpoint() -> None:
    actual_path = compute_page_path(endpoint_name="index")
    assert actual_path == "/"


def test_compute_page_path_handles_multiple_underscores() -> None:
    actual_path = compute_page_path(endpoint_name="user_profile_settings")
    assert actual_path == "/user-profile-settings"


def test_compute_page_path_handles_single_word_endpoint() -> None:
    actual_path = compute_page_path(endpoint_name="home")
    assert actual_path == "/home"


def test_compute_page_path_with_forward_slash_separator() -> None:
    actual_path = compute_page_path(endpoint_name="api_users", separator="/")
    assert actual_path == "/api/users"


def test_compute_page_path_handles_empty_string() -> None:
    actual_path = compute_page_path(endpoint_name="")
    assert actual_path == "/"


def test_cached_signature_basic() -> None:
    """Test basic cached_signature functionality."""

    def sample_func(a: int, b: str) -> None:
        pass

    sig1 = cached_signature(sample_func)
    sig2 = cached_signature(sample_func)

    # Should return the same signature object due to caching
    assert sig1 is sig2
    assert len(sig1.parameters) == 2
    assert "a" in sig1.parameters
    assert "b" in sig1.parameters


def test_cached_signature_with_existing_signature_attribute() -> None:
    """Test that cached_signature uses __signature__ if already set."""

    def func_with_sig(x: int, y: str) -> int:
        return x

    # Pre-set the __signature__ attribute
    original_sig = inspect.signature(func_with_sig)
    func_with_sig.__signature__ = original_sig

    # cached_signature should use the pre-existing __signature__
    result_sig = cached_signature(func_with_sig)

    # Should return the same signature object
    assert result_sig is original_sig
    assert len(result_sig.parameters) == 2


def test_cached_signature_with_none_signature_attribute() -> None:
    """Test that cached_signature handles None __signature__ gracefully."""

    def func_with_none_sig(a: int) -> int:
        return a

    # Set __signature__ to None (unusual but possible)
    func_with_none_sig.__signature__ = None

    # Should fall back to inspect.signature
    result_sig = cached_signature(func_with_none_sig)

    assert result_sig is not None
    assert isinstance(result_sig, inspect.Signature)
    assert len(result_sig.parameters) == 1


def test_cached_unwrap_basic() -> None:
    """Test basic cached_unwrap functionality."""

    def decorator(f: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(f)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            return f(*args, **kwargs)

        return wrapper

    @decorator
    def original_func() -> None:
        pass

    unwrapped1 = cached_unwrap(original_func)
    unwrapped2 = cached_unwrap(original_func)

    # Should return the same unwrapped function due to caching
    assert unwrapped1 is unwrapped2
    assert unwrapped1.__name__ == "original_func"


def test_cached_unwrap_multiple_decorators() -> None:
    """Test cached_unwrap with multiple layers of decorators."""

    def decorator1(f: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(f)
        def wrapper1(*args: Any, **kwargs: Any) -> Any:
            return f(*args, **kwargs)

        return wrapper1

    def decorator2(f: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(f)
        def wrapper2(*args: Any, **kwargs: Any) -> Any:
            return f(*args, **kwargs)

        return wrapper2

    @decorator1
    @decorator2
    def multi_decorated() -> str:
        return "result"

    unwrapped = cached_unwrap(multi_decorated)

    # Should unwrap all layers to get to the original function
    assert unwrapped.__name__ == "multi_decorated"
    assert unwrapped() == "result"


def test_slugify_lowercases_and_replaces_separators() -> None:
    assert slugify("Hello, World!") == "hello-world"


def test_slugify_collapses_and_trims_hyphens() -> None:
    assert slugify("  A -- B  ") == "a-b"


def test_slugify_truncates_to_max_length() -> None:
    assert slugify("a" * 100, max_length=5) == "aaaaa"


def test_slugify_uses_fallback_when_normalized_text_is_empty() -> None:
    assert slugify("!!!", fallback="fallback-slug") == "fallback-slug"


def test_header_get_is_case_insensitive_for_mappings() -> None:
    assert header_get({"Content-Type": "text/html"}, "content-type") == "text/html"
    assert header_get({"content-type": "text/html"}, "Content-Type") == "text/html"


def test_header_get_returns_none_when_missing() -> None:
    assert header_get({}, "content-type") is None


def test_parse_cache_control_directives_tokenizes() -> None:
    assert parse_cache_control_directives("public, max-age=3600") == {"public", "max-age=3600"}


def test_parse_cache_control_directives_handles_empty_input() -> None:
    assert parse_cache_control_directives(None) == set()
    assert parse_cache_control_directives("") == set()


def test_is_public_without_no_store_flags_cacheability() -> None:
    assert is_public_without_no_store({"Cache-Control": "public, max-age=60"}) is True
    assert is_public_without_no_store({"Cache-Control": "public, no-store"}) is False
    assert is_public_without_no_store({"Cache-Control": "no-store"}) is False
    assert is_public_without_no_store({}) is False
