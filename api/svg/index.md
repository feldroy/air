# SVG

In the spirit of helping our users, every **Air SVG Tag** has copious documentation—enough that sometimes it breaks the documentation build process. Therefore, **Air SVG Tag** that directly correspond to their SVG equivalents can be found in smaller, easier-to-compile pages.

- [SVG Air Tags A-D](svg-tags-a-d/)
- [SVG Air Tags E-M](svg-tags-e-m/)
- [SVG Air Tags N-S](svg-tags-n-s/)
- [SVG Air Tags T-Z](svg-tags-t-z/)

What remains on this page are core **Air SVG Tag** that either have great utility or are base classes for other tags.

Air is proud to provide first class SVG support. The entire SVG specification is supported.

## CaseTag

```
CaseTag(*children, **kwargs)
```

Bases: `BaseTag`

This is for case-sensitive tags like those used in SVG generation.

Source code in `src/air/tags/models/base.py`

```
def __init__(self, *children: Renderable, **kwargs: AttributesType) -> None:
    """Initialize a tag with renderable children and HTML attributes.

    Args:
        children: Renderable objects that become the tag's inner content.
        kwargs: Attribute names and values applied to the tag element.
    """
    self._name = self.__class__.__name__
    self._module = self.__class__.__module__
    self._children: tuple[Renderable, ...] = children
    self._attrs: dict[str, AttributesType] = kwargs
```
