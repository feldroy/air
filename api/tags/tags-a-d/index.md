# Tags A-D

## A

```
A(
    *children,
    href=None,
    target=None,
    download=None,
    rel=None,
    hreflang=None,
    type=None,
    referrerpolicy=None,
    media=None,
    ping=None,
    class_=None,
    id=None,
    style=None,
    **kwargs,
)
```

Bases: `BaseTag`

Defines a hyperlink

Parameters:

| Name             | Type             | Description                                        | Default                                                                                                                                                                                      |
| ---------------- | ---------------- | -------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `children`       | `Renderable`     | Tags, strings, or other rendered content.          | `()`                                                                                                                                                                                         |
| `href`           | \`str            | None\`                                             | Specifies the URL of the page the link goes to.                                                                                                                                              |
| `target`         | \`str            | None\`                                             | Specifies where to open the linked document.                                                                                                                                                 |
| `download`       | \`str            | None\`                                             | Specifies that the target will be downloaded when a user clicks on the hyperlink.                                                                                                            |
| `rel`            | \`str            | None\`                                             | Specifies the relationship between the current document and the linked document.                                                                                                             |
| `hreflang`       | \`str            | None\`                                             | Specifies the language of the linked document.                                                                                                                                               |
| `type`           | \`str            | None\`                                             | Specifies the media type of the linked document.                                                                                                                                             |
| `referrerpolicy` | \`str            | None\`                                             | Specifies which referrer information to send with the link.                                                                                                                                  |
| `media`          | \`str            | None\`                                             | Specifies what media/device the linked document is optimized for.                                                                                                                            |
| `ping`           | \`str            | None\`                                             | Specifies a space-separated list of URLs to which, when the link is followed, post requests with the body ping will be sent by the browser (in the background). Typically used for tracking. |
| `class_`         | \`str            | None\`                                             | Substituted as the DOM class attribute.                                                                                                                                                      |
| `id`             | \`str            | None\`                                             | DOM ID attribute.                                                                                                                                                                            |
| `style`          | \`str            | None\`                                             | Inline style attribute.                                                                                                                                                                      |
| `kwargs`         | `AttributesType` | Keyword arguments transformed into tag attributes. | `{}`                                                                                                                                                                                         |

Source code in `src/air/tags/models/stock.py`

```
def __init__(
    self,
    *children: Renderable,
    href: str | None = None,
    target: str | None = None,
    download: str | None = None,
    rel: str | None = None,
    hreflang: str | None = None,
    type: str | None = None,
    referrerpolicy: str | None = None,
    media: str | None = None,
    ping: str | None = None,
    class_: str | None = None,
    id: str | None = None,
    style: str | None = None,
    **kwargs: AttributesType,
) -> None:
    super().__init__(*children, **kwargs | locals_cleanup(locals()))
```

## Area

```
Area(
    *,
    alt=None,
    coords=None,
    download=None,
    href=None,
    ping=None,
    referrerpolicy=None,
    rel=None,
    shape=None,
    target=None,
    class_=None,
    id=None,
    style=None,
    **kwargs,
)
```

Bases: `SelfClosingTag`

Defines an area inside an image map

Parameters:

| Name             | Type             | Description                                        | Default                                                                                                                                                                                      |
| ---------------- | ---------------- | -------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `alt`            | \`str            | None\`                                             | Specifies an alternate text for an area. Required if the href attribute is present.                                                                                                          |
| `coords`         | \`str            | None\`                                             | Specifies the coordinates of an area.                                                                                                                                                        |
| `download`       | \`str            | None\`                                             | Specifies that the target will be downloaded when a user clicks on the hyperlink.                                                                                                            |
| `href`           | \`str            | None\`                                             | Specifies the URL of the page the link goes to.                                                                                                                                              |
| `ping`           | \`str            | None\`                                             | Specifies a space-separated list of URLs to which, when the link is followed, post requests with the body ping will be sent by the browser (in the background). Typically used for tracking. |
| `referrerpolicy` | \`str            | None\`                                             | Specifies which referrer information to send with the link.                                                                                                                                  |
| `rel`            | \`str            | None\`                                             | Specifies the relationship between the current document and the linked document.                                                                                                             |
| `shape`          | \`str            | None\`                                             | Specifies the shape of an area.                                                                                                                                                              |
| `target`         | \`str            | None\`                                             | Specifies where to open the linked document.                                                                                                                                                 |
| `class_`         | \`str            | None\`                                             | Substituted as the DOM class attribute.                                                                                                                                                      |
| `id`             | \`str            | None\`                                             | DOM ID attribute.                                                                                                                                                                            |
| `style`          | \`str            | None\`                                             | Inline style attribute.                                                                                                                                                                      |
| `kwargs`         | `AttributesType` | Keyword arguments transformed into tag attributes. | `{}`                                                                                                                                                                                         |

Source code in `src/air/tags/models/stock.py`

```
def __init__(
    self,
    *,
    alt: str | None = None,
    coords: str | None = None,
    download: str | None = None,
    href: str | None = None,
    ping: str | None = None,
    referrerpolicy: str | None = None,
    rel: str | None = None,
    shape: str | None = None,
    target: str | None = None,
    class_: str | None = None,
    id: str | None = None,
    style: str | None = None,
    **kwargs: AttributesType,
) -> None:
    super().__init__(**kwargs | locals_cleanup(locals()))
```

## Audio

```
Audio(
    *children,
    autoplay=None,
    controls=None,
    loop=None,
    muted=None,
    preload=None,
    src=None,
    class_=None,
    id=None,
    style=None,
    **kwargs,
)
```

Bases: `BaseTag`

Defines embedded sound content

Parameters:

| Name       | Type             | Description                                        | Default                                                                                |
| ---------- | ---------------- | -------------------------------------------------- | -------------------------------------------------------------------------------------- |
| `children` | `Renderable`     | Tags, strings, or other rendered content.          | `()`                                                                                   |
| `autoplay` | \`str            | None\`                                             | Specifies that the audio will start playing as soon as it is ready.                    |
| `controls` | \`str            | None\`                                             | Specifies that audio controls should be displayed (such as a play/pause button etc).   |
| `loop`     | \`str            | None\`                                             | Specifies that the audio will start over again, every time it is finished.             |
| `muted`    | \`str            | None\`                                             | Specifies that the audio output should be muted.                                       |
| `preload`  | \`str            | None\`                                             | Specifies if and how the author thinks the audio should be loaded when the page loads. |
| `src`      | \`str            | None\`                                             | Specifies the URL of the audio file.                                                   |
| `class_`   | \`str            | None\`                                             | Substituted as the DOM class attribute.                                                |
| `id`       | \`str            | None\`                                             | DOM ID attribute.                                                                      |
| `style`    | \`str            | None\`                                             | Inline style attribute.                                                                |
| `kwargs`   | `AttributesType` | Keyword arguments transformed into tag attributes. | `{}`                                                                                   |

Source code in `src/air/tags/models/stock.py`

```
def __init__(
    self,
    *children: Renderable,
    autoplay: str | None = None,
    controls: str | None = None,
    loop: str | None = None,
    muted: str | None = None,
    preload: str | None = None,
    src: str | None = None,
    class_: str | None = None,
    id: str | None = None,
    style: str | None = None,
    **kwargs: AttributesType,
) -> None:
    super().__init__(*children, **kwargs | locals_cleanup(locals()))
```

## Base

```
Base(
    *,
    href=None,
    target=None,
    class_=None,
    id=None,
    style=None,
    **kwargs,
)
```

Bases: `SelfClosingTag`

Specifies the base URL/target for all relative URLs in a document

Parameters:

| Name     | Type             | Description                                        | Default                                 |
| -------- | ---------------- | -------------------------------------------------- | --------------------------------------- |
| `class_` | \`str            | None\`                                             | Substituted as the DOM class attribute. |
| `id`     | \`str            | None\`                                             | DOM ID attribute.                       |
| `style`  | \`str            | None\`                                             | Inline style attribute.                 |
| `kwargs` | `AttributesType` | Keyword arguments transformed into tag attributes. | `{}`                                    |

Source code in `src/air/tags/models/stock.py`

```
def __init__(
    self,
    *,
    href: str | None = None,
    target: str | None = None,
    class_: str | None = None,
    id: str | None = None,
    style: str | None = None,
    **kwargs: AttributesType,
) -> None:
    super().__init__(**kwargs | locals_cleanup(locals()))
```

## Bdi

```
Bdi(*children, class_=None, id=None, style=None, **kwargs)
```

Bases: `BaseTag`

Isolates a part of text that might be formatted in a different direction from other text outside it

Parameters:

| Name       | Type             | Description                                        | Default                                 |
| ---------- | ---------------- | -------------------------------------------------- | --------------------------------------- |
| `children` | `Renderable`     | Tags, strings, or other rendered content.          | `()`                                    |
| `class_`   | \`str            | None\`                                             | Substituted as the DOM class attribute. |
| `id`       | \`str            | None\`                                             | DOM ID attribute.                       |
| `style`    | \`str            | None\`                                             | Inline style attribute.                 |
| `kwargs`   | `AttributesType` | Keyword arguments transformed into tag attributes. | `{}`                                    |

Source code in `src/air/tags/models/stock.py`

```
def __init__(
    self,
    *children: Renderable,
    class_: str | None = None,
    id: str | None = None,
    style: str | None = None,
    **kwargs: AttributesType,
) -> None:
    super().__init__(*children, **kwargs | locals_cleanup(locals()))
```

## Blockquote

```
Blockquote(
    *children,
    cite=None,
    class_=None,
    id=None,
    style=None,
    **kwargs,
)
```

Bases: `BaseTag`

Defines a section that is quoted from another source

Parameters:

| Name       | Type             | Description                                        | Default                                 |
| ---------- | ---------------- | -------------------------------------------------- | --------------------------------------- |
| `children` | `Renderable`     | Tags, strings, or other rendered content.          | `()`                                    |
| `cite`     | \`str            | None\`                                             | Specifies the source of the quotation.  |
| `class_`   | \`str            | None\`                                             | Substituted as the DOM class attribute. |
| `id`       | \`str            | None\`                                             | DOM ID attribute.                       |
| `style`    | \`str            | None\`                                             | Inline style attribute.                 |
| `kwargs`   | `AttributesType` | Keyword arguments transformed into tag attributes. | `{}`                                    |

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

## Button

```
Button(
    *children,
    name=None,
    type=None,
    value=None,
    autofocus=None,
    disabled=None,
    form=None,
    formaction=None,
    formenctype=None,
    formmethod=None,
    formnovalidate=None,
    formtarget=None,
    popovertarget=None,
    popovertargetaction=None,
    class_=None,
    id=None,
    style=None,
    **kwargs,
)
```

Bases: `BaseTag`

Defines a clickable button

Parameters:

| Name                  | Type             | Description                                        | Default                                                                                                     |
| --------------------- | ---------------- | -------------------------------------------------- | ----------------------------------------------------------------------------------------------------------- |
| `children`            | `Renderable`     | Tags, strings, or other rendered content.          | `()`                                                                                                        |
| `name`                | \`str            | None\`                                             | Specifies a name for the button.                                                                            |
| `type`                | \`str            | None\`                                             | Specifies the type of button.                                                                               |
| `value`               | \`str            | None\`                                             | Specifies an initial value for the button.                                                                  |
| `autofocus`           | \`str            | None\`                                             | Specifies that a button should automatically get focus when the page loads.                                 |
| `disabled`            | \`str            | None\`                                             | Specifies that a button should be disabled.                                                                 |
| `form`                | \`str            | None\`                                             | Specifies which form the button belongs to.                                                                 |
| `formaction`          | \`str            | None\`                                             | Specifies where to send the form-data when a form is submitted. Only for type="submit".                     |
| `formenctype`         | \`str            | None\`                                             | Specifies how the form-data should be encoded before sending it to a server. Only for type="submit".        |
| `formmethod`          | \`str            | None\`                                             | Specifies how to send the form-data (which HTTP method to use). Only for type="submit".                     |
| `formnovalidate`      | \`str            | None\`                                             | Specifies that the form-data should not be validated on submission. Only for type="submit".                 |
| `formtarget`          | \`str            | None\`                                             | Specifies where to display the response that is received after submitting the form. Only for type="submit". |
| `popovertarget`       | \`str            | None\`                                             | Specifies which popover element to invoke.                                                                  |
| `popovertargetaction` | \`str            | None\`                                             | Specifies what action to perform on the popover element.                                                    |
| `class_`              | \`str            | None\`                                             | Substituted as the DOM class attribute.                                                                     |
| `id`                  | \`str            | None\`                                             | DOM ID attribute.                                                                                           |
| `style`               | \`str            | None\`                                             | Inline style attribute.                                                                                     |
| `kwargs`              | `AttributesType` | Keyword arguments transformed into tag attributes. | `{}`                                                                                                        |

Source code in `src/air/tags/models/stock.py`

```
def __init__(
    self,
    *children: Renderable,
    name: str | None = None,
    type: str | None = None,
    value: str | None = None,
    autofocus: str | None = None,
    disabled: str | None = None,
    form: str | None = None,
    formaction: str | None = None,
    formenctype: str | None = None,
    formmethod: str | None = None,
    formnovalidate: str | None = None,
    formtarget: str | None = None,
    popovertarget: str | None = None,
    popovertargetaction: str | None = None,
    class_: str | None = None,
    id: str | None = None,
    style: str | None = None,
    **kwargs: AttributesType,
) -> None:
    super().__init__(*children, **kwargs | locals_cleanup(locals()))
```

## Canvas

```
Canvas(
    *children,
    width=None,
    height=None,
    class_=None,
    id=None,
    style=None,
    **kwargs,
)
```

Bases: `BaseTag`

Used to draw graphics, on the fly, via scripting (usually JavaScript)

Parameters:

| Name       | Type             | Description                                        | Default                                 |
| ---------- | ---------------- | -------------------------------------------------- | --------------------------------------- |
| `children` | `Renderable`     | Tags, strings, or other rendered content.          | `()`                                    |
| `width`    | \`str            | int                                                | None\`                                  |
| `height`   | \`str            | int                                                | None\`                                  |
| `class_`   | \`str            | None\`                                             | Substituted as the DOM class attribute. |
| `id`       | \`str            | None\`                                             | DOM ID attribute.                       |
| `style`    | \`str            | None\`                                             | Inline style attribute.                 |
| `kwargs`   | `AttributesType` | Keyword arguments transformed into tag attributes. | `{}`                                    |

Source code in `src/air/tags/models/stock.py`

```
def __init__(
    self,
    *children: Renderable,
    width: str | int | None = None,
    height: str | int | None = None,
    class_: str | None = None,
    id: str | None = None,
    style: str | None = None,
    **kwargs: AttributesType,
) -> None:
    super().__init__(*children, **kwargs | locals_cleanup(locals()))
```

## Col

```
Col(
    *, span=None, class_=None, id=None, style=None, **kwargs
)
```

Bases: `SelfClosingTag`

Specifies column properties for each column within a element

Parameters:

| Name     | Type             | Description                                        | Default                                                |
| -------- | ---------------- | -------------------------------------------------- | ------------------------------------------------------ |
| `span`   | \`str            | None\`                                             | Specifies the number of columns a element should span. |
| `class_` | \`str            | None\`                                             | Substituted as the DOM class attribute.                |
| `id`     | \`str            | None\`                                             | DOM ID attribute.                                      |
| `style`  | \`str            | None\`                                             | Inline style attribute.                                |
| `kwargs` | `AttributesType` | Keyword arguments transformed into tag attributes. | `{}`                                                   |

Source code in `src/air/tags/models/stock.py`

```
def __init__(
    self,
    *,
    span: str | None = None,
    class_: str | None = None,
    id: str | None = None,
    style: str | None = None,
    **kwargs: AttributesType,
) -> None:
    super().__init__(**kwargs | locals_cleanup(locals()))
```

## Colgroup

```
Colgroup(
    *children,
    span=None,
    class_=None,
    id=None,
    style=None,
    **kwargs,
)
```

Bases: `BaseTag`

Specifies a group of one or more columns in a table for formatting

Parameters:

| Name       | Type             | Description                                        | Default                                                |
| ---------- | ---------------- | -------------------------------------------------- | ------------------------------------------------------ |
| `children` | `Renderable`     | Tags, strings, or other rendered content.          | `()`                                                   |
| `span`     | \`str            | None\`                                             | Specifies the number of columns a element should span. |
| `class_`   | \`str            | None\`                                             | Substituted as the DOM class attribute.                |
| `id`       | \`str            | None\`                                             | DOM ID attribute.                                      |
| `style`    | \`str            | None\`                                             | Inline style attribute.                                |
| `kwargs`   | `AttributesType` | Keyword arguments transformed into tag attributes. | `{}`                                                   |

Source code in `src/air/tags/models/stock.py`

```
def __init__(
    self,
    *children: Renderable,
    span: str | None = None,
    class_: str | None = None,
    id: str | None = None,
    style: str | None = None,
    **kwargs: AttributesType,
) -> None:
    super().__init__(*children, **kwargs | locals_cleanup(locals()))
```

## Data

```
Data(
    *children,
    value=None,
    class_=None,
    id=None,
    style=None,
    **kwargs,
)
```

Bases: `BaseTag`

Adds a machine-readable translation of a given content

Parameters:

| Name       | Type             | Description                                        | Default                                                    |
| ---------- | ---------------- | -------------------------------------------------- | ---------------------------------------------------------- |
| `children` | `Renderable`     | Tags, strings, or other rendered content.          | `()`                                                       |
| `value`    | \`str            | None\`                                             | Specifies the machine-readable translation of the content. |
| `class_`   | \`str            | None\`                                             | Substituted as the DOM class attribute.                    |
| `id`       | \`str            | None\`                                             | DOM ID attribute.                                          |
| `style`    | \`str            | None\`                                             | Inline style attribute.                                    |
| `kwargs`   | `AttributesType` | Keyword arguments transformed into tag attributes. | `{}`                                                       |

Source code in `src/air/tags/models/stock.py`

```
def __init__(
    self,
    *children: Renderable,
    value: str | None = None,
    class_: str | None = None,
    id: str | None = None,
    style: str | None = None,
    **kwargs: AttributesType,
) -> None:
    super().__init__(*children, **kwargs | locals_cleanup(locals()))
```

## Dd

```
Dd(
    *children,
    cite=None,
    datetime=None,
    class_=None,
    id=None,
    style=None,
    **kwargs,
)
```

Bases: `BaseTag`

Defines a description/value of a term in a description list

Parameters:

| Name       | Type             | Description                                        | Default                                       |
| ---------- | ---------------- | -------------------------------------------------- | --------------------------------------------- |
| `children` | `Renderable`     | Tags, strings, or other rendered content.          | `()`                                          |
| `cite`     | \`str            | None\`                                             | Specifies the source of the quotation.        |
| `datetime` | \`str            | None\`                                             | Specifies the date and time of the quotation. |
| `class_`   | \`str            | None\`                                             | Substituted as the DOM class attribute.       |
| `id`       | \`str            | None\`                                             | DOM ID attribute.                             |
| `style`    | \`str            | None\`                                             | Inline style attribute.                       |
| `kwargs`   | `AttributesType` | Keyword arguments transformed into tag attributes. | `{}`                                          |

Source code in `src/air/tags/models/stock.py`

```
def __init__(
    self,
    *children: Renderable,
    cite: str | None = None,
    datetime: str | None = None,
    class_: str | None = None,
    id: str | None = None,
    style: str | None = None,
    **kwargs: AttributesType,
) -> None:
    super().__init__(*children, **kwargs | locals_cleanup(locals()))
```

## Details

```
Details(
    *children,
    open=None,
    class_=None,
    id=None,
    style=None,
    **kwargs,
)
```

Bases: `BaseTag`

Defines additional details that the user can view or hide

Parameters:

| Name       | Type             | Description                                        | Default                                                          |
| ---------- | ---------------- | -------------------------------------------------- | ---------------------------------------------------------------- |
| `children` | `Renderable`     | Tags, strings, or other rendered content.          | `()`                                                             |
| `open`     | \`str            | None\`                                             | Specifies that the details should be visible (open) to the user. |
| `class_`   | \`str            | None\`                                             | Substituted as the DOM class attribute.                          |
| `id`       | \`str            | None\`                                             | DOM ID attribute.                                                |
| `style`    | \`str            | None\`                                             | Inline style attribute.                                          |
| `kwargs`   | `AttributesType` | Keyword arguments transformed into tag attributes. | `{}`                                                             |

Source code in `src/air/tags/models/stock.py`

```
def __init__(
    self,
    *children: Renderable,
    open: str | None = None,
    class_: str | None = None,
    id: str | None = None,
    style: str | None = None,
    **kwargs: AttributesType,
) -> None:
    super().__init__(*children, **kwargs | locals_cleanup(locals()))
```

## Dialog

```
Dialog(
    *children,
    open=None,
    class_=None,
    id=None,
    style=None,
    **kwargs,
)
```

Bases: `BaseTag`

Defines a dialog box or window

Parameters:

| Name       | Type             | Description                                        | Default                                                             |
| ---------- | ---------------- | -------------------------------------------------- | ------------------------------------------------------------------- |
| `children` | `Renderable`     | Tags, strings, or other rendered content.          | `()`                                                                |
| `open`     | \`str            | None\`                                             | Specifies that the dialog box should be visible (open) to the user. |
| `class_`   | \`str            | None\`                                             | Substituted as the DOM class attribute.                             |
| `id`       | \`str            | None\`                                             | DOM ID attribute.                                                   |
| `style`    | \`str            | None\`                                             | Inline style attribute.                                             |
| `kwargs`   | `AttributesType` | Keyword arguments transformed into tag attributes. | `{}`                                                                |

Source code in `src/air/tags/models/stock.py`

```
def __init__(
    self,
    *children: Renderable,
    open: str | None = None,
    class_: str | None = None,
    id: str | None = None,
    style: str | None = None,
    **kwargs: AttributesType,
) -> None:
    super().__init__(*children, **kwargs | locals_cleanup(locals()))
```
