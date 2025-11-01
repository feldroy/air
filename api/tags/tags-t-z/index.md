# Tags T-Z

## Td

```
Td(
    *children,
    colspan=None,
    rowspan=None,
    headers=None,
    class_=None,
    id=None,
    style=None,
    **kwargs,
)
```

Bases: `BaseTag`

Defines a cell in a table

Source code in `src/air/tags/models/stock.py`

```
def __init__(
    self,
    *children: Renderable,
    colspan: str | None = None,
    rowspan: str | None = None,
    headers: str | None = None,
    class_: str | None = None,
    id: str | None = None,
    style: str | None = None,
    **kwargs: AttributesType,
) -> None:
    super().__init__(*children, **kwargs | locals_cleanup(locals()))
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
    id=None,
    **kwargs,
)
```

Bases: `BaseTag`

Defines a container for content that should be hidden when the page loads

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
    id: str | None = None,
    **kwargs: AttributesType,
) -> None:
    super().__init__(*children, **kwargs | locals_cleanup(locals()))
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
    id=None,
    style=None,
    **kwargs,
)
```

Bases: `BaseTag`

Defines a multiline input control (text area)

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
    id: str | None = None,
    style: str | None = None,
    **kwargs: AttributesType,
) -> None:
    super().__init__(*children, **kwargs | locals_cleanup(locals()))
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
    id=None,
    style=None,
    **kwargs,
)
```

Bases: `BaseTag`

Defines a header cell in a table

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
    id: str | None = None,
    style: str | None = None,
    **kwargs: AttributesType,
) -> None:
    super().__init__(*children, **kwargs | locals_cleanup(locals()))
```

## Time

```
Time(
    *children,
    datetime=None,
    class_=None,
    id=None,
    style=None,
    **kwargs,
)
```

Bases: `BaseTag`

Defines a specific time (or datetime)

Source code in `src/air/tags/models/stock.py`

```
def __init__(
    self,
    *children: Renderable,
    datetime: str | None = None,
    class_: str | None = None,
    id: str | None = None,
    style: str | None = None,
    **kwargs: AttributesType,
) -> None:
    super().__init__(*children, **kwargs | locals_cleanup(locals()))
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
    id=None,
    style=None,
    **kwargs,
)
```

Bases: `SelfClosingTag`

Defines text tracks for media elements ( and )

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
    id: str | None = None,
    style: str | None = None,
    **kwargs: AttributesType,
) -> None:
    super().__init__(**kwargs | locals_cleanup(locals()))
```

## U

```
U(
    *children,
    compact=None,
    type=None,
    class_=None,
    id=None,
    style=None,
    **kwargs,
)
```

Bases: `BaseTag`

Defines some text that is unarticulated and styled differently from normal text

Source code in `src/air/tags/models/stock.py`

```
def __init__(
    self,
    *children: Renderable,
    compact: str | None = None,
    type: str | None = None,
    class_: str | None = None,
    id: str | None = None,
    style: str | None = None,
    **kwargs: AttributesType,
) -> None:
    super().__init__(*children, **kwargs | locals_cleanup(locals()))
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
    id=None,
    style=None,
    **kwargs,
)
```

Bases: `BaseTag`

Defines embedded video content

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
    id: str | None = None,
    style: str | None = None,
    **kwargs: AttributesType,
) -> None:
    super().__init__(*children, **kwargs | locals_cleanup(locals()))
```
