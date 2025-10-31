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

1. We have defined a function argument named `username`. Because `username` is not part of the decorator's URL path ('/users'), Air automatically treats it as a query parameter.

Try it out by going to <http://localhost:8000/users/?username=Aang>

### Generating URLs

Air allows you to generate URLs programmatically through the `.url()` method accessible on route functions:

```python
@app.get('/users/{username}')
def user_detail(username: str):
    return air.H1(username)

# Generate URL with path parameters
url = user_detail.url(username="Aang")
# Returns: "/users/Aang"
```

This is useful for creating links and redirects without hardcoding URLs:

```python
@app.page
def index():
    return air.layouts.mvpcss(
        air.H1("Home"),
        air.A("View user profile", href=user_detail.url(username="Aang"))
    )
```

### Other HTTP Methods

!!! warning

    By default all HTML forms can only send `GET` and `POST` requests. If you set the form method to something else, like `PUT`, `PATCH`, or `DELETE`, the browser will actually fall back to a GET request. However, the magic of HTMX allows you to send other HTTP methods from forms and links.


Air supports the `PATCH`, `PUT`, or `DELETE` methods natively:

```python hl_lines="1 5 9"
@app.patch('/partial-update/{slug}')
async def partial_update(request: air.Request, slug: str): # (1)!
    ...

@app.put('/create-item')
async def create_item(request: air.Request): # (2)!
    ...

@app.delete('/delete/{slug}')
async def delete_item(request: air.Request, slug: str): # (3)!
    ...
```

1. `PATCH` requests are used for partial updates of resources, such as one field being updated. The `slug` variable in the URL is passed as an argument to the function. While `POST` requests can be used for updates and is the classic method, `PATCH` is more specific to the action being taken.

2. `PUT` requests are used for creating or replacing resources. The function can handle the incoming data, typically from the request body. Like `POST`, `PUT` requests usually require `async` functions and an `air.Request` argument.

3. `DELETE` requests are used to delete resources. Similar to `PATCH`, the `slug` variable in the URL is passed as an argument to the function.

## Air Tags

[Air Tags](../learn/air_tags.md) are one of Air's two ways to generate HTML output. They are useful for keeping file size down, general HTML delivery, and especially with fragment responses via HTMX.


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

## Jinja

In addition to Air Tags, Air supports Jinja natively. In addition to being great at delivering HTML content, Jinja can be used to render all kinds of content.

Here's a simple Jinja template:

```html+jinja title="templates/base.html"
<!doctype html>
<html>
    <body>
        <main class="container">
          <h1>{{title}}</h1>
          <p>{{message}}</p>
        </main>
    </body>
</html>
```

And here's the view that calls it:


```python title="main.py"  hl_lines="6 10 14 16"
import air

app = air.Air()

# Set the Jinja render function
jinja = air.JinjaRenderer(directory="templates") #(1)!

@app.page
def index(request: air.Request):
    return jinja( #(2)!
        request,
        name="base.html",
        # You can pass in individual keyword arguments
        title="Hello, Air Benders", #(3)!
        # Or a dict for the context
        context={"message": "Air + Jinja is awesome"} #(4)!
    )
```

1. This sets up the Jinja environment for calling and rendering of templates.
2. Air automatically handles turning the `jinja` response into an HTML response.
3. Individual keyword arguments for values can be passed, these are added to the Jinja template's context dictionary.
4. This is the standard Jinja context dictionary, which is added to each template.

### Jinja + Air Tags

It is very easy to include Air Tags in Jinja. Let's first create our template:

```jinja title="templates/avatar.html"  hl_lines="6"
<!doctype html>
<html>
    <body>
        <main class="container">
          <h1>{{title}}</h1>
          {{fragment|safe}} {# (1)! #}
        </main>
    </body>
</html>
```

1. The `safe` filter is necessary for using Air Tags in Jinja. This has security implications, so be careful what content you allow.

And here is our Python code describing the view:

```python title="main.py"  hl_lines="13-16"
import air

app = air.Air()

jinja = air.JinjaRenderer(directory="templates")

@app.get("/avatar")
def avatar(request: air.Request):
    return jinja(
        request,
        name="avatar.html",
        title="Hello, Air Benders",
        fragment=air.Div(
            air.P("We are fans of the Last Avatar"),
            class_="thing"
        ) #(1)!
    )
```

1. We can pass Air Tags into the context of a Jinja template.

!!! tip

    Where Jinja + Air Tags truly come alive is when the base templates for a project are in Jinja. For some people this makes styling pages a bit easier. Then content, especially HTMX swaps and other fragments are rendered via Air Tags. This keeps the developer in Python, which means less context switching while working on challenges.



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

### AirForms: pydantic+forms

The pydantic library isn't just a component of Air and FastAPI, it's an industry standard validation library using Python type annotations to determine the validity of incoming data. Here's how to use it with AirForms, which use pydantic models to determine how a form is constructed.

```python
from pydantic import BaseModel, Field
import air

class ContactModel(BaseModel): #(1)!
    name: str = Field(min_length=2, max_length=50)
    age: int = Field(ge=1, le=120)  # Age between 1 and 120
    email: str = Field(pattern=r"^[^@]+@[^@]+\.[^@]+$")  # Basic email pattern

class ContactForm(air.AirForm): #(2)!
    model = ContactModel

app = air.Air()

@app.page
async def index():
    """Show the form initially."""
    form = ContactForm() #(3)!
    return air.layouts.picocss(
        air.Title("Enhanced Form Errors Demo"),
        air.H1("Contact Form - Error Message Demo"),
        air.Form(
            form.render(), #(4)!
            air.Button("Submit", type="submit"),
            method="post",
            action="/submit",
        )
    )

@app.post("/submit")
async def handle_form(request: air.Request):
    """Handle form submission and show errors."""
    form = await ContactForm.from_request(request) #(5)!

    if form.is_valid:  #(6)!
        return air.layouts.picocss(
            air.Title("Success"),
            air.H1("Success!"),
            air.P(f"Name: {form.data.name}"),
            air.P(f"Age: {form.data.age}"),
            air.P(f"Email: {form.data.email}"),
        )

    # Show form with enhanced error messages
    return air.layouts.picocss(
        air.Title("Enhanced Form Errors Demo"),
        air.H1("Contact Form - With Enhanced Error Messages"),
        air.P("Notice the specific, user-friendly error messages below:"),
        air.Form(
            form.render(), #(7)!
            air.Br(),
            air.Button("Submit", type="submit"),
            method="post",
            action="/submit",
        ),
        air.Hr(),
        air.Details(
            air.Summary("Technical Error Details (for developers)"),
            air.P(str(form.errors)) if form.errors else "No errors",
        )
    )
```

1. `ContactModel` is a pydantic model that represents data we want to collect from the user.
2. `ContactForm` is an `AirForm` whose model is the `ContactModel`.
3. This instantiates the form without data.
4. Calling `.render()` on an AirForm generates the form in HTML. This follows a common pattern in Air with `.render()` methods.
5. AirForms have `.from_request()` method which takes the form from an `air.Request` and loads it into the form.
6. The `.is_valid` property of an AirForm is powered by pydantic. It returns a `bool` that can be used to control logic of what to do with form successes or failures.
7. Calling `.render()` on an AirForm generates the form in HTML. This follows a common pattern in Air with `.render()` methods.

## Server-Sent Events

Part of the HTTP specification, Server-Sent Events (SSE) allow the server to push things to the user. Air makes SSE easy to implement and maintain. Here's an example of using it to generate random lottery numbers every second.

```python hl_lines="11 16 17 18 19 23 27 33"
import random
from asyncio import sleep

import air

app = air.Air()

@app.page
def index():
    return air.layouts.mvpcss(
        air.Script(src="https://unpkg.com/htmx-ext-sse@2.2.1/sse.js"), #(1)!
        air.Title("Server Sent Event Demo"),
        air.H1("Server Sent Event Demo"),
        air.P("Lottery number generator"),
        air.Section(
            hx_ext="sse",  #(2)!
            sse_connect="/lottery-numbers", #(3)!
            hx_swap="beforeend show:bottom", #(4)!
            sse_swap="message", #(5)!
        ),
    )

async def lottery_generator():  #(6)!
    while True:
        lottery_numbers = ", ".join([str(random.randint(1, 40)) for x in range(6)])
        # Tags work seamlessly
        yield air.Aside(lottery_numbers) #(7)!
        await sleep(1)


@app.page
async def lottery_numbers():
    return air.SSEResponse(lottery_generator())  #(8)!
```

1. To use SSE, the source for the HTMX plugin for them has to be included in the page.
2. The `hx_ext` attribute is used to initialize the SSE plugin.
3. `sse_connect` is the endpoint where the SSE pushes from.
4. `hx_swap` tells HTMX how to swap or place elements. In this case, it says to place the incoming HTML underneath all the other content in this section. The move the focus of the page to that location.
5. The `sse_swap` attribute informs HTMX that we only want to receive SSE events of the `message` type. This is a common response and shouldn't be changed unless you have a good reason.
6. The `air.SSEResponse` needs a generator function or generator expression. Our example just generates random numbers, but people use similar functions to query databases and fetch data from APIs. Of note is that in our example instead of using `return` statements we use `yield` statements to ensure control is not lost.
7. Air Tags work great, but any type of data can be passed back.
8. Air does all  heavy lifting of setting up a streaming response for us. All we need to do is pass generator functions or generator expressions into it and it just works!


## Want to learn more?

Check out these documentation sections:

- [Learn](../learn/index.md)
- [API Reference](../api/index.md)

## Future Segments

What we plan to include in the Quick Start:

- [x] Jinja
    - [x] The Jinja + Air Tags pattern the core devs love to use
- [x] Forms:
    - [x] Using Pydantic-powered AirForms for validation of incoming data
    - [ ] `HTTP GET` forms, like those used in search forms
    - [ ] File uploads (part of forms)
- [ ] HTMX basics
- [x] Routing
    - [x] Variables in URLs
    - [x] Variables in paths
    - [x] Generating URLs
- [ ] Custom exception handlers
- [ ] Sessions
- [ ] Cookies
- [ ] Large File downloads
- [x] Server Sent Events
