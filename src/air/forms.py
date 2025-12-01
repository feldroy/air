"""Display and Validation of HTML forms. Powered by pydantic.

Pro-tip: Always validate incoming data."""

import re
from collections.abc import Callable, Sequence
from types import UnionType
from typing import Any, Literal, Self, Union, get_args, get_origin

import annotated_types
from pydantic import AliasChoices, AliasPath, BaseModel, Discriminator, Field, JsonValue, ValidationError
from pydantic.fields import Deprecated, FieldInfo
from pydantic_core import ErrorDetails, PydanticUndefined
from starlette.datastructures import FormData

from . import tags
from .requests import Request
from .tags import SafeStr


class AirForm:
    """A form handler that validates incoming form data against a Pydantic model. Can be used with
    awaited form data or with FastAPI's dependency injection system.

    Example:

        from typing import Annotated

        from fastapi import Depends
        from pydantic import BaseModel

        import air

        app = air.Air()


        class FlightModel(BaseModel):
            flight_number: str
            destination: str


        class FlightForm(air.AirForm):
            model = FlightModel


        @app.post("/flight")
        async def flight_form(request: air.Request):
            "Awaited form data"
            flight = await FlightForm.from_request(request)
            if flight.is_valid:
                return air.Html(air.H1(flight.data.flight_number))
            errors = len(flight.errors or [])
            return air.Html(air.H1(air.Raw(str(errors))))


        @app.post("/flight-depends")
        async def flight_form_depends(flight: Annotated[FlightForm, Depends(FlightForm.from_request)]):
            "Dependency injection"
            if flight.is_valid:
                return air.Html(air.H1(flight.data.flight_number))
            errors = len(flight.errors or [])
            return air.Html(air.H1(air.Raw(str(errors))))
    """

    model: type[BaseModel] | None = None
    data: Any = None  # TODO change type to something more specific
    initial_data: dict | None = None
    errors: list[ErrorDetails] | None = None
    is_valid: bool = False
    includes: Sequence[str] | None = None

    def __init__(self, initial_data: dict | None = None) -> None:
        if self.model is None:
            msg = "model"
            raise NotImplementedError(msg)
        self.initial_data = initial_data

    async def __call__(self, form_data: dict[Any, Any] | FormData) -> Self:
        self.validate(form_data)
        return self

    def validate(self, form_data: dict[Any, Any] | FormData) -> bool:
        """Validate form data against the model.

        Args:
            form_data: Dictionary or FormData containing the form fields to validate

        Returns:
            True if validation succeeds, False otherwise

        Example:

            import air

            app = air.Air()


            class FlightModel(air.AirModel):
                flight_number: str
                destination: str


            @app.post("/flight")
            async def submit_flight(request: air.Request):
                form_data = await request.form()
                flight_form = FlightModel.to_form()

                if flight_form.validate(form_data):
                    # Form is valid
                    return air.Html(
                        air.H1("Flight Submitted"),
                        air.P(f"Flight: {flight_form.data.flight_number}"),
                        air.P(f"Destination: {flight_form.data.destination}"),
                    )

                # Form has errors
                return air.Html(
                    air.H1("Validation Failed"),
                    air.P(f"Errors: {len(flight_form.errors or [])}"),
                )
        """
        # Store the submitted data to preserve values on error
        self.submitted_data = dict(form_data) if hasattr(form_data, "items") else form_data
        try:
            assert self.model is not None
            self.data = self.model(**form_data)
            self.is_valid = True
        except ValidationError as e:
            self.errors = e.errors()
        return self.is_valid

    @classmethod
    async def from_request(cls, request: Request) -> Self:
        """Create and validate an AirForm instance from a request.

        Args:
            request: The incoming request containing form data

        Returns:
            An AirForm instance with validation results

        Example:

            import air

            app = air.Air()


            class FlightModel(air.AirModel):
                flight_number: str
                destination: str


            FlightForm = FlightModel.to_form()


            @app.post("/flight")
            async def submit_flight(request: air.Request):
                flight = await FlightForm.from_request(request)

                if flight.is_valid:
                    # Form is valid
                    return air.Html(
                        air.H1("Flight Submitted"),
                        air.P(f"Flight: {flight.data.flight_number}"),
                        air.P(f"Destination: {flight.data.destination}"),
                    )

                # Form has errors
                return air.Html(
                    air.H1("Validation Failed"),
                    air.P(f"Errors: {len(flight.errors or [])}"),
                )
        """
        form_data = await request.form()
        self = cls()
        await self(form_data=form_data)
        return self

    @property
    def widget(self) -> Callable:
        """Widget for rendering of form in HTML

        If you want a custom widget, replace with a function that accepts:

            - model: BaseModel
            - data: dict|None
            - errors:dict|None=None

        Example:

            from collections.abc import Sequence

            from pydantic import BaseModel

            import air
            from air.forms import default_form_widget

            app = air.Air()


            class ContactModel(air.AirModel):
                # Note: This uses `str` for email. For stricter server-side validation,
                # you can use `EmailStr` from pydantic.
                name: str
                email: str
                message: str


            def contact_widget(
                *,
                model: type[BaseModel],
                data: dict | None = None,
                errors: list | None = None,
                includes: Sequence[str] | None = None,
            ):

                base_html = default_form_widget(
                    model=model,
                    data=data,
                    errors=errors,
                    includes=includes,
                )

                return air.Div(
                    air.P("Custom widget wrapper"),
                    air.Raw(base_html),
                    class_="contact-form",
                )


            def get_contact_form() -> air.AirForm:
                return ContactModel.to_form(widget=contact_widget)


            @app.page
            def contact(request: air.Request):

                form = get_contact_form()

                return air.layouts.mvpcss(
                    air.H1("Contact Us"),
                    air.P("This example uses a custom AirForm.widget to wrap the default form HTML."),
                    air.Form(
                        form.render(),
                        air.Button("Send message", type="submit"),
                        method="post",
                        action="/contact",
                    ),
                )


            @app.post("/contact")
            async def submit_contact(request: air.Request):
                form = get_contact_form()
                form_data = await request.form()

                if form.validate(form_data):
                    return air.Html(
                        air.H1("Thank you for your message!"),
                        air.P("Your contact form was submitted successfully."),
                    )

                error_count = len(form.errors or [])
                return air.Html(
                    air.H1("Please fix the errors below."),
                    air.P(f"Found {error_count} validation error(s)."),
                    air.Form(
                        form.render(),
                        air.Button("Send message", type="submit"),
                        method="post",
                        action="/contact",
                    ),
                )


            if __name__ == "__main__":
                import uvicorn

                uvicorn.run(app, host="127.0.0.1", port=8000)
        """
        return default_form_widget

    def render(self) -> SafeStr:
        """Return HTML representation of HTML widget

        Example:

            from pydantic import BaseModel

            import air

            app = air.Air()


            class ContactModel(BaseModel):
                # Pydantic model backing the contact form.

                name: str
                email: str
                message: str


            class ContactForm(air.AirForm):
                # AirForm that uses ContactModel for validation and rendering.

                model = ContactModel


            @app.page
            def contact(request: air.Request):
                # Render a page with a contact form built using AirForm.render()
                form = ContactForm()
                return air.layouts.mvpcss(
                    air.H1("Contact us"),
                    air.P("This form is rendered using AirForm.render()."),
                    air.Form(
                        form.render(),
                        air.Button("Send message", type="submit"),
                        method="post",
                        action=submit.url(),  # type: ignore[unresolved-attribute]
                    ),
                )


            @app.post("/contact")
            async def submit(request: air.Request) -> air.Html:
                # Handle form submission and re-render the form if there are errors.
                form = ContactForm()
                form_data = await request.form()

                # Validate incoming form data; AirForm.render() will then include errors
                # and preserve submitted values when re-rendered.
                form.validate(form_data)

                if form.is_valid:
                    return air.Html(
                        air.H1("Thank you for your message!"),
                        air.P("Your contact form was submitted successfully."),
                    )

                error_count = len(form.errors or [])
                return air.Html(
                    air.H1("Please fix the errors below."),
                    air.P(f"Found {error_count} validation error(s)."),
                    air.Form(
                        form.render(),
                        air.Button("Send message", type="submit"),
                        method="post",
                        action=submit.url(),  # type: ignore[unresolved-attribute]
                    ),
                )


            if __name__ == "__main__":
                import uvicorn

                uvicorn.run(app, host="127.0.0.1", port=8000)
        """

        # Use submitted data if available (preserves values on validation errors)
        render_data = getattr(self, "submitted_data", None) or self.initial_data
        return SafeStr(
            self.widget(
                model=self.model,
                data=render_data,
                errors=self.errors,
                includes=self.includes,
            ),
        )


def pydantic_type_to_html_type(field_info: Any) -> str:
    """Return HTML type from pydantic type.

    Default to 'text' for unknown types.
    """
    special_fields = [
        "hidden",
        "email",
        "password",
        "url",
        "datedatetime-local",
        "month",
        "time",
        "color",
        "file",
    ]
    for field in special_fields:
        if field_info.json_schema_extra and field_info.json_schema_extra.get(field, False):
            return field

    return {int: "number", float: "number", bool: "checkbox", str: "text"}.get(field_info.annotation, "text")


def get_user_error_message(error: dict) -> str:
    """Convert technical pydantic error to user-friendly message."""
    error_type = error.get("type", "")
    technical_msg = error.get("msg", "")

    # Map error types to user-friendly messages
    messages = {
        "missing": "This field is required.",
        "int_parsing": "Please enter a valid number.",
        "float_parsing": "Please enter a valid number.",
        "bool_parsing": "Please select a valid option.",
        "string_too_short": "This value is too short.",
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

    # Get user-friendly message or fallback to technical message
    return messages.get(error_type, technical_msg or "Please correct this error.")


def errors_to_dict(errors: list[dict] | None) -> dict[str, dict]:
    """Converts a pydantic error list to a dictionary for easier reference."""
    if errors is None:
        return {}
    return {error["loc"][0]: error for error in errors}


def default_form_widget(  # noqa: C901
    model: type[BaseModel],
    data: dict | None = None,
    errors: list | None = None,
    includes: Sequence[str] | None = None,
) -> str:
    """Render a form widget for a given Pydantic model.

    Args:
        model: The Pydantic model class to render
        data: Dictionary of data to pre-populate
        errors: List of Pydantic validation errors
        includes: Sequence of field names to include (None means all)

    Returns:
        HTML string representing the form

    Example:

        import air
        from air.forms import default_form_widget

        app = air.Air()


        class FlightModel(air.AirModel):
            flight_number: str
            destination: str
            passengers: int


        @app.page
        def index(request: air.Request):
            # Render different field groups separately using includes parameter
            basic_info = default_form_widget(
                model=FlightModel,
                data={"flight_number": "AA123"},  # Pre-populate flight_number
                includes=["flight_number", "destination"],
            )

            passenger_info = default_form_widget(
                model=FlightModel,
                includes=["passengers"],
            )

            return air.Html(
                air.H1("Flight Booking"),
                air.Form(
                    air.Fieldset(
                        air.Legend("Flight Information"),
                        air.Raw(basic_info),
                    ),
                    air.Fieldset(
                        air.Legend("Passenger Count"),
                        air.Raw(passenger_info),
                    ),
                    air.Button("Submit", type="submit"),
                    method="post",
                    action="/submit",
                ),
            )


        @app.post("/submit")
        async def submit(request: air.Request):
            form_data = await request.form()
            flight_form = FlightModel.to_form()

            if flight_form.validate(form_data):
                return air.Html(
                    air.H1("Flight Booked"),
                    air.P(f"Flight: {flight_form.data.flight_number}"),
                    air.P(f"Destination: {flight_form.data.destination}"),
                    air.P(f"Passengers: {flight_form.data.passengers}"),
                )

            # Re-render with custom layout and errors
            basic_info = default_form_widget(
                model=FlightModel,
                data=dict(form_data),
                errors=flight_form.errors,
                includes=["flight_number", "destination"],
            )

            passenger_info = default_form_widget(
                model=FlightModel,
                data=dict(form_data),
                errors=flight_form.errors,
                includes=["passengers"],
            )

            return air.Html(
                air.H1("Please fix the errors"),
                air.Form(
                    air.Fieldset(
                        air.Legend("Flight Information"),
                        air.Raw(basic_info),
                    ),
                    air.Fieldset(
                        air.Legend("Passenger Count"),
                        air.Raw(passenger_info),
                    ),
                    air.Button("Submit", type="submit"),
                    method="post",
                    action="/submit",
                ),
            )
    """
    error_dict = errors_to_dict(errors)
    fields = []
    for field_name, field_info in model.model_fields.items():
        if includes is not None and field_name not in includes:
            continue

        input_type = pydantic_type_to_html_type(field_info)
        kwargs = {}
        # Inject values
        if data is not None and field_name in data:
            kwargs["value"] = data[field_name]

        error = error_dict.get(field_name)
        if error:
            kwargs["aria-invalid"] = "true"
        json_schema_extra: dict = field_info.json_schema_extra or {}
        if json_schema_extra.get("autofocus"):
            kwargs["autofocus"] = True

        # Add HTML5 validation attributes from Pydantic constraints
        # Check if field is optional (Union with None)
        annotation = field_info.annotation
        origin = get_origin(annotation)
        is_optional = (origin is Union or origin is UnionType) and type(None) in get_args(annotation)

        # Add required attribute for non-optional required fields
        if field_info.is_required() and not is_optional:
            kwargs["required"] = True

        # Extract min_length and max_length from field metadata
        for meta in getattr(field_info, "metadata", []):
            if isinstance(meta, annotated_types.MinLen):
                kwargs["minlength"] = meta.min_length
            elif isinstance(meta, annotated_types.MaxLen):
                kwargs["maxlength"] = meta.max_length
            elif hasattr(annotated_types, "Len") and isinstance(meta, annotated_types.Len):
                if getattr(meta, "min_length", None) is not None:
                    kwargs["minlength"] = meta.min_length
                if getattr(meta, "max_length", None) is not None:
                    kwargs["maxlength"] = meta.max_length

        # Fallback to field_info attributes if present
        if hasattr(field_info, "min_length") and field_info.min_length is not None:
            kwargs.setdefault("minlength", field_info.min_length)
        if hasattr(field_info, "max_length") and field_info.max_length is not None:
            kwargs.setdefault("maxlength", field_info.max_length)

        fields.append(
            tags.Tags(
                tags.Label(
                    json_schema_extra.get("label") or field_name,
                    for_=field_name,
                ),
                tags.Input(name=field_name, type=input_type, id=field_name, **kwargs),
                (tags.Small(get_user_error_message(error), id=f"{field_name}-error") if error else ""),
            ),
        )

    return tags.Tags(*fields).render()


def AirField(
    default: Any = PydanticUndefined,
    *,
    default_factory: Callable[[], Any] | Callable[[dict[str, Any]], Any] | None = None,
    alias: str | None = None,
    alias_priority: int | None = None,
    validation_alias: str | AliasPath | AliasChoices | None = None,
    serialization_alias: str | None = None,
    title: str | None = None,
    field_title_generator: Callable[[str, FieldInfo], str] | None = None,
    description: str | None = None,
    examples: list[Any] | None = None,
    exclude: bool | None = None,
    exclude_if: Callable[[Any], bool] | None = None,
    discriminator: str | Discriminator | None = None,
    deprecated: Deprecated | str | bool | None = None,
    json_schema_extra: dict[str, JsonValue] | None = None,
    frozen: bool | None = None,
    validate_default: bool | None = None,
    repr: bool | None = None,
    init: bool | None = None,
    init_var: bool | None = None,
    kw_only: bool | None = None,
    pattern: str | re.Pattern[str] | None = None,
    strict: bool | None = None,
    coerce_numbers_to_str: bool | None = None,
    gt: annotated_types.SupportsGt | None = None,
    ge: annotated_types.SupportsGe | None = None,
    lt: annotated_types.SupportsLt | None = None,
    le: annotated_types.SupportsLe | None = None,
    multiple_of: float | None = None,
    allow_inf_nan: bool | None = None,
    max_digits: int | None = None,
    decimal_places: int | None = None,
    min_length: int | None = None,
    max_length: int | None = None,
    union_mode: Literal["smart", "left_to_right"] | None = None,
    fail_fast: bool | None = None,
    # Not in pydantic.Field:
    type: str | None = None,
    label: str | None = None,
    autofocus: bool = False,
    **extra: Any,
) -> Any:
    """A wrapper around pydantic.Field to provide a cleaner interface for defining
    special input types and labels in air forms.

    NOTE: This is named AirField to adhere to the same naming convention as AirForm.

    Example:

        from pydantic import BaseModel

        import air

        app = air.Air()


        class ContactModel(BaseModel):
            name: str = air.AirField(label="Full Name", min_length=2, max_length=50)
            # Note: This uses `str` for email. For stricter server-side validation,
            # you can use `EmailStr` from pydantic.
            email: str = air.AirField(type="email", label="Email Address")
            message: str = air.AirField(label="Message", min_length=10, max_length=500)
            preferred_datetime: str = air.AirField(
                type="datedatetime-local",
                label="Preferred Date & Time",
            )


        class ContactForm(air.AirForm):
            model = ContactModel


        @app.page
        def index(request: air.Request):
            # Render a simple page containing the contact form.
            form = ContactForm()
            return air.layouts.mvpcss(
                air.H1("Contact Form Example Using AirField"),
                air.P("Submit the form below to see AirField + AirForm in action."),
                air.Form(
                    form.render(),
                    air.Button("Submit", type="submit"),
                    method="post",
                    action=submit.url(),  # ty: ignore[unresolved-attribute]
                ),
            )


        @app.post("/submit")
        async def submit(request: air.Request) -> air.Html:
            # Handle POSTed form data and re-render with errors if invalid.
            form = ContactForm()

            # Parse form data from the incoming request and validate
            form_data = await request.form()
            form.validate(form_data)

            if form.is_valid:
                return air.Html(
                    air.layouts.mvpcss(
                        air.H1("Thanks for your message!"),
                        air.P("Here is what you sent:"),
                        air.Ul(
                            air.Li(f"Name: {form.data.name}"),
                            air.Li(f"Email: {form.data.email}"),
                            air.Li(f"Message: {form.data.message}"),
                            air.Li(f"Preferred Date & Time: {form.data.preferred_datetime}"),
                        ),
                    )
                )

            # If invalid, re-render the form with errors and values preserved
            return air.Html(
                air.layouts.mvpcss(
                    air.H1("Please fix the errors below."),
                    air.Form(
                        form.render(),
                        air.Button("Submit", type="submit"),
                        method="post",
                        action=submit.url(),  # ty: ignore[unresolved-attribute]
                    ),
                )
            )


        if __name__ == "__main__":
            # Run this example with:
            #   uv run examples/src/forms__AirField.py
            import uvicorn

            uvicorn.run(app, host="127.0.0.1", port=8000)
    """
    schema_extra: dict[str, JsonValue] = json_schema_extra or {}
    if type:
        schema_extra[type] = True
    if label:
        schema_extra["label"] = label
    if autofocus:
        schema_extra["autofocus"] = True
    if extra:
        schema_extra.update(extra)

    # noinspection PyArgumentList
    return Field(
        default,
        default_factory=default_factory,
        alias=alias,
        alias_priority=alias_priority,
        validation_alias=validation_alias,
        serialization_alias=serialization_alias,
        title=title,
        field_title_generator=field_title_generator,
        description=description,
        examples=examples,
        exclude=exclude,
        exclude_if=exclude_if,
        discriminator=discriminator,
        deprecated=deprecated,
        json_schema_extra=schema_extra,
        frozen=frozen,
        validate_default=validate_default,
        repr=repr,
        init=init,
        init_var=init_var,
        kw_only=kw_only,
        pattern=pattern,
        strict=strict,
        coerce_numbers_to_str=coerce_numbers_to_str,
        gt=gt,
        ge=ge,
        lt=lt,
        le=le,
        multiple_of=multiple_of,
        allow_inf_nan=allow_inf_nan,
        max_digits=max_digits,
        decimal_places=decimal_places,
        min_length=min_length,
        max_length=max_length,
        union_mode=union_mode,
        fail_fast=fail_fast,
    )  # ty: ignore[no-matching-overload]


def to_form(
    model: type[BaseModel],
    *,
    name: str | None = None,
    includes: Sequence[str] | None = None,
    widget: Callable | None = None,
) -> "AirForm":
    """Generate an :class:`AirForm` instance for the given Pydantic model.

    Args:
        model: The Pydantic model class the form should validate against.
        name: Optional explicit class name for the generated form.
        includes: Optional iterable of field names to render (defaults to all fields).
        widget: Optional callable to render the form. Falls back to :func:`default_form_widget`.

    Returns:
        A new :class:`AirForm` instance bound to ``model``.
    """

    attrs: dict[str, Any] = {"model": model, "__module__": model.__module__}

    if includes is not None:
        attrs["includes"] = tuple(includes)

    if widget is not None:

        def _widget(self: AirForm, _widget: Callable = widget) -> Callable:
            return _widget

        attrs["widget"] = property(_widget)

    form_name = name or f"{model.__name__}Form"
    generated_form = type(form_name, (AirForm,), attrs)
    generated_form.__doc__ = f"Auto-generated AirForm for {model.__module__}.{model.__name__}."
    return generated_form()
