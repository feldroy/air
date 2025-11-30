from __future__ import annotations

import ast
from typing import TYPE_CHECKING

from air.tags.constants import AIR_PREFIX, INDENT_UNIT
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
        migrate_attribute_name_to_air_tag(name): _evaluate_attribute_value_to_py(value)
        for name, value in node.attributes.items()
    }


def _evaluate_attribute_value_to_py(attr_value: str | None) -> AttributeType:
    if attr_value is None or attr_value.lower() == "true":
        return True
    if attr_value.lower() == "false":
        return False
    try:
        return ast.literal_eval(attr_value)
    except (ValueError, SyntaxError):
        return attr_value
