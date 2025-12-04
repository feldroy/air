from __future__ import annotations

import ast
from typing import TYPE_CHECKING

from air.tags.constants import AIR_PREFIX, BOOLEAN_HTML_ATTRIBUTES, INDENT_UNIT
from air.tags.utils import migrate_attribute_name_to_air_tag

if TYPE_CHECKING:
    from selectolax.lexbor import LexborNode

    from .base import AttributeType, Renderable, TagAttributesType


def _get_paddings(level: int) -> tuple[str, str]:
    """Return indentation paddings for the current depth.

    Args:
        level: Current indentation depth.

    Returns:
        Tuple containing the outer and inner padding strings.
    """
    outer_padding = INDENT_UNIT * level
    inner_padding = INDENT_UNIT * (level + 1)
    return outer_padding, inner_padding


def _format_instantiation_call(tag_name: str, instantiation_args: str, outer_padding: str) -> str:
    """Wrap formatted arguments in a constructor call.

    Args:
        tag_name: The name for the air-tag class.
        instantiation_args: Prepared constructor arguments.
        outer_padding: Padding to prepend to the call.

    Returns:
        The full constructor call string.
    """
    return f"{outer_padding}{AIR_PREFIX}{tag_name}({instantiation_args})"


def _wrap_multiline_instantiation_args(instantiation_args: str, outer_padding: str) -> str:
    """Wrap multiline arguments with newlines and outer padding.

    Args:
        instantiation_args: Joined multiline arguments.
        outer_padding: Padding to reapply after the closing line.

    Returns:
        The wrapped multiline argument string.
    """
    return f"\n{instantiation_args},\n{outer_padding}"


def _format_child_instantiation(child: Renderable, padding: str) -> str:
    """Render a non-tag child argument with indentation applied.

    Args:
        child: The child value to render.
        padding: Padding to prepend to the rendered value.

    Returns:
        The formatted child representation.
    """
    return f"{padding}{child!r}"


def _format_attribute_instantiation(attr_name: str, attr_value: AttributeType, padding: str = "") -> str:
    """Render a single attribute keyword argument with indentation applied.

    Args:
        attr_name: Attribute name to render.
        attr_value: Attribute value to render.
        padding: Padding to prepend to the rendered argument.

    Returns:
        The formatted keyword argument string.
    """
    return f"{padding}{attr_name}={attr_value!r}"


def _migrate_html_attributes_to_air_tag(node: LexborNode) -> TagAttributesType:
    """Convert parsed HTML attributes to Air tag attribute keys.

    Args:
        node: Parsed HTML element node.

    Returns:
        A mapping of normalized attribute names and values.
    """
    return {
        migrate_attribute_name_to_air_tag(attr_name): _evaluate_attribute_value_to_py(
            tag_name=node.tag, attr_name=attr_name, attr_value=attr_value
        )
        for attr_name, attr_value in node.attributes.items()
    }


def _evaluate_attribute_value_to_py(tag_name: str | None, attr_name: str, attr_value: str | None) -> AttributeType:
    """
    Evaluates the attribute value of an HTML tag and converts it into the appropriate type.

    This function attempts to evaluate the provided attribute value to determine its
    Python equivalent type (e.g., boolean, literal, or string).

    Args:
        tag_name: The name of the HTML tag being evaluated.
        attr_name: The name of the attribute belonging to the tag.
        attr_value: The value of the attribute to be evaluated. This can be a string
            or None.

    Returns:
        The evaluated value of the given attribute. The type of the returned value
        may vary depending on the input (e.g., boolean, literal value, or original string).
    """
    if attr_value is None:
        return True
    if attr_value.lower() == "true" or attr_value.lower() == "false":
        return attr_value
    if is_a_boolean_attribute(attr_name=attr_name, tag_name=tag_name):
        return is_conforming_boolean_value(attr_name=attr_name, attr_value=attr_value)
    try:
        return ast.literal_eval(attr_value)
    except (ValueError, SyntaxError):
        return attr_value


def is_a_boolean_attribute(attr_name: str, tag_name: str | None) -> bool:
    """
    Checks whether a given attribute is a boolean attribute for a specified HTML tag.

    This function determines whether the provided attribute name corresponds to a
    boolean HTML attribute for the specified tag. Boolean attributes are those that
    represent fundamental binary states, such as `checked`, `disabled`, or `readonly`,
    and their presence alone is sufficient to imply their values.

    Args:
        attr_name: The name of the HTML attribute to check.
        tag_name: The name of the HTML tag associated with the attribute. It can be
            None to indicate no specific tag.

    Returns:
        bool: True if the attribute is a boolean HTML attribute for the provided tag,
        False otherwise.
    """
    return attr_name in BOOLEAN_HTML_ATTRIBUTES and tag_name in BOOLEAN_HTML_ATTRIBUTES[attr_name]


def is_conforming_boolean_value(attr_name: str, attr_value: str | None) -> bool:
    """
    Determines if a given attribute value for a boolean attribute representation is spec conforming.

    This function compares the provided attribute name and attribute value, checking if they match
    in a case-insensitive manner. If the attribute value is `None` or evaluates to `False`, the
    function will also return `True`. This utility is helpful when validating case-insensitive equality
    or dealing with optional or empty values.

    - Absent attribute is a valid false.
    - Present attribute must have value "" or the canonical name (ASCII case-insensitive).

    Args:
        attr_name: The name of the attribute to compare (case insensitive).
        attr_value: The value of the attribute to compare against, which can be `None`.

    Returns:
        bool: True if the attribute value either matches the attribute name in a case-insensitive
        comparison or is `None`/evaluates to `False`. Otherwise, False.
    """
    return not attr_value or attr_name.casefold() == attr_value.casefold()
