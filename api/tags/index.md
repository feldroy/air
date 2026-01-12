# Tags

Note

Tags, or **Air Tag**, are explained in the [concepts document about tags](https://docs.airwebframework.org/learn/air_tags/index.md).

In the spirit of helping our users, every **Air Tag** has copious documentation—enough that sometimes it breaks the documentation build process. Therefore, **Air Tag** that directly correspond to their HTML equivalents can be found in smaller, easier-to-compile pages.

- [HTML Air Tags A-D](https://docs.airwebframework.org/api/tags/tags-a-d/index.md)
- [HTML Air Tags E-M](https://docs.airwebframework.org/api/tags/tags-e-m/index.md)
- [HTML Air Tags N-S](https://docs.airwebframework.org/api/tags/tags-n-s/index.md)
- [HTML Air Tags T-Z](https://docs.airwebframework.org/api/tags/tags-t-z/index.md)

What remains on this page are core **Air Tag** that either have great utility (**Raw** and **Children** come to mind), or are base classes for other tags.

Easy to write and performant HTML content generation using Python classes to render HTML.

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
Raw(text_child='', /, **attributes)
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
def __init__(self, text_child: str = "", /, **attributes: AttributeType) -> None:
    if not isinstance(text_child, str):
        msg = f"{self!r} only accepts string content"
        raise TypeError(msg)
    if text_child:
        super().__init__(text_child, **attributes)
    else:
        super().__init__(**attributes)
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

## BaseTag

```
BaseTag(*children, **attributes)
```

Base tag for all other tags.

Sets four attributes, name, module, children, and attrs. These are important for Starlette view responses, as nested objects get auto-serialized to JSON and need to be rebuilt. With the values of these attributes, the object reconstruction can occur.

Parameters:

| Name         | Type            | Description                                             | Default |
| ------------ | --------------- | ------------------------------------------------------- | ------- |
| `children`   | `Renderable`    | Renderable objects that become the tag's inner content. | `()`    |
| `attributes` | `AttributeType` | Attribute names and values applied to the tag element.  | `{}`    |

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

### __eq__

```
__eq__(other)
```

Compare tags by their rendered HTML.

Parameters:

| Name    | Type     | Description                | Default    |
| ------- | -------- | -------------------------- | ---------- |
| `other` | `object` | Object to compare against. | *required* |

Returns:

| Type   | Description                          |
| ------ | ------------------------------------ |
| `bool` | True when the rendered HTML matches. |

Raises:

| Type        | Description                          |
| ----------- | ------------------------------------ |
| `TypeError` | If compared to a non-BaseTag object. |

Source code in `src/air/tags/models/base.py`

```
def __eq__(self, other: object, /) -> bool:
    """Compare tags by their rendered HTML.

    Args:
        other: Object to compare against.

    Returns:
        True when the rendered HTML matches.

    Raises:
        TypeError: If compared to a non-BaseTag object.
    """
    if not isinstance(other, BaseTag):
        msg = f"<{self.name}> is comparable only to other air-tags."
        raise TypeError(msg)
    return self.html == other.html
```

### __hash__

```
__hash__()
```

Return the hash of the rendered HTML representation.

Returns:

| Type  | Description                                 |
| ----- | ------------------------------------------- |
| `int` | Hash derived from the rendered HTML string. |

Source code in `src/air/tags/models/base.py`

```
def __hash__(self) -> int:
    """Return the hash of the rendered HTML representation.

    Returns:
        Hash derived from the rendered HTML string.
    """
    return hash(self.html)
```

### __init_subclass__

```
__init_subclass__()
```

Register subclasses so they can be restored from serialized data.

Source code in `src/air/tags/models/base.py`

```
def __init_subclass__(cls) -> None:
    """Register subclasses so they can be restored from serialized data."""
    super().__init_subclass__()
    BaseTag._registry[cls.__name__.lower()] = cls
```

### __new__

```
__new__(*children, **attributes)
```

Create a tag instance while preventing direct BaseTag instantiation.

Raises:

| Type        | Description                                       |
| ----------- | ------------------------------------------------- |
| `TypeError` | If code attempts to instantiate BaseTag directly. |

Source code in `src/air/tags/models/base.py`

```
def __new__(cls, *children: Renderable, **attributes: AttributeType) -> Self:
    """Create a tag instance while preventing direct BaseTag instantiation.

    Raises:
        TypeError: If code attempts to instantiate BaseTag directly.
    """
    if cls is BaseTag:
        msg = f"{cls.__name__} cannot be instantiated; use a subclass"
        raise TypeError(msg)
    return super().__new__(cls)
```

### __repr__

```
__repr__()
```

Return a concise representation showing the tag name and summary.

Returns:

| Type  | Description                                     |
| ----- | ----------------------------------------------- |
| `str` | A readable string representation for debugging. |

Source code in `src/air/tags/models/base.py`

```
def __repr__(self) -> str:
    """Return a concise representation showing the tag name and summary.

    Returns:
        A readable string representation for debugging.
    """
    summary = f'("{self._doc_summary}")' if self._doc_summary else ""
    return f"<air.{self.__class__.__name__}{summary}>"
```

### __str__

```
__str__()
```

Render the HTML representation of the tag.

Returns:

| Type  | Description               |
| ----- | ------------------------- |
| `str` | The rendered HTML string. |

Source code in `src/air/tags/models/base.py`

```
def __str__(self) -> str:
    """Render the HTML representation of the tag.

    Returns:
        The rendered HTML string.
    """
    return self.html
```

### attrs

```
attrs
```

Return the formatted HTML attributes string.

Returns:

| Type  | Description                                                     |
| ----- | --------------------------------------------------------------- |
| `str` | A string containing formatted attributes prefixed with a space, |
| `str` | or an empty string when no attributes are present.              |

### children

```
children
```

Render all child nodes into a single HTML string.

Returns:

| Type  | Description                                                         |
| ----- | ------------------------------------------------------------------- |
| `str` | Concatenated child HTML, or an empty string when no children exist. |

### compact_html

```
compact_html
```

Render the compact-formatted HTML representation of the tag.

Returns:

| Type  | Description                                             |
| ----- | ------------------------------------------------------- |
| `str` | A minimized HTML string produced by minify_html.minify. |

### compact_render

```
compact_render()
```

Render the compact-formatted HTML representation of the tag.

Returns:

| Type  | Description                                             |
| ----- | ------------------------------------------------------- |
| `str` | A minimized HTML string produced by minify_html.minify. |

Source code in `src/air/tags/models/base.py`

```
def compact_render(self) -> str:
    """Render the compact-formatted HTML representation of the tag.

    Returns:
        A minimized HTML string produced by `minify_html.minify`.
    """
    return compact_format_html(self._render())
```

### first_attribute

```
first_attribute
```

Return the first attribute key-value pair or None when none exist.

Returns:

| Type                        | Description |
| --------------------------- | ----------- |
| \`tuple[str, AttributeType] | None\`      |

### first_child

```
first_child
```

Return the first child or None when no children are present.

Returns:

| Type         | Description |
| ------------ | ----------- |
| \`Renderable | None\`      |

### from_dict

```
from_dict(source_dict)
```

Instantiate a tag hierarchy from serialized data.

Parameters:

| Name          | Type          | Description                         | Default    |
| ------------- | ------------- | ----------------------------------- | ---------- |
| `source_dict` | `TagDictType` | The dictionary produced by to_dict. | *required* |

Returns:

| Type      | Description                |
| --------- | -------------------------- |
| `BaseTag` | The restored tag instance. |

Source code in `src/air/tags/models/base.py`

```
@classmethod
def from_dict(cls, source_dict: TagDictType) -> BaseTag:
    """Instantiate a tag hierarchy from serialized data.

    Args:
        source_dict: The dictionary produced by `to_dict`.

    Returns:
        The restored tag instance.
    """
    name: str = source_dict[TagKeys.NAME]
    attributes: TagAttributesType = source_dict[TagKeys.ATTRIBUTES]
    children_dict: TagChildrenTypeForDict = source_dict[TagKeys.CHILDREN]
    children: TagChildrenType = cls._from_child_dict(children_dict)
    return cls._create_tag(name, *children, **attributes)
```

### from_html

```
from_html(html_source)
```

Reconstruct the corresponding air-tag tree from the given HTML content.

Parameters:

| Name          | Type  | Description            | Default    |
| ------------- | ----- | ---------------------- | ---------- |
| `html_source` | `str` | HTML content to parse. | *required* |

Returns:

| Type      | Description                                            |
| --------- | ------------------------------------------------------ |
| `BaseTag` | The root air-tag built from the provided HTML content. |

Raises:

| Type         | Description                      |
| ------------ | -------------------------------- |
| `TypeError`  | If html_source is not a string.  |
| `ValueError` | If the markup is not valid HTML. |

Source code in `src/air/tags/models/base.py`

```
@classmethod
def from_html(cls, html_source: str) -> BaseTag:
    """Reconstruct the corresponding air-tag tree from the given HTML content.

    Args:
        html_source: HTML content to parse.

    Returns:
        The root air-tag built from the provided HTML content.

    Raises:
        TypeError: If ``html_source`` is not a string.
        ValueError: If the markup is not valid HTML.
    """
    if not isinstance(html_source, str):
        msg = f"{cls.__name__}.from_html(html_source) expects a string argument."
        raise TypeError(msg)
    html_source = html_source.strip()
    if not looks_like_html(html_source):
        msg = f"{cls.__name__}.from_html(html_source) expects a valid HTML string."
        raise ValueError(msg)
    is_fragment = not is_full_html_document(html_source)
    parser = LexborHTMLParser(html_source, is_fragment=is_fragment)
    if not _is_lexbor_html_parser_valid(parser=parser, is_fragment=is_fragment):
        msg = f"{cls.__name__}.from_html(html_source) is unable to parse the HTML content."
        raise ValueError(msg)
    air_tag = cls._from_lexbor_node(parser.root)  # type: ignore[arg-type]
    if not air_tag or not isinstance(air_tag, BaseTag):
        msg = f"{cls.__name__}.from_html(html_source) is unable to parse the HTML content."
        raise ValueError(msg)
    return air_tag
```

### from_html_file

```
from_html_file(*, file_path)
```

Reconstruct the corresponding air-tag tree from the given HTML file.

Parameters:

| Name        | Type      | Description                                                                                   | Default    |
| ----------- | --------- | --------------------------------------------------------------------------------------------- | ---------- |
| `file_path` | `StrPath` | The file path pointing to the HTML file or a folder with an index file to be read and parsed. | *required* |

Returns:

| Type      | Description                                         |
| --------- | --------------------------------------------------- |
| `BaseTag` | The root air-tag built from the provided HTML file. |

Source code in `src/air/tags/models/base.py`

```
@classmethod
def from_html_file(cls, *, file_path: StrPath) -> BaseTag:
    """Reconstruct the corresponding air-tag tree from the given HTML file.

    Args:
        file_path: The file path pointing to the HTML file or a folder with an index file to be read and parsed.

    Returns:
        The root air-tag built from the provided HTML file.
    """
    return cls.from_html(html_source=read_html(file_path=file_path))
```

### from_html_file_to_source

```
from_html_file_to_source(*, file_path)
```

Reconstruct the instantiable-formatted representation of the tag from the given HTML file.

For converting the corresponding air-tag tree from the given HTML file, into the instantiable-formatted representation of the tag.

Parameters:

| Name        | Type      | Description                                                                                   | Default    |
| ----------- | --------- | --------------------------------------------------------------------------------------------- | ---------- |
| `file_path` | `StrPath` | The file path pointing to the HTML file or a folder with an index file to be read and parsed. | *required* |

Returns:

| Type  | Description                                                     |
| ----- | --------------------------------------------------------------- |
| `str` | The formatted instantiation call for this tag and its children. |

Source code in `src/air/tags/models/base.py`

```
@classmethod
def from_html_file_to_source(cls, *, file_path: StrPath) -> str:
    """Reconstruct the instantiable-formatted representation of the tag from the given HTML file.

    For converting the corresponding air-tag tree from the given HTML file,
    into the instantiable-formatted representation of the tag.

    Args:
        file_path: The file path pointing to the HTML file or a folder with an index file to be read and parsed.

    Returns:
        The formatted instantiation call for this tag and its children.
    """
    return cls.from_html_file(file_path=file_path).to_source()
```

### from_html_to_source

```
from_html_to_source(html_source)
```

Reconstruct the instantiable-formatted representation of the tag from the given HTML content.

For converting the corresponding air-tag tree from the given HTML content, into the instantiable-formatted representation of the tag.

Parameters:

| Name          | Type  | Description            | Default    |
| ------------- | ----- | ---------------------- | ---------- |
| `html_source` | `str` | HTML content to parse. | *required* |

Returns:

| Type  | Description                                                     |
| ----- | --------------------------------------------------------------- |
| `str` | The formatted instantiation call for this tag and its children. |

Source code in `src/air/tags/models/base.py`

```
@classmethod
def from_html_to_source(cls, html_source: str) -> str:
    """Reconstruct the instantiable-formatted representation of the tag from the given HTML content.

    For converting the corresponding air-tag tree from the given HTML content,
    into the instantiable-formatted representation of the tag.

    Args:
        html_source: HTML content to parse.

    Returns:
        The formatted instantiation call for this tag and its children.
    """
    return cls.from_html(html_source).to_source()
```

### from_json

```
from_json(source_json)
```

Instantiate a tag hierarchy from JSON.

Parameters:

| Name          | Type  | Description                          | Default    |
| ------------- | ----- | ------------------------------------ | ---------- |
| `source_json` | `str` | The JSON string produced by to_json. | *required* |

Returns:

| Type      | Description                |
| --------- | -------------------------- |
| `BaseTag` | The restored tag instance. |

Source code in `src/air/tags/models/base.py`

```
@classmethod
def from_json(cls, source_json: str) -> BaseTag:
    """Instantiate a tag hierarchy from JSON.

    Args:
        source_json: The JSON string produced by `to_json`.

    Returns:
        The restored tag instance.
    """
    return cls.from_dict(json.loads(source_json))
```

### full_repr

```
full_repr()
```

Return an expanded representation including attributes and children.

Returns:

| Type  | Description                                              |
| ----- | -------------------------------------------------------- |
| `str` | The expanded string representation of the tag hierarchy. |

Source code in `src/air/tags/models/base.py`

```
def full_repr(self) -> str:
    """Return an expanded representation including attributes and children.

    Returns:
        The expanded string representation of the tag hierarchy.
    """
    attributes = f"{TagKeys.ATTRIBUTES}={self._attrs}" if self._attrs else ""
    children = INLINE_JOIN_SEPARATOR.join(
        child.full_repr() if isinstance(child, BaseTag) else child for child in self._children
    )  # ty: ignore[no-matching-overload]
    children_str = f"{attributes and ', '}{TagKeys.CHILDREN}={children}" if self._children else ""
    return f"{self._name}({attributes}{children_str})"
```

### has_attributes

```
has_attributes
```

Return True when the tag defines one or more attributes.

Returns:

| Type   | Description                                        |
| ------ | -------------------------------------------------- |
| `bool` | True when attributes are present; otherwise False. |

### has_children

```
has_children
```

Return True when the tag contains one or more children.

Returns:

| Type   | Description                                      |
| ------ | ------------------------------------------------ |
| `bool` | True when children are present; otherwise False. |

### html

```
html
```

Render the HTML representation of the tag.

Returns:

| Type  | Description               |
| ----- | ------------------------- |
| `str` | The rendered HTML string. |

### is_attribute_free_void_element

```
is_attribute_free_void_element
```

Check whether the tag has neither attributes nor children.

Returns:

| Type   | Description                                          |
| ------ | ---------------------------------------------------- |
| `bool` | True when the tag has no attributes and no children. |

### last_attribute

```
last_attribute
```

Return the last attribute key-value pair or None when none exist.

Returns:

| Type                        | Description |
| --------------------------- | ----------- |
| \`tuple[str, AttributeType] | None\`      |

### last_child

```
last_child
```

Return the last child or None when no children are present.

Returns:

| Type         | Description |
| ------------ | ----------- |
| \`Renderable | None\`      |

### name

```
name
```

Return the normalized tag name.

Returns:

| Type  | Description                             |
| ----- | --------------------------------------- |
| `str` | The lowercase tag name for use in HTML. |

### num_of_attributes

```
num_of_attributes
```

Return the number of defined attributes.

Returns:

| Type  | Description              |
| ----- | ------------------------ |
| `int` | The count of attributes. |

### num_of_direct_children

```
num_of_direct_children
```

Return the number of the direct children for an element.

Returns:

| Type  | Description            |
| ----- | ---------------------- |
| `int` | The count of children. |

### pretty_display_in_the_browser

```
pretty_display_in_the_browser()
```

Display pretty-formatted HTML in the browser.

Source code in `src/air/tags/models/base.py`

```
def pretty_display_in_the_browser(self) -> None:
    """Display pretty-formatted HTML in the browser."""
    display_pretty_html_in_the_browser(self.pretty_render(with_body=True, with_doctype=True))
```

### pretty_html

```
pretty_html
```

Render prettified-formatted HTML representation of the tag.

Returns:

| Type  | Description                           |
| ----- | ------------------------------------- |
| `str` | The prettified-formatted HTML string, |

### pretty_print

```
pretty_print()
```

Display pretty-formatted HTML in the console with syntax highlighting.

Source code in `src/air/tags/models/base.py`

```
def pretty_print(self) -> None:
    """Display pretty-formatted HTML in the console with syntax highlighting."""
    pretty_print_html(self.pretty_render())
```

### pretty_render

```
pretty_render(
    *, with_body=False, with_head=False, with_doctype=False
)
```

Render the prettified-formatted HTML representation of the tag.

Parameters:

| Name           | Type   | Description                                              | Default |
| -------------- | ------ | -------------------------------------------------------- | ------- |
| `with_body`    | `bool` | Whether to wrap the HTML inside a <body> element.        | `False` |
| `with_head`    | `bool` | Whether to generate a <head> element.                    | `False` |
| `with_doctype` | `bool` | Whether to prefix the output with a doctype declaration. | `False` |

Returns:

| Type  | Description                       |
| ----- | --------------------------------- |
| `str` | The pretty-formatted HTML string. |

Source code in `src/air/tags/models/base.py`

```
def pretty_render(
    self,
    *,
    with_body: bool = False,
    with_head: bool = False,
    with_doctype: bool = False,
) -> str:
    """Render the prettified-formatted HTML representation of the tag.

    Args:
        with_body: Whether to wrap the HTML inside a `<body>` element.
        with_head: Whether to generate a `<head>` element.
        with_doctype: Whether to prefix the output with a doctype declaration.

    Returns:
        The pretty-formatted HTML string.
    """
    return pretty_format_html(self._render(), with_body=with_body, with_head=with_head, with_doctype=with_doctype)
```

### pretty_render_in_the_browser

```
pretty_render_in_the_browser()
```

Render pretty-formatted HTML and open the result in a browser tab.

Source code in `src/air/tags/models/base.py`

```
def pretty_render_in_the_browser(self) -> None:
    """Render pretty-formatted HTML and open the result in a browser tab."""
    open_html_in_the_browser(self.pretty_render(with_body=True, with_doctype=True))
```

### pretty_save

```
pretty_save(*, file_path)
```

Persist pretty-formatted HTML to disk.

Parameters:

| Name        | Type      | Description                                | Default    |
| ----------- | --------- | ------------------------------------------ | ---------- |
| `file_path` | `StrPath` | Destination path for the pretty HTML file. | *required* |

Source code in `src/air/tags/models/base.py`

```
def pretty_save(self, *, file_path: StrPath) -> None:
    """Persist pretty-formatted HTML to disk.

    Args:
        file_path: Destination path for the pretty HTML file.
    """
    save_text(text=self.pretty_render(), file_path=file_path)
```

### print_source

```
print_source(html_source)
```

Display the instantiable-formatted representation of the tag in the console with syntax highlighting.

1. Reconstruct the corresponding air-tag tree from the given HTML content.
1. Convert air-tag tree into the instantiable-formatted representation of the tag.
1. Display it with syntax highlighting inside a styled terminal panel.

Parameters:

| Name          | Type  | Description            | Default    |
| ------------- | ----- | ---------------------- | ---------- |
| `html_source` | `str` | HTML content to parse. | *required* |

Source code in `src/air/tags/models/base.py`

```
@classmethod
def print_source(cls, html_source: str) -> None:
    """Display the instantiable-formatted representation of the tag in the console with syntax highlighting.

    1. Reconstruct the corresponding air-tag tree from the given HTML content.
    2. Convert air-tag tree into the instantiable-formatted representation of the tag.
    3. Display it with syntax highlighting inside a styled terminal panel.

    Args:
        html_source: HTML content to parse.
    """
    pretty_print_python(cls.from_html(html_source).to_source())
```

### render

```
render()
```

Render the HTML representation of the tag.

Returns:

| Type  | Description               |
| ----- | ------------------------- |
| `str` | The rendered HTML string. |

Source code in `src/air/tags/models/base.py`

```
def render(self) -> str:
    """Render the HTML representation of the tag.

    Returns:
        The rendered HTML string.
    """
    return self.html
```

### render_in_the_browser

```
render_in_the_browser()
```

Render the tag and open the result in a browser tab.

Source code in `src/air/tags/models/base.py`

```
def render_in_the_browser(self) -> None:
    """Render the tag and open the result in a browser tab."""
    open_html_in_the_browser(self.render())
```

### save

```
save(*, file_path)
```

Persist the rendered HTML to disk.

Parameters:

| Name        | Type      | Description                         | Default    |
| ----------- | --------- | ----------------------------------- | ---------- |
| `file_path` | `StrPath` | Destination path for the HTML file. | *required* |

Source code in `src/air/tags/models/base.py`

```
def save(self, *, file_path: StrPath) -> None:
    """Persist the rendered HTML to disk.

    Args:
        file_path: Destination path for the HTML file.
    """
    save_text(text=self.render(), file_path=file_path)
```

### save_source

```
save_source(*, file_path, html_source)
```

Save the instantiable-formatted representation of the tag to disk.

1. Reconstruct the corresponding air-tag tree from the given HTML content.
1. Convert air-tag tree into the instantiable-formatted representation of the tag.
1. Save the Python expression that reconstructs this tag to disk.

Parameters:

| Name          | Type      | Description                        | Default    |
| ------------- | --------- | ---------------------------------- | ---------- |
| `html_source` | `str`     | HTML content to parse.             | *required* |
| `file_path`   | `StrPath` | Destination path for the .py file. | *required* |

Source code in `src/air/tags/models/base.py`

```
@classmethod
def save_source(cls, *, file_path: StrPath, html_source: str) -> None:
    """Save the instantiable-formatted representation of the tag to disk.

    1. Reconstruct the corresponding air-tag tree from the given HTML content.
    2. Convert air-tag tree into the instantiable-formatted representation of the tag.
    3. Save the Python expression that reconstructs this tag to disk.

    Args:
        html_source: HTML content to parse.
        file_path: Destination path for the .py file.
    """
    save_text(text=cls.from_html(html_source).to_source(), file_path=file_path)
```

### tag_id

```
tag_id
```

Return the tag's `id_` attribute when present.

Returns:

| Type            | Description |
| --------------- | ----------- |
| \`AttributeType | None\`      |

### to_dict

```
to_dict()
```

Convert the tag into a JSON-serializable dictionary.

Returns:

| Type          | Description                                                       |
| ------------- | ----------------------------------------------------------------- |
| `TagDictType` | A mapping with the tag name, attributes, and serialized children. |

Source code in `src/air/tags/models/base.py`

```
def to_dict(self) -> TagDictType:
    """Convert the tag into a JSON-serializable dictionary.

    Returns:
        A mapping with the tag name, attributes, and serialized children.
    """
    return {
        TagKeys.NAME: self._name,
        TagKeys.ATTRIBUTES: self._attrs,
        TagKeys.CHILDREN: self._to_child_dict(),
    }
```

### to_json

```
to_json(*, indent_size=None)
```

Serialize the tag to JSON.

Parameters:

| Name          | Type  | Description | Default                                       |
| ------------- | ----- | ----------- | --------------------------------------------- |
| `indent_size` | \`int | None\`      | Indentation width to use for pretty-printing. |

Returns:

| Type  | Description                                |
| ----- | ------------------------------------------ |
| `str` | The JSON string representation of the tag. |

Source code in `src/air/tags/models/base.py`

```
def to_json(self, *, indent_size: int | None = None) -> str:
    """Serialize the tag to JSON.

    Args:
        indent_size: Indentation width to use for pretty-printing.

    Returns:
        The JSON string representation of the tag.
    """
    return json.dumps(self.to_dict(), ensure_ascii=False, indent=indent_size)
```

### to_pretty_dict

```
to_pretty_dict(
    *,
    max_width=170,
    max_length=7,
    max_depth=4,
    max_string=25,
    expand_all=False,
)
```

Produce a human-friendly mapping view of the tag.

Returns:

| Type  | Description                                                            |
| ----- | ---------------------------------------------------------------------- |
| `str` | A formatted string produced by the rich pretty printer when available, |
| `str` | otherwise the standard string form of the mapping.                     |

Source code in `src/air/tags/models/base.py`

```
def to_pretty_dict(
    self,
    *,
    max_width: int = 170,
    max_length: int = 7,
    max_depth: int = 4,
    max_string: int = 25,
    expand_all: bool = False,
) -> str:
    """Produce a human-friendly mapping view of the tag.

    Returns:
        A formatted string produced by the rich pretty printer when available,
        otherwise the standard string form of the mapping.
    """
    return pretty_repr(
        self.to_dict(),
        max_width=max_width,
        max_length=max_length,
        max_depth=max_depth,
        max_string=max_string,
        expand_all=expand_all,
    )
```

### to_pretty_json

```
to_pretty_json()
```

Serialize the tag to formatted JSON.

Returns:

| Type  | Description                                         |
| ----- | --------------------------------------------------- |
| `str` | The indented JSON string representation of the tag. |

Source code in `src/air/tags/models/base.py`

```
def to_pretty_json(self) -> str:
    """Serialize the tag to formatted JSON.

    Returns:
        The indented JSON string representation of the tag.
    """
    return self.to_json(indent_size=DEFAULT_INDENTATION_SIZE)
```

### to_source

```
to_source()
```

Return a Python expression that reconstructs this tag.

Convert this air-tag into the instantiable-formatted representation of the tag.

Returns:

| Type  | Description                                                     |
| ----- | --------------------------------------------------------------- |
| `str` | The formatted instantiation call for this tag and its children. |

Source code in `src/air/tags/models/base.py`

```
def to_source(self) -> str:
    """Return a Python expression that reconstructs this tag.

    Convert this air-tag into the instantiable-formatted representation of the tag.

    Returns:
        The formatted instantiation call for this tag and its children.
    """
    return self._to_source()
```
