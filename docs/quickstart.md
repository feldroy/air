# Quickstart

Eager to get started? This page gives a good introduction to Air. 


## A Minimal Application

A minimal Air application:

=== "Air Tags"

    ```python title="main.py"
    import air

    app = air.Air()

    @app.get('/')
    async def index():
        return air.H1('Hello, world')
    ```

    So what does this code do?

    1. First we import the air project
    2. Next we instantiate the Air app. `air.Air` is just a convenience wrapper around `fastapi.FastAPI` that sets the `default_response_class` to be `air.AirResponse`
    3. We define a GET route using `@app.get`, with comes with a response class of `AirResponse`. Now, when we return Air Tags, they are automatically rendered as HTML
    4. We return `air.H1`, which renders as an `<h1></h1>` tag. The response type is `text/html`, so browsers display web pages

=== "Jinja2"

    Here's the Python code:


    ```python title="main.py"
    import air    
    from air import Request

    app = Air()
    jinja = air.JinjaRenderer(directory="templates")

    @app.get('/')
    async def index(request: Request):
        return jinja(
            request,
            name="home.html"
        )       
    ```

    Now create a directory in your project called `templates`, that's where Air projects put Jinja files like the one we list below. 

    ```jinja title="templates/home.html"
    <h1>Hello, world</h1>
    ```

    So what does this code do?

    1. First we import the air project and a few select things from FastAPI.
    2. Next we instantiate the Air app. `air.Air` is just a convenience wrapper around `fastapi.FastAPI` that sets the `default_response_class` to be `air.AirResponse`
    3. We use `JinjaRenderer` factory to configure a `render()` shortcut. This is easier to remember and faster to type than `template.TemplateResponse`
    4. We define a GET route using `@app.get`. Unlike normal FastAPI projects using Jinja we don't need to set the `response_class` to HtmlResponse. That's because the `air.Air` wrapper handles that for us
    5. Our return calls `render()`, which reads the specified Jinja2 template and then produces the result as an `<h1></h1>` tag. The response type is `text/html`, so browsers display web pages

## Running Apps

To run your Air application with uvicorn:

```bash
uvicorn main:app --reload
```

Where:

- `main` is the name of your Python file (main.py)
- `app` is the name of your FastAPI instance
- `--reload` enables auto-reloading when you make changes to your code (useful for development)

Once the server is running, open your browser and navigate to:

- **[http://localhost:8000](http://localhost:8000)** - Your application

## Running Apps with `fastapi`

As Air is just a layer on top of FastAPI, you can use the `fastapi` command to run Air. In fact, this is how some of the core developers prefer to run Air.

In any case, first make sure `fastapi[standard]` is installed:

```sh
# pip
pip install "fastapi[standard]"
# uv
uv add "fastapi[standard]"
```

Then run the cli command:

```sh
fastapi dev
```

## The `app.page` decorator

For simple HTTP GET requests, Air provides the handy `@app.page` shortcut. 



=== "Air Tags"

    ```python title="main.py"
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


=== "Jinja2"


    ```python title="main.py"
    import air    
    from air import Request

    app = air.Air()
    jinja = air.JinjaRenderer(directory="templates")

    @app.page
    async def dashboard(request: Request):
        return jinja(
            request,
            name="dashboard.html"
        )     
    ```

    ```jinja title="templates/dashboard.html"
    <h1>Dashboard</h1>
    ```

## Charting with Air

FastAPI is awesome at producing JSON for chart libraries, and Air Tags makes that even better. Here's a simple yet animated example of using Plotly+Air to provide charts.

```python title="main.py"
import json
import random
import air

app = air.Air()

def sorted_random_list():
    return [0] + sorted(random.sample(range(1, 9), 4)) + [10]

def generate_data():
    return json.dumps(
        {
            "data": [
                {
                    "x": sorted_random_list(),
                    "y": random.sample(range(10), 6),
                    "type": "scatter",
                },
                {
                    "x": sorted_random_list(),
                    "y": random.sample(range(10), 6),
                    "type": "scatter",
                },
            ],
            "title": "Fun charts with Plotly and Air",
            "description": "This is a demonstration of how to build a chart using Plotly and Air",
            "type": "scatter",
        }
    )

@app.page
def index():
    data = generate_data()
    # Use picocss layout to make things pretty 
    return air.layouts.picocss( 
        air.Title("Chart Demo"),
        air.Script(src="https://cdn.plot.ly/plotly-3.0.1.min.js"),
        air.H1("Animated line chart by Air and Plotly"),
        air.Div(id="randomChart"),
        # We place Script inside air.Tags, which simply passes it through. 
        # We do this so it renders inside the page body instead of the page header
        air.Tags( 
            # Call the Plotly library to plot the library
            air.Script( 
                f"var data = {data}; Plotly.newPlot('randomChart', data);",
                # Used to help HTMX know where to replace data
                id="dataSource",
                # Trigger HTMX to call new data every 2 seconds
                hx_trigger="every 2s",
                # Use HTMX to fetch new info from the /data route
                hx_get="/data",
                # When the data is fetched, replace the whole tag
                hx_swap='outerHTML'
            )
        ),
    )

@app.page
def data():
    data = generate_data()
    # This replaces the script in the web page with new data, and triggers
    # an animation of the transition
    return air.Script(
        f"var data = {data}; Plotly.animate('randomChart', data);",
        id="dataSource",
        hx_trigger="every 2s",
        hx_get="/data",
        hx_swap='outerHTML'
    )
```

## Form Validation with Air Forms

Built on pydantic's `BaseModel`, the `air.AirForm` class is used to validate data coming from HTML forms.

### Form handling in views

=== "Air Tags"

    ```python title="main.py"
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


=== "Jinja2"


    ```python title="main.py"
    import air
    from air import Request
    from fastapi import Depends
    from pydantic import BaseModel
    from typing import Annotated


    app = air.Air()
    jinja = air.JinjaRenderer(directory="templates")


    class CheeseModel(BaseModel):
        name: str
        age: int


    class CheeseForm(air.AirForm):
        model = CheeseModel


    @app.page
    async def cheese(request: Request):
        return jinja(request, name="cheese_form.html")


    @app.post("/cheese-info")
    async def cheese_info(request: Request):
        cheese = await CheeseForm.from_request(request)
        return jinja(request, name="cheese_info.html", cheese=cheese)
    ```

    ```jinja title="templates/cheese_form.html"
    <h1>Cheese Form</h1>
    <form method="post" action="/cheese-info">
      <input name="name" placeholder="name of cheese">
      <input name="age" type="number" placeholder="age of cheese">
      <button type="submit">Submit</button>
    </form>
    ```

    ```jinja title="templates/cheese_info.html"
    {% if cheese.is_valid %}
        <h1>{{cheese.data.name}}</h1>
        <p>Age: {{cheese.data.age}}</p>
    {% else %}
        <h1>Errors {{len(cheese.errors)}}</h1>
    {% endif %}
    ```

### Form handling using dependency injection

Buggy, but we are working to make AirForms work through FastAPI's dependency injection mechanism.



NOTE: This feature is currently in development and does not work yet.

=== "Air Tags"

    ```python title="main.py"
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


=== "Jinja2"


    ```python title="main.py"
    import air
    from air import Request
    from fastapi import Depends
    from pydantic import BaseModel
    from typing import Annotated


    app = air.Air()
    jinja = air.JinjaRenderer(directory="templates")


    class CheeseModel(BaseModel):
        name: str
        age: int


    class CheeseForm(air.AirForm):
        model = CheeseModel


    @app.page
    async def cheese(request: Request):
        return jinja(request, name="cheese_form.html")


    @app.post("/cheese-info")
    async def cheese_info(
        request: Request, cheese: Annotated[CheeseForm, Depends(CheeseForm.validate)]
    ):
        return jinja(request, name="cheese_info.html", cheese=cheese)
    ```

    ```jinja title="templates/cheese_form.html"
    <h1>Cheese Form</h1>
    <form method="post" action="/cheese-info">
      <input name="name">
      <input name="age" type="number">
      <button type="submit">Submit</button>
    </form>
    ```

    ```jinja title="templates/cheese_info.html"
    {% if cheese.is_valid %}
        <h1>{{cheese.data.name}}</h1>
        <p>Age: {{cheese.data.age}}</p>
    {% else %}
        <h1>Errors {{len(cheese.errors)}}</h1>
    {% endif %}
    ```    