# Tags T-Z

Easy to write and performant HTML content generation using Python classes to render HTML.

## Td

```
Td(
    *children,
    colspan=None,
    rowspan=None,
    headers=None,
    class_=None,
    id_=None,
    style=None,
    **custom_attributes,
)
```

Bases: `BaseTag`

Defines a cell in a table

Parameters:

| Name                | Type            | Description                                        | Default                                                        |
| ------------------- | --------------- | -------------------------------------------------- | -------------------------------------------------------------- |
| `children`          | `Renderable`    | Tags, strings, or other rendered content.          | `()`                                                           |
| `colspan`           | \`str           | None\`                                             | Defines the number of columns a cell should span.              |
| `rowspan`           | \`str           | None\`                                             | Defines the number of rows a cell should span.                 |
| `headers`           | \`str           | None\`                                             | list of string ids of the <th> elements that apply to the cell |
| `class_`            | \`str           | None\`                                             | Substituted as the DOM class attribute.                        |
| `id_`               | \`str           | None\`                                             | DOM ID attribute.                                              |
| `style`             | \`str           | None\`                                             | Inline style attribute.                                        |
| `custom_attributes` | `AttributeType` | Keyword arguments transformed into tag attributes. | `{}`                                                           |

Source code in `src/air/tags/models/stock.py`

```
def __init__(
    self,
    *children: Renderable,
    colspan: str | None = None,
    rowspan: str | None = None,
    headers: str | None = None,
    class_: str | None = None,
    id_: str | None = None,
    style: str | None = None,
    **custom_attributes: AttributeType,
) -> None:
    super().__init__(*children, **custom_attributes | locals_cleanup(locals()))
```

## Template

```
Template(
    *children,
    shadowrootmode=None,
    shadowrootdelegatesfocus=None,
    shadowrootclonable=None,
    shadowrootserializable=None,
    class_=None,
    id_=None,
    **custom_attributes,
)
```

Bases: `BaseTag`

Defines a container for content that should be hidden when the page loads

Parameters:

| Name                       | Type            | Description                                        | Default                                                           |
| -------------------------- | --------------- | -------------------------------------------------- | ----------------------------------------------------------------- |
| `children`                 | `Renderable`    | Tags, strings, or other rendered content.          | `()`                                                              |
| `shadowrootmode`           | \`str           | None\`                                             | Creates a shadow root for the parent element.                     |
| `shadowrootdelegatesfocus` | \`str           | None\`                                             | Sets whether the shadow root created delegates focus.             |
| `shadowrootclonable`       | \`str           | None\`                                             | Sets the value of the 'cloneable' property on the shadow root.    |
| `shadowrootserializable`   | \`str           | None\`                                             | Sets the value of the 'serializable' property on the shadow root. |
| `class_`                   | \`str           | None\`                                             | Substituted as the DOM class attribute.                           |
| `id_`                      | \`str           | None\`                                             | DOM ID attribute.                                                 |
| `custom_attributes`        | `AttributeType` | Keyword arguments transformed into tag attributes. | `{}`                                                              |

Source code in `src/air/tags/models/stock.py`

```
def __init__(
    self,
    *children: Renderable,
    shadowrootmode: str | None = None,
    shadowrootdelegatesfocus: str | None = None,
    shadowrootclonable: str | None = None,
    shadowrootserializable: str | None = None,
    class_: str | None = None,
    id_: str | None = None,
    **custom_attributes: AttributeType,
) -> None:
    super().__init__(*children, **custom_attributes | locals_cleanup(locals()))
```

## Textarea

```
Textarea(
    *children,
    autocapitalize=None,
    autocomplete=None,
    autocorrect=None,
    autofocus=None,
    cols=None,
    dirname=None,
    disabled=None,
    form=None,
    maxlength=None,
    minlength=None,
    name=None,
    placeholder=None,
    readonly=None,
    required=None,
    rows=None,
    spellcheck=None,
    wrap=None,
    class_=None,
    id_=None,
    style=None,
    **custom_attributes,
)
```

Bases: `BaseTag`

Defines a multiline input control (text area)

Parameters:

| Name                | Type            | Description                                        | Default                                                                       |
| ------------------- | --------------- | -------------------------------------------------- | ----------------------------------------------------------------------------- |
| `children`          | `Renderable`    | Tags, strings, or other rendered content.          | `()`                                                                          |
| `autocapitalize`    | \`str           | None\`                                             | Determines whether inputted text is automatically capitalized.                |
| `autocomplete`      | \`str           | None\`                                             | Controls whether inputted text can be automatically completed by the browser. |
| `autocorrect`       | \`str           | None\`                                             | Controls whether autocorrect is enabled on the input text.                    |
| `autofocus`         | \`bool          | None\`                                             | Indicates that the text area should have input focus when the page loads.     |
| `cols`              | \`str           | None\`                                             | Defines the visible width of the text area in average character widths.       |
| `dirname`           | \`str           | None\`                                             | Indicates text directionality of the element contents.                        |
| `disabled`          | \`bool          | None\`                                             | Determines if the user can interact with the text area.                       |
| `form`              | \`str           | None\`                                             | Associates the text area with a form element.                                 |
| `maxlength`         | \`str           | None\`                                             | Defines the maximum number of characters allowed in the text area.            |
| `minlength`         | \`str           | None\`                                             | Defines the minimum number of characters required in the text area.           |
| `name`              | \`str           | None\`                                             | The name of the element.                                                      |
| `placeholder`       | \`str           | None\`                                             | Provides a hint to the user of what can be entered in the text area.          |
| `readonly`          | \`bool          | None\`                                             | Indicates that the user may not edit the value of the text area.              |
| `required`          | \`bool          | None\`                                             | Specifies that the text area must be filled out before submitting the form.   |
| `rows`              | \`str           | None\`                                             | Defines the visible number of lines for the control.                          |
| `spellcheck`        | \`str           | None\`                                             | Specifies if the element is subject to browser or OS spell-check.             |
| `wrap`              | \`str           | None\`                                             | Indicates how the text area handles line wrapping.                            |
| `class_`            | \`str           | None\`                                             | Substituted as the DOM class attribute.                                       |
| `id_`               | \`str           | None\`                                             | DOM ID attribute.                                                             |
| `style`             | \`str           | None\`                                             | Inline style attribute.                                                       |
| `custom_attributes` | `AttributeType` | Keyword arguments transformed into tag attributes. | `{}`                                                                          |

Source code in `src/air/tags/models/stock.py`

```
def __init__(
    self,
    *children: Renderable,
    autocapitalize: str | None = None,
    autocomplete: str | None = None,
    autocorrect: str | None = None,
    autofocus: bool | None = None,
    cols: str | None = None,
    dirname: str | None = None,
    disabled: bool | None = None,
    form: str | None = None,
    maxlength: str | None = None,
    minlength: str | None = None,
    name: str | None = None,
    placeholder: str | None = None,
    readonly: bool | None = None,
    required: bool | None = None,
    rows: str | None = None,
    spellcheck: str | None = None,
    wrap: str | None = None,
    class_: str | None = None,
    id_: str | None = None,
    style: str | None = None,
    **custom_attributes: AttributeType,
) -> None:
    super().__init__(*children, **custom_attributes | locals_cleanup(locals()))
```

## Th

```
Th(
    *children,
    abbr=None,
    colspan=None,
    headers=None,
    rowspan=None,
    scope=None,
    class_=None,
    id_=None,
    style=None,
    **custom_attributes,
)
```

Bases: `BaseTag`

Defines a header cell in a table

Parameters:

| Name                | Type            | Description                                        | Default                                                                                       |
| ------------------- | --------------- | -------------------------------------------------- | --------------------------------------------------------------------------------------------- |
| `children`          | `Renderable`    | Tags, strings, or other rendered content.          | `()`                                                                                          |
| `abbr`              | \`str           | None\`                                             | An abbreviated description of the header cell content.                                        |
| `colspan`           | \`str           | None\`                                             | Defines the number of columns a header cell should span.                                      |
| `headers`           | \`str           | None\`                                             | list of string ids of the <th> elements that provide the headers for the cell.                |
| `rowspan`           | \`str           | None\`                                             | Defines the number of rows a header cell should span.                                         |
| `scope`             | \`str           | None\`                                             | Specifies whether the header cell is a header for a column, row, or group of columns or rows. |
| `class_`            | \`str           | None\`                                             | Substituted as the DOM class attribute.                                                       |
| `id_`               | \`str           | None\`                                             | DOM ID attribute.                                                                             |
| `style`             | \`str           | None\`                                             | Inline style attribute.                                                                       |
| `custom_attributes` | `AttributeType` | Keyword arguments transformed into tag attributes. | `{}`                                                                                          |

Source code in `src/air/tags/models/stock.py`

```
def __init__(
    self,
    *children: Renderable,
    abbr: str | None = None,
    colspan: str | None = None,
    headers: str | None = None,
    rowspan: str | None = None,
    scope: str | None = None,
    class_: str | None = None,
    id_: str | None = None,
    style: str | None = None,
    **custom_attributes: AttributeType,
) -> None:
    super().__init__(*children, **custom_attributes | locals_cleanup(locals()))
```

## Time

```
Time(
    *children,
    datetime=None,
    class_=None,
    id_=None,
    style=None,
    **custom_attributes,
)
```

Bases: `BaseTag`

Defines a specific time (or datetime)

Parameters:

| Name                | Type            | Description                                        | Default                                 |
| ------------------- | --------------- | -------------------------------------------------- | --------------------------------------- |
| `children`          | `Renderable`    | Tags, strings, or other rendered content.          | `()`                                    |
| `datetime`          | \`str           | None\`                                             | Specifies the date and/or time format.  |
| `class_`            | \`str           | None\`                                             | Substituted as the DOM class attribute. |
| `id_`               | \`str           | None\`                                             | DOM ID attribute.                       |
| `style`             | \`str           | None\`                                             | Inline style attribute.                 |
| `custom_attributes` | `AttributeType` | Keyword arguments transformed into tag attributes. | `{}`                                    |

Source code in `src/air/tags/models/stock.py`

```
def __init__(
    self,
    *children: Renderable,
    datetime: str | None = None,
    class_: str | None = None,
    id_: str | None = None,
    style: str | None = None,
    **custom_attributes: AttributeType,
) -> None:
    super().__init__(*children, **custom_attributes | locals_cleanup(locals()))
```

## Track

```
Track(
    *,
    default=None,
    kind=None,
    label=None,
    srclang=None,
    src=None,
    class_=None,
    id_=None,
    style=None,
    **custom_attributes,
)
```

Bases: `SelfClosingTag`

Defines text tracks for media elements ( and )

Parameters:

| Name                | Type            | Description                                        | Default                                                                                  |
| ------------------- | --------------- | -------------------------------------------------- | ---------------------------------------------------------------------------------------- |
| `default`           | \`str           | None\`                                             | Indicates that the track is to be enabled if the user's preferences do not indicate any. |
| `kind`              | \`str           | None\`                                             | Specifies how the text track is meant to be used.                                        |
| `label`             | \`str           | None\`                                             | Provides a user-readable title for the text track.                                       |
| `srclang`           | \`str           | None\`                                             | Specifies the language of the text track data.                                           |
| `src`               | \`str           | None\`                                             | Specifies the URL of the track file.                                                     |
| `class_`            | \`str           | None\`                                             | Substituted as the DOM class attribute.                                                  |
| `id_`               | \`str           | None\`                                             | DOM ID attribute.                                                                        |
| `style`             | \`str           | None\`                                             | Inline style attribute.                                                                  |
| `custom_attributes` | `AttributeType` | Keyword arguments transformed into tag attributes. | `{}`                                                                                     |

Source code in `src/air/tags/models/stock.py`

```
def __init__(
    self,
    *,
    default: str | None = None,
    kind: str | None = None,
    label: str | None = None,
    srclang: str | None = None,
    src: str | None = None,
    class_: str | None = None,
    id_: str | None = None,
    style: str | None = None,
    **custom_attributes: AttributeType,
) -> None:
    super().__init__(**custom_attributes | locals_cleanup(locals()))
```

## U

```
U(
    *children,
    compact=None,
    type_=None,
    class_=None,
    id_=None,
    style=None,
    **custom_attributes,
)
```

Bases: `BaseTag`

Defines some text that is unarticulated and styled differently from normal text

Parameters:

| Name                | Type            | Description                                        | Default                                                        |
| ------------------- | --------------- | -------------------------------------------------- | -------------------------------------------------------------- |
| `children`          | `Renderable`    | Tags, strings, or other rendered content.          | `()`                                                           |
| `compact`           | \`str           | None\`                                             | Specifies that the list should be rendered in a compact style. |
| `type_`             | \`str           | None\`                                             | Specifies the kind of marker to use in the list.               |
| `class_`            | \`str           | None\`                                             | Substituted as the DOM class attribute.                        |
| `id_`               | \`str           | None\`                                             | DOM ID attribute.                                              |
| `style`             | \`str           | None\`                                             | Inline style attribute.                                        |
| `custom_attributes` | `AttributeType` | Keyword arguments transformed into tag attributes. | `{}`                                                           |

Source code in `src/air/tags/models/stock.py`

```
def __init__(
    self,
    *children: Renderable,
    compact: str | None = None,
    type_: str | None = None,
    class_: str | None = None,
    id_: str | None = None,
    style: str | None = None,
    **custom_attributes: AttributeType,
) -> None:
    super().__init__(*children, **custom_attributes | locals_cleanup(locals()))
```

## Video

```
Video(
    *children,
    src=None,
    autoplay=None,
    controls=None,
    controlslist=None,
    crossorigin=None,
    disablepictureinpicture=None,
    disableremoteplayback=None,
    height=None,
    width=None,
    loop=None,
    muted=None,
    playsinline=None,
    poster=None,
    preload=None,
    class_=None,
    id_=None,
    style=None,
    **custom_attributes,
)
```

Bases: `BaseTag`

Defines embedded video content

Parameters:

| Name                      | Type            | Description                                        | Default                                                                                |
| ------------------------- | --------------- | -------------------------------------------------- | -------------------------------------------------------------------------------------- |
| `children`                | `Renderable`    | Tags, strings, or other rendered content.          | `()`                                                                                   |
| `src`                     | \`str           | None\`                                             | Specifies the URL of the video file.                                                   |
| `autoplay`                | \`str           | None\`                                             | Specifies that the video will start playing as soon as it is ready.                    |
| `controls`                | \`str           | None\`                                             | Specifies that video controls should be displayed (such as a play/pause button etc).   |
| `controlslist`            | \`str           | None\`                                             | Specifies which controls to show on the media element.                                 |
| `crossorigin`             | \`str           | None\`                                             | Specifies how the element handles cross-origin requests.                               |
| `disablepictureinpicture` | \`str           | None\`                                             | Prevents the browser from suggesting a Picture-in-Picture context menu.                |
| `disableremoteplayback`   | \`str           | None\`                                             | Disables the capability of remote playback on devices.                                 |
| `height`                  | \`str           | int                                                | None\`                                                                                 |
| `width`                   | \`str           | int                                                | None\`                                                                                 |
| `loop`                    | \`str           | None\`                                             | Specifies that the video will start over again, every time it is finished.             |
| `muted`                   | \`str           | None\`                                             | Specifies that the audio output of the video should be muted.                          |
| `playsinline`             | \`str           | None\`                                             | Indicates that the video is to be played inline.                                       |
| `poster`                  | \`str           | None\`                                             | Specifies an image to be shown while the video is downloading.                         |
| `preload`                 | \`str           | None\`                                             | Specifies if and how the author thinks the video should be loaded when the page loads. |
| `class_`                  | \`str           | None\`                                             | Substituted as the DOM class attribute.                                                |
| `id_`                     | \`str           | None\`                                             | DOM ID attribute.                                                                      |
| `style`                   | \`str           | None\`                                             | Inline style attribute.                                                                |
| `custom_attributes`       | `AttributeType` | Keyword arguments transformed into tag attributes. | `{}`                                                                                   |

Source code in `src/air/tags/models/stock.py`

```
def __init__(
    self,
    *children: Renderable,
    src: str | None = None,
    autoplay: str | None = None,
    controls: str | None = None,
    controlslist: str | None = None,
    crossorigin: str | None = None,
    disablepictureinpicture: str | None = None,
    disableremoteplayback: str | None = None,
    height: str | int | None = None,
    width: str | int | None = None,
    loop: str | None = None,
    muted: str | None = None,
    playsinline: str | None = None,
    poster: str | None = None,
    preload: str | None = None,
    class_: str | None = None,
    id_: str | None = None,
    style: str | None = None,
    **custom_attributes: AttributeType,
) -> None:
    super().__init__(*children, **custom_attributes | locals_cleanup(locals()))
```
