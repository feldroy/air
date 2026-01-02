from air.caches import generate_cache_key


def test_generate_cache_key_basic() -> None:
    """Test basic cache key generation."""
    key = generate_cache_key("test_func")
    assert key.startswith("__air:test_func:")
    assert len(key.split(":")) == 3


def test_generate_cache_key_with_args() -> None:
    """Test cache key generation includes arguments in hash."""
    key1 = generate_cache_key("test_func", 1, 2, 3)
    key2 = generate_cache_key("test_func", 1, 2, 3)
    key3 = generate_cache_key("test_func", 1, 2, 4)

    assert key1 == key2
    assert key1 != key3


def test_generate_cache_key_with_kwargs() -> None:
    """Test cache key generation includes kwargs in hash."""
    key1 = generate_cache_key("test_func", foo="bar", baz="qux")
    key2 = generate_cache_key("test_func", foo="bar", baz="qux")
    key3 = generate_cache_key("test_func", foo="bar", baz="different")

    assert key1 == key2
    assert key1 != key3


def test_generate_cache_key_kwargs_order_independent() -> None:
    """Test that kwargs order doesn't affect cache key."""
    key1 = generate_cache_key("test_func", foo="bar", baz="qux")
    key2 = generate_cache_key("test_func", baz="qux", foo="bar")

    assert key1 == key2
