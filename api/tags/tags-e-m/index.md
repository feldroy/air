# Tags E-M

## Embed

```
Embed(
    *,
    src=None,
    type=None,
    width=None,
    height=None,
    class_=None,
    id=None,
    style=None,
    **kwargs,
)
```

Bases: `SelfClosingTag`

Defines a container for an external application

Parameters:

| Name     | Type             | Description                                        | Default                                              |
| -------- | ---------------- | -------------------------------------------------- | ---------------------------------------------------- |
| `src`    | \`str            | None\`                                             | Specifies the address of the external file to embed. |
| `type`   | \`str            | None\`                                             | Specifies the media type of the embedded content.    |
| `width`  | \`str            | int                                                | None\`                                               |
| `height` | \`str            | int                                                | None\`                                               |
| `class_` | \`str            | None\`                                             | Substituted as the DOM class attribute.              |
| `id`     | \`str            | None\`                                             | DOM ID attribute.                                    |
| `style`  | \`str            | None\`                                             | Inline style attribute.                              |
| `kwargs` | `AttributesType` | Keyword arguments transformed into tag attributes. | `{}`                                                 |

Source code in `src/air/tags/models/stock.py`

```
def __init__(
    self,
    *,
    src: str | None = None,
    type: str | None = None,
    width: str | int | None = None,
    height: str | int | None = None,
    class_: str | None = None,
    id: str | None = None,
    style: str | None = None,
    **kwargs: AttributesType,
) -> None:
    super().__init__(**kwargs | locals_cleanup(locals()))
```

## Fieldset

```
Fieldset(
    *children,
    disabled=None,
    form=None,
    name=None,
    class_=None,
    id=None,
    style=None,
    **kwargs,
)
```

Bases: `BaseTag`

Groups related elements in a form

Parameters:

| Name       | Type             | Description                                        | Default                                                             |
| ---------- | ---------------- | -------------------------------------------------- | ------------------------------------------------------------------- |
| `children` | `Renderable`     | Tags, strings, or other rendered content.          | `()`                                                                |
| `disabled` | \`str            | None\`                                             | Specifies that a group of related form elements should be disabled. |
| `form`     | \`str            | None\`                                             | Specifies which form the fieldset belongs to.                       |
| `name`     | \`str            | None\`                                             | Specifies a name for the fieldset.                                  |
| `class_`   | \`str            | None\`                                             | Substituted as the DOM class attribute.                             |
| `id`       | \`str            | None\`                                             | DOM ID attribute.                                                   |
| `style`    | \`str            | None\`                                             | Inline style attribute.                                             |
| `kwargs`   | `AttributesType` | Keyword arguments transformed into tag attributes. | `{}`                                                                |

Source code in `src/air/tags/models/stock.py`

```
def __init__(
    self,
    *children: Renderable,
    disabled: str | None = None,
    form: str | None = None,
    name: str | None = None,
    class_: str | None = None,
    id: str | None = None,
    style: str | None = None,
    **kwargs: AttributesType,
) -> None:
    super().__init__(*children, **kwargs | locals_cleanup(locals()))
```

## Form

```
Form(
    *children,
    action=None,
    method=None,
    accept_charset=None,
    autocomplete=None,
    enctype=None,
    name=None,
    novalidate=None,
    rel=None,
    target=None,
    class_=None,
    id=None,
    style=None,
    **kwargs,
)
```

Bases: `BaseTag`

Defines an HTML form for user input

Parameters:

| Name             | Type             | Description                                        | Default                                                                             |
| ---------------- | ---------------- | -------------------------------------------------- | ----------------------------------------------------------------------------------- |
| `children`       | `Renderable`     | Tags, strings, or other rendered content.          | `()`                                                                                |
| `action`         | \`str            | None\`                                             | Specifies where to send the form-data when a form is submitted.                     |
| `method`         | \`str            | None\`                                             | Specifies the HTTP method to use when sending form-data.                            |
| `accept_charset` | \`str            | None\`                                             | Specifies the character encodings that are to be used for the form submission.      |
| `autocomplete`   | \`str            | None\`                                             | Specifies whether a form should have autocomplete on or off.                        |
| `enctype`        | \`str            | None\`                                             | Specifies how the form-data should be encoded when submitting it to the server.     |
| `name`           | \`str            | None\`                                             | Specifies the name of the form.                                                     |
| `novalidate`     | \`str            | None\`                                             | Specifies that the form should not be validated when submitted.                     |
| `rel`            | \`str            | None\`                                             | Specifies the relationship between a linked resource and the current document.      |
| `target`         | \`str            | None\`                                             | Specifies where to display the response that is received after submitting the form. |
| `class_`         | \`str            | None\`                                             | Substituted as the DOM class attribute.                                             |
| `id`             | \`str            | None\`                                             | DOM ID attribute.                                                                   |
| `style`          | \`str            | None\`                                             | Inline style attribute.                                                             |
| `kwargs`         | `AttributesType` | Keyword arguments transformed into tag attributes. | `{}`                                                                                |

Source code in `src/air/tags/models/stock.py`

```
def __init__(
    self,
    *children: Renderable,
    action: str | None = None,
    method: str | None = None,
    accept_charset: str | None = None,
    autocomplete: str | None = None,
    enctype: str | None = None,
    name: str | None = None,
    novalidate: str | None = None,
    rel: str | None = None,
    target: str | None = None,
    class_: str | None = None,
    id: str | None = None,
    style: str | None = None,
    **kwargs: AttributesType,
) -> None:
    super().__init__(*children, **kwargs | locals_cleanup(locals()))
```

## Head

```
Head(*children, profile=None, **kwargs)
```

Bases: `BaseTag`

Contains metadata/information for the document

Parameters:

| Name       | Type             | Description                                        | Default                                                                             |
| ---------- | ---------------- | -------------------------------------------------- | ----------------------------------------------------------------------------------- |
| `children` | `Renderable`     | Tags, strings, or other rendered content.          | `()`                                                                                |
| `profile`  | \`str            | None\`                                             | Specifies the URL of a document that contains a line-break-separated list of links. |
| `kwargs`   | `AttributesType` | Keyword arguments transformed into tag attributes. | `{}`                                                                                |

Source code in `src/air/tags/models/stock.py`

```
def __init__(
    self,
    *children: Renderable,
    profile: str | None = None,
    **kwargs: AttributesType,
) -> None:
    super().__init__(*children, **kwargs | locals_cleanup(locals()))
```

## Html

```
Html(*children, **kwargs)
```

Bases: `BaseTag`

Defines the root of an HTML document

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

### pretty_render

```
pretty_render(
    *, with_body=False, with_head=False, with_doctype=True
)
```

Pretty-print without escaping.

Source code in `src/air/tags/models/special.py`

```
@override
def pretty_render(
    self,
    *,
    with_body: bool = False,
    with_head: bool = False,
    with_doctype: bool = True,
) -> str:
    """Pretty-print without escaping."""
    return super().pretty_render(with_body=with_body, with_head=with_head, with_doctype=with_doctype)
```

## Iframe

```
Iframe(
    *children,
    src=None,
    srcdoc=None,
    width=None,
    height=None,
    allow=None,
    allowfullscreen=None,
    allowpaymentrequest=None,
    loading=None,
    name=None,
    referrerpolicy=None,
    sandbox=None,
    class_=None,
    id=None,
    style=None,
    **kwargs,
)
```

Bases: `BaseTag`

Defines an inline frame

Parameters:

| Name                  | Type             | Description                                        | Default                                                                                     |
| --------------------- | ---------------- | -------------------------------------------------- | ------------------------------------------------------------------------------------------- |
| `children`            | `Renderable`     | Tags, strings, or other rendered content.          | `()`                                                                                        |
| `src`                 | \`str            | None\`                                             | Specifies the URL of the page to embed.                                                     |
| `srcdoc`              | \`str            | None\`                                             | Specifies the HTML content of the page to show in the <iframe>.                             |
| `width`               | \`str            | int                                                | None\`                                                                                      |
| `height`              | \`str            | int                                                | None\`                                                                                      |
| `allow`               | \`str            | None\`                                             | Specifies a feature policy for the <iframe>.                                                |
| `allowfullscreen`     | \`str            | None\`                                             | Set to true if the <iframe> can activate fullscreen mode.                                   |
| `allowpaymentrequest` | \`str            | None\`                                             | Set to true if a cross-origin <iframe> should be allowed to invoke the Payment Request API. |
| `loading`             | \`str            | None\`                                             | Specifies the loading policy of the <iframe>.                                               |
| `name`                | \`str            | None\`                                             | Specifies the name of an <iframe>.                                                          |
| `referrerpolicy`      | \`str            | None\`                                             | Specifies which referrer information to send when fetching the iframe's content.            |
| `sandbox`             | \`str            | None\`                                             | Enables an extra set of restrictions for the content in an <iframe>.                        |
| `class_`              | \`str            | None\`                                             | Substituted as the DOM class attribute.                                                     |
| `id`                  | \`str            | None\`                                             | DOM ID attribute.                                                                           |
| `style`               | \`str            | None\`                                             | Inline style attribute.                                                                     |
| `kwargs`              | `AttributesType` | Keyword arguments transformed into tag attributes. | `{}`                                                                                        |

Source code in `src/air/tags/models/stock.py`

```
def __init__(
    self,
    *children: Renderable,
    src: str | None = None,
    srcdoc: str | None = None,
    width: str | int | None = None,
    height: str | int | None = None,
    allow: str | None = None,
    allowfullscreen: str | None = None,
    allowpaymentrequest: str | None = None,
    loading: str | None = None,
    name: str | None = None,
    referrerpolicy: str | None = None,
    sandbox: str | None = None,
    class_: str | None = None,
    id: str | None = None,
    style: str | None = None,
    **kwargs: AttributesType,
) -> None:
    super().__init__(*children, **kwargs | locals_cleanup(locals()))
```

## Img

```
Img(
    *,
    src=None,
    width=None,
    height=None,
    srcset=None,
    alt=None,
    crossorigin=None,
    ismap=None,
    loading=None,
    longdesc=None,
    referrerpolicy=None,
    sizes=None,
    usemap=None,
    class_=None,
    id=None,
    style=None,
    **kwargs,
)
```

Bases: `SelfClosingTag`

Defines an image

Parameters:

| Name             | Type             | Description                                        | Default                                                                                                |
| ---------------- | ---------------- | -------------------------------------------------- | ------------------------------------------------------------------------------------------------------ |
| `src`            | \`str            | None\`                                             | Specifies the path to the image.                                                                       |
| `width`          | \`str            | int                                                | None\`                                                                                                 |
| `height`         | \`str            | int                                                | None\`                                                                                                 |
| `srcset`         | \`str            | None\`                                             | Specifies a list of image files to use in different situations.                                        |
| `alt`            | \`str            | None\`                                             | Specifies an alternate text for an image.                                                              |
| `crossorigin`    | \`str            | None\`                                             | Allows images from third-party sites that allow cross-origin access to be used with canvas.            |
| `ismap`          | \`str            | None\`                                             | Specifies an image as a server-side image map.                                                         |
| `loading`        | \`str            | None\`                                             | Specifies whether a browser should load an image immediately or to defer loading of off-screen images. |
| `longdesc`       | \`str            | None\`                                             | Specifies a URL to a detailed description of an image.                                                 |
| `referrerpolicy` | \`str            | None\`                                             | Specifies which referrer information to use when fetching an image.                                    |
| `sizes`          | \`str            | None\`                                             | Specifies image sizes for different page layouts.                                                      |
| `usemap`         | \`str            | None\`                                             | Specifies an image as a client-side image map.                                                         |
| `class_`         | \`str            | None\`                                             | Substituted as the DOM class attribute.                                                                |
| `id`             | \`str            | None\`                                             | DOM ID attribute.                                                                                      |
| `style`          | \`str            | None\`                                             | Inline style attribute.                                                                                |
| `kwargs`         | `AttributesType` | Keyword arguments transformed into tag attributes. | `{}`                                                                                                   |

Source code in `src/air/tags/models/stock.py`

```
def __init__(
    self,
    *,
    src: str | None = None,
    width: str | int | None = None,
    height: str | int | None = None,
    srcset: str | None = None,
    alt: str | None = None,
    crossorigin: str | None = None,
    ismap: str | None = None,
    loading: str | None = None,
    longdesc: str | None = None,
    referrerpolicy: str | None = None,
    sizes: str | None = None,
    usemap: str | None = None,
    class_: str | None = None,
    id: str | None = None,
    style: str | None = None,
    **kwargs: AttributesType,
) -> None:
    super().__init__(**kwargs | locals_cleanup(locals()))
```

## Input

```
Input(
    *,
    name=None,
    type=None,
    value=None,
    readonly=None,
    required=None,
    accept=None,
    alt=None,
    autocomplete=None,
    autofocus=None,
    checked=None,
    dirname=None,
    disabled=None,
    form=None,
    formaction=None,
    formenctype=None,
    formmethod=None,
    formnovalidate=None,
    formtarget=None,
    height=None,
    list=None,
    max=None,
    maxlength=None,
    min=None,
    minlength=None,
    multiple=None,
    pattern=None,
    placeholder=None,
    popovertarget=None,
    popovertargetaction=None,
    size=None,
    src=None,
    step=None,
    class_=None,
    id=None,
    style=None,
    **kwargs,
)
```

Bases: `SelfClosingTag`

Defines an input control

Parameters:

| Name                  | Type             | Description                                        | Default                                                                                       |
| --------------------- | ---------------- | -------------------------------------------------- | --------------------------------------------------------------------------------------------- |
| `name`                | \`str            | None\`                                             | Specifies the name of an <input> element.                                                     |
| `type`                | \`str            | None\`                                             | Specifies the type <input> element to display.                                                |
| `value`               | \`str            | None\`                                             | Specifies the value of an <input> element.                                                    |
| `readonly`            | \`bool           | None\`                                             | Specifies that an input field is read-only.                                                   |
| `required`            | \`bool           | None\`                                             | Specifies that an input field must be filled out before submitting the form.                  |
| `accept`              | \`str            | None\`                                             | Specifies a filter for what file types the user can pick from the file input dialog box.      |
| `alt`                 | \`str            | None\`                                             | Specifies an alternate text for images.                                                       |
| `autocomplete`        | \`str            | None\`                                             | Specifies whether an <input> element should have autocomplete on or off.                      |
| `autofocus`           | \`bool           | None\`                                             | Specifies that an <input> element should automatically get focus when the page loads.         |
| `checked`             | \`bool           | None\`                                             | Specifies that an <input> element should be pre-selected when the page loads.                 |
| `dirname`             | \`str            | None\`                                             | Specifies that the text direction of the input field will be submitted.                       |
| `disabled`            | \`bool           | None\`                                             | Specifies that an <input> element should be disabled.                                         |
| `form`                | \`str            | None\`                                             | Specifies the form the <input> element belongs to.                                            |
| `formaction`          | \`str            | None\`                                             | Specifies the URL of the file that will process the input control when the form is submitted. |
| `formenctype`         | \`str            | None\`                                             | Specifies how the form-data should be encoded when submitting it to the server.               |
| `formmethod`          | \`str            | None\`                                             | Defines the HTTP method for sending data to the action URL.                                   |
| `formnovalidate`      | \`bool           | None\`                                             | Specifies that the form-data should not be validated on submission.                           |
| `formtarget`          | \`str            | None\`                                             | Specifies where to display the response that is received after submitting the form.           |
| `height`              | \`str            | int                                                | None\`                                                                                        |
| `list`                | \`str            | None\`                                             | Refers to a element that contains pre-defined options for an <input> element.                 |
| `max`                 | \`str            | None\`                                             | Specifies the maximum value for an <input> element.                                           |
| `maxlength`           | \`str            | None\`                                             | Specifies the maximum number of characters allowed in an <input> element.                     |
| `min`                 | \`str            | None\`                                             | Specifies a minimum value for an <input> element.                                             |
| `minlength`           | \`str            | None\`                                             | Specifies the minimum number of characters required in an <input> element.                    |
| `multiple`            | \`bool           | None\`                                             | Specifies that a user can enter more than one value in an <input> element.                    |
| `pattern`             | \`str            | None\`                                             | Specifies a regular expression that an <input> element's value is checked against.            |
| `placeholder`         | \`str            | None\`                                             | Specifies a short hint that describes the expected value of an <input> element.               |
| `popovertarget`       | \`str            | None\`                                             | Specifies which popover element to invoke.                                                    |
| `popovertargetaction` | \`str            | None\`                                             | Specifies what action to perform on the popover element.                                      |
| `size`                | \`str            | None\`                                             | Specifies the width, in characters, of an <input> element.                                    |
| `src`                 | \`str            | None\`                                             | Specifies the URL of the image to use as a submit button.                                     |
| `step`                | \`str            | None\`                                             | Specifies the legal number intervals for an input field.                                      |
| `class_`              | \`str            | None\`                                             | Substituted as the DOM class attribute.                                                       |
| `id`                  | \`str            | None\`                                             | DOM ID attribute.                                                                             |
| `style`               | \`str            | None\`                                             | Inline style attribute.                                                                       |
| `kwargs`              | `AttributesType` | Keyword arguments transformed into tag attributes. | `{}`                                                                                          |

Source code in `src/air/tags/models/stock.py`

```
def __init__(
    self,
    *,
    name: str | None = None,
    type: str | None = None,
    value: str | None = None,
    readonly: bool | None = None,
    required: bool | None = None,
    accept: str | None = None,
    alt: str | None = None,
    autocomplete: str | None = None,
    autofocus: bool | None = None,
    checked: bool | None = None,
    dirname: str | None = None,
    disabled: bool | None = None,
    form: str | None = None,
    formaction: str | None = None,
    formenctype: str | None = None,
    formmethod: str | None = None,
    formnovalidate: bool | None = None,
    formtarget: str | None = None,
    height: str | int | None = None,
    list: str | None = None,
    max: str | None = None,
    maxlength: str | None = None,
    min: str | None = None,
    minlength: str | None = None,
    multiple: bool | None = None,
    pattern: str | None = None,
    placeholder: str | None = None,
    popovertarget: str | None = None,
    popovertargetaction: str | None = None,
    size: str | None = None,
    src: str | None = None,
    step: str | None = None,
    class_: str | None = None,
    id: str | None = None,
    style: str | None = None,
    **kwargs: AttributesType,
) -> None:
    super().__init__(**kwargs | locals_cleanup(locals()))
```

## Ins

```
Ins(
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

Defines a text that has been inserted into a document

Parameters:

| Name       | Type             | Description                                        | Default                                                                                   |
| ---------- | ---------------- | -------------------------------------------------- | ----------------------------------------------------------------------------------------- |
| `children` | `Renderable`     | Tags, strings, or other rendered content.          | `()`                                                                                      |
| `cite`     | \`str            | None\`                                             | Specifies a URL to a document that explains the reason why the text was inserted/changed. |
| `datetime` | \`str            | None\`                                             | Specifies the date and time when the text was inserted/changed.                           |
| `class_`   | \`str            | None\`                                             | Substituted as the DOM class attribute.                                                   |
| `id`       | \`str            | None\`                                             | DOM ID attribute.                                                                         |
| `style`    | \`str            | None\`                                             | Inline style attribute.                                                                   |
| `kwargs`   | `AttributesType` | Keyword arguments transformed into tag attributes. | `{}`                                                                                      |

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

## Map

```
Map(
    *children,
    name=None,
    class_=None,
    id=None,
    style=None,
    **kwargs,
)
```

Bases: `BaseTag`

Defines an image map

Parameters:

| Name       | Type             | Description                                        | Default                                 |
| ---------- | ---------------- | -------------------------------------------------- | --------------------------------------- |
| `children` | `Renderable`     | Tags, strings, or other rendered content.          | `()`                                    |
| `name`     | \`str            | None\`                                             | Specifies the name of the image map.    |
| `class_`   | \`str            | None\`                                             | Substituted as the DOM class attribute. |
| `id`       | \`str            | None\`                                             | DOM ID attribute.                       |
| `style`    | \`str            | None\`                                             | Inline style attribute.                 |
| `kwargs`   | `AttributesType` | Keyword arguments transformed into tag attributes. | `{}`                                    |

Source code in `src/air/tags/models/stock.py`

```
def __init__(
    self,
    *children: Renderable,
    name: str | None = None,
    class_: str | None = None,
    id: str | None = None,
    style: str | None = None,
    **kwargs: AttributesType,
) -> None:
    super().__init__(*children, **kwargs | locals_cleanup(locals()))
```

## Menu

```
Menu(
    *children,
    compact=None,
    class_=None,
    id=None,
    style=None,
    **kwargs,
)
```

Bases: `BaseTag`

Defines a menu list

Parameters:

| Name       | Type             | Description                                        | Default                                                         |
| ---------- | ---------------- | -------------------------------------------------- | --------------------------------------------------------------- |
| `children` | `Renderable`     | Tags, strings, or other rendered content.          | `()`                                                            |
| `compact`  | \`str            | None\`                                             | Specifies that the list should be displayed in a compact style. |
| `class_`   | \`str            | None\`                                             | Substituted as the DOM class attribute.                         |
| `id`       | \`str            | None\`                                             | DOM ID attribute.                                               |
| `style`    | \`str            | None\`                                             | Inline style attribute.                                         |
| `kwargs`   | `AttributesType` | Keyword arguments transformed into tag attributes. | `{}`                                                            |

Source code in `src/air/tags/models/stock.py`

```
def __init__(
    self,
    *children: Renderable,
    compact: str | None = None,
    class_: str | None = None,
    id: str | None = None,
    style: str | None = None,
    **kwargs: AttributesType,
) -> None:
    super().__init__(*children, **kwargs | locals_cleanup(locals()))
```

## Meta

```
Meta(
    *,
    charset=None,
    content=None,
    http_equiv=None,
    media=None,
    name=None,
    class_=None,
    id=None,
    **kwargs,
)
```

Bases: `SelfClosingTag`

Defines metadata about an HTML document

Parameters:

| Name         | Type             | Description                                        | Default                                                                     |
| ------------ | ---------------- | -------------------------------------------------- | --------------------------------------------------------------------------- |
| `charset`    | \`str            | None\`                                             | Specifies the character encoding for the HTML document.                     |
| `content`    | \`str            | None\`                                             | Specifies the value associated with the http-equiv or name attribute.       |
| `http_equiv` | \`str            | None\`                                             | Provides an HTTP header for the information/value of the content attribute. |
| `media`      | \`str            | None\`                                             | Specifies what media/device the linked document is optimized for.           |
| `name`       | \`str            | None\`                                             | Specifies a name for the metadata.                                          |
| `class_`     | \`str            | None\`                                             | Substituted as the DOM class attribute.                                     |
| `id`         | \`str            | None\`                                             | DOM ID attribute.                                                           |
| `style`      |                  | Inline style attribute.                            | *required*                                                                  |
| `kwargs`     | `AttributesType` | Keyword arguments transformed into tag attributes. | `{}`                                                                        |

Source code in `src/air/tags/models/stock.py`

```
def __init__(
    self,
    *,
    charset: str | None = None,
    content: str | None = None,
    http_equiv: str | None = None,
    media: str | None = None,
    name: str | None = None,
    class_: str | None = None,
    id: str | None = None,
    **kwargs: AttributesType,
) -> None:
    super().__init__(**kwargs | locals_cleanup(locals()))
```

## Meter

```
Meter(
    *children,
    value=None,
    min=None,
    max=None,
    low=None,
    high=None,
    optimum=None,
    class_=None,
    id=None,
    style=None,
    **kwargs,
)
```

Bases: `BaseTag`

Defines a scalar measurement within a known range (a gauge)

Parameters:

| Name       | Type             | Description                                        | Default                                                            |
| ---------- | ---------------- | -------------------------------------------------- | ------------------------------------------------------------------ |
| `children` | `Renderable`     | Tags, strings, or other rendered content.          | `()`                                                               |
| `value`    | \`str            | None\`                                             | The current numeric value. Must be between the min and max values. |
| `min`      | \`str            | None\`                                             | The lower bound of the measured range.                             |
| `max`      | \`str            | None\`                                             | The upper bound of the measured range.                             |
| `low`      | \`str            | None\`                                             | The upper numeric bound of the low end of the measured range.      |
| `high`     | \`str            | None\`                                             | The lower numeric bound of the high end of the measured range.     |
| `optimum`  | \`str            | None\`                                             | The optimal numeric value.                                         |
| `class_`   | \`str            | None\`                                             | Substituted as the DOM class attribute.                            |
| `id`       | \`str            | None\`                                             | DOM ID attribute.                                                  |
| `style`    | \`str            | None\`                                             | Inline style attribute.                                            |
| `kwargs`   | `AttributesType` | Keyword arguments transformed into tag attributes. | `{}`                                                               |

Source code in `src/air/tags/models/stock.py`

```
def __init__(
    self,
    *children: Renderable,
    value: str | None = None,
    min: str | None = None,
    max: str | None = None,
    low: str | None = None,
    high: str | None = None,
    optimum: str | None = None,
    class_: str | None = None,
    id: str | None = None,
    style: str | None = None,
    **kwargs: AttributesType,
) -> None:
    super().__init__(*children, **kwargs | locals_cleanup(locals()))
```
