# SVG Tags A-D

Air is proud to provide first class SVG support. The entire SVG specification is supported.

## A

```
A(
    *children,
    href=None,
    target=None,
    download=None,
    hreflang=None,
    ping=None,
    referrerpolicy=None,
    rel=None,
    type=None,
    class_=None,
    id=None,
    style=None,
    **kwargs,
)
```

Bases: `CaseTag`

Defines an SVG hyperlink

Parameters:

| Name             | Type             | Description                               | Default                                            |
| ---------------- | ---------------- | ----------------------------------------- | -------------------------------------------------- |
| `children`       | `Renderable`     | Tags, strings, or other rendered content. | `()`                                               |
| `href`           | \`str            | None\`                                    | Hyperlink target URL.                              |
| `target`         | \`str            | None\`                                    | Where to display linked URL (\_self                |
| `download`       | \`str            | None\`                                    | Instructs browser to download instead of navigate. |
| `hreflang`       | \`str            | None\`                                    | Human language of the linked URL.                  |
| `ping`           | \`str            | None\`                                    | Space-separated list of URLs for tracking.         |
| `referrerpolicy` | \`str            | None\`                                    | Referrer policy when fetching the URL.             |
| `rel`            | \`str            | None\`                                    | Relationship to target object.                     |
| `type`           | \`str            | None\`                                    | MIME type of linked URL.                           |
| `class_`         | \`str            | None\`                                    | Substituted as the DOM class attribute.            |
| `id`             | \`str            | None\`                                    | DOM ID attribute.                                  |
| `style`          | \`str            | None\`                                    | Inline style attribute.                            |
| `**kwargs`       | `AttributesType` | Additional attributes.                    | `{}`                                               |

Source code in `src/air/tags/models/svg.py`

```
def __init__(
    self,
    *children: Renderable,
    href: str | None = None,
    target: str | None = None,
    download: str | None = None,
    hreflang: str | None = None,
    ping: str | None = None,
    referrerpolicy: str | None = None,
    rel: str | None = None,
    type: str | None = None,
    class_: str | None = None,
    id: str | None = None,
    style: str | None = None,
    **kwargs: AttributesType,
) -> None:
    super().__init__(*children, **kwargs | locals_cleanup(locals()))
```

## Animate

```
Animate(
    *children,
    attributeName=None,
    attributeType=None,
    values=None,
    dur=None,
    repeatCount=None,
    repeatDur=None,
    from_=None,
    to=None,
    by=None,
    begin=None,
    end=None,
    calcMode=None,
    class_=None,
    id=None,
    style=None,
    **kwargs,
)
```

Bases: `CaseTag`

Defines animation on an SVG element

Parameters:

| Name            | Type             | Description                               | Default                                 |
| --------------- | ---------------- | ----------------------------------------- | --------------------------------------- |
| `children`      | `Renderable`     | Tags, strings, or other rendered content. | `()`                                    |
| `attributeName` | \`str            | None\`                                    | Target attribute to animate.            |
| `attributeType` | \`str            | None\`                                    | Type of target attribute.               |
| `values`        | \`str            | None\`                                    | Values to animate through.              |
| `dur`           | \`str            | None\`                                    | Total animation duration.               |
| `repeatCount`   | \`str            | float                                     | None\`                                  |
| `repeatDur`     | \`str            | None\`                                    | Total duration for repeating.           |
| `from_`         | \`str            | None\`                                    | Starting value (from is reserved).      |
| `to`            | \`str            | None\`                                    | Ending value.                           |
| `by`            | \`str            | None\`                                    | Relative animation value.               |
| `begin`         | \`str            | None\`                                    | Animation start time.                   |
| `end`           | \`str            | None\`                                    | Animation end time.                     |
| `calcMode`      | \`str            | None\`                                    | Interpolation mode (discrete            |
| `class_`        | \`str            | None\`                                    | Substituted as the DOM class attribute. |
| `id`            | \`str            | None\`                                    | DOM ID attribute.                       |
| `style`         | \`str            | None\`                                    | Inline style attribute.                 |
| `**kwargs`      | `AttributesType` | Additional attributes.                    | `{}`                                    |

Source code in `src/air/tags/models/svg.py`

```
def __init__(
    self,
    *children: Renderable,
    attributeName: str | None = None,
    attributeType: str | None = None,
    values: str | None = None,
    dur: str | None = None,
    repeatCount: str | float | None = None,
    repeatDur: str | None = None,
    from_: str | None = None,
    to: str | None = None,
    by: str | None = None,
    begin: str | None = None,
    end: str | None = None,
    calcMode: str | None = None,
    class_: str | None = None,
    id: str | None = None,
    style: str | None = None,
    **kwargs: AttributesType,
) -> None:
    super().__init__(*children, **kwargs | locals_cleanup(locals()))
```

## AnimateMotion

```
AnimateMotion(
    *children,
    path=None,
    keyPoints=None,
    rotate=None,
    dur=None,
    repeatCount=None,
    begin=None,
    class_=None,
    id=None,
    style=None,
    **kwargs,
)
```

Bases: `CaseTag`

Defines how an element moves along a motion path

Parameters:

| Name          | Type             | Description                               | Default                                 |
| ------------- | ---------------- | ----------------------------------------- | --------------------------------------- |
| `children`    | `Renderable`     | Tags, strings, or other rendered content. | `()`                                    |
| `path`        | \`str            | None\`                                    | Motion path using path syntax.          |
| `keyPoints`   | \`str            | None\`                                    | Progress points along path (0-1 range). |
| `rotate`      | \`str            | float                                     | None\`                                  |
| `dur`         | \`str            | None\`                                    | Total animation duration.               |
| `repeatCount` | \`str            | float                                     | None\`                                  |
| `begin`       | \`str            | None\`                                    | Animation start time.                   |
| `class_`      | \`str            | None\`                                    | Substituted as the DOM class attribute. |
| `id`          | \`str            | None\`                                    | DOM ID attribute.                       |
| `style`       | \`str            | None\`                                    | Inline style attribute.                 |
| `**kwargs`    | `AttributesType` | Additional attributes.                    | `{}`                                    |

Source code in `src/air/tags/models/svg.py`

```
def __init__(
    self,
    *children: Renderable,
    path: str | None = None,
    keyPoints: str | None = None,
    rotate: str | float | None = None,
    dur: str | None = None,
    repeatCount: str | float | None = None,
    begin: str | None = None,
    class_: str | None = None,
    id: str | None = None,
    style: str | None = None,
    **kwargs: AttributesType,
) -> None:
    super().__init__(*children, **kwargs | locals_cleanup(locals()))
```

## AnimateTransform

```
AnimateTransform(
    *children,
    type=None,
    by=None,
    from_=None,
    to=None,
    dur=None,
    repeatCount=None,
    begin=None,
    class_=None,
    id=None,
    style=None,
    **kwargs,
)
```

Bases: `CaseTag`

Animates transform attributes on an element

Parameters:

| Name          | Type             | Description                               | Default                                 |
| ------------- | ---------------- | ----------------------------------------- | --------------------------------------- |
| `children`    | `Renderable`     | Tags, strings, or other rendered content. | `()`                                    |
| `type`        | \`str            | None\`                                    | Transformation type (rotate             |
| `by`          | \`str            | None\`                                    | Relative animation value.               |
| `from_`       | \`str            | None\`                                    | Starting transformation value.          |
| `to`          | \`str            | None\`                                    | Ending transformation value.            |
| `dur`         | \`str            | None\`                                    | Total animation duration.               |
| `repeatCount` | \`str            | float                                     | None\`                                  |
| `begin`       | \`str            | None\`                                    | Animation start time.                   |
| `class_`      | \`str            | None\`                                    | Substituted as the DOM class attribute. |
| `id`          | \`str            | None\`                                    | DOM ID attribute.                       |
| `style`       | \`str            | None\`                                    | Inline style attribute.                 |
| `**kwargs`    | `AttributesType` | Additional attributes.                    | `{}`                                    |

Source code in `src/air/tags/models/svg.py`

```
def __init__(
    self,
    *children: Renderable,
    type: str | None = None,
    by: str | None = None,
    from_: str | None = None,
    to: str | None = None,
    dur: str | None = None,
    repeatCount: str | float | None = None,
    begin: str | None = None,
    class_: str | None = None,
    id: str | None = None,
    style: str | None = None,
    **kwargs: AttributesType,
) -> None:
    super().__init__(*children, **kwargs | locals_cleanup(locals()))
```

## Circle

```
Circle(
    *children,
    cx=None,
    cy=None,
    r=None,
    pathLength=None,
    class_=None,
    id=None,
    style=None,
    **kwargs,
)
```

Bases: `CaseTag`

Defines a circle

Parameters:

| Name         | Type             | Description                               | Default                                   |
| ------------ | ---------------- | ----------------------------------------- | ----------------------------------------- |
| `children`   | `Renderable`     | Tags, strings, or other rendered content. | `()`                                      |
| `cx`         | \`str            | float                                     | None\`                                    |
| `cy`         | \`str            | float                                     | None\`                                    |
| `r`          | \`str            | float                                     | None\`                                    |
| `pathLength` | \`float          | None\`                                    | Total circumference length in user units. |
| `class_`     | \`str            | None\`                                    | Substituted as the DOM class attribute.   |
| `id`         | \`str            | None\`                                    | DOM ID attribute.                         |
| `style`      | \`str            | None\`                                    | Inline style attribute.                   |
| `**kwargs`   | `AttributesType` | Additional attributes.                    | `{}`                                      |

Source code in `src/air/tags/models/svg.py`

```
def __init__(
    self,
    *children: Renderable,
    cx: str | float | None = None,
    cy: str | float | None = None,
    r: str | float | None = None,
    pathLength: float | None = None,
    class_: str | None = None,
    id: str | None = None,
    style: str | None = None,
    **kwargs: AttributesType,
) -> None:
    super().__init__(*children, **kwargs | locals_cleanup(locals()))
```

## ClipPath

```
ClipPath(
    *children,
    clipPathUnits=None,
    class_=None,
    id=None,
    style=None,
    **kwargs,
)
```

Bases: `CaseTag`

Defines a clipping path

Parameters:

| Name            | Type             | Description                               | Default                                 |
| --------------- | ---------------- | ----------------------------------------- | --------------------------------------- |
| `children`      | `Renderable`     | Tags, strings, or other rendered content. | `()`                                    |
| `clipPathUnits` | \`str            | None\`                                    | Coordinate system (userSpaceOnUse       |
| `class_`        | \`str            | None\`                                    | Substituted as the DOM class attribute. |
| `id`            | \`str            | None\`                                    | DOM ID attribute.                       |
| `style`         | \`str            | None\`                                    | Inline style attribute.                 |
| `**kwargs`      | `AttributesType` | Additional attributes.                    | `{}`                                    |

Source code in `src/air/tags/models/svg.py`

```
def __init__(
    self,
    *children: Renderable,
    clipPathUnits: str | None = None,
    class_: str | None = None,
    id: str | None = None,
    style: str | None = None,
    **kwargs: AttributesType,
) -> None:
    super().__init__(*children, **kwargs | locals_cleanup(locals()))
```

## Defs

```
Defs(*children, class_=None, id=None, style=None, **kwargs)
```

Bases: `CaseTag`

Defines reusable objects

Parameters:

| Name       | Type             | Description                               | Default                                 |
| ---------- | ---------------- | ----------------------------------------- | --------------------------------------- |
| `children` | `Renderable`     | Tags, strings, or other rendered content. | `()`                                    |
| `class_`   | \`str            | None\`                                    | Substituted as the DOM class attribute. |
| `id`       | \`str            | None\`                                    | DOM ID attribute.                       |
| `style`    | \`str            | None\`                                    | Inline style attribute.                 |
| `**kwargs` | `AttributesType` | Additional attributes.                    | `{}`                                    |

Source code in `src/air/tags/models/svg.py`

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

## Desc

```
Desc(*children, class_=None, id=None, style=None, **kwargs)
```

Bases: `CaseTag`

Defines a description of an element

Parameters:

| Name       | Type             | Description                               | Default                                 |
| ---------- | ---------------- | ----------------------------------------- | --------------------------------------- |
| `children` | `Renderable`     | Tags, strings, or other rendered content. | `()`                                    |
| `class_`   | \`str            | None\`                                    | Substituted as the DOM class attribute. |
| `id`       | \`str            | None\`                                    | DOM ID attribute.                       |
| `style`    | \`str            | None\`                                    | Inline style attribute.                 |
| `**kwargs` | `AttributesType` | Additional attributes.                    | `{}`                                    |

Source code in `src/air/tags/models/svg.py`

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
