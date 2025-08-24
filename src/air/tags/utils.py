"""Utilities for the Air Tag system."""

from .config import HTML_ATTRIBUTES


def clean_html_attr_key(key: str) -> str:
    """Clean up HTML attribute keys to match the standard W3C HTML spec.

    Args:
        key: An uncleaned HTML attribute key

    Returns:

        Cleaned HTML attribute key
    """
    # If a "_"-suffixed proxy for "class", "for", or "id" is used,
    # convert it to its normal HTML equivalent.
    key = {"class_": "class", "for_": "for", "id_": "id", "as_": "as"}.get(key, key)
    # Remove leading underscores and replace underscores with dashes
    return key.lstrip("_").replace("_", "-")


class SafeStr(str):
    """A string subclass that doesn't trigger html.escape() when called by Tag.render()

    Example:
        sample = SafeStr('Hello, world')
    """


def locals_cleanup(local_data, obj):
    """Converts arguments to kwargs per the html_attributes structure"""
    data = {}
    attrs = [*HTML_ATTRIBUTES.get(obj.__class__.__name__, []), "class_", "for_", "as_", "id", "style"]
    for attr in attrs:
        # For performance reasons we use key checks rather than local_data.get
        if attr in local_data and local_data[attr] is not None:
            data[attr] = local_data[attr]
    return data
