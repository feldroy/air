from __future__ import annotations

from typing import Final

from .models import (
    Base,
    BaseTag,
    Link,
    Meta,
    Script,
    Style,
    Title,
)
from .models.base import AttributesType as AttributesType

type TagTypes = tuple[type[BaseTag], ...]
HEAD_TAG_TYPES: Final[TagTypes] = (Title, Style, Meta, Link, Script, Base)
