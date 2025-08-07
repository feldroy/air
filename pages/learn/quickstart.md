# Quickstart

The TL;DR for getting started with Air.

## Installation

To start a new Air project, create a directory and set up your environment:

```sh
mkdir helloair
cd helloair
uv venv
source .venv/bin/activate
uv add air
uv add fastapi[standard]
```

> [!TIP]
> You can also do `pip install -U air` or `conda install air -c conda-forge`, and similar for fastapi[standard], in any project directory.

## Hello, Air! Example

Create a `main.py` file in your new directory with:

```python
import air

app = air.Air()

@app.get("/")
async def index():
    return air.layouts.mvpcss(air.H1("Hello, Air!", style="color: blue;"))
```

Serve your app with:

```sh
fastapi dev
```

## The app.page decorator

For simple HTTP GET requests, Air provides the handy @app.page shortcut. It converts the name of the function to a URL, where underscores are replaced with dashes and `index` is replaced with '/'.

```python
import air

app = air.Air()


@app.page 
def index():
    # Same as route app.get('/')
    return air.H1('Welcome to our site!')

@app.page
def dashboard():
    # Same as route app.get('/dashboard')
    return air.H1('Dashboard')

@app.page
def show_item():
    # same as app.get('/get-item')
    return air.H1('Showing an item')
```

## Form validation with Air Forms

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

## Form handling using dependency injection

It is possible to use dependency injection to manage form validation

NOTE: This functionality is currently in development and this feature currently does not work

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