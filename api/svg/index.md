# SVG

In the spirit of helping our users, every **Air SVG Tag** has copious documentation—enough that sometimes it breaks the documentation build process. Therefore, **Air SVG Tag** that directly correspond to their SVG equivalents can be found in smaller, easier-to-compile pages.

- [SVG Air Tags A-D](https://docs.airwebframework.org/api/svg/svg-tags-a-d/index.md)
- [SVG Air Tags E-M](https://docs.airwebframework.org/api/svg/svg-tags-e-m/index.md)
- [SVG Air Tags N-S](https://docs.airwebframework.org/api/svg/svg-tags-n-s/index.md)
- [SVG Air Tags T-Z](https://docs.airwebframework.org/api/svg/svg-tags-t-z/index.md)

What remains on this page are core **Air SVG Tag** that either have great utility or are base classes for other tags.

Air is proud to provide first class SVG support. The entire SVG specification is supported.

## CaseTag

```
CaseTag(*children, **attributes)
```

Bases: `BaseTag`

This is for case-sensitive tags like those used in SVG generation.

Source code in `src/air/tags/models/base.py`

```
def __init__(self, *children: Renderable, **attributes: AttributeType) -> None:
    """Initialize a tag with renderable children and HTML attributes.

    Args:
        children: Renderable objects that become the tag's inner content.
        attributes: Attribute names and values applied to the tag element.
    """
    self._name = self.__class__.__name__
    self._module = self.__class__.__module__
    self._children: TagChildrenType = children
    self._attrs: TagAttributesType = attributes
```
