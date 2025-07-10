from typing import Callable, Any, get_args

from . import tags
from fastapi import Request
from pydantic import ValidationError, BaseModel

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

    model = None
    data = None
    errors = None
    is_valid = None
    action = '.'

    async def __call__(self, request: Request) -> Self:
        if self.model is None:
            raise NotImplementedError("model")
        data = await request.form()
        try:
            self.data = self.model(**data)
            self.is_valid = True
        except ValidationError as e:
            self.errors = e.errors()
            self.is_valid = False
        return self

    @classmethod
    async def validate(cls, request: Request) -> Self:
        self = cls()
        await self(request)
        return self

    @property
    def widget(self) -> Callable:
        """Widget for rendering of form in HTML
        
        If you want a custom widget, replace with a function that accepts:

            - model: BaseModel
            - action:str=".",
            - data: dict|None
            - errors:dict|None=None
        """
        return default_form_widget
    
    def render(self) -> str:
        return self.widget(model=self.model, action=self.action,data=self.data, errors=self.errors)
    
def pydantic_type_to_html_type(field_type: Any):
    """Return HTML type from pydantic type.
    
    Default to 'text' for unknown types.
    """
    return {
        int: 'number',
        float: 'number',
        bool: 'checkbox',
        str: 'text'
    }.get(field_type, 'text')



def default_form_widget(model: type[BaseModel], action:str=".",
                        data: dict|None=None, errors:dict|None=None) -> str:
    # TODO add looping through data and associated with any errors
    # Make individual inputs their own widget?
    fields = []
    for field_name, field_info in model.model_fields.items():
        field_type = field_info.annotation
        
        # Handle optional types (Union with None)
        if hasattr(field_type, '__origin__') and field_type.__origin__ is type(None | str).__origin__:
            # This is a Union type, get the non-None type
            args = get_args(field_type)
            field_type = next((arg for arg in args if arg is not type(None)), str)        
        input_type = pydantic_type_to_html_type(field_type)
        fields.append(
            tags.Input(name=field_name, type=input_type, id=field_name)
        )
    fields.append(tags.Button('Submit', type='submit'))

    return tags.Form(
            *fields,
            action=action).render()
