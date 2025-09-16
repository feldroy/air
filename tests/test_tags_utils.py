"""Tests for the tags utilities.

These tests focus on `locals_cleanup` which filters a mapping of local
arguments down to only those allowed for a given tag object.
"""

from air.tags.utils import format_html, locals_cleanup


def test_locals_cleanup_selects_allowed_attrs() -> None:
    """Only attributes allowed for the tag (plus defaults) are kept.

    Given a mapping with known HTML attributes, random keys, and default
    attributes such as `class_` and `id`, ensure the function returns a
    dict containing only the allowed keys and their values.
    """
    local_data = {
        "href": "/home",
        "class_": "link",
        "id": "elem",
    }

    result = locals_cleanup(local_data)

    # Only allowed HTML attributes and explicit defaults should be present
    assert result == {"href": "/home", "class_": "link", "id": "elem"}


def test_locals_cleanup_ignores_none_values() -> None:
    """Entries with value ``None`` are filtered out from the result.

    This prevents accidental inclusion of attributes that were provided but
    intentionally set to ``None``.
    """
    local_data = {"href": None, "class_": None, "target": "_self"}
    result = locals_cleanup(local_data)
    # None values are dropped
    assert result == {"target": "_self"}


def test_locals_cleanup_for_and_for_underscore() -> None:
    """Keys like ``for_`` provided by callers remain present in the output.

    The function doesn't rename the keys, it merely filters by membership
    in the allowed attribute list for the tag.
    """
    local_data = {"for_": "email"}
    result = locals_cleanup(local_data)

    # locals_cleanup should include the key as provided (no renaming)
    assert result == {"for_": "email"}


def test_locals_cleanup_defaults_for_unknown_class() -> None:
    """For unknown/unsupported object classes, only default attribute
    keys (like ``class_``, ``for_``, ``style``, etc.) are retained.
    """

    local_data = {"class_": "c", "for_": "x", "style": "s"}
    result = locals_cleanup(local_data)

    # Only the default attribute keys are allowed for unknown classes
    assert result == {"class_": "c", "for_": "x", "style": "s"}


def test_format_html():
    escaped_html = (
        "&lt;!doctype html&gt;&lt;html&gt;&lt;body&gt;&lt;h1&gt;Hello, world&lt;/h1&gt;&lt;/body&gt;&lt;/html&gt;"
    )
    html = "<!doctype html><html><body><h1>Hello, world</h1></body></html>"
    assert html in format_html(escaped_html)
