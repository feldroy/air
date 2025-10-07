# Quickstart

The TL;DR for getting started with Air.

## Installation

To start a new Air project, create a directory and set up your environment:

```sh
mkdir helloair
cd helloair
uv venv
source .venv/bin/activate
uv init
uv add air
uv add "fastapi[standard]"
```

!!! note
    You can also do:

    ```sh
    pip install -U air "fastapi[standard]"
    ```

    or even 

    ```sh
    conda install air -c conda-forge
    conda install "fastapi[standard]" -c conda-forge
    ```


## Hello, Air! Example

Create a `main.py` file in your new directory with:

```python title="main.py"
import air

app = air.Air()

@app.get("/")
async def index():
    return air.layouts.mvpcss(
        air.H1("Hello, Air!"),
        air.P("Breathe it in.")
    )
```

Serve your app with:

```sh
fastapi dev
```

Open your page by clicking this link: <a href="http://localhost:8000/" target="_blank">http://localhost:8000/</a>

Here's a few interesting things about this page:

1. The page has an attractive layout and typography
2. The Python for this app is similar in design to how FastAPI code is written
3. If you typed the code out in an IDE with intellisense, you'll have seen every Air object includes useful instruction. Air is designed to be friendly to both humans and LLMs, hence every object is carefully typed and documented

## Routing

Routing is how users on paths are directed to the correct 'view' function that handles their request.

### Basics

Air wraps FastAPI so you can use the same decorator patterns for specifying URLs:

```python  hl_lines="5 12 25"
import air

app = air.Air()

@app.get("/")
def index():
    return air.layouts.mvpcss(
        air.H1("Hello, Air!"),
        air.P("Breathe it in.")
    )

@app.get("/air-is-grounded")
def air_is_grounded():
    return air.layouts.mvpcss(
        air.H1("Air is Grounded"),
        air.P("Built on industry standard libraries including:"),
        air.Ul(
            air.Li('FastAPI'),
            air.Li('Starlette'),
            air.Li('Pydantic'),
            air.Li('Jinja'),
        )
    )

@app.post('/form-handler')
async def form_handler(request: air.Request): # (1)!
    ...
```

1. Form handling in Air requires `async` functions and usually an `air.Request` argument. We cover forms later on this page as well as in numerous places across the Air documentation.

### app.page decorator

To expedite `HTTP GET` pages we provide the `app.page` decorator, which can replace the `app.get()` decorator for views without arguments. `app.page` converts the name of the function to the route, converting underscores to dashes:

```python hl_lines="5-6 12-13"
import air

app = air.Air()

@app.page # Renders as '/'
def index(): # (1)!
    return air.layouts.mvpcss(
        air.H1("Hello, Air!"),
        air.P("Breathe it in.")
    )

@app.page # Renders as '/air-is-grounded'
def air_is_grounded(): # (2)!
    return air.layouts.mvpcss(
        air.H1("Air is Grounded"),
        air.P("Built on industry standard libraries including:"),
        air.Ul(
            air.Li('FastAPI'),
            air.Li('Starlette'),
            air.Li('Pydantic'),
            air.Li('Jinja'),
        )
    )
```  

1. `app.page` used over functions named `index` are converted to the `/` route.
2. `app.page` used over functions are converted to a route based on their name, with underscores converted to dashes. 

### Variables in Paths

Variables can be added to URLs by marking them in curly braces like `{variable}` in the `application.get`, `application.post`, `application.put`, and `application.delete`  function decorators. The function receives the `{variable}` so long as it is the correct type specified by the function. 

```python hl_lines="5-6"
import air

app = air.Air()

@app.get('/users/{username}') # (1)!
def user_detail(username: str): # (2)!
    return air.layouts.mvpcss(
        air.Title(username),
        air.H1(username)
    )
```

1. We've specified a variable called `username`.
2. We have defined a function argument named `username`, which is identical to the variable specified in the decorator. We also specified the Python type in this definition.

Try it out by going to <http://localhost:8000/users/Aang>

### Variables in URLs

If you specify variables in in the function definition but not the function decorator, those become URL parameters. 

The function receives the `{variable}` so long as it is the correct type specified by the function. 

```python hl_lines="6"
import air

app = air.Air()

@app.get('/users')
def user_detail(username: str): # (1)!
    return air.layouts.mvpcss(
        air.Title(username),
        air.H1(username)
    )
```

1. We have defined a function argument named `username`, which is identical to the variable specified in the decorator. We also specified the Python type in this definition.

Try it out by going to <http://localhost:8000/users/?username=Aang>


## Air Tags

[Air Tags](learn/air_tags) are one of Air's two ways to generate HTML output. They are useful for keeping file size down, general HTML delivery, and especially with fragment responses via HTMX.


### JavaScript Files

Using Air Tags to call external JavaScript files:

```python hl_lines="7"
import air

app = air.Air()

@app.page
def index():
    return air.Script(src="https://cdn.jsdelivr.net/npm/htmx.org@2.0.7/dist/htmx.min.js")
```

### Inline Scripts

When you need to use JavaScript inline in Air Tags:


```python hl_lines="7"
import air

app = air.Air()

@app.page
def index():
    return air.Script("alert('The Last Airbender is an awesome series.')")
```

### CSS Files

Here's how to use Air Tags to call external CSS files:

```python hl_lines="9"
import air

app = air.Air()

@app.page
def index():
    return air.Html(
        air.Head(
            air.Link(rel="stylesheet", href="https://unpkg.com/mvp.css"),
        ),
        air.Body(
            air.Main(
                air.H1("Air Web Framework"),
                air.P("The web framework for Air Nomads.")
            )
        )
    )
```

### Inline CSS Styles

Inline CSS styles via Air are a good way to control design elements at runtime.

```python hl_lines="9"
import air

app = air.Air()

@app.page
def index():
    return air.Html(
        air.Head(
            air.Style("h1 {color: red;}"),
        ),
        air.Body(
            air.H1("Air Web Framework"),
            air.P("The web framework for Air Nomads.")
        )
    )
```

## Forms

In HTML, forms are the primary method of receiving data from users. Most forms receive `POST` data. Here's a basic yet workable example of receiving data using a `Request` object. 

```python hl_lines="19 20"
import air

app = air.Air()

@app.page
def index():
    return air.layouts.mvpcss(
        air.H1('Email form'),
        air.Form(
            air.Label("Email:", for_="email"),
            air.Input(type="email", name="email", required=True),
            air.Button("Submit", type="submit"),
            method="POST",
            action="/submit"
        )
    )

@app.post('/submit')
async def email_handler(request: air.Request): #(1)!
    form = await request.form() #(2)!
    return air.layouts.mvpcss(
        air.H1('Email form data'),
        air.Pre(
            air.Code(form),
            air.Code(form.keys()),
            air.Code(form.values()),
        )
    )
```

1. As Air is based off starlette, when we receive data from a form it needs to occur within an `async` view. Also, the form data is contained within the `air.Request` object.
2.Form data needs to be received via an `await` keyword on `request.form()`. 


!!! tip "FormData is a dict-like object"

    While the value `FormData([('email', 'aang@example.com')])` might be displayed, the keys and values are accessed via traditional methods.

### Validating form data with pydantic-powered AirForms

The pydantic library isn't just a component of Air and FastAPI, it's an industry standard validation library using Python type annotations to determine the validity of incoming data. Here's how to use it with AirForms, which use pydantic models to determine how a form is constructed.

```python
from pydantic import BaseModel, Field
from rich import print

import air


class ContactModel(BaseModel):
    name: str = Field(min_length=2, max_length=50)
    age: int = Field(ge=1, le=120)  # Age between 1 and 120
    email: str = Field(pattern=r"^[^@]+@[^@]+\.[^@]+$")  # Basic email pattern


class ContactForm(air.AirForm):
    model = ContactModel


app = air.Air()


@app.get("/")
async def show_form():
    """Show the form initially."""
    form = ContactForm()
    return air.layouts.mvpcss(
        air.Title("Enhanced Form Errors Demo"),
        air.Head(
            air.Title("Enhanced Form Errors Demo"),
            air.Link(rel="stylesheet", href="https://unpkg.com/@picocss/pico@latest/css/pico.min.css"),
        ),
        air.H1("Contact Form - Error Message Demo"),
        air.Form(
            form.render(),
            air.Button("Submit", type="submit"),
            method="post",
            action="/submit",
        )
    )


@app.post("/submit")
async def handle_form(request: air.Request):
    """Handle form submission and show errors."""
    form = await ContactForm.from_request(request)

    if form.is_valid:
        return air.Html(
            air.Head(air.Title("Success")),
            air.Body(
                air.H1("Success!"),
                air.P(f"Name: {form.data.name}"),
                air.P(f"Age: {form.data.age}"),
                air.P(f"Email: {form.data.email}"),
            ),
        )

    # Show form with enhanced error messages
    return air.Html(
        air.Head(
            air.Title("Enhanced Form Errors Demo"),
            air.Link(rel="stylesheet", href="https://unpkg.com/@picocss/pico@latest/css/pico.min.css"),
        ),
        air.Body(
            air.Main(
                air.H1("Contact Form - With Enhanced Error Messages"),
                air.P("Notice the specific, user-friendly error messages below:"),
                air.Form(
                    form.render(),
                    air.Button("Submit", type="submit"),
                    method="post",
                    action="/submit",
                ),
                air.Hr(),
                air.Details(
                    air.Summary("Technical Error Details (for developers)"),
                    air.Pre(str(form.errors)) if form.errors else "No errors",
                ),
                class_="container",
            )
        ),
    )

```


## Want to learn more?

Check out these documentation sections:

- [Learn](/learn)
- [API Reference](/api)

## Future Segments

What we plan to include in the Quick Start:

- [ ] Jinja
    - [ ] The Jinja + Air Tags pattern the core devs love to use
- [x] Forms: 
    - [ ] Using Pydantic-powered AirForms for validation of incoming data
    - [ ] `HTTP GET` forms, like those used in search forms
    - [ ] File uploads (part of forms)    
- [ ] HTMX basics
- [x] Routing
    - [x] Variables in URLs
    - [x] Variables in paths
- [ ] Custom exception handlers
- [ ] Sessions
- [ ] Cookies
- [ ] Large File downloads
- [ ] Server Sent Events