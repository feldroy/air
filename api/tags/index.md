# Tags

Note

Tags, or **Air Tag**, are explained in the [concepts document about tags](http://feldroy.github.io/air/learn/air_tags/index.md).

In the spirit of helping our users, every **Air Tag** has copious documentation—enough that sometimes it breaks the documentation build process. Therefore, **Air Tag** that directly correspond to their HTML equivalents can be found in smaller, easier-to-compile pages.

- [HTML Air Tags A-D](http://feldroy.github.io/air/api/tags/tags-a-d/index.md)
- [HTML Air Tags E-M](http://feldroy.github.io/air/api/tags/tags-e-m/index.md)
- [HTML Air Tags N-S](http://feldroy.github.io/air/api/tags/tags-n-s/index.md)
- [HTML Air Tags T-Z](http://feldroy.github.io/air/api/tags/tags-t-z/index.md)

What remains on this page are core **Air Tag** that either have great utility (**Raw** and **Children** come to mind), or are base classes for other tags.

## Tag

```
Tag(*children)
```

Bases: `Transparent`

Alias for the `Transparent` tag; use it if it improves clarity.

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
def __init__(self, text_child: str = "", /, **kwargs: AttributeType) -> None:
    if not isinstance(text_child, str):
        msg = f"{self!r} only accepts string content"
        raise TypeError(msg)
    super().__init__(text_child, **kwargs)
```

## Children

```
Children(*children)
```

Bases: `Transparent`

Alias for the `Transparent` tag; use it if it improves clarity.

Source code in `src/air/tags/models/special.py`

```
def __init__(
    self,
    *children: Renderable,
) -> None:
    super().__init__(*children)
```

## SafeStr

Bases: `UserString`

String subclass that bypasses HTML escaping when rendered.
