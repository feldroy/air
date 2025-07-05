from fastapi import Request
from pydantic import ValidationError

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
