from __future__ import annotations

from typing import Annotated, Final, TypedDict

from typing_extensions import Doc

from air.tags.utils import SafeStr

from .base import BaseTag
from .special import (
    Script,
    Style,
)
from .stock import (
    Base,
    Link,
    Meta,
    Title,
)

type Renderable = Annotated[
    str | BaseTag | SafeStr | int | float,
    Doc(
        """
        The type for any renderable content(a child of a tag)
        Excludes types like None (renders as "None"), bool ("True"/"False"),
        complex ("(1+2j)"), bytes ("b'...'"), and others that produce
        undesirable or unintended HTML output.
        """
    ),
]
type AttributeType = Annotated[
    str | int | float | bool,
    Doc(
        """
        The type for any HTML attribute value.
        """
    ),
]
type TagAttributesType = Annotated[
    dict[str, AttributeType],
    Doc(
        """
        The type for a dictionary of HTML attributes.
        """
    ),
]
type TagChildrenType = Annotated[
    tuple[Renderable, ...],
    Doc(
        """
        The type for all the children of an HTML tag.
        """
    ),
]
type TagChildrenTypeForDict = Annotated[
    tuple[TagDictType | Renderable, ...],
    Doc(
        """
        The type of the children of the serialized dictionary representation of an air-tag.
        """
    ),
]


class TagDictType(TypedDict):
    name: str
    attributes: TagAttributesType
    children: TagChildrenType | TagChildrenTypeForDict


type TagTypes = tuple[type[BaseTag], ...]
HEAD_TAG_TYPES: Final[TagTypes] = (Title, Style, Meta, Link, Script, Base)
