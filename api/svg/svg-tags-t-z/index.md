# SVG Tags T-Z

Air is proud to provide first class SVG support. The entire SVG specification is supported.

## Text

```
Text(
    *children,
    x=None,
    y=None,
    dx=None,
    dy=None,
    rotate=None,
    lengthAdjust=None,
    textLength=None,
    class_=None,
    id=None,
    style=None,
    **kwargs,
)
```

Bases: `CaseTag`

Defines text content

Parameters:

| Name           | Type             | Description                               | Default                                 |
| -------------- | ---------------- | ----------------------------------------- | --------------------------------------- |
| `children`     | `Renderable`     | Tags, strings, or other rendered content. | `()`                                    |
| `x`            | \`str            | float                                     | None\`                                  |
| `y`            | \`str            | float                                     | None\`                                  |
| `dx`           | \`str            | float                                     | None\`                                  |
| `dy`           | \`str            | float                                     | None\`                                  |
| `rotate`       | \`str            | None\`                                    | Rotation of individual glyphs.          |
| `lengthAdjust` | \`str            | None\`                                    | Text stretching method.                 |
| `textLength`   | \`str            | float                                     | None\`                                  |
| `class_`       | \`str            | None\`                                    | Substituted as the DOM class attribute. |
| `id`           | \`str            | None\`                                    | DOM ID attribute.                       |
| `style`        | \`str            | None\`                                    | Inline style attribute.                 |
| `**kwargs`     | `AttributesType` | Additional attributes.                    | `{}`                                    |

Source code in `src/air/tags/models/svg.py`

```
def __init__(
    self,
    *children: Renderable,
    x: str | float | None = None,
    y: str | float | None = None,
    dx: str | float | None = None,
    dy: str | float | None = None,
    rotate: str | None = None,
    lengthAdjust: str | None = None,
    textLength: str | float | None = None,
    class_: str | None = None,
    id: str | None = None,
    style: str | None = None,
    **kwargs: AttributesType,
) -> None:
    super().__init__(*children, **kwargs | locals_cleanup(locals()))
```

## TextPath

```
TextPath(
    *children,
    href=None,
    lengthAdjust=None,
    method=None,
    path=None,
    side=None,
    spacing=None,
    startOffset=None,
    textLength=None,
    class_=None,
    id=None,
    style=None,
    **kwargs,
)
```

Bases: `CaseTag`

Defines text along a path

Parameters:

| Name           | Type             | Description                               | Default                                    |
| -------------- | ---------------- | ----------------------------------------- | ------------------------------------------ |
| `children`     | `Renderable`     | Tags, strings, or other rendered content. | `()`                                       |
| `href`         | \`str            | None\`                                    | Reference to path element for text layout. |
| `lengthAdjust` | \`str            | None\`                                    | Length adjustment method.                  |
| `method`       | \`str            | None\`                                    | Glyph rendering method.                    |
| `path`         | \`str            | None\`                                    | Path data for text layout.                 |
| `side`         | \`str            | None\`                                    | Which side of path to render text.         |
| `spacing`      | \`str            | None\`                                    | Glyph spacing handling.                    |
| `startOffset`  | \`str            | float                                     | None\`                                     |
| `textLength`   | \`str            | float                                     | None\`                                     |
| `class_`       | \`str            | None\`                                    | Substituted as the DOM class attribute.    |
| `id`           | \`str            | None\`                                    | DOM ID attribute.                          |
| `style`        | \`str            | None\`                                    | Inline style attribute.                    |
| `**kwargs`     | `AttributesType` | Additional attributes.                    | `{}`                                       |

Source code in `src/air/tags/models/svg.py`

```
def __init__(
    self,
    *children: Renderable,
    href: str | None = None,
    lengthAdjust: str | None = None,
    method: str | None = None,
    path: str | None = None,
    side: str | None = None,
    spacing: str | None = None,
    startOffset: str | float | None = None,
    textLength: str | float | None = None,
    class_: str | None = None,
    id: str | None = None,
    style: str | None = None,
    **kwargs: AttributesType,
) -> None:
    super().__init__(*children, **kwargs | locals_cleanup(locals()))
```

## Title

```
Title(
    *children, class_=None, id=None, style=None, **kwargs
)
```

Bases: `CaseTag`

Defines a title for the SVG document

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

## Tspan

```
Tspan(
    *children,
    x=None,
    y=None,
    dx=None,
    dy=None,
    rotate=None,
    lengthAdjust=None,
    textLength=None,
    class_=None,
    id=None,
    style=None,
    **kwargs,
)
```

Bases: `CaseTag`

Defines a text span

Parameters:

| Name           | Type             | Description                               | Default                                 |
| -------------- | ---------------- | ----------------------------------------- | --------------------------------------- |
| `children`     | `Renderable`     | Tags, strings, or other rendered content. | `()`                                    |
| `x`            | \`str            | float                                     | None\`                                  |
| `y`            | \`str            | float                                     | None\`                                  |
| `dx`           | \`str            | float                                     | None\`                                  |
| `dy`           | \`str            | float                                     | None\`                                  |
| `rotate`       | \`str            | None\`                                    | Rotation of individual glyphs.          |
| `lengthAdjust` | \`str            | None\`                                    | Text stretching method.                 |
| `textLength`   | \`str            | float                                     | None\`                                  |
| `class_`       | \`str            | None\`                                    | Substituted as the DOM class attribute. |
| `id`           | \`str            | None\`                                    | DOM ID attribute.                       |
| `style`        | \`str            | None\`                                    | Inline style attribute.                 |
| `**kwargs`     | `AttributesType` | Additional attributes.                    | `{}`                                    |

Source code in `src/air/tags/models/svg.py`

```
def __init__(
    self,
    *children: Renderable,
    x: str | float | None = None,
    y: str | float | None = None,
    dx: str | float | None = None,
    dy: str | float | None = None,
    rotate: str | None = None,
    lengthAdjust: str | None = None,
    textLength: str | float | None = None,
    class_: str | None = None,
    id: str | None = None,
    style: str | None = None,
    **kwargs: AttributesType,
) -> None:
    super().__init__(*children, **kwargs | locals_cleanup(locals()))
```

## Use

```
Use(
    *children,
    href=None,
    x=None,
    y=None,
    width=None,
    height=None,
    class_=None,
    id=None,
    style=None,
    **kwargs,
)
```

Bases: `CaseTag`

References another element

Parameters:

| Name       | Type             | Description                               | Default                                 |
| ---------- | ---------------- | ----------------------------------------- | --------------------------------------- |
| `children` | `Renderable`     | Tags, strings, or other rendered content. | `()`                                    |
| `href`     | \`str            | None\`                                    | Reference to element to duplicate.      |
| `x`        | \`str            | float                                     | None\`                                  |
| `y`        | \`str            | float                                     | None\`                                  |
| `width`    | \`str            | float                                     | None\`                                  |
| `height`   | \`str            | float                                     | None\`                                  |
| `class_`   | \`str            | None\`                                    | Substituted as the DOM class attribute. |
| `id`       | \`str            | None\`                                    | DOM ID attribute.                       |
| `style`    | \`str            | None\`                                    | Inline style attribute.                 |
| `**kwargs` | `AttributesType` | Additional attributes.                    | `{}`                                    |

Source code in `src/air/tags/models/svg.py`

```
def __init__(
    self,
    *children: Renderable,
    href: str | None = None,
    x: str | float | None = None,
    y: str | float | None = None,
    width: str | float | None = None,
    height: str | float | None = None,
    class_: str | None = None,
    id: str | None = None,
    style: str | None = None,
    **kwargs: AttributesType,
) -> None:
    super().__init__(*children, **kwargs | locals_cleanup(locals()))
```

## View

```
View(
    *children,
    viewBox=None,
    preserveAspectRatio=None,
    class_=None,
    id=None,
    style=None,
    **kwargs,
)
```

Bases: `CaseTag`

Defines a view

Parameters:

| Name                  | Type             | Description                               | Default                                 |
| --------------------- | ---------------- | ----------------------------------------- | --------------------------------------- |
| `children`            | `Renderable`     | Tags, strings, or other rendered content. | `()`                                    |
| `viewBox`             | \`str            | None\`                                    | Viewport bounds.                        |
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
    viewBox: str | None = None,
    preserveAspectRatio: str | None = None,
    class_: str | None = None,
    id: str | None = None,
    style: str | None = None,
    **kwargs: AttributesType,
) -> None:
    super().__init__(*children, **kwargs | locals_cleanup(locals()))
```
