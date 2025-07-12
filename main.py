from pydantic import BaseModel

import air

app = air.Air()


class CheeseModel(BaseModel):
    name: str  # type: ignore [annotation-unchecked]
    age: int  # type: ignore [annotation-unchecked]


class CheeseForm(air.AirForm):
    model = CheeseModel


@app.page
def index():
    cheese = CheeseForm()
    cheese.validate({})

    return air.layouts.picocss(
        air.Body(air.Form(air.H1("Cheese Form"), cheese.render(), action="."))
    )
