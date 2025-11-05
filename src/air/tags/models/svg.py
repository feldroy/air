"""Air is proud to provide first class SVG support. The entire SVG specification
is supported.
"""

from ..utils import locals_cleanup
from .base import AttributeType, BaseTag, Renderable


class CaseTag(BaseTag):
    """This is for case-sensitive tags like those used in SVG generation."""

    @property
    def name(self) -> str:
        return self._name[0].lower() + self._name[1:]


class A(CaseTag):
    """Defines an SVG hyperlink

    Args:
        children: Tags, strings, or other rendered content.
        href: Hyperlink target URL.
        target: Where to display linked URL (_self|_parent|_top|_blank).
        download: Instructs browser to download instead of navigate.
        hreflang: Human language of the linked URL.
        ping: Space-separated list of URLs for tracking.
        referrerpolicy: Referrer policy when fetching the URL.
        rel: Relationship to target object.
        type: MIME type of linked URL.
        class_: Substituted as the DOM `class` attribute.
        id: DOM ID attribute.
        style: Inline style attribute.
        **kwargs: Additional attributes.
    """

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
        **kwargs: AttributeType,
    ) -> None:
        super().__init__(*children, **kwargs | locals_cleanup(locals()))


class Animate(CaseTag):
    """Defines animation on an SVG element

    Args:
        children: Tags, strings, or other rendered content.
        attributeName: Target attribute to animate.
        attributeType: Type of target attribute.
        values: Values to animate through.
        dur: Total animation duration.
        repeatCount: Number of repetitions.
        repeatDur: Total duration for repeating.
        from_: Starting value (from is reserved).
        to: Ending value.
        by: Relative animation value.
        begin: Animation start time.
        end: Animation end time.
        calcMode: Interpolation mode (discrete|linear|paced|spline).
        class_: Substituted as the DOM `class` attribute.
        id: DOM ID attribute.
        style: Inline style attribute.
        **kwargs: Additional attributes.
    """

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
        **kwargs: AttributeType,
    ) -> None:
        super().__init__(*children, **kwargs | locals_cleanup(locals()))


class AnimateMotion(CaseTag):
    """Defines how an element moves along a motion path

    Args:
        children: Tags, strings, or other rendered content.
        path: Motion path using path syntax.
        keyPoints: Progress points along path (0-1 range).
        rotate: Rotation along path (Number|auto|auto-reverse).
        dur: Total animation duration.
        repeatCount: Number of repetitions.
        begin: Animation start time.
        class_: Substituted as the DOM `class` attribute.
        id: DOM ID attribute.
        style: Inline style attribute.
        **kwargs: Additional attributes.
    """

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
        **kwargs: AttributeType,
    ) -> None:
        super().__init__(*children, **kwargs | locals_cleanup(locals()))


class AnimateTransform(CaseTag):
    """Animates transform attributes on an element

    Args:
        children: Tags, strings, or other rendered content.
        type: Transformation type (rotate|scale|translate|skew).
        by: Relative animation value.
        from_: Starting transformation value.
        to: Ending transformation value.
        dur: Total animation duration.
        repeatCount: Number of repetitions.
        begin: Animation start time.
        class_: Substituted as the DOM `class` attribute.
        id: DOM ID attribute.
        style: Inline style attribute.
        **kwargs: Additional attributes.
    """

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
        **kwargs: AttributeType,
    ) -> None:
        super().__init__(*children, **kwargs | locals_cleanup(locals()))


class Circle(CaseTag):
    """Defines a circle

    Args:
        children: Tags, strings, or other rendered content.
        cx: X-coordinate of center.
        cy: Y-coordinate of center.
        r: Radius.
        pathLength: Total circumference length in user units.
        class_: Substituted as the DOM `class` attribute.
        id: DOM ID attribute.
        style: Inline style attribute.
        **kwargs: Additional attributes.
    """

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
        **kwargs: AttributeType,
    ) -> None:
        super().__init__(*children, **kwargs | locals_cleanup(locals()))


class ClipPath(CaseTag):
    """Defines a clipping path

    Args:
        children: Tags, strings, or other rendered content.
        clipPathUnits: Coordinate system (userSpaceOnUse|objectBoundingBox).
        class_: Substituted as the DOM `class` attribute.
        id: DOM ID attribute.
        style: Inline style attribute.
        **kwargs: Additional attributes.
    """

    def __init__(
        self,
        *children: Renderable,
        clipPathUnits: str | None = None,
        class_: str | None = None,
        id: str | None = None,
        style: str | None = None,
        **kwargs: AttributeType,
    ) -> None:
        super().__init__(*children, **kwargs | locals_cleanup(locals()))


class Defs(CaseTag):
    """Defines reusable objects

    Args:
        children: Tags, strings, or other rendered content.
        class_: Substituted as the DOM `class` attribute.
        id: DOM ID attribute.
        style: Inline style attribute.
        **kwargs: Additional attributes.
    """

    def __init__(
        self,
        *children: Renderable,
        class_: str | None = None,
        id: str | None = None,
        style: str | None = None,
        **kwargs: AttributeType,
    ) -> None:
        super().__init__(*children, **kwargs | locals_cleanup(locals()))


class Desc(CaseTag):
    """Defines a description of an element

    Args:
        children: Tags, strings, or other rendered content.
        class_: Substituted as the DOM `class` attribute.
        id: DOM ID attribute.
        style: Inline style attribute.
        **kwargs: Additional attributes.
    """

    def __init__(
        self,
        *children: Renderable,
        class_: str | None = None,
        id: str | None = None,
        style: str | None = None,
        **kwargs: AttributeType,
    ) -> None:
        super().__init__(*children, **kwargs | locals_cleanup(locals()))


class Ellipse(CaseTag):
    """Defines an ellipse

    Args:
        children: Tags, strings, or other rendered content.
        cx: X-coordinate of center.
        cy: Y-coordinate of center.
        rx: Horizontal radius.
        ry: Vertical radius.
        pathLength: Total path length in user units.
        class_: Substituted as the DOM `class` attribute.
        id: DOM ID attribute.
        style: Inline style attribute.
        **kwargs: Additional attributes.
    """

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
        **kwargs: AttributeType,
    ) -> None:
        super().__init__(*children, **kwargs | locals_cleanup(locals()))


class FeBlend(CaseTag):
    """Defines image blending

    Args:
        children: Tags, strings, or other rendered content.
        in_: Input image reference.
        in2: Second input image reference.
        mode: Blending mode.
        result: Result identifier.
        class_: Substituted as the DOM `class` attribute.
        id: DOM ID attribute.
        style: Inline style attribute.
        **kwargs: Additional attributes.
    """

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
        **kwargs: AttributeType,
    ) -> None:
        super().__init__(*children, **kwargs | locals_cleanup(locals()))


class FeColorMatrix(CaseTag):
    """Applies a matrix transformation on color values

    Args:
        children: Tags, strings, or other rendered content.
        in_: Input image reference.
        type: Matrix type (matrix|saturate|hueRotate|luminanceToAlpha).
        values: Matrix values.
        result: Result identifier.
        class_: Substituted as the DOM `class` attribute.
        id: DOM ID attribute.
        style: Inline style attribute.
        **kwargs: Additional attributes.
    """

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
        **kwargs: AttributeType,
    ) -> None:
        super().__init__(*children, **kwargs | locals_cleanup(locals()))


class FeComponentTransfer(CaseTag):
    """Performs component-wise remapping of data

    Args:
        children: Tags, strings, or other rendered content.
        in_: Input image reference.
        result: Result identifier.
        class_: Substituted as the DOM `class` attribute.
        id: DOM ID attribute.
        style: Inline style attribute.
        **kwargs: Additional attributes.
    """

    def __init__(
        self,
        *children: Renderable,
        in_: str | None = None,
        result: str | None = None,
        class_: str | None = None,
        id: str | None = None,
        style: str | None = None,
        **kwargs: AttributeType,
    ) -> None:
        super().__init__(*children, **kwargs | locals_cleanup(locals()))


class FeComposite(CaseTag):
    """Performs image compositing

    Args:
        children: Tags, strings, or other rendered content.
        in_: Input image reference.
        in2: Second input image reference.
        operator: Compositing operation.
        k1: Coefficient for arithmetic operation.
        k2: Coefficient for arithmetic operation.
        k3: Coefficient for arithmetic operation.
        k4: Coefficient for arithmetic operation.
        result: Result identifier.
        class_: Substituted as the DOM `class` attribute.
        id: DOM ID attribute.
        style: Inline style attribute.
        **kwargs: Additional attributes.
    """

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
        **kwargs: AttributeType,
    ) -> None:
        super().__init__(*children, **kwargs | locals_cleanup(locals()))


class FeConvolveMatrix(CaseTag):
    """Applies a matrix convolution filter

    Args:
        children: Tags, strings, or other rendered content.
        in_: Input image reference.
        order: Matrix dimensions.
        kernelMatrix: Matrix values.
        divisor: Divisor for matrix sum.
        bias: Bias value.
        targetX: Target X position.
        targetY: Target Y position.
        edgeMode: Edge handling mode.
        preserveAlpha: Preserve alpha channel.
        result: Result identifier.
        class_: Substituted as the DOM `class` attribute.
        id: DOM ID attribute.
        style: Inline style attribute.
        **kwargs: Additional attributes.
    """

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
        **kwargs: AttributeType,
    ) -> None:
        super().__init__(*children, **kwargs | locals_cleanup(locals()))


class FeDiffuseLighting(CaseTag):
    """Lights an image using diffuse lighting

    Args:
        children: Tags, strings, or other rendered content.
        in_: Input image reference.
        surfaceScale: Surface height scale.
        diffuseConstant: Diffuse lighting constant.
        kernelUnitLength: Kernel unit length.
        result: Result identifier.
        class_: Substituted as the DOM `class` attribute.
        id: DOM ID attribute.
        style: Inline style attribute.
        **kwargs: Additional attributes.
    """

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
        **kwargs: AttributeType,
    ) -> None:
        super().__init__(*children, **kwargs | locals_cleanup(locals()))


class FeDisplacementMap(CaseTag):
    """Displaces an image using another image

    Args:
        children: Tags, strings, or other rendered content.
        in_: Input image reference.
        in2: Displacement map reference.
        scale: Displacement scale factor.
        xChannelSelector: X displacement channel (R|G|B|A).
        yChannelSelector: Y displacement channel (R|G|B|A).
        result: Result identifier.
        class_: Substituted as the DOM `class` attribute.
        id: DOM ID attribute.
        style: Inline style attribute.
        **kwargs: Additional attributes.
    """

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
        **kwargs: AttributeType,
    ) -> None:
        super().__init__(*children, **kwargs | locals_cleanup(locals()))


class FeDistantLight(CaseTag):
    """Defines a distant light source

    Args:
        children: Tags, strings, or other rendered content.
        azimuth: Direction angle on XY plane (degrees).
        elevation: Direction angle from XY plane to z-axis (degrees).
        class_: Substituted as the DOM `class` attribute.
        id: DOM ID attribute.
        style: Inline style attribute.
        **kwargs: Additional attributes.
    """

    def __init__(
        self,
        *children: Renderable,
        azimuth: str | float | None = None,
        elevation: str | float | None = None,
        class_: str | None = None,
        id: str | None = None,
        style: str | None = None,
        **kwargs: AttributeType,
    ) -> None:
        super().__init__(*children, **kwargs | locals_cleanup(locals()))


class FeDropShadow(CaseTag):
    """Creates a drop shadow effect

    Args:
        children: Tags, strings, or other rendered content.
        dx: X offset of drop shadow.
        dy: Y offset of drop shadow.
        stdDeviation: Blur standard deviation.
        flood_color: Shadow color.
        flood_opacity: Shadow opacity.
        class_: Substituted as the DOM `class` attribute.
        id: DOM ID attribute.
        style: Inline style attribute.
        **kwargs: Additional attributes.
    """

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
        **kwargs: AttributeType,
    ) -> None:
        super().__init__(*children, **kwargs | locals_cleanup(locals()))


class FeFlood(CaseTag):
    """Fills the filter region with a color

    Args:
        children: Tags, strings, or other rendered content.
        flood_color: Fill color.
        flood_opacity: Fill opacity.
        result: Result identifier.
        class_: Substituted as the DOM `class` attribute.
        id: DOM ID attribute.
        style: Inline style attribute.
        **kwargs: Additional attributes.
    """

    def __init__(
        self,
        *children: Renderable,
        flood_color: str | None = None,
        flood_opacity: str | float | None = None,
        result: str | None = None,
        class_: str | None = None,
        id: str | None = None,
        style: str | None = None,
        **kwargs: AttributeType,
    ) -> None:
        super().__init__(*children, **kwargs | locals_cleanup(locals()))


class FeFuncA(CaseTag):
    """Defines the alpha transfer function

    Args:
        children: Tags, strings, or other rendered content.
        type: Transfer function type.
        tableValues: Lookup table values.
        slope: Linear function slope.
        intercept: Linear function intercept.
        amplitude: Gamma function amplitude.
        exponent: Gamma function exponent.
        offset: Gamma function offset.
        class_: Substituted as the DOM `class` attribute.
        id: DOM ID attribute.
        style: Inline style attribute.
        **kwargs: Additional attributes.
    """

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
        **kwargs: AttributeType,
    ) -> None:
        super().__init__(*children, **kwargs | locals_cleanup(locals()))


class FeFuncB(CaseTag):
    """Defines the blue transfer function

    Args:
        children: Tags, strings, or other rendered content.
        type: Transfer function type.
        tableValues: Lookup table values.
        slope: Linear function slope.
        intercept: Linear function intercept.
        amplitude: Gamma function amplitude.
        exponent: Gamma function exponent.
        offset: Gamma function offset.
        class_: Substituted as the DOM `class` attribute.
        id: DOM ID attribute.
        style: Inline style attribute.
        **kwargs: Additional attributes.
    """

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
        **kwargs: AttributeType,
    ) -> None:
        super().__init__(*children, **kwargs | locals_cleanup(locals()))


class FeFuncG(CaseTag):
    """Defines the green transfer function

    Args:
        children: Tags, strings, or other rendered content.
        type: Transfer function type.
        tableValues: Lookup table values.
        slope: Linear function slope.
        intercept: Linear function intercept.
        amplitude: Gamma function amplitude.
        exponent: Gamma function exponent.
        offset: Gamma function offset.
        class_: Substituted as the DOM `class` attribute.
        id: DOM ID attribute.
        style: Inline style attribute.
        **kwargs: Additional attributes.
    """

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
        **kwargs: AttributeType,
    ) -> None:
        super().__init__(*children, **kwargs | locals_cleanup(locals()))


class FeFuncR(CaseTag):
    """Defines the red transfer function

    Args:
        children: Tags, strings, or other rendered content.
        type: Transfer function type.
        tableValues: Lookup table values.
        slope: Linear function slope.
        intercept: Linear function intercept.
        amplitude: Gamma function amplitude.
        exponent: Gamma function exponent.
        offset: Gamma function offset.
        class_: Substituted as the DOM `class` attribute.
        id: DOM ID attribute.
        style: Inline style attribute.
        **kwargs: Additional attributes.
    """

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
        **kwargs: AttributeType,
    ) -> None:
        super().__init__(*children, **kwargs | locals_cleanup(locals()))


class FeGaussianBlur(CaseTag):
    """Applies Gaussian blur to an image

    Args:
        children: Tags, strings, or other rendered content.
        in_: Input image reference.
        stdDeviation: Blur amount using bell-curve.
        edgeMode: Edge handling during blur.
        result: Result identifier.
        class_: Substituted as the DOM `class` attribute.
        id: DOM ID attribute.
        style: Inline style attribute.
        **kwargs: Additional attributes.
    """

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
        **kwargs: AttributeType,
    ) -> None:
        super().__init__(*children, **kwargs | locals_cleanup(locals()))


class FeImage(CaseTag):
    """Refers to an external image

    Args:
        children: Tags, strings, or other rendered content.
        href: URL to image file.
        preserveAspectRatio: Image scaling control.
        crossorigin: CORS credentials flag.
        result: Result identifier.
        class_: Substituted as the DOM `class` attribute.
        id: DOM ID attribute.
        style: Inline style attribute.
        **kwargs: Additional attributes.
    """

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
        **kwargs: AttributeType,
    ) -> None:
        super().__init__(*children, **kwargs | locals_cleanup(locals()))


class FeMerge(CaseTag):
    """Merges multiple filter nodes

    Args:
        children: Tags, strings, or other rendered content.
        result: Result identifier.
        class_: Substituted as the DOM `class` attribute.
        id: DOM ID attribute.
        style: Inline style attribute.
        **kwargs: Additional attributes.
    """

    def __init__(
        self,
        *children: Renderable,
        result: str | None = None,
        class_: str | None = None,
        id: str | None = None,
        style: str | None = None,
        **kwargs: AttributeType,
    ) -> None:
        super().__init__(*children, **kwargs | locals_cleanup(locals()))


class FeMergeNode(CaseTag):
    """Defines a node for feMerge

    Args:
        children: Tags, strings, or other rendered content.
        in_: Input image reference.
        class_: Substituted as the DOM `class` attribute.
        id: DOM ID attribute.
        style: Inline style attribute.
        **kwargs: Additional attributes.
    """

    def __init__(
        self,
        *children: Renderable,
        in_: str | None = None,
        class_: str | None = None,
        id: str | None = None,
        style: str | None = None,
        **kwargs: AttributeType,
    ) -> None:
        super().__init__(*children, **kwargs | locals_cleanup(locals()))


class FeMorphology(CaseTag):
    """Applies morphological operations

    Args:
        children: Tags, strings, or other rendered content.
        in_: Input image reference.
        operator: Morphology operator (erode|dilate).
        radius: Morphology radius.
        result: Result identifier.
        class_: Substituted as the DOM `class` attribute.
        id: DOM ID attribute.
        style: Inline style attribute.
        **kwargs: Additional attributes.
    """

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
        **kwargs: AttributeType,
    ) -> None:
        super().__init__(*children, **kwargs | locals_cleanup(locals()))


class FeOffset(CaseTag):
    """Offsets an image

    Args:
        children: Tags, strings, or other rendered content.
        in_: Input graphic reference.
        dx: Horizontal offset distance.
        dy: Vertical offset distance.
        result: Result identifier.
        class_: Substituted as the DOM `class` attribute.
        id: DOM ID attribute.
        style: Inline style attribute.
        **kwargs: Additional attributes.
    """

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
        **kwargs: AttributeType,
    ) -> None:
        super().__init__(*children, **kwargs | locals_cleanup(locals()))


class FePointLight(CaseTag):
    """Defines a point light source

    Args:
        children: Tags, strings, or other rendered content.
        x: X-coordinate of light position.
        y: Y-coordinate of light position.
        z: Z-coordinate of light position.
        class_: Substituted as the DOM `class` attribute.
        id: DOM ID attribute.
        style: Inline style attribute.
        **kwargs: Additional attributes.
    """

    def __init__(
        self,
        *children: Renderable,
        x: str | float | None = None,
        y: str | float | None = None,
        z: str | float | None = None,
        class_: str | None = None,
        id: str | None = None,
        style: str | None = None,
        **kwargs: AttributeType,
    ) -> None:
        super().__init__(*children, **kwargs | locals_cleanup(locals()))


class FeSpecularLighting(CaseTag):
    """Lights an image using specular lighting

    Args:
        children: Tags, strings, or other rendered content.
        in_: Input image reference.
        surfaceScale: Surface height scale.
        specularConstant: Specular lighting constant.
        specularExponent: Specular lighting exponent.
        kernelUnitLength: Kernel unit length.
        result: Result identifier.
        class_: Substituted as the DOM `class` attribute.
        id: DOM ID attribute.
        style: Inline style attribute.
        **kwargs: Additional attributes.
    """

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
        **kwargs: AttributeType,
    ) -> None:
        super().__init__(*children, **kwargs | locals_cleanup(locals()))


class FeSpotLight(CaseTag):
    """Defines a spot light source

    Args:
        children: Tags, strings, or other rendered content.
        x: X-coordinate of light position.
        y: Y-coordinate of light position.
        z: Z-coordinate of light position.
        pointsAtX: X-coordinate of point light points at.
        pointsAtY: Y-coordinate of point light points at.
        pointsAtZ: Z-coordinate of point light points at.
        specularExponent: Focus control for light source.
        limitingConeAngle: Angle of spot light cone.
        class_: Substituted as the DOM `class` attribute.
        id: DOM ID attribute.
        style: Inline style attribute.
        **kwargs: Additional attributes.
    """

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
        **kwargs: AttributeType,
    ) -> None:
        super().__init__(*children, **kwargs | locals_cleanup(locals()))


class FeTile(CaseTag):
    """Tiles an image to fill a rectangle

    Args:
        children: Tags, strings, or other rendered content.
        in_: Input image reference.
        result: Result identifier.
        class_: Substituted as the DOM `class` attribute.
        id: DOM ID attribute.
        style: Inline style attribute.
        **kwargs: Additional attributes.
    """

    def __init__(
        self,
        *children: Renderable,
        in_: str | None = None,
        result: str | None = None,
        class_: str | None = None,
        id: str | None = None,
        style: str | None = None,
        **kwargs: AttributeType,
    ) -> None:
        super().__init__(*children, **kwargs | locals_cleanup(locals()))


class FeTurbulence(CaseTag):
    """Creates turbulence noise

    Args:
        children: Tags, strings, or other rendered content.
        baseFrequency: Base frequency for turbulence.
        numOctaves: Number of noise octaves.
        seed: Random seed for turbulence.
        stitchTiles: Tile stitching mode (stitch|noStitch).
        type: Turbulence type (fractalNoise|turbulence).
        result: Result identifier.
        class_: Substituted as the DOM `class` attribute.
        id: DOM ID attribute.
        style: Inline style attribute.
        **kwargs: Additional attributes.
    """

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
        **kwargs: AttributeType,
    ) -> None:
        super().__init__(*children, **kwargs | locals_cleanup(locals()))


class Filter(CaseTag):
    """Defines a filter effect

    Args:
        children: Tags, strings, or other rendered content.
        x: X-coordinate of filter region.
        y: Y-coordinate of filter region.
        width: Width of filter region.
        height: Height of filter region.
        filterUnits: Coordinate system for position/size.
        primitiveUnits: Coordinate system for primitives.
        class_: Substituted as the DOM `class` attribute.
        id: DOM ID attribute.
        style: Inline style attribute.
        **kwargs: Additional attributes.
    """

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
        **kwargs: AttributeType,
    ) -> None:
        super().__init__(*children, **kwargs | locals_cleanup(locals()))


class ForeignObject(CaseTag):
    """Allows inclusion of foreign XML

    Args:
        children: Tags, strings, or other rendered content.
        x: X-coordinate.
        y: Y-coordinate.
        width: Width.
        height: Height.
        class_: Substituted as the DOM `class` attribute.
        id: DOM ID attribute.
        style: Inline style attribute.
        **kwargs: Additional attributes.
    """

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
        **kwargs: AttributeType,
    ) -> None:
        super().__init__(*children, **kwargs | locals_cleanup(locals()))


class G(CaseTag):
    """Groups SVG elements

    Args:
        children: Tags, strings, or other rendered content.
        class_: Substituted as the DOM `class` attribute.
        id: DOM ID attribute.
        style: Inline style attribute.
        **kwargs: Additional attributes.
    """

    def __init__(
        self,
        *children: Renderable,
        class_: str | None = None,
        id: str | None = None,
        style: str | None = None,
        **kwargs: AttributeType,
    ) -> None:
        super().__init__(*children, **kwargs | locals_cleanup(locals()))


class Image(CaseTag):
    """Embeds an image

    Args:
        children: Tags, strings, or other rendered content.
        x: Horizontal position from origin.
        y: Vertical position from origin.
        width: Width (required).
        height: Height (required).
        href: URL to image file.
        preserveAspectRatio: Image scaling control.
        crossorigin: CORS credentials flag.
        decoding: Image decoding hint.
        fetchpriority: Fetch priority hint (experimental).
        class_: Substituted as the DOM `class` attribute.
        id: DOM ID attribute.
        style: Inline style attribute.
        **kwargs: Additional attributes.
    """

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
        **kwargs: AttributeType,
    ) -> None:
        super().__init__(*children, **kwargs | locals_cleanup(locals()))


class Line(CaseTag):
    """Defines a line

    Args:
        children: Tags, strings, or other rendered content.
        x1: X-coordinate of start point.
        y1: Y-coordinate of start point.
        x2: X-coordinate of end point.
        y2: Y-coordinate of end point.
        pathLength: Total path length in user units.
        class_: Substituted as the DOM `class` attribute.
        id: DOM ID attribute.
        style: Inline style attribute.
        **kwargs: Additional attributes.
    """

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
        **kwargs: AttributeType,
    ) -> None:
        super().__init__(*children, **kwargs | locals_cleanup(locals()))


class LinearGradient(CaseTag):
    """Defines a linear gradient

    Args:
        children: Tags, strings, or other rendered content.
        x1: X-coordinate of gradient start.
        y1: Y-coordinate of gradient start.
        x2: X-coordinate of gradient end.
        y2: Y-coordinate of gradient end.
        gradientUnits: Coordinate system.
        gradientTransform: Additional transformation.
        href: Reference to template gradient.
        spreadMethod: Gradient behavior outside bounds.
        class_: Substituted as the DOM `class` attribute.
        id: DOM ID attribute.
        style: Inline style attribute.
        **kwargs: Additional attributes.
    """

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
        **kwargs: AttributeType,
    ) -> None:
        super().__init__(*children, **kwargs | locals_cleanup(locals()))


class Marker(CaseTag):
    """Defines a graphic for drawing on lines

    Args:
        children: Tags, strings, or other rendered content.
        markerWidth: Width of marker viewport.
        markerHeight: Height of marker viewport.
        markerUnits: Coordinate system.
        refX: X reference point.
        refY: Y reference point.
        orient: Marker orientation.
        viewBox: Viewport bounds.
        preserveAspectRatio: Aspect ratio handling.
        class_: Substituted as the DOM `class` attribute.
        id: DOM ID attribute.
        style: Inline style attribute.
        **kwargs: Additional attributes.
    """

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
        **kwargs: AttributeType,
    ) -> None:
        super().__init__(*children, **kwargs | locals_cleanup(locals()))


class Mask(CaseTag):
    """Defines a mask

    Args:
        children: Tags, strings, or other rendered content.
        x: X-coordinate of top-left corner.
        y: Y-coordinate of top-left corner.
        width: Width of masking area.
        height: Height of masking area.
        maskUnits: Coordinate system for position/size.
        maskContentUnits: Coordinate system for contents.
        mask_type: Mask mode (alpha|luminance).
        class_: Substituted as the DOM `class` attribute.
        id: DOM ID attribute.
        style: Inline style attribute.
        **kwargs: Additional attributes.
    """

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
        **kwargs: AttributeType,
    ) -> None:
        super().__init__(*children, **kwargs | locals_cleanup(locals()))


class Metadata(CaseTag):
    """Defines metadata

    Args:
        children: Tags, strings, or other rendered content.
        class_: Substituted as the DOM `class` attribute.
        id: DOM ID attribute.
        style: Inline style attribute.
        **kwargs: Additional attributes.
    """

    def __init__(
        self,
        *children: Renderable,
        class_: str | None = None,
        id: str | None = None,
        style: str | None = None,
        **kwargs: AttributeType,
    ) -> None:
        super().__init__(*children, **kwargs | locals_cleanup(locals()))


class Mpath(CaseTag):
    """Defines a motion path

    Args:
        children: Tags, strings, or other rendered content.
        href: Reference to path element.
        class_: Substituted as the DOM `class` attribute.
        id: DOM ID attribute.
        style: Inline style attribute.
        **kwargs: Additional attributes.
    """

    def __init__(
        self,
        *children: Renderable,
        href: str | None = None,
        class_: str | None = None,
        id: str | None = None,
        style: str | None = None,
        **kwargs: AttributeType,
    ) -> None:
        super().__init__(*children, **kwargs | locals_cleanup(locals()))


class Path(CaseTag):
    """Defines a path

    Args:
        children: Tags, strings, or other rendered content.
        d: Path data defining the shape.
        pathLength: Total path length in user units.
        class_: Substituted as the DOM `class` attribute.
        id: DOM ID attribute.
        style: Inline style attribute.
        **kwargs: Additional attributes.
    """

    def __init__(
        self,
        *children: Renderable,
        d: str | None = None,
        pathLength: float | None = None,
        class_: str | None = None,
        id: str | None = None,
        style: str | None = None,
        **kwargs: AttributeType,
    ) -> None:
        super().__init__(*children, **kwargs | locals_cleanup(locals()))


class Pattern(CaseTag):
    """Defines a pattern

    Args:
        children: Tags, strings, or other rendered content.
        x: X-coordinate shift of pattern tile.
        y: Y-coordinate shift of pattern tile.
        width: Width of pattern tile.
        height: Height of pattern tile.
        patternUnits: Coordinate system for position/size.
        patternContentUnits: Coordinate system for contents.
        patternTransform: Additional transformation.
        href: Reference to template pattern.
        viewBox: Viewport bounds for pattern.
        preserveAspectRatio: Aspect ratio handling.
        class_: Substituted as the DOM `class` attribute.
        id: DOM ID attribute.
        style: Inline style attribute.
        **kwargs: Additional attributes.
    """

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
        **kwargs: AttributeType,
    ) -> None:
        super().__init__(*children, **kwargs | locals_cleanup(locals()))


class Polygon(CaseTag):
    """Defines a polygon

    Args:
        children: Tags, strings, or other rendered content.
        points: List of x,y coordinate pairs.
        pathLength: Total path length in user units.
        class_: Substituted as the DOM `class` attribute.
        id: DOM ID attribute.
        style: Inline style attribute.
        **kwargs: Additional attributes.
    """

    def __init__(
        self,
        *children: Renderable,
        points: str | None = None,
        pathLength: float | None = None,
        class_: str | None = None,
        id: str | None = None,
        style: str | None = None,
        **kwargs: AttributeType,
    ) -> None:
        super().__init__(*children, **kwargs | locals_cleanup(locals()))


class Polyline(CaseTag):
    """Defines a polyline

    Args:
        children: Tags, strings, or other rendered content.
        points: List of x,y coordinate pairs.
        pathLength: Total path length in user units.
        class_: Substituted as the DOM `class` attribute.
        id: DOM ID attribute.
        style: Inline style attribute.
        **kwargs: Additional attributes.
    """

    def __init__(
        self,
        *children: Renderable,
        points: str | None = None,
        pathLength: float | None = None,
        class_: str | None = None,
        id: str | None = None,
        style: str | None = None,
        **kwargs: AttributeType,
    ) -> None:
        super().__init__(*children, **kwargs | locals_cleanup(locals()))


class RadialGradient(CaseTag):
    """Defines a radial gradient

    Args:
        children: Tags, strings, or other rendered content.
        cx: X-coordinate of end circle.
        cy: Y-coordinate of end circle.
        r: Radius of end circle.
        fx: X-coordinate of start circle.
        fy: Y-coordinate of start circle.
        fr: Radius of start circle.
        gradientUnits: Coordinate system.
        gradientTransform: Additional transformation.
        href: Reference to template gradient.
        spreadMethod: Gradient behavior.
        class_: Substituted as the DOM `class` attribute.
        id: DOM ID attribute.
        style: Inline style attribute.
        **kwargs: Additional attributes.
    """

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
        **kwargs: AttributeType,
    ) -> None:
        super().__init__(*children, **kwargs | locals_cleanup(locals()))


class Rect(CaseTag):
    """Defines a rectangle

    Args:
        children: Tags, strings, or other rendered content.
        x: X-coordinate.
        y: Y-coordinate.
        width: Width.
        height: Height.
        rx: Horizontal corner radius.
        ry: Vertical corner radius.
        pathLength: Total perimeter length in user units.
        class_: Substituted as the DOM `class` attribute.
        id: DOM ID attribute.
        style: Inline style attribute.
        **kwargs: Additional attributes.
    """

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
        **kwargs: AttributeType,
    ) -> None:
        super().__init__(*children, **kwargs | locals_cleanup(locals()))


class Script(CaseTag):
    """Defines a script

    Args:
        children: Tags, strings, or other rendered content.
        type: Script MIME type.
        href: External script URL.
        crossorigin: CORS credentials flag.
        fetchpriority: Fetch priority hint (experimental).
        class_: Substituted as the DOM `class` attribute.
        id: DOM ID attribute.
        style: Inline style attribute.
        **kwargs: Additional attributes.
    """

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
        **kwargs: AttributeType,
    ) -> None:
        super().__init__(*children, **kwargs | locals_cleanup(locals()))


class Set(CaseTag):
    """Sets an attribute value

    Args:
        children: Tags, strings, or other rendered content.
        to: Value to apply for animation duration.
        attributeName: Target attribute to set.
        begin: Animation start time.
        dur: Animation duration.
        class_: Substituted as the DOM `class` attribute.
        id: DOM ID attribute.
        style: Inline style attribute.
        **kwargs: Additional attributes.
    """

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
        **kwargs: AttributeType,
    ) -> None:
        super().__init__(*children, **kwargs | locals_cleanup(locals()))


class Stop(CaseTag):
    """Defines a gradient stop

    Args:
        children: Tags, strings, or other rendered content.
        offset: Position along gradient vector.
        stop_color: Color of gradient stop.
        stop_opacity: Opacity of gradient stop.
        class_: Substituted as the DOM `class` attribute.
        id: DOM ID attribute.
        style: Inline style attribute.
        **kwargs: Additional attributes.
    """

    def __init__(
        self,
        *children: Renderable,
        offset: str | float | None = None,
        stop_color: str | None = None,
        stop_opacity: str | float | None = None,
        class_: str | None = None,
        id: str | None = None,
        style: str | None = None,
        **kwargs: AttributeType,
    ) -> None:
        super().__init__(*children, **kwargs | locals_cleanup(locals()))


class Style(CaseTag):
    """Defines style information

    Args:
        children: Tags, strings, or other rendered content.
        type: Style sheet language MIME type.
        media: Media query for when styles apply.
        class_: Substituted as the DOM `class` attribute.
        id: DOM ID attribute.
        style: Inline style attribute.
        **kwargs: Additional attributes.
    """

    def __init__(
        self,
        *children: Renderable,
        type: str | None = None,
        media: str | None = None,
        class_: str | None = None,
        id: str | None = None,
        style: str | None = None,
        **kwargs: AttributeType,
    ) -> None:
        super().__init__(*children, **kwargs | locals_cleanup(locals()))


class Svg(CaseTag):
    """Defines an SVG document fragment

    Args:
        children: Tags, strings, or other rendered content.
        width: Displayed width of viewport.
        height: Displayed height of viewport.
        x: X-coordinate of container.
        y: Y-coordinate of container.
        viewBox: SVG viewport coordinates.
        preserveAspectRatio: Aspect ratio handling.
        class_: Substituted as the DOM `class` attribute.
        id: DOM ID attribute.
        style: Inline style attribute.
        **kwargs: Additional attributes.
    """

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
        **kwargs: AttributeType,
    ) -> None:
        super().__init__(*children, **kwargs | locals_cleanup(locals()))


class Switch(CaseTag):
    """Defines conditional processing

    Args:
        children: Tags, strings, or other rendered content.
        class_: Substituted as the DOM `class` attribute.
        id: DOM ID attribute.
        style: Inline style attribute.
        **kwargs: Additional attributes.
    """

    def __init__(
        self,
        *children: Renderable,
        class_: str | None = None,
        id: str | None = None,
        style: str | None = None,
        **kwargs: AttributeType,
    ) -> None:
        super().__init__(*children, **kwargs | locals_cleanup(locals()))


class Symbol(CaseTag):
    """Defines a reusable symbol

    Args:
        children: Tags, strings, or other rendered content.
        width: Width of symbol.
        height: Height of symbol.
        x: X-coordinate.
        y: Y-coordinate.
        viewBox: Viewport bounds for symbol.
        preserveAspectRatio: Aspect ratio handling.
        refX: X reference point.
        refY: Y reference point.
        class_: Substituted as the DOM `class` attribute.
        id: DOM ID attribute.
        style: Inline style attribute.
        **kwargs: Additional attributes.
    """

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
        **kwargs: AttributeType,
    ) -> None:
        super().__init__(*children, **kwargs | locals_cleanup(locals()))


class Text(CaseTag):
    """Defines text content

    Args:
        children: Tags, strings, or other rendered content.
        x: X-coordinates of text baseline.
        y: Y-coordinates of text baseline.
        dx: Horizontal shift from previous text.
        dy: Vertical shift from previous text.
        rotate: Rotation of individual glyphs.
        lengthAdjust: Text stretching method.
        textLength: Target width for text scaling.
        class_: Substituted as the DOM `class` attribute.
        id: DOM ID attribute.
        style: Inline style attribute.
        **kwargs: Additional attributes.
    """

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
        **kwargs: AttributeType,
    ) -> None:
        super().__init__(*children, **kwargs | locals_cleanup(locals()))


class TextPath(CaseTag):
    """Defines text along a path

    Args:
        children: Tags, strings, or other rendered content.
        href: Reference to path element for text layout.
        lengthAdjust: Length adjustment method.
        method: Glyph rendering method.
        path: Path data for text layout.
        side: Which side of path to render text.
        spacing: Glyph spacing handling.
        startOffset: Offset from path beginning.
        textLength: Text rendering width.
        class_: Substituted as the DOM `class` attribute.
        id: DOM ID attribute.
        style: Inline style attribute.
        **kwargs: Additional attributes.
    """

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
        **kwargs: AttributeType,
    ) -> None:
        super().__init__(*children, **kwargs | locals_cleanup(locals()))


class Title(CaseTag):
    """Defines a title for the SVG document

    Args:
        children: Tags, strings, or other rendered content.
        class_: Substituted as the DOM `class` attribute.
        id: DOM ID attribute.
        style: Inline style attribute.
        **kwargs: Additional attributes.
    """

    def __init__(
        self,
        *children: Renderable,
        class_: str | None = None,
        id: str | None = None,
        style: str | None = None,
        **kwargs: AttributeType,
    ) -> None:
        super().__init__(*children, **kwargs | locals_cleanup(locals()))


class Tspan(CaseTag):
    """Defines a text span

    Args:
        children: Tags, strings, or other rendered content.
        x: X-coordinates of text baseline.
        y: Y-coordinates of text baseline.
        dx: Horizontal shift from previous text.
        dy: Vertical shift from previous text.
        rotate: Rotation of individual glyphs.
        lengthAdjust: Text stretching method.
        textLength: Target width for text scaling.
        class_: Substituted as the DOM `class` attribute.
        id: DOM ID attribute.
        style: Inline style attribute.
        **kwargs: Additional attributes.
    """

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
        **kwargs: AttributeType,
    ) -> None:
        super().__init__(*children, **kwargs | locals_cleanup(locals()))


class Use(CaseTag):
    """References another element

    Args:
        children: Tags, strings, or other rendered content.
        href: Reference to element to duplicate.
        x: X offset transformation.
        y: Y offset transformation.
        width: Width (only for elements with viewBox).
        height: Height (only for elements with viewBox).
        class_: Substituted as the DOM `class` attribute.
        id: DOM ID attribute.
        style: Inline style attribute.
        **kwargs: Additional attributes.
    """

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
        **kwargs: AttributeType,
    ) -> None:
        super().__init__(*children, **kwargs | locals_cleanup(locals()))


class View(CaseTag):
    """Defines a view

    Args:
        children: Tags, strings, or other rendered content.
        viewBox: Viewport bounds.
        preserveAspectRatio: Aspect ratio handling.
        class_: Substituted as the DOM `class` attribute.
        id: DOM ID attribute.
        style: Inline style attribute.
        **kwargs: Additional attributes.
    """

    def __init__(
        self,
        *children: Renderable,
        viewBox: str | None = None,
        preserveAspectRatio: str | None = None,
        class_: str | None = None,
        id: str | None = None,
        style: str | None = None,
        **kwargs: AttributeType,
    ) -> None:
        super().__init__(*children, **kwargs | locals_cleanup(locals()))
