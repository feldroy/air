"""Air is proud to provide first class SVG support. The entire SVG specification
is supported.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from air.tags.utils import locals_cleanup

from .base import BaseTag

if TYPE_CHECKING:
    from .types import AttributeType, Renderable


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
        type_: MIME type of linked URL.
        class_: Substituted as the DOM `class` attribute.
        id_: DOM ID attribute.
        style: Inline style attribute.
        **custom_attributes: Additional attributes.
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
        type_: str | None = None,
        class_: str | None = None,
        id_: str | None = None,
        style: str | None = None,
        **custom_attributes: AttributeType,
    ) -> None:
        super().__init__(*children, **custom_attributes | locals_cleanup(locals()))


class Animate(CaseTag):
    """Defines animation on an SVG element

    Args:
        children: Tags, strings, or other rendered content.
        attribute_name: Target attribute to animate.
        attribute_type: Type of target attribute.
        values: Values to animate through.
        dur: Total animation duration.
        repeat_count: Number of repetitions.
        repeat_dur: Total duration for repeating.
        from_: Starting value (from is reserved).
        to: Ending value.
        by: Relative animation value.
        begin: Animation start time.
        end: Animation end time.
        calc_mode: Interpolation mode (discrete|linear|paced|spline).
        class_: Substituted as the DOM `class` attribute.
        id_: DOM ID attribute.
        style: Inline style attribute.
        **custom_attributes: Additional attributes.
    """

    def __init__(
        self,
        *children: Renderable,
        attribute_name: str | None = None,
        attribute_type: str | None = None,
        values: str | None = None,
        dur: str | None = None,
        repeat_count: str | float | None = None,
        repeat_dur: str | None = None,
        from_: str | None = None,
        to: str | None = None,
        by: str | None = None,
        begin: str | None = None,
        end: str | None = None,
        calc_mode: str | None = None,
        class_: str | None = None,
        id_: str | None = None,
        style: str | None = None,
        **custom_attributes: AttributeType,
    ) -> None:
        super().__init__(*children, **custom_attributes | locals_cleanup(locals()))


class AnimateMotion(CaseTag):
    """Defines how an element moves along a motion path

    Args:
        children: Tags, strings, or other rendered content.
        path: Motion path using path syntax.
        key_points: Progress points along path (0-1 range).
        rotate: Rotation along path (Number|auto|auto-reverse).
        dur: Total animation duration.
        repeat_count: Number of repetitions.
        begin: Animation start time.
        class_: Substituted as the DOM `class` attribute.
        id_: DOM ID attribute.
        style: Inline style attribute.
        **custom_attributes: Additional attributes.
    """

    def __init__(
        self,
        *children: Renderable,
        path: str | None = None,
        key_points: str | None = None,
        rotate: str | float | None = None,
        dur: str | None = None,
        repeat_count: str | float | None = None,
        begin: str | None = None,
        class_: str | None = None,
        id_: str | None = None,
        style: str | None = None,
        **custom_attributes: AttributeType,
    ) -> None:
        super().__init__(*children, **custom_attributes | locals_cleanup(locals()))


class AnimateTransform(CaseTag):
    """Animates transform attributes on an element

    Args:
        children: Tags, strings, or other rendered content.
        type_: Transformation type (rotate|scale|translate|skew).
        by: Relative animation value.
        from_: Starting transformation value.
        to: Ending transformation value.
        dur: Total animation duration.
        repeat_count: Number of repetitions.
        begin: Animation start time.
        class_: Substituted as the DOM `class` attribute.
        id_: DOM ID attribute.
        style: Inline style attribute.
        **custom_attributes: Additional attributes.
    """

    def __init__(
        self,
        *children: Renderable,
        type_: str | None = None,
        by: str | None = None,
        from_: str | None = None,
        to: str | None = None,
        dur: str | None = None,
        repeat_count: str | float | None = None,
        begin: str | None = None,
        class_: str | None = None,
        id_: str | None = None,
        style: str | None = None,
        **custom_attributes: AttributeType,
    ) -> None:
        super().__init__(*children, **custom_attributes | locals_cleanup(locals()))


class Circle(CaseTag):
    """Defines a circle

    Args:
        children: Tags, strings, or other rendered content.
        cx: X-coordinate of center.
        cy: Y-coordinate of center.
        r: Radius.
        path_length: Total circumference length in user units.
        class_: Substituted as the DOM `class` attribute.
        id_: DOM ID attribute.
        style: Inline style attribute.
        **custom_attributes: Additional attributes.
    """

    def __init__(
        self,
        *children: Renderable,
        cx: str | float | None = None,
        cy: str | float | None = None,
        r: str | float | None = None,
        path_length: float | None = None,
        class_: str | None = None,
        id_: str | None = None,
        style: str | None = None,
        **custom_attributes: AttributeType,
    ) -> None:
        super().__init__(*children, **custom_attributes | locals_cleanup(locals()))


class ClipPath(CaseTag):
    """Defines a clipping path

    Args:
        children: Tags, strings, or other rendered content.
        clip_path_units: Coordinate system (userSpaceOnUse|objectBoundingBox).
        class_: Substituted as the DOM `class` attribute.
        id_: DOM ID attribute.
        style: Inline style attribute.
        **custom_attributes: Additional attributes.
    """

    def __init__(
        self,
        *children: Renderable,
        clip_path_units: str | None = None,
        class_: str | None = None,
        id_: str | None = None,
        style: str | None = None,
        **custom_attributes: AttributeType,
    ) -> None:
        super().__init__(*children, **custom_attributes | locals_cleanup(locals()))


class Defs(CaseTag):
    """Defines reusable objects

    Args:
        children: Tags, strings, or other rendered content.
        class_: Substituted as the DOM `class` attribute.
        id_: DOM ID attribute.
        style: Inline style attribute.
        **custom_attributes: Additional attributes.
    """

    def __init__(
        self,
        *children: Renderable,
        class_: str | None = None,
        id_: str | None = None,
        style: str | None = None,
        **custom_attributes: AttributeType,
    ) -> None:
        super().__init__(*children, **custom_attributes | locals_cleanup(locals()))


class Desc(CaseTag):
    """Defines a description of an element

    Args:
        children: Tags, strings, or other rendered content.
        class_: Substituted as the DOM `class` attribute.
        id_: DOM ID attribute.
        style: Inline style attribute.
        **custom_attributes: Additional attributes.
    """

    def __init__(
        self,
        *children: Renderable,
        class_: str | None = None,
        id_: str | None = None,
        style: str | None = None,
        **custom_attributes: AttributeType,
    ) -> None:
        super().__init__(*children, **custom_attributes | locals_cleanup(locals()))


class Ellipse(CaseTag):
    """Defines an ellipse

    Args:
        children: Tags, strings, or other rendered content.
        cx: X-coordinate of center.
        cy: Y-coordinate of center.
        rx: Horizontal radius.
        ry: Vertical radius.
        path_length: Total path length in user units.
        class_: Substituted as the DOM `class` attribute.
        id_: DOM ID attribute.
        style: Inline style attribute.
        **custom_attributes: Additional attributes.
    """

    def __init__(
        self,
        *children: Renderable,
        cx: str | float | None = None,
        cy: str | float | None = None,
        rx: str | float | None = None,
        ry: str | float | None = None,
        path_length: float | None = None,
        class_: str | None = None,
        id_: str | None = None,
        style: str | None = None,
        **custom_attributes: AttributeType,
    ) -> None:
        super().__init__(*children, **custom_attributes | locals_cleanup(locals()))


class FeBlend(CaseTag):
    """Defines image blending

    Args:
        children: Tags, strings, or other rendered content.
        in_: Input image reference.
        in2: Second input image reference.
        mode: Blending mode.
        result: Result identifier.
        class_: Substituted as the DOM `class` attribute.
        id_: DOM ID attribute.
        style: Inline style attribute.
        **custom_attributes: Additional attributes.
    """

    def __init__(
        self,
        *children: Renderable,
        in_: str | None = None,
        in2: str | None = None,
        mode: str | None = None,
        result: str | None = None,
        class_: str | None = None,
        id_: str | None = None,
        style: str | None = None,
        **custom_attributes: AttributeType,
    ) -> None:
        super().__init__(*children, **custom_attributes | locals_cleanup(locals()))


class FeColorMatrix(CaseTag):
    """Applies a matrix transformation on color values

    Args:
        children: Tags, strings, or other rendered content.
        in_: Input image reference.
        type_: Matrix type (matrix|saturate|hueRotate|luminanceToAlpha).
        values: Matrix values.
        result: Result identifier.
        class_: Substituted as the DOM `class` attribute.
        id_: DOM ID attribute.
        style: Inline style attribute.
        **custom_attributes: Additional attributes.
    """

    def __init__(
        self,
        *children: Renderable,
        in_: str | None = None,
        type_: str | None = None,
        values: str | None = None,
        result: str | None = None,
        class_: str | None = None,
        id_: str | None = None,
        style: str | None = None,
        **custom_attributes: AttributeType,
    ) -> None:
        super().__init__(*children, **custom_attributes | locals_cleanup(locals()))


class FeComponentTransfer(CaseTag):
    """Performs component-wise remapping of data

    Args:
        children: Tags, strings, or other rendered content.
        in_: Input image reference.
        result: Result identifier.
        class_: Substituted as the DOM `class` attribute.
        id_: DOM ID attribute.
        style: Inline style attribute.
        **custom_attributes: Additional attributes.
    """

    def __init__(
        self,
        *children: Renderable,
        in_: str | None = None,
        result: str | None = None,
        class_: str | None = None,
        id_: str | None = None,
        style: str | None = None,
        **custom_attributes: AttributeType,
    ) -> None:
        super().__init__(*children, **custom_attributes | locals_cleanup(locals()))


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
        id_: DOM ID attribute.
        style: Inline style attribute.
        **custom_attributes: Additional attributes.
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
        id_: str | None = None,
        style: str | None = None,
        **custom_attributes: AttributeType,
    ) -> None:
        super().__init__(*children, **custom_attributes | locals_cleanup(locals()))


class FeConvolveMatrix(CaseTag):
    """Applies a matrix convolution filter

    Args:
        children: Tags, strings, or other rendered content.
        in_: Input image reference.
        order: Matrix dimensions.
        kernel_matrix: Matrix values.
        divisor: Divisor for matrix sum.
        bias: Bias value.
        target_x: Target X position.
        target_y: Target Y position.
        edge_mode: Edge handling mode.
        preserve_alpha: Preserve alpha channel.
        result: Result identifier.
        class_: Substituted as the DOM `class` attribute.
        id_: DOM ID attribute.
        style: Inline style attribute.
        **custom_attributes: Additional attributes.
    """

    def __init__(
        self,
        *children: Renderable,
        in_: str | None = None,
        order: str | None = None,
        kernel_matrix: str | None = None,
        divisor: float | None = None,
        bias: float | None = None,
        target_x: int | None = None,
        target_y: int | None = None,
        edge_mode: str | None = None,
        preserve_alpha: str | None = None,
        result: str | None = None,
        class_: str | None = None,
        id_: str | None = None,
        style: str | None = None,
        **custom_attributes: AttributeType,
    ) -> None:
        super().__init__(*children, **custom_attributes | locals_cleanup(locals()))


class FeDiffuseLighting(CaseTag):
    """Lights an image using diffuse lighting

    Args:
        children: Tags, strings, or other rendered content.
        in_: Input image reference.
        surface_scale: Surface height scale.
        diffuse_constant: Diffuse lighting constant.
        kernel_unit_length: Kernel unit length.
        result: Result identifier.
        class_: Substituted as the DOM `class` attribute.
        id_: DOM ID attribute.
        style: Inline style attribute.
        **custom_attributes: Additional attributes.
    """

    def __init__(
        self,
        *children: Renderable,
        in_: str | None = None,
        surface_scale: float | None = None,
        diffuse_constant: float | None = None,
        kernel_unit_length: str | None = None,
        result: str | None = None,
        class_: str | None = None,
        id_: str | None = None,
        style: str | None = None,
        **custom_attributes: AttributeType,
    ) -> None:
        super().__init__(*children, **custom_attributes | locals_cleanup(locals()))


class FeDisplacementMap(CaseTag):
    """Displaces an image using another image

    Args:
        children: Tags, strings, or other rendered content.
        in_: Input image reference.
        in2: Displacement map reference.
        scale: Displacement scale factor.
        x_channel_selector: X displacement channel (R|G|B|A).
        y_channel_selector: Y displacement channel (R|G|B|A).
        result: Result identifier.
        class_: Substituted as the DOM `class` attribute.
        id_: DOM ID attribute.
        style: Inline style attribute.
        **custom_attributes: Additional attributes.
    """

    def __init__(
        self,
        *children: Renderable,
        in_: str | None = None,
        in2: str | None = None,
        scale: float | None = None,
        x_channel_selector: str | None = None,
        y_channel_selector: str | None = None,
        result: str | None = None,
        class_: str | None = None,
        id_: str | None = None,
        style: str | None = None,
        **custom_attributes: AttributeType,
    ) -> None:
        super().__init__(*children, **custom_attributes | locals_cleanup(locals()))


class FeDistantLight(CaseTag):
    """Defines a distant light source

    Args:
        children: Tags, strings, or other rendered content.
        azimuth: Direction angle on XY plane (degrees).
        elevation: Direction angle from XY plane to z-axis (degrees).
        class_: Substituted as the DOM `class` attribute.
        id_: DOM ID attribute.
        style: Inline style attribute.
        **custom_attributes: Additional attributes.
    """

    def __init__(
        self,
        *children: Renderable,
        azimuth: str | float | None = None,
        elevation: str | float | None = None,
        class_: str | None = None,
        id_: str | None = None,
        style: str | None = None,
        **custom_attributes: AttributeType,
    ) -> None:
        super().__init__(*children, **custom_attributes | locals_cleanup(locals()))


class FeDropShadow(CaseTag):
    """Creates a drop shadow effect

    Args:
        children: Tags, strings, or other rendered content.
        dx: X offset of drop shadow.
        dy: Y offset of drop shadow.
        std_deviation: Blur standard deviation.
        flood_color: Shadow color.
        flood_opacity: Shadow opacity.
        class_: Substituted as the DOM `class` attribute.
        id_: DOM ID attribute.
        style: Inline style attribute.
        **custom_attributes: Additional attributes.
    """

    def __init__(
        self,
        *children: Renderable,
        dx: str | float | None = None,
        dy: str | float | None = None,
        std_deviation: str | float | None = None,
        flood_color: str | None = None,
        flood_opacity: str | float | None = None,
        class_: str | None = None,
        id_: str | None = None,
        style: str | None = None,
        **custom_attributes: AttributeType,
    ) -> None:
        super().__init__(*children, **custom_attributes | locals_cleanup(locals()))


class FeFlood(CaseTag):
    """Fills the filter region with a color

    Args:
        children: Tags, strings, or other rendered content.
        flood_color: Fill color.
        flood_opacity: Fill opacity.
        result: Result identifier.
        class_: Substituted as the DOM `class` attribute.
        id_: DOM ID attribute.
        style: Inline style attribute.
        **custom_attributes: Additional attributes.
    """

    def __init__(
        self,
        *children: Renderable,
        flood_color: str | None = None,
        flood_opacity: str | float | None = None,
        result: str | None = None,
        class_: str | None = None,
        id_: str | None = None,
        style: str | None = None,
        **custom_attributes: AttributeType,
    ) -> None:
        super().__init__(*children, **custom_attributes | locals_cleanup(locals()))


class FeFuncA(CaseTag):
    """Defines the alpha transfer function

    Args:
        children: Tags, strings, or other rendered content.
        type_: Transfer function type.
        table_values: Lookup table values.
        slope: Linear function slope.
        intercept: Linear function intercept.
        amplitude: Gamma function amplitude.
        exponent: Gamma function exponent.
        offset: Gamma function offset.
        class_: Substituted as the DOM `class` attribute.
        id_: DOM ID attribute.
        style: Inline style attribute.
        **custom_attributes: Additional attributes.
    """

    def __init__(
        self,
        *children: Renderable,
        type_: str | None = None,
        table_values: str | None = None,
        slope: float | None = None,
        intercept: float | None = None,
        amplitude: float | None = None,
        exponent: float | None = None,
        offset: float | None = None,
        class_: str | None = None,
        id_: str | None = None,
        style: str | None = None,
        **custom_attributes: AttributeType,
    ) -> None:
        super().__init__(*children, **custom_attributes | locals_cleanup(locals()))


class FeFuncB(CaseTag):
    """Defines the blue transfer function

    Args:
        children: Tags, strings, or other rendered content.
        type_: Transfer function type.
        table_values: Lookup table values.
        slope: Linear function slope.
        intercept: Linear function intercept.
        amplitude: Gamma function amplitude.
        exponent: Gamma function exponent.
        offset: Gamma function offset.
        class_: Substituted as the DOM `class` attribute.
        id_: DOM ID attribute.
        style: Inline style attribute.
        **custom_attributes: Additional attributes.
    """

    def __init__(
        self,
        *children: Renderable,
        type_: str | None = None,
        table_values: str | None = None,
        slope: float | None = None,
        intercept: float | None = None,
        amplitude: float | None = None,
        exponent: float | None = None,
        offset: float | None = None,
        class_: str | None = None,
        id_: str | None = None,
        style: str | None = None,
        **custom_attributes: AttributeType,
    ) -> None:
        super().__init__(*children, **custom_attributes | locals_cleanup(locals()))


class FeFuncG(CaseTag):
    """Defines the green transfer function

    Args:
        children: Tags, strings, or other rendered content.
        type_: Transfer function type.
        table_values: Lookup table values.
        slope: Linear function slope.
        intercept: Linear function intercept.
        amplitude: Gamma function amplitude.
        exponent: Gamma function exponent.
        offset: Gamma function offset.
        class_: Substituted as the DOM `class` attribute.
        id_: DOM ID attribute.
        style: Inline style attribute.
        **custom_attributes: Additional attributes.
    """

    def __init__(
        self,
        *children: Renderable,
        type_: str | None = None,
        table_values: str | None = None,
        slope: float | None = None,
        intercept: float | None = None,
        amplitude: float | None = None,
        exponent: float | None = None,
        offset: float | None = None,
        class_: str | None = None,
        id_: str | None = None,
        style: str | None = None,
        **custom_attributes: AttributeType,
    ) -> None:
        super().__init__(*children, **custom_attributes | locals_cleanup(locals()))


class FeFuncR(CaseTag):
    """Defines the red transfer function

    Args:
        children: Tags, strings, or other rendered content.
        type_: Transfer function type.
        table_values: Lookup table values.
        slope: Linear function slope.
        intercept: Linear function intercept.
        amplitude: Gamma function amplitude.
        exponent: Gamma function exponent.
        offset: Gamma function offset.
        class_: Substituted as the DOM `class` attribute.
        id_: DOM ID attribute.
        style: Inline style attribute.
        **custom_attributes: Additional attributes.
    """

    def __init__(
        self,
        *children: Renderable,
        type_: str | None = None,
        table_values: str | None = None,
        slope: float | None = None,
        intercept: float | None = None,
        amplitude: float | None = None,
        exponent: float | None = None,
        offset: float | None = None,
        class_: str | None = None,
        id_: str | None = None,
        style: str | None = None,
        **custom_attributes: AttributeType,
    ) -> None:
        super().__init__(*children, **custom_attributes | locals_cleanup(locals()))


class FeGaussianBlur(CaseTag):
    """Applies Gaussian blur to an image

    Args:
        children: Tags, strings, or other rendered content.
        in_: Input image reference.
        std_deviation: Blur amount using bell-curve.
        edge_mode: Edge handling during blur.
        result: Result identifier.
        class_: Substituted as the DOM `class` attribute.
        id_: DOM ID attribute.
        style: Inline style attribute.
        **custom_attributes: Additional attributes.
    """

    def __init__(
        self,
        *children: Renderable,
        in_: str | None = None,
        std_deviation: str | float | None = None,
        edge_mode: str | None = None,
        result: str | None = None,
        class_: str | None = None,
        id_: str | None = None,
        style: str | None = None,
        **custom_attributes: AttributeType,
    ) -> None:
        super().__init__(*children, **custom_attributes | locals_cleanup(locals()))


class FeImage(CaseTag):
    """Refers to an external image

    Args:
        children: Tags, strings, or other rendered content.
        href: URL to image file.
        preserve_aspect_ratio: Image scaling control.
        crossorigin: CORS credentials flag.
        result: Result identifier.
        class_: Substituted as the DOM `class` attribute.
        id_: DOM ID attribute.
        style: Inline style attribute.
        **custom_attributes: Additional attributes.
    """

    def __init__(
        self,
        *children: Renderable,
        href: str | None = None,
        preserve_aspect_ratio: str | None = None,
        crossorigin: str | None = None,
        result: str | None = None,
        class_: str | None = None,
        id_: str | None = None,
        style: str | None = None,
        **custom_attributes: AttributeType,
    ) -> None:
        super().__init__(*children, **custom_attributes | locals_cleanup(locals()))


class FeMerge(CaseTag):
    """Merges multiple filter nodes

    Args:
        children: Tags, strings, or other rendered content.
        result: Result identifier.
        class_: Substituted as the DOM `class` attribute.
        id_: DOM ID attribute.
        style: Inline style attribute.
        **custom_attributes: Additional attributes.
    """

    def __init__(
        self,
        *children: Renderable,
        result: str | None = None,
        class_: str | None = None,
        id_: str | None = None,
        style: str | None = None,
        **custom_attributes: AttributeType,
    ) -> None:
        super().__init__(*children, **custom_attributes | locals_cleanup(locals()))


class FeMergeNode(CaseTag):
    """Defines a node for feMerge

    Args:
        children: Tags, strings, or other rendered content.
        in_: Input image reference.
        class_: Substituted as the DOM `class` attribute.
        id_: DOM ID attribute.
        style: Inline style attribute.
        **custom_attributes: Additional attributes.
    """

    def __init__(
        self,
        *children: Renderable,
        in_: str | None = None,
        class_: str | None = None,
        id_: str | None = None,
        style: str | None = None,
        **custom_attributes: AttributeType,
    ) -> None:
        super().__init__(*children, **custom_attributes | locals_cleanup(locals()))


class FeMorphology(CaseTag):
    """Applies morphological operations

    Args:
        children: Tags, strings, or other rendered content.
        in_: Input image reference.
        operator: Morphology operator (erode|dilate).
        radius: Morphology radius.
        result: Result identifier.
        class_: Substituted as the DOM `class` attribute.
        id_: DOM ID attribute.
        style: Inline style attribute.
        **custom_attributes: Additional attributes.
    """

    def __init__(
        self,
        *children: Renderable,
        in_: str | None = None,
        operator: str | None = None,
        radius: str | float | None = None,
        result: str | None = None,
        class_: str | None = None,
        id_: str | None = None,
        style: str | None = None,
        **custom_attributes: AttributeType,
    ) -> None:
        super().__init__(*children, **custom_attributes | locals_cleanup(locals()))


class FeOffset(CaseTag):
    """Offsets an image

    Args:
        children: Tags, strings, or other rendered content.
        in_: Input graphic reference.
        dx: Horizontal offset distance.
        dy: Vertical offset distance.
        result: Result identifier.
        class_: Substituted as the DOM `class` attribute.
        id_: DOM ID attribute.
        style: Inline style attribute.
        **custom_attributes: Additional attributes.
    """

    def __init__(
        self,
        *children: Renderable,
        in_: str | None = None,
        dx: str | float | None = None,
        dy: str | float | None = None,
        result: str | None = None,
        class_: str | None = None,
        id_: str | None = None,
        style: str | None = None,
        **custom_attributes: AttributeType,
    ) -> None:
        super().__init__(*children, **custom_attributes | locals_cleanup(locals()))


class FePointLight(CaseTag):
    """Defines a point light source

    Args:
        children: Tags, strings, or other rendered content.
        x: X-coordinate of light position.
        y: Y-coordinate of light position.
        z: Z-coordinate of light position.
        class_: Substituted as the DOM `class` attribute.
        id_: DOM ID attribute.
        style: Inline style attribute.
        **custom_attributes: Additional attributes.
    """

    def __init__(
        self,
        *children: Renderable,
        x: str | float | None = None,
        y: str | float | None = None,
        z: str | float | None = None,
        class_: str | None = None,
        id_: str | None = None,
        style: str | None = None,
        **custom_attributes: AttributeType,
    ) -> None:
        super().__init__(*children, **custom_attributes | locals_cleanup(locals()))


class FeSpecularLighting(CaseTag):
    """Lights an image using specular lighting

    Args:
        children: Tags, strings, or other rendered content.
        in_: Input image reference.
        surface_scale: Surface height scale.
        specular_constant: Specular lighting constant.
        specular_exponent: Specular lighting exponent.
        kernel_unit_length: Kernel unit length.
        result: Result identifier.
        class_: Substituted as the DOM `class` attribute.
        id_: DOM ID attribute.
        style: Inline style attribute.
        **custom_attributes: Additional attributes.
    """

    def __init__(
        self,
        *children: Renderable,
        in_: str | None = None,
        surface_scale: float | None = None,
        specular_constant: float | None = None,
        specular_exponent: float | None = None,
        kernel_unit_length: str | None = None,
        result: str | None = None,
        class_: str | None = None,
        id_: str | None = None,
        style: str | None = None,
        **custom_attributes: AttributeType,
    ) -> None:
        super().__init__(*children, **custom_attributes | locals_cleanup(locals()))


class FeSpotLight(CaseTag):
    """Defines a spot light source

    Args:
        children: Tags, strings, or other rendered content.
        x: X-coordinate of light position.
        y: Y-coordinate of light position.
        z: Z-coordinate of light position.
        points_at_x: X-coordinate of point light points at.
        points_at_y: Y-coordinate of point light points at.
        points_at_z: Z-coordinate of point light points at.
        specular_exponent: Focus control for light source.
        limiting_cone_angle: Angle of spot light cone.
        class_: Substituted as the DOM `class` attribute.
        id_: DOM ID attribute.
        style: Inline style attribute.
        **custom_attributes: Additional attributes.
    """

    def __init__(
        self,
        *children: Renderable,
        x: str | float | None = None,
        y: str | float | None = None,
        z: str | float | None = None,
        points_at_x: str | float | None = None,
        points_at_y: str | float | None = None,
        points_at_z: str | float | None = None,
        specular_exponent: float | None = None,
        limiting_cone_angle: float | None = None,
        class_: str | None = None,
        id_: str | None = None,
        style: str | None = None,
        **custom_attributes: AttributeType,
    ) -> None:
        super().__init__(*children, **custom_attributes | locals_cleanup(locals()))


class FeTile(CaseTag):
    """Tiles an image to fill a rectangle

    Args:
        children: Tags, strings, or other rendered content.
        in_: Input image reference.
        result: Result identifier.
        class_: Substituted as the DOM `class` attribute.
        id_: DOM ID attribute.
        style: Inline style attribute.
        **custom_attributes: Additional attributes.
    """

    def __init__(
        self,
        *children: Renderable,
        in_: str | None = None,
        result: str | None = None,
        class_: str | None = None,
        id_: str | None = None,
        style: str | None = None,
        **custom_attributes: AttributeType,
    ) -> None:
        super().__init__(*children, **custom_attributes | locals_cleanup(locals()))


class FeTurbulence(CaseTag):
    """Creates turbulence noise

    Args:
        children: Tags, strings, or other rendered content.
        base_frequency: Base frequency for turbulence.
        num_octaves: Number of noise octaves.
        seed: Random seed for turbulence.
        stitch_tiles: Tile stitching mode (stitch|noStitch).
        type_: Turbulence type (fractalNoise|turbulence).
        result: Result identifier.
        class_: Substituted as the DOM `class` attribute.
        id_: DOM ID attribute.
        style: Inline style attribute.
        **custom_attributes: Additional attributes.
    """

    def __init__(
        self,
        *children: Renderable,
        base_frequency: str | float | None = None,
        num_octaves: int | None = None,
        seed: float | None = None,
        stitch_tiles: str | None = None,
        type_: str | None = None,
        result: str | None = None,
        class_: str | None = None,
        id_: str | None = None,
        style: str | None = None,
        **custom_attributes: AttributeType,
    ) -> None:
        super().__init__(*children, **custom_attributes | locals_cleanup(locals()))


class Filter(CaseTag):
    """Defines a filter effect

    Args:
        children: Tags, strings, or other rendered content.
        x: X-coordinate of filter region.
        y: Y-coordinate of filter region.
        width: Width of filter region.
        height: Height of filter region.
        filter_units: Coordinate system for position/size.
        primitive_units: Coordinate system for primitives.
        class_: Substituted as the DOM `class` attribute.
        id_: DOM ID attribute.
        style: Inline style attribute.
        **custom_attributes: Additional attributes.
    """

    def __init__(
        self,
        *children: Renderable,
        x: str | float | None = None,
        y: str | float | None = None,
        width: str | float | None = None,
        height: str | float | None = None,
        filter_units: str | None = None,
        primitive_units: str | None = None,
        class_: str | None = None,
        id_: str | None = None,
        style: str | None = None,
        **custom_attributes: AttributeType,
    ) -> None:
        super().__init__(*children, **custom_attributes | locals_cleanup(locals()))


class ForeignObject(CaseTag):
    """Allows inclusion of foreign XML

    Args:
        children: Tags, strings, or other rendered content.
        x: X-coordinate.
        y: Y-coordinate.
        width: Width.
        height: Height.
        class_: Substituted as the DOM `class` attribute.
        id_: DOM ID attribute.
        style: Inline style attribute.
        **custom_attributes: Additional attributes.
    """

    def __init__(
        self,
        *children: Renderable,
        x: str | float | None = None,
        y: str | float | None = None,
        width: str | float | None = None,
        height: str | float | None = None,
        class_: str | None = None,
        id_: str | None = None,
        style: str | None = None,
        **custom_attributes: AttributeType,
    ) -> None:
        super().__init__(*children, **custom_attributes | locals_cleanup(locals()))


class G(CaseTag):
    """Groups SVG elements

    Args:
        children: Tags, strings, or other rendered content.
        class_: Substituted as the DOM `class` attribute.
        id_: DOM ID attribute.
        style: Inline style attribute.
        **custom_attributes: Additional attributes.
    """

    def __init__(
        self,
        *children: Renderable,
        class_: str | None = None,
        id_: str | None = None,
        style: str | None = None,
        **custom_attributes: AttributeType,
    ) -> None:
        super().__init__(*children, **custom_attributes | locals_cleanup(locals()))


class Image(CaseTag):
    """Embeds an image

    Args:
        children: Tags, strings, or other rendered content.
        x: Horizontal position from origin.
        y: Vertical position from origin.
        width: Width (required).
        height: Height (required).
        href: URL to image file.
        preserve_aspect_ratio: Image scaling control.
        crossorigin: CORS credentials flag.
        decoding: Image decoding hint.
        fetchpriority: Fetch priority hint (experimental).
        class_: Substituted as the DOM `class` attribute.
        id_: DOM ID attribute.
        style: Inline style attribute.
        **custom_attributes: Additional attributes.
    """

    def __init__(
        self,
        *children: Renderable,
        x: str | float | None = None,
        y: str | float | None = None,
        width: str | float | None = None,
        height: str | float | None = None,
        href: str | None = None,
        preserve_aspect_ratio: str | None = None,
        crossorigin: str | None = None,
        decoding: str | None = None,
        fetchpriority: str | None = None,
        class_: str | None = None,
        id_: str | None = None,
        style: str | None = None,
        **custom_attributes: AttributeType,
    ) -> None:
        super().__init__(*children, **custom_attributes | locals_cleanup(locals()))


class Line(CaseTag):
    """Defines a line

    Args:
        children: Tags, strings, or other rendered content.
        x1: X-coordinate of start point.
        y1: Y-coordinate of start point.
        x2: X-coordinate of end point.
        y2: Y-coordinate of end point.
        path_length: Total path length in user units.
        class_: Substituted as the DOM `class` attribute.
        id_: DOM ID attribute.
        style: Inline style attribute.
        **custom_attributes: Additional attributes.
    """

    def __init__(
        self,
        *children: Renderable,
        x1: str | float | None = None,
        y1: str | float | None = None,
        x2: str | float | None = None,
        y2: str | float | None = None,
        path_length: float | None = None,
        class_: str | None = None,
        id_: str | None = None,
        style: str | None = None,
        **custom_attributes: AttributeType,
    ) -> None:
        super().__init__(*children, **custom_attributes | locals_cleanup(locals()))


class LinearGradient(CaseTag):
    """Defines a linear gradient

    Args:
        children: Tags, strings, or other rendered content.
        x1: X-coordinate of gradient start.
        y1: Y-coordinate of gradient start.
        x2: X-coordinate of gradient end.
        y2: Y-coordinate of gradient end.
        gradient_units: Coordinate system.
        gradient_transform: Additional transformation.
        href: Reference to template gradient.
        spread_method: Gradient behavior outside bounds.
        class_: Substituted as the DOM `class` attribute.
        id_: DOM ID attribute.
        style: Inline style attribute.
        **custom_attributes: Additional attributes.
    """

    def __init__(
        self,
        *children: Renderable,
        x1: str | float | None = None,
        y1: str | float | None = None,
        x2: str | float | None = None,
        y2: str | float | None = None,
        gradient_units: str | None = None,
        gradient_transform: str | None = None,
        href: str | None = None,
        spread_method: str | None = None,
        class_: str | None = None,
        id_: str | None = None,
        style: str | None = None,
        **custom_attributes: AttributeType,
    ) -> None:
        super().__init__(*children, **custom_attributes | locals_cleanup(locals()))


class Marker(CaseTag):
    """Defines a graphic for drawing on lines

    Args:
        children: Tags, strings, or other rendered content.
        marker_width: Width of marker viewport.
        marker_height: Height of marker viewport.
        marker_units: Coordinate system.
        ref_x: X reference point.
        ref_y: Y reference point.
        orient: Marker orientation.
        view_box: Viewport bounds.
        preserve_aspect_ratio: Aspect ratio handling.
        class_: Substituted as the DOM `class` attribute.
        id_: DOM ID attribute.
        style: Inline style attribute.
        **custom_attributes: Additional attributes.
    """

    def __init__(
        self,
        *children: Renderable,
        marker_width: str | float | None = None,
        marker_height: str | float | None = None,
        marker_units: str | None = None,
        ref_x: str | float | None = None,
        ref_y: str | float | None = None,
        orient: str | float | None = None,
        view_box: str | None = None,
        preserve_aspect_ratio: str | None = None,
        class_: str | None = None,
        id_: str | None = None,
        style: str | None = None,
        **custom_attributes: AttributeType,
    ) -> None:
        super().__init__(*children, **custom_attributes | locals_cleanup(locals()))


class Mask(CaseTag):
    """Defines a mask

    Args:
        children: Tags, strings, or other rendered content.
        x: X-coordinate of top-left corner.
        y: Y-coordinate of top-left corner.
        width: Width of masking area.
        height: Height of masking area.
        mask_units: Coordinate system for position/size.
        mask_content_units: Coordinate system for contents.
        mask_type: Mask mode (alpha|luminance).
        class_: Substituted as the DOM `class` attribute.
        id_: DOM ID attribute.
        style: Inline style attribute.
        **custom_attributes: Additional attributes.
    """

    def __init__(
        self,
        *children: Renderable,
        x: str | float | None = None,
        y: str | float | None = None,
        width: str | float | None = None,
        height: str | float | None = None,
        mask_units: str | None = None,
        mask_content_units: str | None = None,
        mask_type: str | None = None,
        class_: str | None = None,
        id_: str | None = None,
        style: str | None = None,
        **custom_attributes: AttributeType,
    ) -> None:
        super().__init__(*children, **custom_attributes | locals_cleanup(locals()))


class Metadata(CaseTag):
    """Defines metadata

    Args:
        children: Tags, strings, or other rendered content.
        class_: Substituted as the DOM `class` attribute.
        id_: DOM ID attribute.
        style: Inline style attribute.
        **custom_attributes: Additional attributes.
    """

    def __init__(
        self,
        *children: Renderable,
        class_: str | None = None,
        id_: str | None = None,
        style: str | None = None,
        **custom_attributes: AttributeType,
    ) -> None:
        super().__init__(*children, **custom_attributes | locals_cleanup(locals()))


class Mpath(CaseTag):
    """Defines a motion path

    Args:
        children: Tags, strings, or other rendered content.
        href: Reference to path element.
        class_: Substituted as the DOM `class` attribute.
        id_: DOM ID attribute.
        style: Inline style attribute.
        **custom_attributes: Additional attributes.
    """

    def __init__(
        self,
        *children: Renderable,
        href: str | None = None,
        class_: str | None = None,
        id_: str | None = None,
        style: str | None = None,
        **custom_attributes: AttributeType,
    ) -> None:
        super().__init__(*children, **custom_attributes | locals_cleanup(locals()))


class Path(CaseTag):
    """Defines a path

    Args:
        children: Tags, strings, or other rendered content.
        d: Path data defining the shape.
        path_length: Total path length in user units.
        class_: Substituted as the DOM `class` attribute.
        id_: DOM ID attribute.
        style: Inline style attribute.
        **custom_attributes: Additional attributes.
    """

    def __init__(
        self,
        *children: Renderable,
        d: str | None = None,
        path_length: float | None = None,
        class_: str | None = None,
        id_: str | None = None,
        style: str | None = None,
        **custom_attributes: AttributeType,
    ) -> None:
        super().__init__(*children, **custom_attributes | locals_cleanup(locals()))


class Pattern(CaseTag):
    """Defines a pattern

    Args:
        children: Tags, strings, or other rendered content.
        x: X-coordinate shift of pattern tile.
        y: Y-coordinate shift of pattern tile.
        width: Width of pattern tile.
        height: Height of pattern tile.
        pattern_units: Coordinate system for position/size.
        pattern_content_units: Coordinate system for contents.
        pattern_transform: Additional transformation.
        href: Reference to template pattern.
        view_box: Viewport bounds for pattern.
        preserve_aspect_ratio: Aspect ratio handling.
        class_: Substituted as the DOM `class` attribute.
        id_: DOM ID attribute.
        style: Inline style attribute.
        **custom_attributes: Additional attributes.
    """

    def __init__(
        self,
        *children: Renderable,
        x: str | float | None = None,
        y: str | float | None = None,
        width: str | float | None = None,
        height: str | float | None = None,
        pattern_units: str | None = None,
        pattern_content_units: str | None = None,
        pattern_transform: str | None = None,
        href: str | None = None,
        view_box: str | None = None,
        preserve_aspect_ratio: str | None = None,
        class_: str | None = None,
        id_: str | None = None,
        style: str | None = None,
        **custom_attributes: AttributeType,
    ) -> None:
        super().__init__(*children, **custom_attributes | locals_cleanup(locals()))


class Polygon(CaseTag):
    """Defines a polygon

    Args:
        children: Tags, strings, or other rendered content.
        points: List of x,y coordinate pairs.
        path_length: Total path length in user units.
        class_: Substituted as the DOM `class` attribute.
        id_: DOM ID attribute.
        style: Inline style attribute.
        **custom_attributes: Additional attributes.
    """

    def __init__(
        self,
        *children: Renderable,
        points: str | None = None,
        path_length: float | None = None,
        class_: str | None = None,
        id_: str | None = None,
        style: str | None = None,
        **custom_attributes: AttributeType,
    ) -> None:
        super().__init__(*children, **custom_attributes | locals_cleanup(locals()))


class Polyline(CaseTag):
    """Defines a polyline

    Args:
        children: Tags, strings, or other rendered content.
        points: List of x,y coordinate pairs.
        path_length: Total path length in user units.
        class_: Substituted as the DOM `class` attribute.
        id_: DOM ID attribute.
        style: Inline style attribute.
        **custom_attributes: Additional attributes.
    """

    def __init__(
        self,
        *children: Renderable,
        points: str | None = None,
        path_length: float | None = None,
        class_: str | None = None,
        id_: str | None = None,
        style: str | None = None,
        **custom_attributes: AttributeType,
    ) -> None:
        super().__init__(*children, **custom_attributes | locals_cleanup(locals()))


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
        gradient_units: Coordinate system.
        gradient_transform: Additional transformation.
        href: Reference to template gradient.
        spread_method: Gradient behavior.
        class_: Substituted as the DOM `class` attribute.
        id_: DOM ID attribute.
        style: Inline style attribute.
        **custom_attributes: Additional attributes.
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
        gradient_units: str | None = None,
        gradient_transform: str | None = None,
        href: str | None = None,
        spread_method: str | None = None,
        class_: str | None = None,
        id_: str | None = None,
        style: str | None = None,
        **custom_attributes: AttributeType,
    ) -> None:
        super().__init__(*children, **custom_attributes | locals_cleanup(locals()))


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
        path_length: Total perimeter length in user units.
        class_: Substituted as the DOM `class` attribute.
        id_: DOM ID attribute.
        style: Inline style attribute.
        **custom_attributes: Additional attributes.
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
        path_length: float | None = None,
        class_: str | None = None,
        id_: str | None = None,
        style: str | None = None,
        **custom_attributes: AttributeType,
    ) -> None:
        super().__init__(*children, **custom_attributes | locals_cleanup(locals()))


class Script(CaseTag):
    """Defines a script

    Args:
        children: Tags, strings, or other rendered content.
        type_: Script MIME type.
        href: External script URL.
        crossorigin: CORS credentials flag.
        fetchpriority: Fetch priority hint (experimental).
        class_: Substituted as the DOM `class` attribute.
        id_: DOM ID attribute.
        style: Inline style attribute.
        **custom_attributes: Additional attributes.
    """

    def __init__(
        self,
        *children: Renderable,
        type_: str | None = None,
        href: str | None = None,
        crossorigin: str | None = None,
        fetchpriority: str | None = None,
        class_: str | None = None,
        id_: str | None = None,
        style: str | None = None,
        **custom_attributes: AttributeType,
    ) -> None:
        super().__init__(*children, **custom_attributes | locals_cleanup(locals()))


class Set(CaseTag):
    """Sets an attribute value

    Args:
        children: Tags, strings, or other rendered content.
        to: Value to apply for animation duration.
        attribute_name: Target attribute to set.
        begin: Animation start time.
        dur: Animation duration.
        class_: Substituted as the DOM `class` attribute.
        id_: DOM ID attribute.
        style: Inline style attribute.
        **custom_attributes: Additional attributes.
    """

    def __init__(
        self,
        *children: Renderable,
        to: str | None = None,
        attribute_name: str | None = None,
        begin: str | None = None,
        dur: str | None = None,
        class_: str | None = None,
        id_: str | None = None,
        style: str | None = None,
        **custom_attributes: AttributeType,
    ) -> None:
        super().__init__(*children, **custom_attributes | locals_cleanup(locals()))


class Stop(CaseTag):
    """Defines a gradient stop

    Args:
        children: Tags, strings, or other rendered content.
        offset: Position along gradient vector.
        stop_color: Color of gradient stop.
        stop_opacity: Opacity of gradient stop.
        class_: Substituted as the DOM `class` attribute.
        id_: DOM ID attribute.
        style: Inline style attribute.
        **custom_attributes: Additional attributes.
    """

    def __init__(
        self,
        *children: Renderable,
        offset: str | float | None = None,
        stop_color: str | None = None,
        stop_opacity: str | float | None = None,
        class_: str | None = None,
        id_: str | None = None,
        style: str | None = None,
        **custom_attributes: AttributeType,
    ) -> None:
        super().__init__(*children, **custom_attributes | locals_cleanup(locals()))


class Style(CaseTag):
    """Defines style information

    Args:
        children: Tags, strings, or other rendered content.
        type_: Style sheet language MIME type.
        media: Media query for when styles apply.
        class_: Substituted as the DOM `class` attribute.
        id_: DOM ID attribute.
        style: Inline style attribute.
        **custom_attributes: Additional attributes.
    """

    def __init__(
        self,
        *children: Renderable,
        type_: str | None = None,
        media: str | None = None,
        class_: str | None = None,
        id_: str | None = None,
        style: str | None = None,
        **custom_attributes: AttributeType,
    ) -> None:
        super().__init__(*children, **custom_attributes | locals_cleanup(locals()))


class Svg(CaseTag):
    """Defines an SVG document fragment

    Args:
        children: Tags, strings, or other rendered content.
        width: Displayed width of viewport.
        height: Displayed height of viewport.
        x: X-coordinate of container.
        y: Y-coordinate of container.
        view_box: SVG viewport coordinates.
        preserve_aspect_ratio: Aspect ratio handling.
        class_: Substituted as the DOM `class` attribute.
        id_: DOM ID attribute.
        style: Inline style attribute.
        **custom_attributes: Additional attributes.
    """

    def __init__(
        self,
        *children: Renderable,
        width: str | float | None = None,
        height: str | float | None = None,
        x: str | float | None = None,
        y: str | float | None = None,
        view_box: str | None = None,
        preserve_aspect_ratio: str | None = None,
        class_: str | None = None,
        id_: str | None = None,
        style: str | None = None,
        **custom_attributes: AttributeType,
    ) -> None:
        super().__init__(*children, **custom_attributes | locals_cleanup(locals()))


class Switch(CaseTag):
    """Defines conditional processing

    Args:
        children: Tags, strings, or other rendered content.
        class_: Substituted as the DOM `class` attribute.
        id_: DOM ID attribute.
        style: Inline style attribute.
        **custom_attributes: Additional attributes.
    """

    def __init__(
        self,
        *children: Renderable,
        class_: str | None = None,
        id_: str | None = None,
        style: str | None = None,
        **custom_attributes: AttributeType,
    ) -> None:
        super().__init__(*children, **custom_attributes | locals_cleanup(locals()))


class Symbol(CaseTag):
    """Defines a reusable symbol

    Args:
        children: Tags, strings, or other rendered content.
        width: Width of symbol.
        height: Height of symbol.
        x: X-coordinate.
        y: Y-coordinate.
        view_box: Viewport bounds for symbol.
        preserve_aspect_ratio: Aspect ratio handling.
        ref_x: X reference point.
        ref_y: Y reference point.
        class_: Substituted as the DOM `class` attribute.
        id_: DOM ID attribute.
        style: Inline style attribute.
        **custom_attributes: Additional attributes.
    """

    def __init__(
        self,
        *children: Renderable,
        width: str | float | None = None,
        height: str | float | None = None,
        x: str | float | None = None,
        y: str | float | None = None,
        view_box: str | None = None,
        preserve_aspect_ratio: str | None = None,
        ref_x: str | float | None = None,
        ref_y: str | float | None = None,
        class_: str | None = None,
        id_: str | None = None,
        style: str | None = None,
        **custom_attributes: AttributeType,
    ) -> None:
        super().__init__(*children, **custom_attributes | locals_cleanup(locals()))


class Text(CaseTag):
    """Defines text content

    Args:
        children: Tags, strings, or other rendered content.
        x: X-coordinates of text baseline.
        y: Y-coordinates of text baseline.
        dx: Horizontal shift from previous text.
        dy: Vertical shift from previous text.
        rotate: Rotation of individual glyphs.
        length_adjust: Text stretching method.
        text_length: Target width for text scaling.
        class_: Substituted as the DOM `class` attribute.
        id_: DOM ID attribute.
        style: Inline style attribute.
        **custom_attributes: Additional attributes.
    """

    def __init__(
        self,
        *children: Renderable,
        x: str | float | None = None,
        y: str | float | None = None,
        dx: str | float | None = None,
        dy: str | float | None = None,
        rotate: str | None = None,
        length_adjust: str | None = None,
        text_length: str | float | None = None,
        class_: str | None = None,
        id_: str | None = None,
        style: str | None = None,
        **custom_attributes: AttributeType,
    ) -> None:
        super().__init__(*children, **custom_attributes | locals_cleanup(locals()))


class TextPath(CaseTag):
    """Defines text along a path

    Args:
        children: Tags, strings, or other rendered content.
        href: Reference to path element for text layout.
        length_adjust: Length adjustment method.
        method: Glyph rendering method.
        path: Path data for text layout.
        side: Which side of path to render text.
        spacing: Glyph spacing handling.
        start_offset: Offset from path beginning.
        text_length: Text rendering width.
        class_: Substituted as the DOM `class` attribute.
        id_: DOM ID attribute.
        style: Inline style attribute.
        **custom_attributes: Additional attributes.
    """

    def __init__(
        self,
        *children: Renderable,
        href: str | None = None,
        length_adjust: str | None = None,
        method: str | None = None,
        path: str | None = None,
        side: str | None = None,
        spacing: str | None = None,
        start_offset: str | float | None = None,
        text_length: str | float | None = None,
        class_: str | None = None,
        id_: str | None = None,
        style: str | None = None,
        **custom_attributes: AttributeType,
    ) -> None:
        super().__init__(*children, **custom_attributes | locals_cleanup(locals()))


class Title(CaseTag):
    """Defines a title for the SVG document

    Args:
        children: Tags, strings, or other rendered content.
        class_: Substituted as the DOM `class` attribute.
        id_: DOM ID attribute.
        style: Inline style attribute.
        **custom_attributes: Additional attributes.
    """

    def __init__(
        self,
        *children: Renderable,
        class_: str | None = None,
        id_: str | None = None,
        style: str | None = None,
        **custom_attributes: AttributeType,
    ) -> None:
        super().__init__(*children, **custom_attributes | locals_cleanup(locals()))


class Tspan(CaseTag):
    """Defines a text span

    Args:
        children: Tags, strings, or other rendered content.
        x: X-coordinates of text baseline.
        y: Y-coordinates of text baseline.
        dx: Horizontal shift from previous text.
        dy: Vertical shift from previous text.
        rotate: Rotation of individual glyphs.
        length_adjust: Text stretching method.
        text_length: Target width for text scaling.
        class_: Substituted as the DOM `class` attribute.
        id_: DOM ID attribute.
        style: Inline style attribute.
        **custom_attributes: Additional attributes.
    """

    def __init__(
        self,
        *children: Renderable,
        x: str | float | None = None,
        y: str | float | None = None,
        dx: str | float | None = None,
        dy: str | float | None = None,
        rotate: str | None = None,
        length_adjust: str | None = None,
        text_length: str | float | None = None,
        class_: str | None = None,
        id_: str | None = None,
        style: str | None = None,
        **custom_attributes: AttributeType,
    ) -> None:
        super().__init__(*children, **custom_attributes | locals_cleanup(locals()))


class Use(CaseTag):
    """References another element

    Args:
        children: Tags, strings, or other rendered content.
        href: Reference to element to duplicate.
        x: X offset transformation.
        y: Y offset transformation.
        width: Width (only for elements with view_box).
        height: Height (only for elements with view_box).
        class_: Substituted as the DOM `class` attribute.
        id_: DOM ID attribute.
        style: Inline style attribute.
        **custom_attributes: Additional attributes.
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
        id_: str | None = None,
        style: str | None = None,
        **custom_attributes: AttributeType,
    ) -> None:
        super().__init__(*children, **custom_attributes | locals_cleanup(locals()))


class View(CaseTag):
    """Defines a view

    Args:
        children: Tags, strings, or other rendered content.
        view_box: Viewport bounds.
        preserve_aspect_ratio: Aspect ratio handling.
        class_: Substituted as the DOM `class` attribute.
        id_: DOM ID attribute.
        style: Inline style attribute.
        **custom_attributes: Additional attributes.
    """

    def __init__(
        self,
        *children: Renderable,
        view_box: str | None = None,
        preserve_aspect_ratio: str | None = None,
        class_: str | None = None,
        id_: str | None = None,
        style: str | None = None,
        **custom_attributes: AttributeType,
    ) -> None:
        super().__init__(*children, **custom_attributes | locals_cleanup(locals()))
