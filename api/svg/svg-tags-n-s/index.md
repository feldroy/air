# SVG Tags N-S

Air is proud to provide first class SVG support. The entire SVG specification is supported.

## Path

```
Path(
    *children,
    d=None,
    pathLength=None,
    class_=None,
    id=None,
    style=None,
    **kwargs,
)
```

Bases: `CaseTag`

Defines a path

Parameters:

| Name         | Type             | Description                               | Default                                 |
| ------------ | ---------------- | ----------------------------------------- | --------------------------------------- |
| `children`   | `Renderable`     | Tags, strings, or other rendered content. | `()`                                    |
| `d`          | \`str            | None\`                                    | Path data defining the shape.           |
| `pathLength` | \`float          | None\`                                    | Total path length in user units.        |
| `class_`     | \`str            | None\`                                    | Substituted as the DOM class attribute. |
| `id`         | \`str            | None\`                                    | DOM ID attribute.                       |
| `style`      | \`str            | None\`                                    | Inline style attribute.                 |
| `**kwargs`   | `AttributesType` | Additional attributes.                    | `{}`                                    |

Source code in `src/air/tags/models/svg.py`

```
def __init__(
    self,
    *children: Renderable,
    d: str | None = None,
    pathLength: float | None = None,
    class_: str | None = None,
    id: str | None = None,
    style: str | None = None,
    **kwargs: AttributesType,
) -> None:
    super().__init__(*children, **kwargs | locals_cleanup(locals()))
```

## Pattern

```
Pattern(
    *children,
    x=None,
    y=None,
    width=None,
    height=None,
    patternUnits=None,
    patternContentUnits=None,
    patternTransform=None,
    href=None,
    viewBox=None,
    preserveAspectRatio=None,
    class_=None,
    id=None,
    style=None,
    **kwargs,
)
```

Bases: `CaseTag`

Defines a pattern

Parameters:

| Name                  | Type             | Description                               | Default                                 |
| --------------------- | ---------------- | ----------------------------------------- | --------------------------------------- |
| `children`            | `Renderable`     | Tags, strings, or other rendered content. | `()`                                    |
| `x`                   | \`str            | float                                     | None\`                                  |
| `y`                   | \`str            | float                                     | None\`                                  |
| `width`               | \`str            | float                                     | None\`                                  |
| `height`              | \`str            | float                                     | None\`                                  |
| `patternUnits`        | \`str            | None\`                                    | Coordinate system for position/size.    |
| `patternContentUnits` | \`str            | None\`                                    | Coordinate system for contents.         |
| `patternTransform`    | \`str            | None\`                                    | Additional transformation.              |
| `href`                | \`str            | None\`                                    | Reference to template pattern.          |
| `viewBox`             | \`str            | None\`                                    | Viewport bounds for pattern.            |
| `preserveAspectRatio` | \`str            | None\`                                    | Aspect ratio handling.                  |
| `class_`              | \`str            | None\`                                    | Substituted as the DOM class attribute. |
| `id`                  | \`str            | None\`                                    | DOM ID attribute.                       |
| `style`               | \`str            | None\`                                    | Inline style attribute.                 |
| `**kwargs`            | `AttributesType` | Additional attributes.                    | `{}`                                    |

Source code in `src/air/tags/models/svg.py`

```
def __init__(
    self,
    *children: Renderable,
    x: str | float | None = None,
    y: str | float | None = None,
    width: str | float | None = None,
    height: str | float | None = None,
    patternUnits: str | None = None,
    patternContentUnits: str | None = None,
    patternTransform: str | None = None,
    href: str | None = None,
    viewBox: str | None = None,
    preserveAspectRatio: str | None = None,
    class_: str | None = None,
    id: str | None = None,
    style: str | None = None,
    **kwargs: AttributesType,
) -> None:
    super().__init__(*children, **kwargs | locals_cleanup(locals()))
```

## Polygon

```
Polygon(
    *children,
    points=None,
    pathLength=None,
    class_=None,
    id=None,
    style=None,
    **kwargs,
)
```

Bases: `CaseTag`

Defines a polygon

Parameters:

| Name         | Type             | Description                               | Default                                 |
| ------------ | ---------------- | ----------------------------------------- | --------------------------------------- |
| `children`   | `Renderable`     | Tags, strings, or other rendered content. | `()`                                    |
| `points`     | \`str            | None\`                                    | List of x,y coordinate pairs.           |
| `pathLength` | \`float          | None\`                                    | Total path length in user units.        |
| `class_`     | \`str            | None\`                                    | Substituted as the DOM class attribute. |
| `id`         | \`str            | None\`                                    | DOM ID attribute.                       |
| `style`      | \`str            | None\`                                    | Inline style attribute.                 |
| `**kwargs`   | `AttributesType` | Additional attributes.                    | `{}`                                    |

Source code in `src/air/tags/models/svg.py`

```
def __init__(
    self,
    *children: Renderable,
    points: str | None = None,
    pathLength: float | None = None,
    class_: str | None = None,
    id: str | None = None,
    style: str | None = None,
    **kwargs: AttributesType,
) -> None:
    super().__init__(*children, **kwargs | locals_cleanup(locals()))
```

## Polyline

```
Polyline(
    *children,
    points=None,
    pathLength=None,
    class_=None,
    id=None,
    style=None,
    **kwargs,
)
```

Bases: `CaseTag`

Defines a polyline

Parameters:

| Name         | Type             | Description                               | Default                                 |
| ------------ | ---------------- | ----------------------------------------- | --------------------------------------- |
| `children`   | `Renderable`     | Tags, strings, or other rendered content. | `()`                                    |
| `points`     | \`str            | None\`                                    | List of x,y coordinate pairs.           |
| `pathLength` | \`float          | None\`                                    | Total path length in user units.        |
| `class_`     | \`str            | None\`                                    | Substituted as the DOM class attribute. |
| `id`         | \`str            | None\`                                    | DOM ID attribute.                       |
| `style`      | \`str            | None\`                                    | Inline style attribute.                 |
| `**kwargs`   | `AttributesType` | Additional attributes.                    | `{}`                                    |

Source code in `src/air/tags/models/svg.py`

```
def __init__(
    self,
    *children: Renderable,
    points: str | None = None,
    pathLength: float | None = None,
    class_: str | None = None,
    id: str | None = None,
    style: str | None = None,
    **kwargs: AttributesType,
) -> None:
    super().__init__(*children, **kwargs | locals_cleanup(locals()))
```

## RadialGradient

```
RadialGradient(
    *children,
    cx=None,
    cy=None,
    r=None,
    fx=None,
    fy=None,
    fr=None,
    gradientUnits=None,
    gradientTransform=None,
    href=None,
    spreadMethod=None,
    class_=None,
    id=None,
    style=None,
    **kwargs,
)
```

Bases: `CaseTag`

Defines a radial gradient

Parameters:

| Name                | Type             | Description                               | Default                                 |
| ------------------- | ---------------- | ----------------------------------------- | --------------------------------------- |
| `children`          | `Renderable`     | Tags, strings, or other rendered content. | `()`                                    |
| `cx`                | \`str            | float                                     | None\`                                  |
| `cy`                | \`str            | float                                     | None\`                                  |
| `r`                 | \`str            | float                                     | None\`                                  |
| `fx`                | \`str            | float                                     | None\`                                  |
| `fy`                | \`str            | float                                     | None\`                                  |
| `fr`                | \`str            | float                                     | None\`                                  |
| `gradientUnits`     | \`str            | None\`                                    | Coordinate system.                      |
| `gradientTransform` | \`str            | None\`                                    | Additional transformation.              |
| `href`              | \`str            | None\`                                    | Reference to template gradient.         |
| `spreadMethod`      | \`str            | None\`                                    | Gradient behavior.                      |
| `class_`            | \`str            | None\`                                    | Substituted as the DOM class attribute. |
| `id`                | \`str            | None\`                                    | DOM ID attribute.                       |
| `style`             | \`str            | None\`                                    | Inline style attribute.                 |
| `**kwargs`          | `AttributesType` | Additional attributes.                    | `{}`                                    |

Source code in `src/air/tags/models/svg.py`

```
def __init__(
    self,
    *children: Renderable,
    cx: str | float | None = None,
    cy: str | float | None = None,
    r: str | float | None = None,
    fx: str | float | None = None,
    fy: str | float | None = None,
    fr: str | float | None = None,
    gradientUnits: str | None = None,
    gradientTransform: str | None = None,
    href: str | None = None,
    spreadMethod: str | None = None,
    class_: str | None = None,
    id: str | None = None,
    style: str | None = None,
    **kwargs: AttributesType,
) -> None:
    super().__init__(*children, **kwargs | locals_cleanup(locals()))
```

## Rect

```
Rect(
    *children,
    x=None,
    y=None,
    width=None,
    height=None,
    rx=None,
    ry=None,
    pathLength=None,
    class_=None,
    id=None,
    style=None,
    **kwargs,
)
```

Bases: `CaseTag`

Defines a rectangle

Parameters:

| Name         | Type             | Description                               | Default                                 |
| ------------ | ---------------- | ----------------------------------------- | --------------------------------------- |
| `children`   | `Renderable`     | Tags, strings, or other rendered content. | `()`                                    |
| `x`          | \`str            | float                                     | None\`                                  |
| `y`          | \`str            | float                                     | None\`                                  |
| `width`      | \`str            | float                                     | None\`                                  |
| `height`     | \`str            | float                                     | None\`                                  |
| `rx`         | \`str            | float                                     | None\`                                  |
| `ry`         | \`str            | float                                     | None\`                                  |
| `pathLength` | \`float          | None\`                                    | Total perimeter length in user units.   |
| `class_`     | \`str            | None\`                                    | Substituted as the DOM class attribute. |
| `id`         | \`str            | None\`                                    | DOM ID attribute.                       |
| `style`      | \`str            | None\`                                    | Inline style attribute.                 |
| `**kwargs`   | `AttributesType` | Additional attributes.                    | `{}`                                    |

Source code in `src/air/tags/models/svg.py`

```
def __init__(
    self,
    *children: Renderable,
    x: str | float | None = None,
    y: str | float | None = None,
    width: str | float | None = None,
    height: str | float | None = None,
    rx: str | float | None = None,
    ry: str | float | None = None,
    pathLength: float | None = None,
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
    *children,
    type=None,
    href=None,
    crossorigin=None,
    fetchpriority=None,
    class_=None,
    id=None,
    style=None,
    **kwargs,
)
```

Bases: `CaseTag`

Defines a script

Parameters:

| Name            | Type             | Description                               | Default                                 |
| --------------- | ---------------- | ----------------------------------------- | --------------------------------------- |
| `children`      | `Renderable`     | Tags, strings, or other rendered content. | `()`                                    |
| `type`          | \`str            | None\`                                    | Script MIME type.                       |
| `href`          | \`str            | None\`                                    | External script URL.                    |
| `crossorigin`   | \`str            | None\`                                    | CORS credentials flag.                  |
| `fetchpriority` | \`str            | None\`                                    | Fetch priority hint (experimental).     |
| `class_`        | \`str            | None\`                                    | Substituted as the DOM class attribute. |
| `id`            | \`str            | None\`                                    | DOM ID attribute.                       |
| `style`         | \`str            | None\`                                    | Inline style attribute.                 |
| `**kwargs`      | `AttributesType` | Additional attributes.                    | `{}`                                    |

Source code in `src/air/tags/models/svg.py`

```
def __init__(
    self,
    *children: Renderable,
    type: str | None = None,
    href: str | None = None,
    crossorigin: str | None = None,
    fetchpriority: str | None = None,
    class_: str | None = None,
    id: str | None = None,
    style: str | None = None,
    **kwargs: AttributesType,
) -> None:
    super().__init__(*children, **kwargs | locals_cleanup(locals()))
```

## Set

```
Set(
    *children,
    to=None,
    attributeName=None,
    begin=None,
    dur=None,
    class_=None,
    id=None,
    style=None,
    **kwargs,
)
```

Bases: `CaseTag`

Sets an attribute value

Parameters:

| Name            | Type             | Description                               | Default                                 |
| --------------- | ---------------- | ----------------------------------------- | --------------------------------------- |
| `children`      | `Renderable`     | Tags, strings, or other rendered content. | `()`                                    |
| `to`            | \`str            | None\`                                    | Value to apply for animation duration.  |
| `attributeName` | \`str            | None\`                                    | Target attribute to set.                |
| `begin`         | \`str            | None\`                                    | Animation start time.                   |
| `dur`           | \`str            | None\`                                    | Animation duration.                     |
| `class_`        | \`str            | None\`                                    | Substituted as the DOM class attribute. |
| `id`            | \`str            | None\`                                    | DOM ID attribute.                       |
| `style`         | \`str            | None\`                                    | Inline style attribute.                 |
| `**kwargs`      | `AttributesType` | Additional attributes.                    | `{}`                                    |

Source code in `src/air/tags/models/svg.py`

```
def __init__(
    self,
    *children: Renderable,
    to: str | None = None,
    attributeName: str | None = None,
    begin: str | None = None,
    dur: str | None = None,
    class_: str | None = None,
    id: str | None = None,
    style: str | None = None,
    **kwargs: AttributesType,
) -> None:
    super().__init__(*children, **kwargs | locals_cleanup(locals()))
```

## Stop

```
Stop(
    *children,
    offset=None,
    stop_color=None,
    stop_opacity=None,
    class_=None,
    id=None,
    style=None,
    **kwargs,
)
```

Bases: `CaseTag`

Defines a gradient stop

Parameters:

| Name           | Type             | Description                               | Default                                 |
| -------------- | ---------------- | ----------------------------------------- | --------------------------------------- |
| `children`     | `Renderable`     | Tags, strings, or other rendered content. | `()`                                    |
| `offset`       | \`str            | float                                     | None\`                                  |
| `stop_color`   | \`str            | None\`                                    | Color of gradient stop.                 |
| `stop_opacity` | \`str            | float                                     | None\`                                  |
| `class_`       | \`str            | None\`                                    | Substituted as the DOM class attribute. |
| `id`           | \`str            | None\`                                    | DOM ID attribute.                       |
| `style`        | \`str            | None\`                                    | Inline style attribute.                 |
| `**kwargs`     | `AttributesType` | Additional attributes.                    | `{}`                                    |

Source code in `src/air/tags/models/svg.py`

```
def __init__(
    self,
    *children: Renderable,
    offset: str | float | None = None,
    stop_color: str | None = None,
    stop_opacity: str | float | None = None,
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
    *children,
    type=None,
    media=None,
    class_=None,
    id=None,
    style=None,
    **kwargs,
)
```

Bases: `CaseTag`

Defines style information

Parameters:

| Name       | Type             | Description                               | Default                                 |
| ---------- | ---------------- | ----------------------------------------- | --------------------------------------- |
| `children` | `Renderable`     | Tags, strings, or other rendered content. | `()`                                    |
| `type`     | \`str            | None\`                                    | Style sheet language MIME type.         |
| `media`    | \`str            | None\`                                    | Media query for when styles apply.      |
| `class_`   | \`str            | None\`                                    | Substituted as the DOM class attribute. |
| `id`       | \`str            | None\`                                    | DOM ID attribute.                       |
| `style`    | \`str            | None\`                                    | Inline style attribute.                 |
| `**kwargs` | `AttributesType` | Additional attributes.                    | `{}`                                    |

Source code in `src/air/tags/models/svg.py`

```
def __init__(
    self,
    *children: Renderable,
    type: str | None = None,
    media: str | None = None,
    class_: str | None = None,
    id: str | None = None,
    style: str | None = None,
    **kwargs: AttributesType,
) -> None:
    super().__init__(*children, **kwargs | locals_cleanup(locals()))
```

## Svg

```
Svg(
    *children,
    width=None,
    height=None,
    x=None,
    y=None,
    viewBox=None,
    preserveAspectRatio=None,
    class_=None,
    id=None,
    style=None,
    **kwargs,
)
```

Bases: `CaseTag`

Defines an SVG document fragment

Parameters:

| Name                  | Type             | Description                               | Default                                 |
| --------------------- | ---------------- | ----------------------------------------- | --------------------------------------- |
| `children`            | `Renderable`     | Tags, strings, or other rendered content. | `()`                                    |
| `width`               | \`str            | float                                     | None\`                                  |
| `height`              | \`str            | float                                     | None\`                                  |
| `x`                   | \`str            | float                                     | None\`                                  |
| `y`                   | \`str            | float                                     | None\`                                  |
| `viewBox`             | \`str            | None\`                                    | SVG viewport coordinates.               |
| `preserveAspectRatio` | \`str            | None\`                                    | Aspect ratio handling.                  |
| `class_`              | \`str            | None\`                                    | Substituted as the DOM class attribute. |
| `id`                  | \`str            | None\`                                    | DOM ID attribute.                       |
| `style`               | \`str            | None\`                                    | Inline style attribute.                 |
| `**kwargs`            | `AttributesType` | Additional attributes.                    | `{}`                                    |

Source code in `src/air/tags/models/svg.py`

```
def __init__(
    self,
    *children: Renderable,
    width: str | float | None = None,
    height: str | float | None = None,
    x: str | float | None = None,
    y: str | float | None = None,
    viewBox: str | None = None,
    preserveAspectRatio: str | None = None,
    class_: str | None = None,
    id: str | None = None,
    style: str | None = None,
    **kwargs: AttributesType,
) -> None:
    super().__init__(*children, **kwargs | locals_cleanup(locals()))
```

## Switch

```
Switch(
    *children, class_=None, id=None, style=None, **kwargs
)
```

Bases: `CaseTag`

Defines conditional processing

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

## Symbol

```
Symbol(
    *children,
    width=None,
    height=None,
    x=None,
    y=None,
    viewBox=None,
    preserveAspectRatio=None,
    refX=None,
    refY=None,
    class_=None,
    id=None,
    style=None,
    **kwargs,
)
```

Bases: `CaseTag`

Defines a reusable symbol

Parameters:

| Name                  | Type             | Description                               | Default                                 |
| --------------------- | ---------------- | ----------------------------------------- | --------------------------------------- |
| `children`            | `Renderable`     | Tags, strings, or other rendered content. | `()`                                    |
| `width`               | \`str            | float                                     | None\`                                  |
| `height`              | \`str            | float                                     | None\`                                  |
| `x`                   | \`str            | float                                     | None\`                                  |
| `y`                   | \`str            | float                                     | None\`                                  |
| `viewBox`             | \`str            | None\`                                    | Viewport bounds for symbol.             |
| `preserveAspectRatio` | \`str            | None\`                                    | Aspect ratio handling.                  |
| `refX`                | \`str            | float                                     | None\`                                  |
| `refY`                | \`str            | float                                     | None\`                                  |
| `class_`              | \`str            | None\`                                    | Substituted as the DOM class attribute. |
| `id`                  | \`str            | None\`                                    | DOM ID attribute.                       |
| `style`               | \`str            | None\`                                    | Inline style attribute.                 |
| `**kwargs`            | `AttributesType` | Additional attributes.                    | `{}`                                    |

Source code in `src/air/tags/models/svg.py`

```
def __init__(
    self,
    *children: Renderable,
    width: str | float | None = None,
    height: str | float | None = None,
    x: str | float | None = None,
    y: str | float | None = None,
    viewBox: str | None = None,
    preserveAspectRatio: str | None = None,
    refX: str | float | None = None,
    refY: str | float | None = None,
    class_: str | None = None,
    id: str | None = None,
    style: str | None = None,
    **kwargs: AttributesType,
) -> None:
    super().__init__(*children, **kwargs | locals_cleanup(locals()))
```
