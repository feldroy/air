"""Display and Validation of HTML forms. Powered by pydantic.

Pro-tip: Always validate incoming data.

Based on Daniel Roy Greenfeld's original air.forms design. His pattern:
a swappable widget property, a render() method that calls it, and
pydantic-type-to-HTML-type mapping. Extended here to read the full
AirField metadata vocabulary.
"""

from __future__ import annotations

from enum import Enum
from html import escape
from types import UnionType
from typing import TYPE_CHECKING, Any, ClassVar, Literal, Self, Union, get_args, get_origin

import annotated_types
from pydantic import BaseModel, ValidationError

from air.field import Autofocus, Label, Widget
from air.field.types import (
    BasePresentation,
    Choices,
    HelpText,
    Hidden,
    Placeholder,
    PrimaryKey,
    ReadOnly,
)
from air.requests import Request  # noqa: TC001 (FastAPI needs this at runtime for DI)

if TYPE_CHECKING:
    from collections.abc import Callable, Mapping, Sequence

    from pydantic_core import ErrorDetails

# ---------------------------------------------------------------------------
# Safe HTML output
# ---------------------------------------------------------------------------


class SafeHTML(str):  # noqa: FURB189
    """A str subclass that HTML-aware systems can trust without escaping.

    Follows the __html__ protocol used by Jinja2 and MarkupSafe.
    Air's tag system checks for __html__ and skips escaping, so
    form.render() output can be passed directly to Air tags without
    air.Raw() wrapping.
    """

    def __html__(self) -> str:
        """Return self for the __html__ protocol.

        Jinja2/MarkupSafe calls obj.__html__() and expects an HTML
        string back. Air's tag system checks hasattr(child, '__html__')
        and skips escaping. This satisfies both.
        """
        return str(self)


# ---------------------------------------------------------------------------
# Metadata helpers
# ---------------------------------------------------------------------------


def _meta_dict(field_info: Any) -> dict[type, BasePresentation]:
    """Build a {type: instance} dict for O(1) metadata lookup."""
    return {type(m): m for m in field_info.metadata if isinstance(m, BasePresentation)}


def _get_meta[T](meta: dict[type, BasePresentation], cls: type[T]) -> T | None:
    """Get a typed metadata value from the meta dict, or None."""
    val = meta.get(cls)
    return val if isinstance(val, cls) else None


def _is_optional(annotation: Any) -> bool:
    """Return True if annotation is X | None or Optional[X]."""
    origin = get_origin(annotation)
    if origin is UnionType or origin is Union:
        return type(None) in get_args(annotation)
    return False


# ---------------------------------------------------------------------------
# Type and option helpers
# ---------------------------------------------------------------------------


_WIDGET_TO_HTML_TYPE: dict[str, str] = {
    "toggle": "checkbox",
    "slider": "range",
    "phone": "tel",
    "currency": "number",
    "search": "search",
    "rich_text": "textarea",
    "code": "textarea",
}


def pydantic_type_to_html_type(field_info: Any) -> str:
    """Return HTML input type from a Pydantic field's type and metadata.

    Checks AirField metadata first (Widget, Choices), then infers
    from the Python type annotation. Semantic widget names (toggle,
    slider, etc.) are mapped to valid HTML input types.
    """
    meta = _meta_dict(field_info)

    widget = _get_meta(meta, Widget)
    if widget:
        return _WIDGET_TO_HTML_TYPE.get(widget.kind, widget.kind)
    if Choices in meta:
        return "select"

    annotation = field_info.annotation
    if annotation is bool:
        return "checkbox"
    if annotation is int or annotation is float:
        return "number"
    if isinstance(annotation, type) and issubclass(annotation, Enum):
        return "select"
    if get_origin(annotation) is Literal:
        return "select"

    return "text"


def _get_options(annotation: Any, meta: dict[type, BasePresentation]) -> list[tuple[str, str]]:
    """Get select/dropdown options from metadata or type."""
    choices = _get_meta(meta, Choices)
    if choices:
        return [(str(v), lbl) for v, lbl in choices.options]
    if isinstance(annotation, type) and issubclass(annotation, Enum):
        return [(m.value, m.name.replace("_", " ").title()) for m in annotation]
    if get_origin(annotation) is Literal:
        return [(str(a), str(a).replace("_", " ").title()) for a in get_args(annotation)]
    return []


# ---------------------------------------------------------------------------
# Error helpers
# ---------------------------------------------------------------------------


def get_user_error_message(error: dict) -> str:
    """Convert technical pydantic error to user-friendly message."""
    error_type = error.get("type", "")
    technical_msg = error.get("msg", "")

    messages = {
        "missing": "This field is required.",
        "int_parsing": "Please enter a valid number.",
        "float_parsing": "Please enter a valid number.",
        "bool_parsing": "Please select a valid option.",
        "string_too_short": "This field is required." if error.get("input") == "" else "This value is too short.",  # noqa: PLC1901
        "string_too_long": "This value is too long.",
        "value_error": "This value is not valid.",
        "type_error": "Please enter the correct type of value.",
        "assertion_error": "This value doesn't meet the requirements.",
        "url_parsing": "Please enter a valid URL.",
        "email": "Please enter a valid email address.",
        "json_invalid": "Please enter valid JSON.",
        "enum": "Please select a valid option.",
        "greater_than": "This value must be greater than the minimum.",
        "greater_than_equal": "This value must be at least the minimum.",
        "less_than": "This value must be less than the maximum.",
        "less_than_equal": "This value must be at most the maximum.",
    }

    return messages.get(error_type, technical_msg or "Please correct this error.")


def errors_to_dict(errors: list[dict] | None) -> dict[str, dict]:
    """Converts a pydantic error list to a dictionary for easier reference."""
    if errors is None:
        return {}
    return {error["loc"][0]: error for error in errors}


def label_for_field(field_name: str, field_info: Any) -> str:
    """Return the label for a field from AirField metadata."""
    for m in getattr(field_info, "metadata", []):
        if isinstance(m, Label):
            return m.text
    return field_name


# ---------------------------------------------------------------------------
# Default form widget -- reads the full AirField vocabulary
# ---------------------------------------------------------------------------


def _attr_str(attrs: dict[str, str]) -> str:
    """Build an HTML attribute string from a dict."""
    parts = []
    for key, val in attrs.items():
        if val == "":  # noqa: PLC1901
            parts.append(f" {key}")
        else:
            parts.append(f' {escape(key)}="{escape(val)}"')
    return "".join(parts)


def default_form_widget(  # noqa: C901
    *,
    model: type[BaseModel],
    data: dict | None = None,
    errors: list | None = None,
    excludes: set[str] | None = None,
) -> str:
    """Render form fields for a Pydantic model as HTML.

    Reads the full AirField metadata vocabulary: Widget, Label,
    Placeholder, HelpText, Choices, Autofocus, PrimaryKey, Hidden,
    ReadOnly.

    This is the default widget for AirForm.render(). Swap it by
    setting ``widget`` on your AirForm subclass.

    Args:
        model: The Pydantic model class to render.
        data: Dictionary of data to pre-populate fields.
        errors: List of Pydantic validation errors.
        excludes: Field names to skip when rendering.
    """
    error_dict = errors_to_dict(errors)
    field_parts: list[str] = []

    for field_name, field_info in model.model_fields.items():
        if excludes is not None and field_name in excludes:
            continue

        meta = _meta_dict(field_info)
        annotation = field_info.annotation

        # Skip fields hidden in form context
        hidden = _get_meta(meta, Hidden)
        if hidden and hidden.in_context("form"):
            continue
        readonly = _get_meta(meta, ReadOnly)
        if readonly and readonly.in_context("form"):
            continue

        input_type = pydantic_type_to_html_type(field_info)
        label_text = label_for_field(field_name, field_info)
        error = error_dict.get(field_name)
        value = data.get(field_name) if data is not None else None
        has_error = error is not None

        # Build wrapper
        wrapper_cls = "air-field" + (" air-field-error" if has_error else "")
        parts: list[str] = [f'<div class="{wrapper_cls}">']

        # Label (after input for checkboxes)
        label_html = f'  <label for="{escape(field_name)}">{escape(label_text)}</label>'
        if input_type != "checkbox":
            parts.append(label_html)

        # Build input attributes
        input_attrs: dict[str, str] = {"name": field_name, "id": field_name}

        if input_type not in ("textarea", "select"):
            input_attrs["type"] = input_type

        # Required: non-optional required fields
        if field_info.is_required() and not _is_optional(annotation):
            input_attrs["required"] = ""

        if Autofocus in meta:
            input_attrs["autofocus"] = ""

        placeholder = _get_meta(meta, Placeholder)
        if placeholder:
            input_attrs["placeholder"] = placeholder.text

        if has_error:
            input_attrs["aria-invalid"] = "true"
            input_attrs["aria-describedby"] = f"{field_name}-error"

        # Pydantic constraints -> HTML5 validation attributes
        for m in field_info.metadata:
            if isinstance(m, annotated_types.MinLen):
                input_attrs["minlength"] = str(m.min_length)
            elif isinstance(m, annotated_types.MaxLen):
                input_attrs["maxlength"] = str(m.max_length)
            elif hasattr(annotated_types, "Len") and isinstance(m, annotated_types.Len):
                if getattr(m, "min_length", None) is not None:
                    input_attrs.setdefault("minlength", str(m.min_length))
                if getattr(m, "max_length", None) is not None:
                    input_attrs.setdefault("maxlength", str(m.max_length))

        # Fallback to field_info attributes
        if hasattr(field_info, "min_length") and field_info.min_length is not None:
            input_attrs.setdefault("minlength", str(field_info.min_length))
        if hasattr(field_info, "max_length") and field_info.max_length is not None:
            input_attrs.setdefault("maxlength", str(field_info.max_length))

        # Render the input element
        if input_type == "textarea":
            val = escape(str(value)) if value is not None else ""
            parts.append(f"  <textarea{_attr_str(input_attrs)}>{val}</textarea>")

        elif input_type == "select":
            options = _get_options(annotation, meta)
            parts.extend((
                f"  <select{_attr_str(input_attrs)}>",
                '    <option value="" disabled selected hidden>Select...</option>',
            ))
            for opt_val, opt_label in options:
                sel = " selected" if value is not None and str(value) == opt_val else ""
                parts.append(f'    <option value="{escape(opt_val)}"{sel}>{escape(opt_label)}</option>')
            parts.append("  </select>")

        elif input_type == "checkbox":
            checked = " checked" if value else ""
            parts.append(f"  <input{_attr_str(input_attrs)}{checked}>")

        else:
            val_attr = f' value="{escape(str(value))}"' if value is not None else ""
            parts.append(f"  <input{_attr_str(input_attrs)}{val_attr}>")

        if input_type == "checkbox":
            parts.append(label_html)

        # Help text
        help_text = _get_meta(meta, HelpText)
        if help_text:
            parts.append(f'  <div class="air-field-help" id="{escape(field_name)}-help">{escape(help_text.text)}</div>')

        # Error message
        if error:
            parts.append(
                f'  <div class="air-field-message" id="{escape(field_name)}-error" role="alert">'
                f"{escape(get_user_error_message(error))}</div>"
            )

        parts.append("</div>")
        field_parts.append("\n".join(parts))

    return "\n".join(field_parts)


# ---------------------------------------------------------------------------
# AirForm class
# ---------------------------------------------------------------------------


def _build_excludes(
    model: type[BaseModel],
    user_excludes: Sequence[str | tuple[str, ...]] | None,
) -> tuple[set[str], set[str]]:
    """Build effective display and save exclude sets.

    Scans model metadata for PrimaryKey (default display exclude),
    then merges with the user's excludes tuple.

    A bare string in excludes means both display and save.
    A tuple like ("field", "display") or ("field", "save") or
    ("field", "display", "save") targets specific scopes.

    CSRF is not in the excludes system. render() pushes the token,
    validate() pops it. It never reaches the model or form.data.
    """
    display: set[str] = set()
    save: set[str] = set()

    # Metadata defaults
    for name, field_info in model.model_fields.items():
        meta = _meta_dict(field_info)
        if PrimaryKey in meta:
            display.add(name)

    # User-provided excludes
    if user_excludes is not None:
        for entry in user_excludes:
            if isinstance(entry, str):
                display.add(entry)
                save.add(entry)
            else:
                field_name = entry[0]
                scopes = entry[1:]
                if "display" in scopes:
                    display.add(field_name)
                if "save" in scopes:
                    save.add(field_name)

    return display, save


class AirForm[M: BaseModel]:
    """A form handler that validates and renders Pydantic models as HTML.

    Daniel's original pattern: the form knows its model, validates
    from a dict, and renders itself through a swappable widget.

    CSRF protection is automatic. render() embeds a signed token
    as a hidden input. validate() pops and checks the token before
    Pydantic sees the data. If validate() is called directly
    without render() (programmatic use, tests), CSRF is skipped.

    Example::

        from pydantic import BaseModel
        from air import AirForm


        class WatercolorModel(BaseModel):
            pigment: str
            opacity: int


        class WatercolorForm(AirForm[WatercolorModel]):
            pass


        form = WatercolorForm()
        form.validate({"pigment": "burnt sienna", "opacity": 80})
        if form.is_valid:
            print(form.data.pigment)

        # Render a blank form (includes CSRF token automatically)
        html = WatercolorForm().render()


        # Swap the widget for custom rendering
        class CustomWatercolorForm(AirForm[WatercolorModel]):
            widget = my_custom_renderer
    """

    model: type[M] | None = None
    _data: M | None = None
    initial_data: dict | None = None
    errors: list[ErrorDetails] | None = None
    is_valid: bool = False
    excludes: Sequence[str | tuple[str, ...]] | None = None
    _display_excludes: ClassVar[set[str]] = set()
    _save_excludes: ClassVar[set[str]] = set()

    def __init_subclass__(cls, **kwargs: Any) -> None:
        super().__init_subclass__(**kwargs)
        if "model" not in cls.__dict__:
            for base in getattr(cls, "__orig_bases__", ()):
                if get_origin(base) is AirForm:
                    args = get_args(base)
                    if args and isinstance(args[0], type) and issubclass(args[0], BaseModel):
                        cls.model = args[0]
                        break

        # Build effective exclude sets from metadata defaults + user tuple
        if cls.model is not None:
            cls._display_excludes, cls._save_excludes = _build_excludes(cls.model, cls.excludes)

    def __init__(self, initial_data: dict | None = None) -> None:
        if self.model is None:
            msg = "model"
            raise NotImplementedError(msg)
        self.initial_data = initial_data
        self.submitted_data: dict | None = None
        self._csrf_token: str | None = None

    @property
    def data(self) -> M:
        """The validated model instance.

        Raises:
            AttributeError: If accessed before successful validation.
        """
        if self._data is None:
            msg = "No validated data available. Check is_valid before accessing data."
            raise AttributeError(msg)
        return self._data

    async def __call__(self, form_data: Mapping[str, Any]) -> Self:
        self.validate(form_data)
        return self

    @classmethod
    async def from_request(cls, request: Request) -> Self:
        """Create and validate an AirForm instance from a request.

        CSRF is always enforced for browser submissions.

        Args:
            request: An object with an async ``form()`` method.
        """
        form_data = await request.form()
        self = cls()
        # A browser submission came from a rendered form, enforce CSRF
        self._csrf_token = "from_request"
        self.validate(dict(form_data))
        return self

    def validate(self, form_data: Mapping[str, Any]) -> bool:
        """Validate form data against the model.

        If render() or from_request() set a CSRF expectation, the
        token is popped and checked before Pydantic sees the data.
        Fields in _save_excludes are excluded from form.data.

        Args:
            form_data: Mapping containing the form fields to validate.

        Raises:
            ValueError: If the CSRF token is missing, tampered, or expired.
        """
        from air.form.csrf import CSRF_FIELD_NAME, _check_csrf_token  # noqa: PLC0415

        self._data = None
        self.is_valid = False
        self.errors = None
        self.submitted_data = dict(form_data) if hasattr(form_data, "items") else form_data

        # Pop and check CSRF token before Pydantic sees it
        if self._csrf_token is not None:
            raw_token = self.submitted_data.pop(CSRF_FIELD_NAME, None)
            try:
                if raw_token is None:
                    msg = "CSRF token is missing."
                    raise ValueError(msg)  # noqa: TRY301
                _check_csrf_token(raw_token)
            except ValueError as e:
                self.errors = [{"type": "value_error", "loc": (CSRF_FIELD_NAME,), "msg": str(e), "input": raw_token}]
                return self.is_valid

        # Coerce bool fields for HTML checkbox behavior:
        # checked -> "on", unchecked -> key missing entirely
        assert self.model is not None
        for field_name, field_info in self.model.model_fields.items():
            if field_info.annotation is bool and field_name not in self.submitted_data:
                self.submitted_data[field_name] = False

        # Validate against the user's model
        try:
            self._data = self.model(**self.submitted_data)
            self.is_valid = True
        except ValidationError as e:
            self.errors = e.errors()
        return self.is_valid

    def save_data(self) -> dict[str, Any]:
        """Return validated data as a dict, excluding save-excluded fields.

        Use this when persisting to a database::

            await MyModel.create(**form.save_data())

        Raises:
            AttributeError: If accessed before successful validation.
        """
        if self._data is None:
            msg = "No validated data available. Check is_valid before calling save_data()."
            raise AttributeError(msg)
        return self._data.model_dump(exclude=self._save_excludes or None)

    #: Widget for rendering the form as HTML. A callable with signature
    #: ``(*, model, data, errors, excludes) -> str``.
    #: Override on your subclass to swap in a custom renderer::
    #:
    #:     class MyForm(AirForm[MyModel]):
    #:         widget = staticmethod(my_custom_widget)
    widget: Callable = staticmethod(default_form_widget)

    def render(self) -> str:
        """Render the form as HTML using the widget.

        Automatically embeds a signed CSRF token as a hidden field.
        Uses submitted data if available (preserves values after
        validation errors), falls back to initial_data.
        """
        from air.form.csrf import csrf_hidden_input  # noqa: PLC0415

        csrf_html, self._csrf_token = csrf_hidden_input()
        render_data = self.submitted_data or self.initial_data
        fields_html = self.widget(
            model=self.model,
            data=render_data,
            errors=self.errors,
            excludes=self._display_excludes or None,
        )
        return SafeHTML(f"{csrf_html}\n{fields_html}")
