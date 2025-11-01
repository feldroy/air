# Tags N-S

## Object

```
Object(
    *children,
    archive=None,
    border=None,
    classid=None,
    codebase=None,
    codetype=None,
    data=None,
    declare=None,
    form=None,
    height=None,
    name=None,
    standby=None,
    type=None,
    usemap=None,
    width=None,
    class_=None,
    id=None,
    style=None,
    **kwargs,
)
```

Bases: `BaseTag`

Defines an embedded object

Parameters:

| Name              | Type             | Description                                        | Default                                                                  |
| ----------------- | ---------------- | -------------------------------------------------- | ------------------------------------------------------------------------ |
| `children`        | `Renderable`     | Tags, strings, or other rendered content.          | `()`                                                                     |
| `archive`         | \`str            | None\`                                             | A space-separated list of URIs for archives of resources for the object. |
| `border`          | \`str            | None\`                                             | The width of a border around the object.                                 |
| `classidcodebase` |                  | The codebase URL for the object.                   | *required*                                                               |
| `codetype`        | \`str            | None\`                                             | The content type of the code.                                            |
| `data`            | \`str            | None\`                                             | The address of the object's data.                                        |
| `declare`         | \`str            | None\`                                             | Declares the object without instantiating it.                            |
| `form`            | \`str            | None\`                                             | The form the object belongs to.                                          |
| `height`          | \`str            | int                                                | None\`                                                                   |
| `name`            | \`str            | None\`                                             | The name of the object.                                                  |
| `standby`         | \`str            | None\`                                             | A message to display while the object is loading.                        |
| `type`            | \`str            | None\`                                             | The content type of the data.                                            |
| `usemap`          | \`str            | None\`                                             | The name of a client-side image map to be used with the object.          |
| `width`           | \`str            | int                                                | None\`                                                                   |
| `class_`          | \`str            | None\`                                             | Substituted as the DOM class attribute.                                  |
| `id`              | \`str            | None\`                                             | DOM ID attribute.                                                        |
| `style`           | \`str            | None\`                                             | Inline style attribute.                                                  |
| `kwargs`          | `AttributesType` | Keyword arguments transformed into tag attributes. | `{}`                                                                     |

Source code in `src/air/tags/models/stock.py`

```
def __init__(
    self,
    *children: Renderable,
    archive: str | None = None,
    border: str | None = None,
    classid: str | None = None,
    codebase: str | None = None,
    codetype: str | None = None,
    data: str | None = None,
    declare: str | None = None,
    form: str | None = None,
    height: str | int | None = None,
    name: str | None = None,
    standby: str | None = None,
    type: str | None = None,
    usemap: str | None = None,
    width: str | int | None = None,
    class_: str | None = None,
    id: str | None = None,
    style: str | None = None,
    **kwargs: AttributesType,
) -> None:
    super().__init__(*children, **kwargs | locals_cleanup(locals()))
```

## Ol

```
Ol(
    *children,
    compact=None,
    reversed=None,
    start=None,
    type=None,
    class_=None,
    id=None,
    style=None,
    **kwargs,
)
```

Bases: `BaseTag`

Defines an ordered list

Parameters:

| Name       | Type             | Description                                        | Default                                                        |
| ---------- | ---------------- | -------------------------------------------------- | -------------------------------------------------------------- |
| `children` | `Renderable`     | Tags, strings, or other rendered content.          | `()`                                                           |
| `compact`  | \`str            | None\`                                             | Specifies that the list should be rendered in a compact style. |
| `reversed` | \`str            | None\`                                             | Specifies that the list order should be descending.            |
| `start`    | \`str            | None\`                                             | Specifies the start value of an ordered list.                  |
| `type`     | \`str            | None\`                                             | Specifies the kind of marker to use in the list.               |
| `class_`   | \`str            | None\`                                             | Substituted as the DOM class attribute.                        |
| `id`       | \`str            | None\`                                             | DOM ID attribute.                                              |
| `style`    | \`str            | None\`                                             | Inline style attribute.                                        |
| `kwargs`   | `AttributesType` | Keyword arguments transformed into tag attributes. | `{}`                                                           |

Source code in `src/air/tags/models/stock.py`

```
def __init__(
    self,
    *children: Renderable,
    compact: str | None = None,
    reversed: str | None = None,
    start: str | None = None,
    type: str | None = None,
    class_: str | None = None,
    id: str | None = None,
    style: str | None = None,
    **kwargs: AttributesType,
) -> None:
    super().__init__(*children, **kwargs | locals_cleanup(locals()))
```

## Optgroup

```
Optgroup(
    *children,
    disabled=None,
    label=None,
    class_=None,
    id=None,
    style=None,
    **kwargs,
)
```

Bases: `BaseTag`

Defines a group of related options in a drop-down list

Parameters:

| Name       | Type             | Description                                        | Default                                                    |
| ---------- | ---------------- | -------------------------------------------------- | ---------------------------------------------------------- |
| `children` | `Renderable`     | Tags, strings, or other rendered content.          | `()`                                                       |
| `disabled` | \`str            | None\`                                             | Indicates if items in the option group are not selectable. |
| `label`    | \`str            | None\`                                             | Specifies a label for the group of options.                |
| `class_`   | \`str            | None\`                                             | Substituted as the DOM class attribute.                    |
| `id`       | \`str            | None\`                                             | DOM ID attribute.                                          |
| `style`    | \`str            | None\`                                             | Inline style attribute.                                    |
| `kwargs`   | `AttributesType` | Keyword arguments transformed into tag attributes. | `{}`                                                       |

Source code in `src/air/tags/models/stock.py`

```
def __init__(
    self,
    *children: Renderable,
    disabled: str | None = None,
    label: str | None = None,
    class_: str | None = None,
    id: str | None = None,
    style: str | None = None,
    **kwargs: AttributesType,
) -> None:
    super().__init__(*children, **kwargs | locals_cleanup(locals()))
```

## Option

```
Option(
    *children,
    disabled=None,
    label=None,
    selected=None,
    value=None,
    class_=None,
    id=None,
    style=None,
    **kwargs,
)
```

Bases: `BaseTag`

Defines an option in a drop-down list

Parameters:

| Name       | Type             | Description                                        | Default                                                                |
| ---------- | ---------------- | -------------------------------------------------- | ---------------------------------------------------------------------- |
| `children` | `Renderable`     | Tags, strings, or other rendered content.          | `()`                                                                   |
| `disabled` | \`str            | None\`                                             | Indicates if the option is not selectable.                             |
| `label`    | \`str            | None\`                                             | Specifies a label for the option indicating the meaning of the option. |
| `selected` | \`bool           | None\`                                             | Specifies that the option should be pre-selected.                      |
| `value`    | \`str            | None\`                                             | Specifies the value to be sent with the form.                          |
| `class_`   | \`str            | None\`                                             | Substituted as the DOM class attribute.                                |
| `id`       | \`str            | None\`                                             | DOM ID attribute.                                                      |
| `style`    | \`str            | None\`                                             | Inline style attribute.                                                |
| `kwargs`   | `AttributesType` | Keyword arguments transformed into tag attributes. | `{}`                                                                   |

Source code in `src/air/tags/models/stock.py`

```
def __init__(
    self,
    *children: Renderable,
    disabled: str | None = None,
    label: str | None = None,
    selected: bool | None = None,
    value: str | None = None,
    class_: str | None = None,
    id: str | None = None,
    style: str | None = None,
    **kwargs: AttributesType,
) -> None:
    super().__init__(*children, **kwargs | locals_cleanup(locals()))
```

## Output

```
Output(
    *children,
    for_=None,
    form=None,
    name=None,
    class_=None,
    id=None,
    style=None,
    **kwargs,
)
```

Bases: `BaseTag`

Defines the result of a calculation

Parameters:

| Name       | Type             | Description                                        | Default                                                            |
| ---------- | ---------------- | -------------------------------------------------- | ------------------------------------------------------------------ |
| `children` | `Renderable`     | Tags, strings, or other rendered content.          | `()`                                                               |
| `for_`     | \`str            | None\`                                             | Lists the IDs of the elements that contributed to the calculation. |
| `form`     | \`str            | None\`                                             | Associates the output with a form element.                         |
| `name`     | \`str            | None\`                                             | Defines a name for the output element.                             |
| `class_`   | \`str            | None\`                                             | Substituted as the DOM class attribute.                            |
| `id`       | \`str            | None\`                                             | DOM ID attribute.                                                  |
| `style`    | \`str            | None\`                                             | Inline style attribute.                                            |
| `kwargs`   | `AttributesType` | Keyword arguments transformed into tag attributes. | `{}`                                                               |

Source code in `src/air/tags/models/stock.py`

```
def __init__(
    self,
    *children: Renderable,
    for_: str | None = None,
    form: str | None = None,
    name: str | None = None,
    class_: str | None = None,
    id: str | None = None,
    style: str | None = None,
    **kwargs: AttributesType,
) -> None:
    super().__init__(*children, **kwargs | locals_cleanup(locals()))
```

## Pre

```
Pre(
    *children,
    width=None,
    wrap=None,
    class_=None,
    id=None,
    style=None,
    **kwargs,
)
```

Bases: `BaseTag`

Defines preformatted text

Parameters:

| Name       | Type             | Description                                        | Default                                  |
| ---------- | ---------------- | -------------------------------------------------- | ---------------------------------------- |
| `children` | `Renderable`     | Tags, strings, or other rendered content.          | `()`                                     |
| `width`    | \`str            | int                                                | None\`                                   |
| `wrap`     | \`str            | None\`                                             | hint indicating how overflow must happen |
| `class_`   | \`str            | None\`                                             | Substituted as the DOM class attribute.  |
| `id`       | \`str            | None\`                                             | DOM ID attribute.                        |
| `style`    | \`str            | None\`                                             | Inline style attribute.                  |
| `kwargs`   | `AttributesType` | Keyword arguments transformed into tag attributes. | `{}`                                     |

Source code in `src/air/tags/models/stock.py`

```
def __init__(
    self,
    *children: Renderable,
    width: str | int | None = None,
    wrap: str | None = None,
    class_: str | None = None,
    id: str | None = None,
    style: str | None = None,
    **kwargs: AttributesType,
) -> None:
    super().__init__(*children, **kwargs | locals_cleanup(locals()))
```

## Progress

```
Progress(
    *children,
    max=None,
    value=None,
    class_=None,
    id=None,
    style=None,
    **kwargs,
)
```

Bases: `BaseTag`

Represents the progress of a task

Parameters:

| Name       | Type             | Description                                        | Default                                 |
| ---------- | ---------------- | -------------------------------------------------- | --------------------------------------- |
| `children` | `Renderable`     | Tags, strings, or other rendered content.          | `()`                                    |
| `max`      | \`str            | None\`                                             | The maximum value of the progress bar.  |
| `value`    | \`str            | None\`                                             | The current value of the progress bar.  |
| `class_`   | \`str            | None\`                                             | Substituted as the DOM class attribute. |
| `id`       | \`str            | None\`                                             | DOM ID attribute.                       |
| `style`    | \`str            | None\`                                             | Inline style attribute.                 |
| `kwargs`   | `AttributesType` | Keyword arguments transformed into tag attributes. | `{}`                                    |

Source code in `src/air/tags/models/stock.py`

```
def __init__(
    self,
    *children: Renderable,
    max: str | None = None,
    value: str | None = None,
    class_: str | None = None,
    id: str | None = None,
    style: str | None = None,
    **kwargs: AttributesType,
) -> None:
    super().__init__(*children, **kwargs | locals_cleanup(locals()))
```

## Q

```
Q(
    *children,
    cite=None,
    class_=None,
    id=None,
    style=None,
    **kwargs,
)
```

Bases: `BaseTag`

Defines a short quotation

Parameters:

| Name       | Type             | Description                                        | Default                                         |
| ---------- | ---------------- | -------------------------------------------------- | ----------------------------------------------- |
| `children` | `Renderable`     | Tags, strings, or other rendered content.          | `()`                                            |
| `cite`     | \`str            | None\`                                             | Specifies a URL to the source of the quotation. |
| `class_`   | \`str            | None\`                                             | Substituted as the DOM class attribute.         |
| `id`       | \`str            | None\`                                             | DOM ID attribute.                               |
| `style`    | \`str            | None\`                                             | Inline style attribute.                         |
| `kwargs`   | `AttributesType` | Keyword arguments transformed into tag attributes. | `{}`                                            |

Source code in `src/air/tags/models/stock.py`

```
def __init__(
    self,
    *children: Renderable,
    cite: str | None = None,
    class_: str | None = None,
    id: str | None = None,
    style: str | None = None,
    **kwargs: AttributesType,
) -> None:
    super().__init__(*children, **kwargs | locals_cleanup(locals()))
```

## Script

```
Script(
    text_child="",
    /,
    *,
    src=None,
    type=None,
    async_=False,
    defer=False,
    nomodule=False,
    crossorigin=None,
    integrity=None,
    referrerpolicy=None,
    fetchpriority=None,
    blocking=None,
    attributionsrc=None,
    nonce=None,
    class_=None,
    id=None,
    style=None,
    **kwargs,
)
```

Bases: `UnSafeTag`

Defines a client-side script. Warning: Script tag does not protect against code injection.

Parameters:

| Name             | Type                                                                                                                                                                          | Description                                                              | Default                                                                                                                                                                                             |
| ---------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `text_child`     | `str`                                                                                                                                                                         | Inline script code. Use an empty string when providing src.              | `''`                                                                                                                                                                                                |
| `src`            | \`str                                                                                                                                                                         | None\`                                                                   | URI of the external script.                                                                                                                                                                         |
| `type`           | \`str                                                                                                                                                                         | None\`                                                                   | Script type. Examples: module, importmap, speculationrules, a JavaScript MIME type (e.g. text/javascript), or empty for classic scripts.                                                            |
| `async_`         | `bool`                                                                                                                                                                        | Fetch in parallel and execute as soon as ready; order is not guaranteed. | `False`                                                                                                                                                                                             |
| `defer`          | `bool`                                                                                                                                                                        | Execute after parsing (classic scripts only; modules defer by default).  | `False`                                                                                                                                                                                             |
| `nomodule`       | `bool`                                                                                                                                                                        | Do not execute on browsers that support ES modules.                      | `False`                                                                                                                                                                                             |
| `crossorigin`    | \`Literal['anonymous', 'use-credentials']                                                                                                                                     | None\`                                                                   | CORS mode. One of "anonymous" or "use-credentials".                                                                                                                                                 |
| `integrity`      | \`str                                                                                                                                                                         | None\`                                                                   | Subresource Integrity hash (e.g. "sha384-...").                                                                                                                                                     |
| `referrerpolicy` | \`Literal['no-referrer', 'no-referrer-when-downgrade', 'origin', 'origin-when-cross-origin', 'same-origin', 'strict-origin', 'strict-origin-when-cross-origin', 'unsafe-url'] | None\`                                                                   | Which referrer to send. One of: "no-referrer", "no-referrer-when-downgrade", "origin", "origin-when-cross-origin", "same-origin", "strict-origin", "strict-origin-when-cross-origin", "unsafe-url". |
| `fetchpriority`  | \`Literal['high', 'low', 'auto']                                                                                                                                              | None\`                                                                   | Network priority hint. One of "high", "low", "auto".                                                                                                                                                |
| `blocking`       | \`Literal['render']                                                                                                                                                           | None\`                                                                   | Space-separated tokens that block operations; currently "render".                                                                                                                                   |
| `attributionsrc` | \`str                                                                                                                                                                         | None\`                                                                   | Space-separated URLs for Attribution Reporting (experimental).                                                                                                                                      |
| `nonce`          | \`str                                                                                                                                                                         | None\`                                                                   | CSP nonce (meaning: one-time token) to allow this inline script.                                                                                                                                    |
| `class_`         | \`str                                                                                                                                                                         | None\`                                                                   | Substituted as the DOM class attribute.                                                                                                                                                             |
| `id`             | \`str                                                                                                                                                                         | None\`                                                                   | DOM id attribute.                                                                                                                                                                                   |
| `style`          | \`str                                                                                                                                                                         | None\`                                                                   | Inline style attribute.                                                                                                                                                                             |
| `kwargs`         | `AttributesType`                                                                                                                                                              | Keyword arguments transformed into tag attributes.                       | `{}`                                                                                                                                                                                                |

Source code in `src/air/tags/models/special.py`

```
@override
def __init__(
    self,
    text_child: str = "",
    /,
    *,
    src: str | None = None,
    type: str | None = None,
    async_: bool = False,
    defer: bool = False,
    nomodule: bool = False,
    crossorigin: Literal["anonymous", "use-credentials"] | None = None,
    integrity: str | None = None,
    referrerpolicy: Literal[
        "no-referrer",
        "no-referrer-when-downgrade",
        "origin",
        "origin-when-cross-origin",
        "same-origin",
        "strict-origin",
        "strict-origin-when-cross-origin",
        "unsafe-url",
    ]
    | None = None,
    fetchpriority: Literal["high", "low", "auto"] | None = None,
    blocking: Literal["render"] | None = None,
    attributionsrc: str | None = None,
    nonce: str | None = None,
    class_: str | None = None,
    id: str | None = None,
    style: str | None = None,
    **kwargs: AttributesType,
) -> None:
    super().__init__(text_child, **kwargs | locals_cleanup(locals()))
```

## Select

```
Select(
    *children,
    autocomplete=None,
    autofocus=None,
    disabled=None,
    form=None,
    multiple=None,
    name=None,
    required=None,
    size=None,
    class_=None,
    id=None,
    style=None,
    **kwargs,
)
```

Bases: `BaseTag`

Defines a drop-down list

Parameters:

| Name           | Type             | Description                                        | Default                                                                             |
| -------------- | ---------------- | -------------------------------------------------- | ----------------------------------------------------------------------------------- |
| `children`     | `Renderable`     | Tags, strings, or other rendered content.          | `()`                                                                                |
| `autocomplete` | \`str            | None\`                                             | Hint for a user agent's autocomplete feature.                                       |
| `autofocus`    | \`str            | None\`                                             | Indicate that a form control should have input focus when the page loads.           |
| `disabled`     | \`str            | None\`                                             | Indicates that the user cannot interact with the control.                           |
| `form`         | \`str            | None\`                                             | Associates the drop-down list with a form element.                                  |
| `multiple`     | \`str            | None\`                                             | Indicates that multiple options can be selected at once.                            |
| `name`         | \`str            | None\`                                             | Specifies the name of the drop-down list.                                           |
| `required`     | \`str            | None\`                                             | Indicates that an option must be selected before the form can be submitted.         |
| `size`         | \`str            | None\`                                             | If drop-down list is a scrolling list box, specifies the number of visible options. |
| `class_`       | \`str            | None\`                                             | Substituted as the DOM class attribute.                                             |
| `id`           | \`str            | None\`                                             | DOM ID attribute.                                                                   |
| `style`        | \`str            | None\`                                             | Inline style attribute.                                                             |
| `kwargs`       | `AttributesType` | Keyword arguments transformed into tag attributes. | `{}`                                                                                |

Source code in `src/air/tags/models/stock.py`

```
def __init__(
    self,
    *children: Renderable,
    autocomplete: str | None = None,
    autofocus: str | None = None,
    disabled: str | None = None,
    form: str | None = None,
    multiple: str | None = None,
    name: str | None = None,
    required: str | None = None,
    size: str | None = None,
    class_: str | None = None,
    id: str | None = None,
    style: str | None = None,
    **kwargs: AttributesType,
) -> None:
    super().__init__(*children, **kwargs | locals_cleanup(locals()))
```

## Source

```
Source(
    *children,
    src=None,
    type=None,
    sizes=None,
    media=None,
    srcset=None,
    height=None,
    width=None,
    class_=None,
    id=None,
    style=None,
    **kwargs,
)
```

Bases: `BaseTag`

Defines multiple media resources for media elements ( and )

Parameters:

| Name       | Type             | Description                                        | Default                                                                   |
| ---------- | ---------------- | -------------------------------------------------- | ------------------------------------------------------------------------- |
| `children` | `Renderable`     | Tags, strings, or other rendered content.          | `()`                                                                      |
| `src`      | \`str            | None\`                                             | Specifies the URL of the media resource.                                  |
| `type`     | \`str            | None\`                                             | Specifies the MIME type of the media resource.                            |
| `sizes`    | \`str            | None\`                                             | List of source sizes that describe the final rendered width of the image. |
| `media`    | \`str            | None\`                                             | Specifies the media query for the media resource.                         |
| `srcset`   | \`str            | None\`                                             | Specifies a list of one or more image URLs and their descriptors.         |
| `height`   | \`str            | int                                                | None\`                                                                    |
| `width`    | \`str            | int                                                | None\`                                                                    |
| `class_`   | \`str            | None\`                                             | Substituted as the DOM class attribute.                                   |
| `id`       | \`str            | None\`                                             | DOM ID attribute.                                                         |
| `style`    | \`str            | None\`                                             | Inline style attribute.                                                   |
| `kwargs`   | `AttributesType` | Keyword arguments transformed into tag attributes. | `{}`                                                                      |

Source code in `src/air/tags/models/stock.py`

```
def __init__(
    self,
    *children: Renderable,
    src: str | None = None,
    type: str | None = None,
    sizes: str | None = None,
    media: str | None = None,
    srcset: str | None = None,
    height: str | int | None = None,
    width: str | int | None = None,
    class_: str | None = None,
    id: str | None = None,
    style: str | None = None,
    **kwargs: AttributesType,
) -> None:
    super().__init__(*children, **kwargs | locals_cleanup(locals()))
```

## Style

```
Style(
    text_child="",
    /,
    *,
    media=None,
    title=None,
    blocking=None,
    nonce=None,
    type=None,
    class_=None,
    id=None,
    style=None,
    **kwargs,
)
```

Bases: `UnSafeTag`

Defines style information for a document. Warning: Style tag does not protect against code injection.

Parameters:

| Name         | Type                | Description                                        | Default                                                                |
| ------------ | ------------------- | -------------------------------------------------- | ---------------------------------------------------------------------- |
| `text_child` | `str`               | CSS stylesheet text.                               | `''`                                                                   |
| `media`      | \`str               | None\`                                             | Media query (e.g. "(width < 500px)"). Defaults to "all".               |
| `title`      | \`str               | None\`                                             | Title for alternate style sheet sets.                                  |
| `blocking`   | \`Literal['render'] | None\`                                             | Space-separated tokens that block operations; currently "render".      |
| `nonce`      | \`str               | None\`                                             | CSP nonce (meaning: one-time token) to allow this inline style.        |
| `type`       | \`str               | None\`                                             | (Deprecated) Only "" or "text/css" are permitted; omit in modern HTML. |
| `class_`     | \`str               | None\`                                             | Substituted as the DOM class attribute.                                |
| `id`         | \`str               | None\`                                             | DOM id attribute.                                                      |
| `style`      | \`str               | None\`                                             | Inline style attribute.                                                |
| `kwargs`     | `AttributesType`    | Keyword arguments transformed into tag attributes. | `{}`                                                                   |

Source code in `src/air/tags/models/special.py`

```
@override
def __init__(
    self,
    text_child: str = "",
    /,
    *,
    media: str | None = None,
    title: str | None = None,
    blocking: Literal["render"] | None = None,
    nonce: str | None = None,
    type: str | None = None,  # deprecated
    class_: str | None = None,
    id: str | None = None,
    style: str | None = None,
    **kwargs: AttributesType,
) -> None:
    super().__init__(text_child, **kwargs | locals_cleanup(locals()))
```
