from typing import Any, Callable, get_args

from fastapi import Request
from pydantic import BaseModel, ValidationError
from starlette.datastructures import FormData

from . import tags

try:
    from typing import Self  # type: ignore [attr-defined]
except ImportError:
    # NOTE: Remove once Python 3.10 support is dropped
    Self = "AirForm"  # type: ignore [assignment]


class AirForm:
    """
    A form handler that validates incoming form data against a Pydantic model.
    To be used with FastAPI's dependency injection system.

        class CheeseModel(pydantic.BaseModel):
            name: str
            age: int

        class CheeseForm(air.AirForm):
            model = CheeseModel

        @app.post("/cheese")
        async def cheese_form(cheese: Annotated[CheeseForm, Depends(CheeseForm())]):
            if cheese.is_valid:
                return air.Html(air.H1(cheese.data.name))
            return air.Html(air.H1(air.RawHTML(str(len(cheese.errors)))))

    NOTE: This is named AirForm to avoid collisions with tags.Form
    """

    model: type[BaseModel] | None = None
    data: Any = None  # TODO change type to something more specific
    initial_data = None
    errors = None
    is_valid = None

    def __init__(self, initial_data: dict | None = None):
        if self.model is None:
            raise NotImplementedError("model")
        self.initial_data = initial_data

    async def __call__(self, form_data: dict[Any, Any] | FormData) -> Self:
        self.validate(form_data)
        return self

    def validate(self, form_data: dict[Any, Any] | FormData):
        if self.model is None:
            raise NotImplementedError("model")
        try:
            self.data = self.model(**form_data)
            self.is_valid = True
        except ValidationError as e:
            self.errors = e.errors()
            self.is_valid = False

    @classmethod
    async def from_request(cls, request: Request) -> Self:
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
        """
        return default_form_widget

    def render(self) -> tags.SafeStr:
        return tags.SafeStr(
            self.widget(model=self.model, data=self.initial_data, errors=self.errors)
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
        if field_info.json_schema_extra and field_info.json_schema_extra.get(
            field, False
        ):
            return field

    return {int: "number", float: "number", bool: "checkbox", str: "text"}.get(
        field_info.annotation, "text"
    )


def errors_to_dict(errors: list[dict] | None) -> dict[str, dict]:
    "Converts a pydantic error list to a dictionary for easier reference."
    if errors is None:
        return {}
    return {error["loc"][0]: error for error in errors}


def default_form_widget(
    model: type[BaseModel], data: dict | None = None, errors: list | None = None
) -> str:
    error_dict = errors_to_dict(errors)
    fields = []
    for field_name, field_info in model.model_fields.items():
        field_type = field_info.annotation

        # Handle optional types (Union with None)
        if (
            hasattr(field_type, "__origin__")
            and field_type.__origin__ is type(None | str).__origin__  # type: ignore
        ):
            # This is a Union type, get the non-None type
            args = get_args(field_type)
            field_type = next((arg for arg in args if arg is not type(None)), str)
        input_type = pydantic_type_to_html_type(field_info)
        kwargs = {}
        # Inject values
        if data is not None and field_name in data:
            kwargs["value"] = data[field_name]

        if error := error_dict.get(field_name, False):
            kwargs["aria-invalid"] = "true"
        fields.append(
            tags.Label(
                field_name,
                tags.Input(name=field_name, type=input_type, id=field_name, **kwargs),
                tags.Small("Please correct this error.", id=f"{field_name}-error")
                if error
                else "",
            )
        )

    return tags.Fieldset(*fields).render()
