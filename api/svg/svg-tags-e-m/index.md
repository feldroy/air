# SVG Tags E-M

Air is proud to provide first class SVG support. The entire SVG specification is supported.

## Ellipse

```
Ellipse(
    *children,
    cx=None,
    cy=None,
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

Defines an ellipse

Parameters:

| Name         | Type             | Description                               | Default                                 |
| ------------ | ---------------- | ----------------------------------------- | --------------------------------------- |
| `children`   | `Renderable`     | Tags, strings, or other rendered content. | `()`                                    |
| `cx`         | \`str            | float                                     | None\`                                  |
| `cy`         | \`str            | float                                     | None\`                                  |
| `rx`         | \`str            | float                                     | None\`                                  |
| `ry`         | \`str            | float                                     | None\`                                  |
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
    cx: str | float | None = None,
    cy: str | float | None = None,
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

## FeBlend

```
FeBlend(
    *children,
    in_=None,
    in2=None,
    mode=None,
    result=None,
    class_=None,
    id=None,
    style=None,
    **kwargs,
)
```

Bases: `CaseTag`

Defines image blending

Parameters:

| Name       | Type             | Description                               | Default                                 |
| ---------- | ---------------- | ----------------------------------------- | --------------------------------------- |
| `children` | `Renderable`     | Tags, strings, or other rendered content. | `()`                                    |
| `in_`      | \`str            | None\`                                    | Input image reference.                  |
| `in2`      | \`str            | None\`                                    | Second input image reference.           |
| `mode`     | \`str            | None\`                                    | Blending mode.                          |
| `result`   | \`str            | None\`                                    | Result identifier.                      |
| `class_`   | \`str            | None\`                                    | Substituted as the DOM class attribute. |
| `id`       | \`str            | None\`                                    | DOM ID attribute.                       |
| `style`    | \`str            | None\`                                    | Inline style attribute.                 |
| `**kwargs` | `AttributesType` | Additional attributes.                    | `{}`                                    |

Source code in `src/air/tags/models/svg.py`

```
def __init__(
    self,
    *children: Renderable,
    in_: str | None = None,
    in2: str | None = None,
    mode: str | None = None,
    result: str | None = None,
    class_: str | None = None,
    id: str | None = None,
    style: str | None = None,
    **kwargs: AttributesType,
) -> None:
    super().__init__(*children, **kwargs | locals_cleanup(locals()))
```

## FeColorMatrix

```
FeColorMatrix(
    *children,
    in_=None,
    type=None,
    values=None,
    result=None,
    class_=None,
    id=None,
    style=None,
    **kwargs,
)
```

Bases: `CaseTag`

Applies a matrix transformation on color values

Parameters:

| Name       | Type             | Description                               | Default                                 |
| ---------- | ---------------- | ----------------------------------------- | --------------------------------------- |
| `children` | `Renderable`     | Tags, strings, or other rendered content. | `()`                                    |
| `in_`      | \`str            | None\`                                    | Input image reference.                  |
| `type`     | \`str            | None\`                                    | Matrix type (matrix                     |
| `values`   | \`str            | None\`                                    | Matrix values.                          |
| `result`   | \`str            | None\`                                    | Result identifier.                      |
| `class_`   | \`str            | None\`                                    | Substituted as the DOM class attribute. |
| `id`       | \`str            | None\`                                    | DOM ID attribute.                       |
| `style`    | \`str            | None\`                                    | Inline style attribute.                 |
| `**kwargs` | `AttributesType` | Additional attributes.                    | `{}`                                    |

Source code in `src/air/tags/models/svg.py`

```
def __init__(
    self,
    *children: Renderable,
    in_: str | None = None,
    type: str | None = None,
    values: str | None = None,
    result: str | None = None,
    class_: str | None = None,
    id: str | None = None,
    style: str | None = None,
    **kwargs: AttributesType,
) -> None:
    super().__init__(*children, **kwargs | locals_cleanup(locals()))
```

## FeComponentTransfer

```
FeComponentTransfer(
    *children,
    in_=None,
    result=None,
    class_=None,
    id=None,
    style=None,
    **kwargs,
)
```

Bases: `CaseTag`

Performs component-wise remapping of data

Parameters:

| Name       | Type             | Description                               | Default                                 |
| ---------- | ---------------- | ----------------------------------------- | --------------------------------------- |
| `children` | `Renderable`     | Tags, strings, or other rendered content. | `()`                                    |
| `in_`      | \`str            | None\`                                    | Input image reference.                  |
| `result`   | \`str            | None\`                                    | Result identifier.                      |
| `class_`   | \`str            | None\`                                    | Substituted as the DOM class attribute. |
| `id`       | \`str            | None\`                                    | DOM ID attribute.                       |
| `style`    | \`str            | None\`                                    | Inline style attribute.                 |
| `**kwargs` | `AttributesType` | Additional attributes.                    | `{}`                                    |

Source code in `src/air/tags/models/svg.py`

```
def __init__(
    self,
    *children: Renderable,
    in_: str | None = None,
    result: str | None = None,
    class_: str | None = None,
    id: str | None = None,
    style: str | None = None,
    **kwargs: AttributesType,
) -> None:
    super().__init__(*children, **kwargs | locals_cleanup(locals()))
```

## FeComposite

```
FeComposite(
    *children,
    in_=None,
    in2=None,
    operator=None,
    k1=None,
    k2=None,
    k3=None,
    k4=None,
    result=None,
    class_=None,
    id=None,
    style=None,
    **kwargs,
)
```

Bases: `CaseTag`

Performs image compositing

Parameters:

| Name       | Type             | Description                               | Default                                 |
| ---------- | ---------------- | ----------------------------------------- | --------------------------------------- |
| `children` | `Renderable`     | Tags, strings, or other rendered content. | `()`                                    |
| `in_`      | \`str            | None\`                                    | Input image reference.                  |
| `in2`      | \`str            | None\`                                    | Second input image reference.           |
| `operator` | \`str            | None\`                                    | Compositing operation.                  |
| `k1`       | \`float          | None\`                                    | Coefficient for arithmetic operation.   |
| `k2`       | \`float          | None\`                                    | Coefficient for arithmetic operation.   |
| `k3`       | \`float          | None\`                                    | Coefficient for arithmetic operation.   |
| `k4`       | \`float          | None\`                                    | Coefficient for arithmetic operation.   |
| `result`   | \`str            | None\`                                    | Result identifier.                      |
| `class_`   | \`str            | None\`                                    | Substituted as the DOM class attribute. |
| `id`       | \`str            | None\`                                    | DOM ID attribute.                       |
| `style`    | \`str            | None\`                                    | Inline style attribute.                 |
| `**kwargs` | `AttributesType` | Additional attributes.                    | `{}`                                    |

Source code in `src/air/tags/models/svg.py`

```
def __init__(
    self,
    *children: Renderable,
    in_: str | None = None,
    in2: str | None = None,
    operator: str | None = None,
    k1: float | None = None,
    k2: float | None = None,
    k3: float | None = None,
    k4: float | None = None,
    result: str | None = None,
    class_: str | None = None,
    id: str | None = None,
    style: str | None = None,
    **kwargs: AttributesType,
) -> None:
    super().__init__(*children, **kwargs | locals_cleanup(locals()))
```

## FeConvolveMatrix

```
FeConvolveMatrix(
    *children,
    in_=None,
    order=None,
    kernelMatrix=None,
    divisor=None,
    bias=None,
    targetX=None,
    targetY=None,
    edgeMode=None,
    preserveAlpha=None,
    result=None,
    class_=None,
    id=None,
    style=None,
    **kwargs,
)
```

Bases: `CaseTag`

Applies a matrix convolution filter

Parameters:

| Name            | Type             | Description                               | Default                                 |
| --------------- | ---------------- | ----------------------------------------- | --------------------------------------- |
| `children`      | `Renderable`     | Tags, strings, or other rendered content. | `()`                                    |
| `in_`           | \`str            | None\`                                    | Input image reference.                  |
| `order`         | \`str            | None\`                                    | Matrix dimensions.                      |
| `kernelMatrix`  | \`str            | None\`                                    | Matrix values.                          |
| `divisor`       | \`float          | None\`                                    | Divisor for matrix sum.                 |
| `bias`          | \`float          | None\`                                    | Bias value.                             |
| `targetX`       | \`int            | None\`                                    | Target X position.                      |
| `targetY`       | \`int            | None\`                                    | Target Y position.                      |
| `edgeMode`      | \`str            | None\`                                    | Edge handling mode.                     |
| `preserveAlpha` | \`str            | None\`                                    | Preserve alpha channel.                 |
| `result`        | \`str            | None\`                                    | Result identifier.                      |
| `class_`        | \`str            | None\`                                    | Substituted as the DOM class attribute. |
| `id`            | \`str            | None\`                                    | DOM ID attribute.                       |
| `style`         | \`str            | None\`                                    | Inline style attribute.                 |
| `**kwargs`      | `AttributesType` | Additional attributes.                    | `{}`                                    |

Source code in `src/air/tags/models/svg.py`

```
def __init__(
    self,
    *children: Renderable,
    in_: str | None = None,
    order: str | None = None,
    kernelMatrix: str | None = None,
    divisor: float | None = None,
    bias: float | None = None,
    targetX: int | None = None,
    targetY: int | None = None,
    edgeMode: str | None = None,
    preserveAlpha: str | None = None,
    result: str | None = None,
    class_: str | None = None,
    id: str | None = None,
    style: str | None = None,
    **kwargs: AttributesType,
) -> None:
    super().__init__(*children, **kwargs | locals_cleanup(locals()))
```

## FeDiffuseLighting

```
FeDiffuseLighting(
    *children,
    in_=None,
    surfaceScale=None,
    diffuseConstant=None,
    kernelUnitLength=None,
    result=None,
    class_=None,
    id=None,
    style=None,
    **kwargs,
)
```

Bases: `CaseTag`

Lights an image using diffuse lighting

Parameters:

| Name               | Type             | Description                               | Default                                 |
| ------------------ | ---------------- | ----------------------------------------- | --------------------------------------- |
| `children`         | `Renderable`     | Tags, strings, or other rendered content. | `()`                                    |
| `in_`              | \`str            | None\`                                    | Input image reference.                  |
| `surfaceScale`     | \`float          | None\`                                    | Surface height scale.                   |
| `diffuseConstant`  | \`float          | None\`                                    | Diffuse lighting constant.              |
| `kernelUnitLength` | \`str            | None\`                                    | Kernel unit length.                     |
| `result`           | \`str            | None\`                                    | Result identifier.                      |
| `class_`           | \`str            | None\`                                    | Substituted as the DOM class attribute. |
| `id`               | \`str            | None\`                                    | DOM ID attribute.                       |
| `style`            | \`str            | None\`                                    | Inline style attribute.                 |
| `**kwargs`         | `AttributesType` | Additional attributes.                    | `{}`                                    |

Source code in `src/air/tags/models/svg.py`

```
def __init__(
    self,
    *children: Renderable,
    in_: str | None = None,
    surfaceScale: float | None = None,
    diffuseConstant: float | None = None,
    kernelUnitLength: str | None = None,
    result: str | None = None,
    class_: str | None = None,
    id: str | None = None,
    style: str | None = None,
    **kwargs: AttributesType,
) -> None:
    super().__init__(*children, **kwargs | locals_cleanup(locals()))
```

## FeDisplacementMap

```
FeDisplacementMap(
    *children,
    in_=None,
    in2=None,
    scale=None,
    xChannelSelector=None,
    yChannelSelector=None,
    result=None,
    class_=None,
    id=None,
    style=None,
    **kwargs,
)
```

Bases: `CaseTag`

Displaces an image using another image

Parameters:

| Name               | Type             | Description                               | Default                                 |
| ------------------ | ---------------- | ----------------------------------------- | --------------------------------------- |
| `children`         | `Renderable`     | Tags, strings, or other rendered content. | `()`                                    |
| `in_`              | \`str            | None\`                                    | Input image reference.                  |
| `in2`              | \`str            | None\`                                    | Displacement map reference.             |
| `scale`            | \`float          | None\`                                    | Displacement scale factor.              |
| `xChannelSelector` | \`str            | None\`                                    | X displacement channel (R               |
| `yChannelSelector` | \`str            | None\`                                    | Y displacement channel (R               |
| `result`           | \`str            | None\`                                    | Result identifier.                      |
| `class_`           | \`str            | None\`                                    | Substituted as the DOM class attribute. |
| `id`               | \`str            | None\`                                    | DOM ID attribute.                       |
| `style`            | \`str            | None\`                                    | Inline style attribute.                 |
| `**kwargs`         | `AttributesType` | Additional attributes.                    | `{}`                                    |

Source code in `src/air/tags/models/svg.py`

```
def __init__(
    self,
    *children: Renderable,
    in_: str | None = None,
    in2: str | None = None,
    scale: float | None = None,
    xChannelSelector: str | None = None,
    yChannelSelector: str | None = None,
    result: str | None = None,
    class_: str | None = None,
    id: str | None = None,
    style: str | None = None,
    **kwargs: AttributesType,
) -> None:
    super().__init__(*children, **kwargs | locals_cleanup(locals()))
```

## FeDistantLight

```
FeDistantLight(
    *children,
    azimuth=None,
    elevation=None,
    class_=None,
    id=None,
    style=None,
    **kwargs,
)
```

Bases: `CaseTag`

Defines a distant light source

Parameters:

| Name        | Type             | Description                               | Default                                 |
| ----------- | ---------------- | ----------------------------------------- | --------------------------------------- |
| `children`  | `Renderable`     | Tags, strings, or other rendered content. | `()`                                    |
| `azimuth`   | \`str            | float                                     | None\`                                  |
| `elevation` | \`str            | float                                     | None\`                                  |
| `class_`    | \`str            | None\`                                    | Substituted as the DOM class attribute. |
| `id`        | \`str            | None\`                                    | DOM ID attribute.                       |
| `style`     | \`str            | None\`                                    | Inline style attribute.                 |
| `**kwargs`  | `AttributesType` | Additional attributes.                    | `{}`                                    |

Source code in `src/air/tags/models/svg.py`

```
def __init__(
    self,
    *children: Renderable,
    azimuth: str | float | None = None,
    elevation: str | float | None = None,
    class_: str | None = None,
    id: str | None = None,
    style: str | None = None,
    **kwargs: AttributesType,
) -> None:
    super().__init__(*children, **kwargs | locals_cleanup(locals()))
```

## FeDropShadow

```
FeDropShadow(
    *children,
    dx=None,
    dy=None,
    stdDeviation=None,
    flood_color=None,
    flood_opacity=None,
    class_=None,
    id=None,
    style=None,
    **kwargs,
)
```

Bases: `CaseTag`

Creates a drop shadow effect

Parameters:

| Name            | Type             | Description                               | Default                                 |
| --------------- | ---------------- | ----------------------------------------- | --------------------------------------- |
| `children`      | `Renderable`     | Tags, strings, or other rendered content. | `()`                                    |
| `dx`            | \`str            | float                                     | None\`                                  |
| `dy`            | \`str            | float                                     | None\`                                  |
| `stdDeviation`  | \`str            | float                                     | None\`                                  |
| `flood_color`   | \`str            | None\`                                    | Shadow color.                           |
| `flood_opacity` | \`str            | float                                     | None\`                                  |
| `class_`        | \`str            | None\`                                    | Substituted as the DOM class attribute. |
| `id`            | \`str            | None\`                                    | DOM ID attribute.                       |
| `style`         | \`str            | None\`                                    | Inline style attribute.                 |
| `**kwargs`      | `AttributesType` | Additional attributes.                    | `{}`                                    |

Source code in `src/air/tags/models/svg.py`

```
def __init__(
    self,
    *children: Renderable,
    dx: str | float | None = None,
    dy: str | float | None = None,
    stdDeviation: str | float | None = None,
    flood_color: str | None = None,
    flood_opacity: str | float | None = None,
    class_: str | None = None,
    id: str | None = None,
    style: str | None = None,
    **kwargs: AttributesType,
) -> None:
    super().__init__(*children, **kwargs | locals_cleanup(locals()))
```

## FeFlood

```
FeFlood(
    *children,
    flood_color=None,
    flood_opacity=None,
    result=None,
    class_=None,
    id=None,
    style=None,
    **kwargs,
)
```

Bases: `CaseTag`

Fills the filter region with a color

Parameters:

| Name            | Type             | Description                               | Default                                 |
| --------------- | ---------------- | ----------------------------------------- | --------------------------------------- |
| `children`      | `Renderable`     | Tags, strings, or other rendered content. | `()`                                    |
| `flood_color`   | \`str            | None\`                                    | Fill color.                             |
| `flood_opacity` | \`str            | float                                     | None\`                                  |
| `result`        | \`str            | None\`                                    | Result identifier.                      |
| `class_`        | \`str            | None\`                                    | Substituted as the DOM class attribute. |
| `id`            | \`str            | None\`                                    | DOM ID attribute.                       |
| `style`         | \`str            | None\`                                    | Inline style attribute.                 |
| `**kwargs`      | `AttributesType` | Additional attributes.                    | `{}`                                    |

Source code in `src/air/tags/models/svg.py`

```
def __init__(
    self,
    *children: Renderable,
    flood_color: str | None = None,
    flood_opacity: str | float | None = None,
    result: str | None = None,
    class_: str | None = None,
    id: str | None = None,
    style: str | None = None,
    **kwargs: AttributesType,
) -> None:
    super().__init__(*children, **kwargs | locals_cleanup(locals()))
```

## FeFuncA

```
FeFuncA(
    *children,
    type=None,
    tableValues=None,
    slope=None,
    intercept=None,
    amplitude=None,
    exponent=None,
    offset=None,
    class_=None,
    id=None,
    style=None,
    **kwargs,
)
```

Bases: `CaseTag`

Defines the alpha transfer function

Parameters:

| Name          | Type             | Description                               | Default                                 |
| ------------- | ---------------- | ----------------------------------------- | --------------------------------------- |
| `children`    | `Renderable`     | Tags, strings, or other rendered content. | `()`                                    |
| `type`        | \`str            | None\`                                    | Transfer function type.                 |
| `tableValues` | \`str            | None\`                                    | Lookup table values.                    |
| `slope`       | \`float          | None\`                                    | Linear function slope.                  |
| `intercept`   | \`float          | None\`                                    | Linear function intercept.              |
| `amplitude`   | \`float          | None\`                                    | Gamma function amplitude.               |
| `exponent`    | \`float          | None\`                                    | Gamma function exponent.                |
| `offset`      | \`float          | None\`                                    | Gamma function offset.                  |
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
    tableValues: str | None = None,
    slope: float | None = None,
    intercept: float | None = None,
    amplitude: float | None = None,
    exponent: float | None = None,
    offset: float | None = None,
    class_: str | None = None,
    id: str | None = None,
    style: str | None = None,
    **kwargs: AttributesType,
) -> None:
    super().__init__(*children, **kwargs | locals_cleanup(locals()))
```

## FeFuncB

```
FeFuncB(
    *children,
    type=None,
    tableValues=None,
    slope=None,
    intercept=None,
    amplitude=None,
    exponent=None,
    offset=None,
    class_=None,
    id=None,
    style=None,
    **kwargs,
)
```

Bases: `CaseTag`

Defines the blue transfer function

Parameters:

| Name          | Type             | Description                               | Default                                 |
| ------------- | ---------------- | ----------------------------------------- | --------------------------------------- |
| `children`    | `Renderable`     | Tags, strings, or other rendered content. | `()`                                    |
| `type`        | \`str            | None\`                                    | Transfer function type.                 |
| `tableValues` | \`str            | None\`                                    | Lookup table values.                    |
| `slope`       | \`float          | None\`                                    | Linear function slope.                  |
| `intercept`   | \`float          | None\`                                    | Linear function intercept.              |
| `amplitude`   | \`float          | None\`                                    | Gamma function amplitude.               |
| `exponent`    | \`float          | None\`                                    | Gamma function exponent.                |
| `offset`      | \`float          | None\`                                    | Gamma function offset.                  |
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
    tableValues: str | None = None,
    slope: float | None = None,
    intercept: float | None = None,
    amplitude: float | None = None,
    exponent: float | None = None,
    offset: float | None = None,
    class_: str | None = None,
    id: str | None = None,
    style: str | None = None,
    **kwargs: AttributesType,
) -> None:
    super().__init__(*children, **kwargs | locals_cleanup(locals()))
```

## FeFuncG

```
FeFuncG(
    *children,
    type=None,
    tableValues=None,
    slope=None,
    intercept=None,
    amplitude=None,
    exponent=None,
    offset=None,
    class_=None,
    id=None,
    style=None,
    **kwargs,
)
```

Bases: `CaseTag`

Defines the green transfer function

Parameters:

| Name          | Type             | Description                               | Default                                 |
| ------------- | ---------------- | ----------------------------------------- | --------------------------------------- |
| `children`    | `Renderable`     | Tags, strings, or other rendered content. | `()`                                    |
| `type`        | \`str            | None\`                                    | Transfer function type.                 |
| `tableValues` | \`str            | None\`                                    | Lookup table values.                    |
| `slope`       | \`float          | None\`                                    | Linear function slope.                  |
| `intercept`   | \`float          | None\`                                    | Linear function intercept.              |
| `amplitude`   | \`float          | None\`                                    | Gamma function amplitude.               |
| `exponent`    | \`float          | None\`                                    | Gamma function exponent.                |
| `offset`      | \`float          | None\`                                    | Gamma function offset.                  |
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
    tableValues: str | None = None,
    slope: float | None = None,
    intercept: float | None = None,
    amplitude: float | None = None,
    exponent: float | None = None,
    offset: float | None = None,
    class_: str | None = None,
    id: str | None = None,
    style: str | None = None,
    **kwargs: AttributesType,
) -> None:
    super().__init__(*children, **kwargs | locals_cleanup(locals()))
```

## FeFuncR

```
FeFuncR(
    *children,
    type=None,
    tableValues=None,
    slope=None,
    intercept=None,
    amplitude=None,
    exponent=None,
    offset=None,
    class_=None,
    id=None,
    style=None,
    **kwargs,
)
```

Bases: `CaseTag`

Defines the red transfer function

Parameters:

| Name          | Type             | Description                               | Default                                 |
| ------------- | ---------------- | ----------------------------------------- | --------------------------------------- |
| `children`    | `Renderable`     | Tags, strings, or other rendered content. | `()`                                    |
| `type`        | \`str            | None\`                                    | Transfer function type.                 |
| `tableValues` | \`str            | None\`                                    | Lookup table values.                    |
| `slope`       | \`float          | None\`                                    | Linear function slope.                  |
| `intercept`   | \`float          | None\`                                    | Linear function intercept.              |
| `amplitude`   | \`float          | None\`                                    | Gamma function amplitude.               |
| `exponent`    | \`float          | None\`                                    | Gamma function exponent.                |
| `offset`      | \`float          | None\`                                    | Gamma function offset.                  |
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
    tableValues: str | None = None,
    slope: float | None = None,
    intercept: float | None = None,
    amplitude: float | None = None,
    exponent: float | None = None,
    offset: float | None = None,
    class_: str | None = None,
    id: str | None = None,
    style: str | None = None,
    **kwargs: AttributesType,
) -> None:
    super().__init__(*children, **kwargs | locals_cleanup(locals()))
```

## FeGaussianBlur

```
FeGaussianBlur(
    *children,
    in_=None,
    stdDeviation=None,
    edgeMode=None,
    result=None,
    class_=None,
    id=None,
    style=None,
    **kwargs,
)
```

Bases: `CaseTag`

Applies Gaussian blur to an image

Parameters:

| Name           | Type             | Description                               | Default                                 |
| -------------- | ---------------- | ----------------------------------------- | --------------------------------------- |
| `children`     | `Renderable`     | Tags, strings, or other rendered content. | `()`                                    |
| `in_`          | \`str            | None\`                                    | Input image reference.                  |
| `stdDeviation` | \`str            | float                                     | None\`                                  |
| `edgeMode`     | \`str            | None\`                                    | Edge handling during blur.              |
| `result`       | \`str            | None\`                                    | Result identifier.                      |
| `class_`       | \`str            | None\`                                    | Substituted as the DOM class attribute. |
| `id`           | \`str            | None\`                                    | DOM ID attribute.                       |
| `style`        | \`str            | None\`                                    | Inline style attribute.                 |
| `**kwargs`     | `AttributesType` | Additional attributes.                    | `{}`                                    |

Source code in `src/air/tags/models/svg.py`

```
def __init__(
    self,
    *children: Renderable,
    in_: str | None = None,
    stdDeviation: str | float | None = None,
    edgeMode: str | None = None,
    result: str | None = None,
    class_: str | None = None,
    id: str | None = None,
    style: str | None = None,
    **kwargs: AttributesType,
) -> None:
    super().__init__(*children, **kwargs | locals_cleanup(locals()))
```

## FeImage

```
FeImage(
    *children,
    href=None,
    preserveAspectRatio=None,
    crossorigin=None,
    result=None,
    class_=None,
    id=None,
    style=None,
    **kwargs,
)
```

Bases: `CaseTag`

Refers to an external image

Parameters:

| Name                  | Type             | Description                               | Default                                 |
| --------------------- | ---------------- | ----------------------------------------- | --------------------------------------- |
| `children`            | `Renderable`     | Tags, strings, or other rendered content. | `()`                                    |
| `href`                | \`str            | None\`                                    | URL to image file.                      |
| `preserveAspectRatio` | \`str            | None\`                                    | Image scaling control.                  |
| `crossorigin`         | \`str            | None\`                                    | CORS credentials flag.                  |
| `result`              | \`str            | None\`                                    | Result identifier.                      |
| `class_`              | \`str            | None\`                                    | Substituted as the DOM class attribute. |
| `id`                  | \`str            | None\`                                    | DOM ID attribute.                       |
| `style`               | \`str            | None\`                                    | Inline style attribute.                 |
| `**kwargs`            | `AttributesType` | Additional attributes.                    | `{}`                                    |

Source code in `src/air/tags/models/svg.py`

```
def __init__(
    self,
    *children: Renderable,
    href: str | None = None,
    preserveAspectRatio: str | None = None,
    crossorigin: str | None = None,
    result: str | None = None,
    class_: str | None = None,
    id: str | None = None,
    style: str | None = None,
    **kwargs: AttributesType,
) -> None:
    super().__init__(*children, **kwargs | locals_cleanup(locals()))
```

## FeMerge

```
FeMerge(
    *children,
    result=None,
    class_=None,
    id=None,
    style=None,
    **kwargs,
)
```

Bases: `CaseTag`

Merges multiple filter nodes

Parameters:

| Name       | Type             | Description                               | Default                                 |
| ---------- | ---------------- | ----------------------------------------- | --------------------------------------- |
| `children` | `Renderable`     | Tags, strings, or other rendered content. | `()`                                    |
| `result`   | \`str            | None\`                                    | Result identifier.                      |
| `class_`   | \`str            | None\`                                    | Substituted as the DOM class attribute. |
| `id`       | \`str            | None\`                                    | DOM ID attribute.                       |
| `style`    | \`str            | None\`                                    | Inline style attribute.                 |
| `**kwargs` | `AttributesType` | Additional attributes.                    | `{}`                                    |

Source code in `src/air/tags/models/svg.py`

```
def __init__(
    self,
    *children: Renderable,
    result: str | None = None,
    class_: str | None = None,
    id: str | None = None,
    style: str | None = None,
    **kwargs: AttributesType,
) -> None:
    super().__init__(*children, **kwargs | locals_cleanup(locals()))
```

## FeMergeNode

```
FeMergeNode(
    *children,
    in_=None,
    class_=None,
    id=None,
    style=None,
    **kwargs,
)
```

Bases: `CaseTag`

Defines a node for feMerge

Parameters:

| Name       | Type             | Description                               | Default                                 |
| ---------- | ---------------- | ----------------------------------------- | --------------------------------------- |
| `children` | `Renderable`     | Tags, strings, or other rendered content. | `()`                                    |
| `in_`      | \`str            | None\`                                    | Input image reference.                  |
| `class_`   | \`str            | None\`                                    | Substituted as the DOM class attribute. |
| `id`       | \`str            | None\`                                    | DOM ID attribute.                       |
| `style`    | \`str            | None\`                                    | Inline style attribute.                 |
| `**kwargs` | `AttributesType` | Additional attributes.                    | `{}`                                    |

Source code in `src/air/tags/models/svg.py`

```
def __init__(
    self,
    *children: Renderable,
    in_: str | None = None,
    class_: str | None = None,
    id: str | None = None,
    style: str | None = None,
    **kwargs: AttributesType,
) -> None:
    super().__init__(*children, **kwargs | locals_cleanup(locals()))
```

## FeMorphology

```
FeMorphology(
    *children,
    in_=None,
    operator=None,
    radius=None,
    result=None,
    class_=None,
    id=None,
    style=None,
    **kwargs,
)
```

Bases: `CaseTag`

Applies morphological operations

Parameters:

| Name       | Type             | Description                               | Default                                 |
| ---------- | ---------------- | ----------------------------------------- | --------------------------------------- |
| `children` | `Renderable`     | Tags, strings, or other rendered content. | `()`                                    |
| `in_`      | \`str            | None\`                                    | Input image reference.                  |
| `operator` | \`str            | None\`                                    | Morphology operator (erode              |
| `radius`   | \`str            | float                                     | None\`                                  |
| `result`   | \`str            | None\`                                    | Result identifier.                      |
| `class_`   | \`str            | None\`                                    | Substituted as the DOM class attribute. |
| `id`       | \`str            | None\`                                    | DOM ID attribute.                       |
| `style`    | \`str            | None\`                                    | Inline style attribute.                 |
| `**kwargs` | `AttributesType` | Additional attributes.                    | `{}`                                    |

Source code in `src/air/tags/models/svg.py`

```
def __init__(
    self,
    *children: Renderable,
    in_: str | None = None,
    operator: str | None = None,
    radius: str | float | None = None,
    result: str | None = None,
    class_: str | None = None,
    id: str | None = None,
    style: str | None = None,
    **kwargs: AttributesType,
) -> None:
    super().__init__(*children, **kwargs | locals_cleanup(locals()))
```

## FeOffset

```
FeOffset(
    *children,
    in_=None,
    dx=None,
    dy=None,
    result=None,
    class_=None,
    id=None,
    style=None,
    **kwargs,
)
```

Bases: `CaseTag`

Offsets an image

Parameters:

| Name       | Type             | Description                               | Default                                 |
| ---------- | ---------------- | ----------------------------------------- | --------------------------------------- |
| `children` | `Renderable`     | Tags, strings, or other rendered content. | `()`                                    |
| `in_`      | \`str            | None\`                                    | Input graphic reference.                |
| `dx`       | \`str            | float                                     | None\`                                  |
| `dy`       | \`str            | float                                     | None\`                                  |
| `result`   | \`str            | None\`                                    | Result identifier.                      |
| `class_`   | \`str            | None\`                                    | Substituted as the DOM class attribute. |
| `id`       | \`str            | None\`                                    | DOM ID attribute.                       |
| `style`    | \`str            | None\`                                    | Inline style attribute.                 |
| `**kwargs` | `AttributesType` | Additional attributes.                    | `{}`                                    |

Source code in `src/air/tags/models/svg.py`

```
def __init__(
    self,
    *children: Renderable,
    in_: str | None = None,
    dx: str | float | None = None,
    dy: str | float | None = None,
    result: str | None = None,
    class_: str | None = None,
    id: str | None = None,
    style: str | None = None,
    **kwargs: AttributesType,
) -> None:
    super().__init__(*children, **kwargs | locals_cleanup(locals()))
```

## FePointLight

```
FePointLight(
    *children,
    x=None,
    y=None,
    z=None,
    class_=None,
    id=None,
    style=None,
    **kwargs,
)
```

Bases: `CaseTag`

Defines a point light source

Parameters:

| Name       | Type             | Description                               | Default                                 |
| ---------- | ---------------- | ----------------------------------------- | --------------------------------------- |
| `children` | `Renderable`     | Tags, strings, or other rendered content. | `()`                                    |
| `x`        | \`str            | float                                     | None\`                                  |
| `y`        | \`str            | float                                     | None\`                                  |
| `z`        | \`str            | float                                     | None\`                                  |
| `class_`   | \`str            | None\`                                    | Substituted as the DOM class attribute. |
| `id`       | \`str            | None\`                                    | DOM ID attribute.                       |
| `style`    | \`str            | None\`                                    | Inline style attribute.                 |
| `**kwargs` | `AttributesType` | Additional attributes.                    | `{}`                                    |

Source code in `src/air/tags/models/svg.py`

```
def __init__(
    self,
    *children: Renderable,
    x: str | float | None = None,
    y: str | float | None = None,
    z: str | float | None = None,
    class_: str | None = None,
    id: str | None = None,
    style: str | None = None,
    **kwargs: AttributesType,
) -> None:
    super().__init__(*children, **kwargs | locals_cleanup(locals()))
```

## FeSpecularLighting

```
FeSpecularLighting(
    *children,
    in_=None,
    surfaceScale=None,
    specularConstant=None,
    specularExponent=None,
    kernelUnitLength=None,
    result=None,
    class_=None,
    id=None,
    style=None,
    **kwargs,
)
```

Bases: `CaseTag`

Lights an image using specular lighting

Parameters:

| Name               | Type             | Description                               | Default                                 |
| ------------------ | ---------------- | ----------------------------------------- | --------------------------------------- |
| `children`         | `Renderable`     | Tags, strings, or other rendered content. | `()`                                    |
| `in_`              | \`str            | None\`                                    | Input image reference.                  |
| `surfaceScale`     | \`float          | None\`                                    | Surface height scale.                   |
| `specularConstant` | \`float          | None\`                                    | Specular lighting constant.             |
| `specularExponent` | \`float          | None\`                                    | Specular lighting exponent.             |
| `kernelUnitLength` | \`str            | None\`                                    | Kernel unit length.                     |
| `result`           | \`str            | None\`                                    | Result identifier.                      |
| `class_`           | \`str            | None\`                                    | Substituted as the DOM class attribute. |
| `id`               | \`str            | None\`                                    | DOM ID attribute.                       |
| `style`            | \`str            | None\`                                    | Inline style attribute.                 |
| `**kwargs`         | `AttributesType` | Additional attributes.                    | `{}`                                    |

Source code in `src/air/tags/models/svg.py`

```
def __init__(
    self,
    *children: Renderable,
    in_: str | None = None,
    surfaceScale: float | None = None,
    specularConstant: float | None = None,
    specularExponent: float | None = None,
    kernelUnitLength: str | None = None,
    result: str | None = None,
    class_: str | None = None,
    id: str | None = None,
    style: str | None = None,
    **kwargs: AttributesType,
) -> None:
    super().__init__(*children, **kwargs | locals_cleanup(locals()))
```

## FeSpotLight

```
FeSpotLight(
    *children,
    x=None,
    y=None,
    z=None,
    pointsAtX=None,
    pointsAtY=None,
    pointsAtZ=None,
    specularExponent=None,
    limitingConeAngle=None,
    class_=None,
    id=None,
    style=None,
    **kwargs,
)
```

Bases: `CaseTag`

Defines a spot light source

Parameters:

| Name                | Type             | Description                               | Default                                 |
| ------------------- | ---------------- | ----------------------------------------- | --------------------------------------- |
| `children`          | `Renderable`     | Tags, strings, or other rendered content. | `()`                                    |
| `x`                 | \`str            | float                                     | None\`                                  |
| `y`                 | \`str            | float                                     | None\`                                  |
| `z`                 | \`str            | float                                     | None\`                                  |
| `pointsAtX`         | \`str            | float                                     | None\`                                  |
| `pointsAtY`         | \`str            | float                                     | None\`                                  |
| `pointsAtZ`         | \`str            | float                                     | None\`                                  |
| `specularExponent`  | \`float          | None\`                                    | Focus control for light source.         |
| `limitingConeAngle` | \`float          | None\`                                    | Angle of spot light cone.               |
| `class_`            | \`str            | None\`                                    | Substituted as the DOM class attribute. |
| `id`                | \`str            | None\`                                    | DOM ID attribute.                       |
| `style`             | \`str            | None\`                                    | Inline style attribute.                 |
| `**kwargs`          | `AttributesType` | Additional attributes.                    | `{}`                                    |

Source code in `src/air/tags/models/svg.py`

```
def __init__(
    self,
    *children: Renderable,
    x: str | float | None = None,
    y: str | float | None = None,
    z: str | float | None = None,
    pointsAtX: str | float | None = None,
    pointsAtY: str | float | None = None,
    pointsAtZ: str | float | None = None,
    specularExponent: float | None = None,
    limitingConeAngle: float | None = None,
    class_: str | None = None,
    id: str | None = None,
    style: str | None = None,
    **kwargs: AttributesType,
) -> None:
    super().__init__(*children, **kwargs | locals_cleanup(locals()))
```

## FeTile

```
FeTile(
    *children,
    in_=None,
    result=None,
    class_=None,
    id=None,
    style=None,
    **kwargs,
)
```

Bases: `CaseTag`

Tiles an image to fill a rectangle

Parameters:

| Name       | Type             | Description                               | Default                                 |
| ---------- | ---------------- | ----------------------------------------- | --------------------------------------- |
| `children` | `Renderable`     | Tags, strings, or other rendered content. | `()`                                    |
| `in_`      | \`str            | None\`                                    | Input image reference.                  |
| `result`   | \`str            | None\`                                    | Result identifier.                      |
| `class_`   | \`str            | None\`                                    | Substituted as the DOM class attribute. |
| `id`       | \`str            | None\`                                    | DOM ID attribute.                       |
| `style`    | \`str            | None\`                                    | Inline style attribute.                 |
| `**kwargs` | `AttributesType` | Additional attributes.                    | `{}`                                    |

Source code in `src/air/tags/models/svg.py`

```
def __init__(
    self,
    *children: Renderable,
    in_: str | None = None,
    result: str | None = None,
    class_: str | None = None,
    id: str | None = None,
    style: str | None = None,
    **kwargs: AttributesType,
) -> None:
    super().__init__(*children, **kwargs | locals_cleanup(locals()))
```

## FeTurbulence

```
FeTurbulence(
    *children,
    baseFrequency=None,
    numOctaves=None,
    seed=None,
    stitchTiles=None,
    type=None,
    result=None,
    class_=None,
    id=None,
    style=None,
    **kwargs,
)
```

Bases: `CaseTag`

Creates turbulence noise

Parameters:

| Name            | Type             | Description                               | Default                                 |
| --------------- | ---------------- | ----------------------------------------- | --------------------------------------- |
| `children`      | `Renderable`     | Tags, strings, or other rendered content. | `()`                                    |
| `baseFrequency` | \`str            | float                                     | None\`                                  |
| `numOctaves`    | \`int            | None\`                                    | Number of noise octaves.                |
| `seed`          | \`float          | None\`                                    | Random seed for turbulence.             |
| `stitchTiles`   | \`str            | None\`                                    | Tile stitching mode (stitch             |
| `type`          | \`str            | None\`                                    | Turbulence type (fractalNoise           |
| `result`        | \`str            | None\`                                    | Result identifier.                      |
| `class_`        | \`str            | None\`                                    | Substituted as the DOM class attribute. |
| `id`            | \`str            | None\`                                    | DOM ID attribute.                       |
| `style`         | \`str            | None\`                                    | Inline style attribute.                 |
| `**kwargs`      | `AttributesType` | Additional attributes.                    | `{}`                                    |

Source code in `src/air/tags/models/svg.py`

```
def __init__(
    self,
    *children: Renderable,
    baseFrequency: str | float | None = None,
    numOctaves: int | None = None,
    seed: float | None = None,
    stitchTiles: str | None = None,
    type: str | None = None,
    result: str | None = None,
    class_: str | None = None,
    id: str | None = None,
    style: str | None = None,
    **kwargs: AttributesType,
) -> None:
    super().__init__(*children, **kwargs | locals_cleanup(locals()))
```

## Filter

```
Filter(
    *children,
    x=None,
    y=None,
    width=None,
    height=None,
    filterUnits=None,
    primitiveUnits=None,
    class_=None,
    id=None,
    style=None,
    **kwargs,
)
```

Bases: `CaseTag`

Defines a filter effect

Parameters:

| Name             | Type             | Description                               | Default                                 |
| ---------------- | ---------------- | ----------------------------------------- | --------------------------------------- |
| `children`       | `Renderable`     | Tags, strings, or other rendered content. | `()`                                    |
| `x`              | \`str            | float                                     | None\`                                  |
| `y`              | \`str            | float                                     | None\`                                  |
| `width`          | \`str            | float                                     | None\`                                  |
| `height`         | \`str            | float                                     | None\`                                  |
| `filterUnits`    | \`str            | None\`                                    | Coordinate system for position/size.    |
| `primitiveUnits` | \`str            | None\`                                    | Coordinate system for primitives.       |
| `class_`         | \`str            | None\`                                    | Substituted as the DOM class attribute. |
| `id`             | \`str            | None\`                                    | DOM ID attribute.                       |
| `style`          | \`str            | None\`                                    | Inline style attribute.                 |
| `**kwargs`       | `AttributesType` | Additional attributes.                    | `{}`                                    |

Source code in `src/air/tags/models/svg.py`

```
def __init__(
    self,
    *children: Renderable,
    x: str | float | None = None,
    y: str | float | None = None,
    width: str | float | None = None,
    height: str | float | None = None,
    filterUnits: str | None = None,
    primitiveUnits: str | None = None,
    class_: str | None = None,
    id: str | None = None,
    style: str | None = None,
    **kwargs: AttributesType,
) -> None:
    super().__init__(*children, **kwargs | locals_cleanup(locals()))
```

## ForeignObject

```
ForeignObject(
    *children,
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

Allows inclusion of foreign XML

Parameters:

| Name       | Type             | Description                               | Default                                 |
| ---------- | ---------------- | ----------------------------------------- | --------------------------------------- |
| `children` | `Renderable`     | Tags, strings, or other rendered content. | `()`                                    |
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

## G

```
G(*children, class_=None, id=None, style=None, **kwargs)
```

Bases: `CaseTag`

Groups SVG elements

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

## Image

```
Image(
    *children,
    x=None,
    y=None,
    width=None,
    height=None,
    href=None,
    preserveAspectRatio=None,
    crossorigin=None,
    decoding=None,
    fetchpriority=None,
    class_=None,
    id=None,
    style=None,
    **kwargs,
)
```

Bases: `CaseTag`

Embeds an image

Parameters:

| Name                  | Type             | Description                               | Default                                 |
| --------------------- | ---------------- | ----------------------------------------- | --------------------------------------- |
| `children`            | `Renderable`     | Tags, strings, or other rendered content. | `()`                                    |
| `x`                   | \`str            | float                                     | None\`                                  |
| `y`                   | \`str            | float                                     | None\`                                  |
| `width`               | \`str            | float                                     | None\`                                  |
| `height`              | \`str            | float                                     | None\`                                  |
| `href`                | \`str            | None\`                                    | URL to image file.                      |
| `preserveAspectRatio` | \`str            | None\`                                    | Image scaling control.                  |
| `crossorigin`         | \`str            | None\`                                    | CORS credentials flag.                  |
| `decoding`            | \`str            | None\`                                    | Image decoding hint.                    |
| `fetchpriority`       | \`str            | None\`                                    | Fetch priority hint (experimental).     |
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
    href: str | None = None,
    preserveAspectRatio: str | None = None,
    crossorigin: str | None = None,
    decoding: str | None = None,
    fetchpriority: str | None = None,
    class_: str | None = None,
    id: str | None = None,
    style: str | None = None,
    **kwargs: AttributesType,
) -> None:
    super().__init__(*children, **kwargs | locals_cleanup(locals()))
```

## Line

```
Line(
    *children,
    x1=None,
    y1=None,
    x2=None,
    y2=None,
    pathLength=None,
    class_=None,
    id=None,
    style=None,
    **kwargs,
)
```

Bases: `CaseTag`

Defines a line

Parameters:

| Name         | Type             | Description                               | Default                                 |
| ------------ | ---------------- | ----------------------------------------- | --------------------------------------- |
| `children`   | `Renderable`     | Tags, strings, or other rendered content. | `()`                                    |
| `x1`         | \`str            | float                                     | None\`                                  |
| `y1`         | \`str            | float                                     | None\`                                  |
| `x2`         | \`str            | float                                     | None\`                                  |
| `y2`         | \`str            | float                                     | None\`                                  |
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
    x1: str | float | None = None,
    y1: str | float | None = None,
    x2: str | float | None = None,
    y2: str | float | None = None,
    pathLength: float | None = None,
    class_: str | None = None,
    id: str | None = None,
    style: str | None = None,
    **kwargs: AttributesType,
) -> None:
    super().__init__(*children, **kwargs | locals_cleanup(locals()))
```

## LinearGradient

```
LinearGradient(
    *children,
    x1=None,
    y1=None,
    x2=None,
    y2=None,
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

Defines a linear gradient

Parameters:

| Name                | Type             | Description                               | Default                                 |
| ------------------- | ---------------- | ----------------------------------------- | --------------------------------------- |
| `children`          | `Renderable`     | Tags, strings, or other rendered content. | `()`                                    |
| `x1`                | \`str            | float                                     | None\`                                  |
| `y1`                | \`str            | float                                     | None\`                                  |
| `x2`                | \`str            | float                                     | None\`                                  |
| `y2`                | \`str            | float                                     | None\`                                  |
| `gradientUnits`     | \`str            | None\`                                    | Coordinate system.                      |
| `gradientTransform` | \`str            | None\`                                    | Additional transformation.              |
| `href`              | \`str            | None\`                                    | Reference to template gradient.         |
| `spreadMethod`      | \`str            | None\`                                    | Gradient behavior outside bounds.       |
| `class_`            | \`str            | None\`                                    | Substituted as the DOM class attribute. |
| `id`                | \`str            | None\`                                    | DOM ID attribute.                       |
| `style`             | \`str            | None\`                                    | Inline style attribute.                 |
| `**kwargs`          | `AttributesType` | Additional attributes.                    | `{}`                                    |

Source code in `src/air/tags/models/svg.py`

```
def __init__(
    self,
    *children: Renderable,
    x1: str | float | None = None,
    y1: str | float | None = None,
    x2: str | float | None = None,
    y2: str | float | None = None,
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

## Marker

```
Marker(
    *children,
    markerWidth=None,
    markerHeight=None,
    markerUnits=None,
    refX=None,
    refY=None,
    orient=None,
    viewBox=None,
    preserveAspectRatio=None,
    class_=None,
    id=None,
    style=None,
    **kwargs,
)
```

Bases: `CaseTag`

Defines a graphic for drawing on lines

Parameters:

| Name                  | Type             | Description                               | Default                                 |
| --------------------- | ---------------- | ----------------------------------------- | --------------------------------------- |
| `children`            | `Renderable`     | Tags, strings, or other rendered content. | `()`                                    |
| `markerWidth`         | \`str            | float                                     | None\`                                  |
| `markerHeight`        | \`str            | float                                     | None\`                                  |
| `markerUnits`         | \`str            | None\`                                    | Coordinate system.                      |
| `refX`                | \`str            | float                                     | None\`                                  |
| `refY`                | \`str            | float                                     | None\`                                  |
| `orient`              | \`str            | float                                     | None\`                                  |
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
    markerWidth: str | float | None = None,
    markerHeight: str | float | None = None,
    markerUnits: str | None = None,
    refX: str | float | None = None,
    refY: str | float | None = None,
    orient: str | float | None = None,
    viewBox: str | None = None,
    preserveAspectRatio: str | None = None,
    class_: str | None = None,
    id: str | None = None,
    style: str | None = None,
    **kwargs: AttributesType,
) -> None:
    super().__init__(*children, **kwargs | locals_cleanup(locals()))
```

## Mask

```
Mask(
    *children,
    x=None,
    y=None,
    width=None,
    height=None,
    maskUnits=None,
    maskContentUnits=None,
    mask_type=None,
    class_=None,
    id=None,
    style=None,
    **kwargs,
)
```

Bases: `CaseTag`

Defines a mask

Parameters:

| Name               | Type             | Description                               | Default                                 |
| ------------------ | ---------------- | ----------------------------------------- | --------------------------------------- |
| `children`         | `Renderable`     | Tags, strings, or other rendered content. | `()`                                    |
| `x`                | \`str            | float                                     | None\`                                  |
| `y`                | \`str            | float                                     | None\`                                  |
| `width`            | \`str            | float                                     | None\`                                  |
| `height`           | \`str            | float                                     | None\`                                  |
| `maskUnits`        | \`str            | None\`                                    | Coordinate system for position/size.    |
| `maskContentUnits` | \`str            | None\`                                    | Coordinate system for contents.         |
| `mask_type`        | \`str            | None\`                                    | Mask mode (alpha                        |
| `class_`           | \`str            | None\`                                    | Substituted as the DOM class attribute. |
| `id`               | \`str            | None\`                                    | DOM ID attribute.                       |
| `style`            | \`str            | None\`                                    | Inline style attribute.                 |
| `**kwargs`         | `AttributesType` | Additional attributes.                    | `{}`                                    |

Source code in `src/air/tags/models/svg.py`

```
def __init__(
    self,
    *children: Renderable,
    x: str | float | None = None,
    y: str | float | None = None,
    width: str | float | None = None,
    height: str | float | None = None,
    maskUnits: str | None = None,
    maskContentUnits: str | None = None,
    mask_type: str | None = None,
    class_: str | None = None,
    id: str | None = None,
    style: str | None = None,
    **kwargs: AttributesType,
) -> None:
    super().__init__(*children, **kwargs | locals_cleanup(locals()))
```

## Metadata

```
Metadata(
    *children, class_=None, id=None, style=None, **kwargs
)
```

Bases: `CaseTag`

Defines metadata

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

## Mpath

```
Mpath(
    *children,
    href=None,
    class_=None,
    id=None,
    style=None,
    **kwargs,
)
```

Bases: `CaseTag`

Defines a motion path

Parameters:

| Name       | Type             | Description                               | Default                                 |
| ---------- | ---------------- | ----------------------------------------- | --------------------------------------- |
| `children` | `Renderable`     | Tags, strings, or other rendered content. | `()`                                    |
| `href`     | \`str            | None\`                                    | Reference to path element.              |
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
    class_: str | None = None,
    id: str | None = None,
    style: str | None = None,
    **kwargs: AttributesType,
) -> None:
    super().__init__(*children, **kwargs | locals_cleanup(locals()))
```
