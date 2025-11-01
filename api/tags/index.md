# Tags

Note

Tags, or **Air Tag**, are explained in the [concepts document about tags](../../learn/air_tags/).

In the spirit of helping our users, every **Air Tag** has copious documentation—enough that sometimes it breaks the documentation build process. Therefore, **Air Tag** that directly correspond to their HTML equivalents can be found in smaller, easier-to-compile pages.

- [HTML Air Tags A-D](tags-a-d/)
- [HTML Air Tags E-M](tags-e-m/)
- [HTML Air Tags N-S](tags-n-s/)
- [HTML Air Tags T-Z](tags-t-z/)

What remains on this page are core **Air Tag** that either have great utility (**Raw** and **Children** come to mind), or are base classes for other tags.

## Tag

```
Tag(*children)
```

Bases: `Transparent`

Source code in `src/air/tags/models/special.py`

```
def __init__(
    self,
    *children: Renderable,
) -> None:
    super().__init__(*children)
```

## Raw

```
Raw(text_child='', /, **kwargs)
```

Bases: `UnSafeTag`, `Transparent`

Renders raw HTML content without escaping.

Raises:

| Type        | Description                       |
| ----------- | --------------------------------- |
| `TypeError` | If non-string content is provided |

Example: Raw('**Bold** text')

# Produces '**Bold** text'

# Use with other tags

Div( P("Safe content"), Raw('

______________________________________________________________________

'), P("More safe content") )

Source code in `src/air/tags/models/special.py`

```
@override
def __init__(self, text_child: str = "", /, **kwargs: AttributesType) -> None:
    super().__init__(text_child, **kwargs)
    if not isinstance(text_child, str):
        msg = f"{self!r} only accepts string content"
        raise TypeError(msg)
```

## Children

```
Children(*children)
```

Bases: `Transparent`

Source code in `src/air/tags/models/special.py`

```
def __init__(
    self,
    *children: Renderable,
) -> None:
    super().__init__(*children)
```

## SafeStr

Bases: `str`

String subclass that bypasses HTML escaping when rendered.
