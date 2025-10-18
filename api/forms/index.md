# Forms

Display and Validation of HTML forms. Powered by pydantic.

Pro-tip: Always validate incoming data.

## AirForm

```
AirForm(initial_data=None)
```

A form handler that validates incoming form data against a Pydantic model. Can be used with awaited form data or with FastAPI's dependency injection system.

Example:

```
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
    return air.Html(air.H1(air.Raw(str(len(flight.errors)))))

@app.post("/flight-depends")
async def flight_form_depends(flight: Annotated[FlightForm, Depends(FlightForm())]):
    "Dependency injection"
    if flight.is_valid:
        return air.Html(air.H1(flight.data.flight_number))
    return air.Html(air.H1(air.Raw(str(len(flight.errors)))))
```

NOTE: This is named AirForm to avoid collisions with tags.Form

Source code in `src/air/forms.py`

```
def __init__(self, initial_data: dict | None = None) -> None:
    if self.model is None:
        msg = "model"
        raise NotImplementedError(msg)
    self.initial_data = initial_data
```

### widget

```
widget
```

Widget for rendering of form in HTML

If you want a custom widget, replace with a function that accepts:

```
- model: BaseModel
- data: dict|None
- errors:dict|None=None
```

## AirField

```
AirField(
    default=PydanticUndefined,
    *,
    default_factory=None,
    alias=None,
    alias_priority=None,
    validation_alias=None,
    serialization_alias=None,
    title=None,
    field_title_generator=None,
    description=None,
    examples=None,
    exclude=None,
    exclude_if=None,
    discriminator=None,
    deprecated=None,
    json_schema_extra=None,
    frozen=None,
    validate_default=None,
    repr=None,
    init=None,
    init_var=None,
    kw_only=None,
    pattern=None,
    strict=None,
    coerce_numbers_to_str=None,
    gt=None,
    ge=None,
    lt=None,
    le=None,
    multiple_of=None,
    allow_inf_nan=None,
    max_digits=None,
    decimal_places=None,
    min_length=None,
    max_length=None,
    union_mode=None,
    fail_fast=None,
    type=None,
    label=None,
    autofocus=False,
    **extra,
)
```

A wrapper around pydantic.Field to provide a cleaner interface for defining special input types and labels in air forms.

NOTE: This is named AirField to adhere to the same naming convention as AirForm.

Example:

```
class CheeseModel(BaseModel):
    name: str = air.AirField(label="Name", autofocus=True)
    age: int

class CheeseForm(air.AirForm):
    model = CheeseModel
```

Used with FastAPI's dependency injection system: class CheeseModel(pydantic.BaseModel): name: str age: int

```
class CheeseForm(air.AirForm):
    model = CheeseModel

@app.post("/cheese")
async def cheese_form(cheese: Annotated[CheeseForm, Depends(CheeseForm())]):
    if cheese.is_valid:
        return air.Html(air.H1(cheese.data.name))
    return air.Html(air.H1(air.Raw(str(len(cheese.errors)))))
```

Source code in `src/air/forms.py`

```
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

        class CheeseModel(BaseModel):
            name: str = air.AirField(label="Name", autofocus=True)
            age: int

        class CheeseForm(air.AirForm):
            model = CheeseModel

    Used with FastAPI's dependency injection system:
        class CheeseModel(pydantic.BaseModel):
            name: str
            age: int

        class CheeseForm(air.AirForm):
            model = CheeseModel

        @app.post("/cheese")
        async def cheese_form(cheese: Annotated[CheeseForm, Depends(CheeseForm())]):
            if cheese.is_valid:
                return air.Html(air.H1(cheese.data.name))
            return air.Html(air.H1(air.Raw(str(len(cheese.errors)))))
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
```

## default_form_widget

```
default_form_widget(
    model, data=None, errors=None, includes=None
)
```

Render a form widget for a given Pydantic model.

Parameters:

| Name       | Type              | Description                        | Default                                             |
| ---------- | ----------------- | ---------------------------------- | --------------------------------------------------- |
| `model`    | `type[BaseModel]` | The Pydantic model class to render | *required*                                          |
| `data`     | \`dict            | None\`                             | Dictionary of data to pre-populate                  |
| `errors`   | \`list            | None\`                             | List of Pydantic validation errors                  |
| `includes` | \`Sequence[str]   | None\`                             | Sequence of field names to include (None means all) |

Returns:

| Type  | Description                       |
| ----- | --------------------------------- |
| `str` | HTML string representing the form |

Source code in `src/air/forms.py`

```
def default_form_widget(
    model: type[BaseModel],
    data: dict | None = None,
    errors: list | None = None,
    includes: Sequence[str] | None = None,
) -> str:
    """
    Render a form widget for a given Pydantic model.

    Args:
        model: The Pydantic model class to render
        data: Dictionary of data to pre-populate
        errors: List of Pydantic validation errors
        includes: Sequence of field names to include (None means all)

    Returns:
        HTML string representing the form
    """
    error_dict = errors_to_dict(errors)
    fields = []
    for field_name, field_info in model.model_fields.items():
        if includes is not None and field_name not in includes:
            continue
        field_type = field_info.annotation
        origin = get_origin(field_type)

        # Handle optional types (Union with None)
        if (origin is Union or origin is UnionType) and type(None) in get_args(field_type):
            # This is a Union type, get the non-None type
            args = get_args(field_type)
            field_type = next((arg for arg in args if arg is not type(None)), str)
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
```

## errors_to_dict

```
errors_to_dict(errors)
```

Converts a pydantic error list to a dictionary for easier reference.

Source code in `src/air/forms.py`

```
def errors_to_dict(errors: list[dict] | None) -> dict[str, dict]:
    """Converts a pydantic error list to a dictionary for easier reference."""
    if errors is None:
        return {}
    return {error["loc"][0]: error for error in errors}
```

## get_user_error_message

```
get_user_error_message(error)
```

Convert technical pydantic error to user-friendly message.

Source code in `src/air/forms.py`

```
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
```

## pydantic_type_to_html_type

```
pydantic_type_to_html_type(field_info)
```

Return HTML type from pydantic type.

Default to 'text' for unknown types.

Source code in `src/air/forms.py`

```
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
```
