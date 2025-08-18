# Forms & validation

Built on Pydantic's `BaseModel`, the `air.AirForm` class is used to validate data coming from HTML forms.

```python
from typing import Annotated

from fastapi import Depends, Request
from pydantic import BaseModel
import air

app = air.Air()


class CheeseModel(BaseModel):
    name: str
    age: int


class CheeseForm(air.AirForm):
    model = CheeseModel

@app.page
async def index():
    return air.layouts.mvpcss(
        air.H1("Cheese Form"),
        air.Form(
            air.Input(name="name", placeholder='name of cheese'),
            air.Input(name="age", type="number", placeholder='age'),
            air.Button("Submit", type="submit"),
            method="post",
            action="/cheese-info",
        ),
    )

@app.post("/cheese-info")
async def cheese_info(request: Request):
    cheese = await CheeseForm.from_request(request)
    if cheese.is_valid:
        return air.Html(air.H1(f'{cheese.data.name} age {cheese.data.age}'))
    return air.Html(air.H1(f"Errors {len(cheese.errors)}"))
```

## Coming Soon: Dependency-Injection Form Handling

It is possible to use dependency injection to manage form validation.

NOTE: This functionality is currently in development. This feature was working before but currently does not work.

```python
from typing import Annotated

from fastapi import Depends
from pydantic import BaseModel
import air

app = air.Air()


class CheeseModel(BaseModel):
    name: str
    age: int


class CheeseForm(air.AirForm):
    model = CheeseModel


@app.page
async def cheese():
    return air.Html(
        air.H1("Cheese Form"),
        air.Form(
            air.Input(name="name"),
            air.Input(name="age", type="number"),
            air.Button("Submit", type="submit"),
            method="post",
            action="/cheese-info",
        ),
    )


@app.post("/cheese-info")
async def cheese_info(cheese: Annotated[CheeseForm, Depends(CheeseForm.validate)]):
    if cheese.is_valid:
        return air.Html(air.H1(cheese.data.name))
    return air.Html(air.H1(f"Errors {len(cheese.errors)}"))
```
