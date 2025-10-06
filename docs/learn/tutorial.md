# The Air Web Framework: A Complete Guide

Welcome to **The Air Web Framework: A Complete Guide** - your comprehensive resource for building modern web applications with Air. This book will transform you from a beginner to an expert in creating beautiful, interactive web applications that combine HTML pages with REST APIs using the Air framework.

Air is a friendly layer over FastAPI, making it easy to create both interactive sites and robust APIs—all in one seamless app. In this book, you'll learn to build real-world applications that demonstrate the power and elegance of the Air framework.

## About This Book

This book is designed to be both a comprehensive tutorial and a reference manual. You'll progress from basic concepts to advanced patterns, with each chapter building upon the previous one. By the end of this book, you'll have the knowledge to build sophisticated web applications using Air's powerful features.

## Table of Contents

1. [Introduction to Air](#introduction-to-air)
2. [Getting Started](#getting-started)
3. [Core Concepts: Air Tags and Layouts](#core-concepts)
4. [Building Our Blog Application](#building-our-blog-application)
5. [Advanced Routing and URL Management](#advanced-routing)
6. [Forms and Data Validation](#forms-and-data-validation)
7. [Working with Databases](#working-with-databases)
8. [API Development](#api-development)
9. [HTMX and Interactive Interfaces](#htmx-and-interactive-interfaces)
10. [Authentication and Security](#authentication-and-security)
11. [Testing](#testing)
12. [Deployment](#deployment)
13. [Advanced Patterns and Best Practices](#advanced-patterns)

---

## Introduction to Air

### What is Air?

Air is a Python web framework built on top of FastAPI that makes it easy to build both beautiful HTML interfaces and powerful REST APIs in a single application. It combines the elegance of Python with the power of FastAPI's ecosystem, offering a fresh approach to web development.

### Key Features of Air

1. **Air Tags**: Python classes that generate HTML, providing type safety and IDE autocompletion.
2. **Layouts**: Automatic separation of head and body content with built-in styling options.
3. **Easy Routing**: Simplified URL mapping with both standard and path-based routing.
4. **Form Handling**: Built-in form validation using Pydantic models.
5. **HTMX Integration**: Seamless integration with HTMX for modern, dynamic interfaces.
6. **Jinja Support**: Ability to mix Air Tags with traditional Jinja templates.
7. **Database Agnostic**: Works with any Python database library.
8. **API First**: Built-in support for creating REST APIs alongside HTML interfaces.

### Why Choose Air?

Air is designed for developers who want to:
- Build modern, interactive web applications quickly
- Leverage the power of FastAPI without the complexity of pure HTML responses
- Create both HTML interfaces and APIs in a single codebase
- Have type safety and IDE support throughout their development process
- Work with clean, Pythonic syntax rather than mixing HTML and Python

### Philosophy of Air

Air follows several key principles:
1. **Developer Experience First**: Prioritizes intuitive, easy-to-use APIs
2. **Pythonic**: Uses Python's natural syntax and conventions
3. **Type-Safe**: Leverages Python's type hints for better development experience
4. **Flexible**: Accommodates different architectural patterns and preferences
5. **Fast Development**: Reduces boilerplate and speeds up common tasks

---

## Getting Started

### Prerequisites

Before we begin, you'll need:
1. Python 3.11 or higher (3.14 is recommended)
2. [uv](https://docs.astral.sh/uv/getting-started/installation/#installing-uv) (recommended for dependency management)
3. A code editor like [VS Code](https://code.visualstudio.com/)
4. Basic knowledge of Python and web development concepts

### Installing Air

Let's start by creating a new project. At the command line, create your project:

```bash
uv init airblog
```

Enter the new directory:

```bash
cd airblog
```

Initialize a virtual environment in which we can install dependencies:

```bash
uv venv
```

Activate the virtual environment (instructions will vary based on your operating system). For Unix systems, run:

```bash
source .venv/bin/activate
```

Now install Air:

```bash
uv add "air[standard]"
```

### Your First Air App

Delete the content of the `main.py` that `uv` created. Let's start by replacing it with the simplest possible Air application:

```python title="main.py"
import air

app = air.Air()

@app.page
def index():
    title = "My Blog"
    return air.layouts.mvpcss(
        air.Head(air.Title(title)),
        air.H1(title),
        air.P("Welcome to my awesome Air-powered blog."),
    )
```

Let's see what this looks like. Run the following command to start the development server:

```bash
fastapi dev
```

Open your page by clicking this link: <a href="http://localhost:8000/" target="_blank">http://localhost:8000/</a>

!!! question "Why are we using fastapi to run Air?"

    Air is built on top of FastAPI, so we use the `fastapi` CLI command to run our Air application. This allows us to leverage FastAPI's powerful features while enjoying the simplicity and elegance of Air for building our web pages.

### Understanding Your First Application

Let's break down what's happening in this code:

1. **Import**: `import air` imports the Air framework
2. **App Creation**: `app = air.Air()` creates a new Air application instance
3. **Decorator**: `@app.page` is a decorator that tells Air to handle requests to the root path (`/`)
4. **Function**: `index()` is the function that processes the request and returns the response
5. **Layout**: `air.layouts.mvpcss()` provides a complete HTML document structure with basic styling

The `mvpcss` layout function automatically:
- Wraps content in proper HTML structure
- Includes MVP.css for basic styling
- Includes HTMX for interactive features
- Separates head and body content automatically

### Air Tags Explained

Air Tags are Python classes that generate HTML. Each tag (like `H1`, `P`, `Div`) corresponds to an HTML element. When you create an instance of an Air Tag, it renders to the corresponding HTML:

```python
air.H1("Hello, World!")  # Renders as <h1>Hello, World!</h1>
air.P("This is a paragraph")  # Renders as <p>This is a paragraph</p>
```

Air Tags are type-safe and provide IDE autocompletion, making it easier to write correct HTML.

---

## Core Concepts

### Air Tags: The Foundation of Air

Air Tags are the primary method for generating HTML in Air applications. Each tag class corresponds to an HTML element and provides a Pythonic interface to create that element.

#### Basic Tag Usage

```python
# Simple tags
air.H1("Main Header")
air.P("This is a paragraph")
air.Div("This is a division")

# Tags with attributes
air.A("Click here", href="/page", class_="button primary")
air.Img(src="image.jpg", alt="An image", width="300", height="200")
air.Input(type="text", name="username", required=True)
```

#### Nested Tags

Tags can be nested by passing child tags as arguments:

```python
air.Div(
    air.H2("Section Title"),
    air.P("Some content here"),
    air.Button("Submit", type="submit")
)
```

#### Attributes and the Underscore Convention

In Air Tags, HTML attributes that conflict with Python keywords are suffixed with an underscore:

- `class` becomes `class_`
- `for` becomes `for_`
- `id` remains `id`
- `type` remains `type`

```python
air.Label("Username", for_="username-field")
air.Div(class_="container", id="main-content")
```

### Layouts: Structuring Complete Documents

Air's layout system automatically handles the separation of head and body content, eliminating boilerplate and making it easy to create complete HTML documents.

#### How Layout Filtering Works

Air layouts use intelligent filtering to determine which tags belong in the head and which belong in the body:

- **Head tags**: `Title`, `Style`, `Meta`, `Link`, `Script`, `Base`
- **Body tags**: All other tags

```python
# Without layout (manual creation)
air.Html(
    air.Head(
        air.Title("My App"),
        air.Link(rel="stylesheet", href="style.css")
    ),
    air.Body(
        air.H1("Welcome"),
        air.P("Content here")
    )
)

# With layout (automatic separation)
air.layouts.mvpcss(
    air.Title("My App"),           # Automatically goes to <head>
    air.Link(rel="stylesheet", href="style.css"),  # Also goes to <head>
    air.H1("Welcome"),             # Goes to <body>
    air.P("Content here")          # Also goes to <body>
)
```

#### Built-in Layouts

Air provides several built-in layouts for rapid prototyping:

1. **mvpcss**: Uses MVP.css for minimal styling
2. **picocss**: Uses PicoCSS for slightly more sophisticated styling

Both layouts include HTMX by default for interactive features.

#### Creating Custom Layouts

For production applications, you'll often want to create custom layouts. Here's the pattern:

```python
import air

def my_custom_layout(*children):
    # Separate head and body content
    head_tags = air.layouts.filter_head_tags(children)
    body_tags = air.layouts.filter_body_tags(children)
    
    # Build your custom structure
    return air.Html(
        air.Head(
            # Your custom head content
            air.Link(rel="stylesheet", href="/css/custom.css"),
            air.Script(src="/js/custom.js"),
            *head_tags  # User's head tags
        ),
        air.Body(
            air.Header("My App"),
            air.Main(*body_tags),  # User's body content
            air.Footer("© 2024 My App")
        ),
    )
```

### The App Object

The `air.Air()` object is the core of every Air application. It inherits from FastAPI but is configured with Air-specific defaults.

#### Common Configuration Options

```python
app = air.Air(
    debug=True,  # Enable debug mode
    docs_url="/docs",  # Swagger UI endpoint
    redoc_url="/redoc",  # ReDoc endpoint
    path_separator="-"  # How to convert function names to URLs
)
```

---

## Building Our Blog Application

### Project AirBlog

We're going to create a markdown file-powered blogging platform called AirBlog. It will have:

1. A web interface for reading blog posts
2. A REST API for programmatic access to blog posts
3. Administrative interface for managing posts

### Creating Article Files

First, let's create a directory to store our blog articles and some sample content:

Create a new directory called `articles` in the root of your project. Inside this directory, create a new file called `hello-world.md` with the following content:

```markdown title="articles/hello-world.md"
---
title: Hello World
description: A simple example of an Air application that responds with "Hello, World!".
slug: hello-world
published: true
date: 2025-09-26
author: Daniel Roy Greenfeld
tags:
- example
- beginner
- tutorial
---

Let's create a simple AirBlog application powered by Markdown.

```python
for i in range(10):
    print("Hello, World!")
```
```

The file has two sections:
- **Frontmatter**: Delimited by `---` lines, contains metadata like title, description, slug, etc.
- **Content**: The main body of the article, written in Markdown format

Create another file called `markdown-features.md`:

```markdown title="articles/markdown-features.md"
---
title: Markdown features
description: A page for showing off all the things markdown renders to.
slug: markdown-features
published: true
date: 2025-09-27
author: Daniel Roy Greenfeld
tags:
- example
- beginner
- tutorial
- markdown
---

# H1 title

A paragraph with **bold** text, *italic* text, and `inline code`.

# H2 title

A list of items:

- one
- two
- three

# H3 title

A numbered list:

1. First item
2. Second item
3. Third item

A blockquote:

> This is a blockquote.
```

### Reading Articles into Our Application

To read the articles from the `articles` directory, we'll use the `pathlib` and `python-frontmatter` libraries. First, install the frontmatter library:

```bash
uv add python-frontmatter
```

Now, let's modify our `main.py` file to read the articles and display them on the homepage:

```python title="main.py"
from pathlib import Path
from frontmatter import Frontmatter
import air


def get_articles() -> list[dict]:
    """Read all markdown files in the articles directory and return their content."""
    articles = []
    # Read all markdown files in the articles directory
    for path in Path("articles").glob("*.md"):
        # Parse the frontmatter and content of each file
        # then add it to the articles list
        articles.append(Frontmatter.read_file(path))
    # Sort articles by date in descending date order
    return sorted(articles, key=lambda x: x["attributes"]["date"], reverse=True)


app = air.Air()

@app.page
def index():
    title = "AirBlog!"
    articles = get_articles()
    return air.layouts.mvpcss(
        air.Head(air.Title(title)),
        air.H1(title),
        air.P("Your go-to platform for blogging with Air."),
        air.Ul(
            *[
                air.Li(
                    air.A(
                        article["attributes"]["title"],
                        href=f'/{article["attributes"]["slug"]}',
                    ),
                    air.Br(),
                    air.Small(article["attributes"]["description"]),
                    air.Br(),
                    air.Time(
                        f'Published: {article["attributes"]["date"]}', 
                        datetime=str(article["attributes"]["date"])
                    )
                )
                for article in articles
            ]
        )
    )
```

### Creating Article Detail Pages

Now let's add individual pages for each article. We'll modify our `main.py` to include a route for each article:

```python title="main.py"
from pathlib import Path
from frontmatter import Frontmatter
import markdown
import air


def get_articles() -> list[dict]:
    """Read all markdown files in the articles directory and return their content."""
    articles = []
    for path in Path("articles").glob("*.md"):
        articles.append(Frontmatter.read_file(path))
    return sorted(articles, key=lambda x: x["attributes"]["date"], reverse=True)


def get_article(slug: str) -> dict | None:
    """Get a specific article by its slug."""
    for article in get_articles():
        if article["attributes"]["slug"] == slug:
            return article
    return None


app = air.Air()

@app.page
def index():
    title = "AirBlog!"
    articles = get_articles()
    return air.layouts.mvpcss(
        air.Head(air.Title(title)),
        air.H1(title),
        air.P("Your go-to platform for blogging with Air."),
        air.H2("Latest Articles"),
        air.Ul(
            *[
                air.Li(
                    air.A(
                        article["attributes"]["title"],
                        href=f'/{article["attributes"]["slug"]}',
                        style="font-size: 1.2em; font-weight: bold;"
                    ),
                    air.Br(),
                    air.Small(article["attributes"]["description"]),
                    air.Br(),
                    air.Time(
                        f'Published: {article["attributes"]["date"]}', 
                        datetime=str(article["attributes"]["date"]),
                        style="color: #666;"
                    )
                )
                for article in articles
            ]
        )
    )


@app.get("/{slug}")
def article_detail(slug: str):
    """Display a single article."""
    article = get_article(slug)
    if not article:
        return air.layouts.mvpcss(
            air.H1("Article not found"),
            air.P("The requested article could not be found.")
        )
    
    # Convert markdown content to HTML
    html_content = markdown.markdown(article["body"])
    
    return air.layouts.mvpcss(
        air.Title(article["attributes"]["title"]),
        air.Article(
            air.H1(article["attributes"]["title"]),
            air.Time(
                f'Published: {article["attributes"]["date"]}',
                datetime=str(article["attributes"]["date"])
            ),
            air.P(f"By {article['attributes']['author']}"),
            air.Div(air.Raw(html_content))
        ),
        air.Nav(
            air.A("← Back to Home", href="/")
        )
    )
```

First, install the markdown library to convert Markdown to HTML:

```bash
uv add markdown
```

### Adding a Contact Form

Let's add a contact form to our application to demonstrate form handling:

```python title="main.py"
from pathlib import Path
from frontmatter import Frontmatter
import markdown
from datetime import datetime
import air


def get_articles() -> list[dict]:
    """Read all markdown files in the articles directory and return their content."""
    articles = []
    for path in Path("articles").glob("*.md"):
        articles.append(Frontmatter.read_file(path))
    return sorted(articles, key=lambda x: x["attributes"]["date"], reverse=True)


def get_article(slug: str) -> dict | None:
    """Get a specific article by its slug."""
    for article in get_articles():
        if article["attributes"]["slug"] == slug:
            return article
    return None


app = air.Air()

@app.page
def index():
    title = "AirBlog!"
    articles = get_articles()
    return air.layouts.mvpcss(
        air.Head(air.Title(title)),
        air.Header(
            air.Nav(
                air.A("AirBlog", href="/", style="font-size: 1.5em; font-weight: bold;"),
                air.Span(" | ", style="margin: 0 10px;"),
                air.A("Contact", href="/contact")
            )
        ),
        air.H1(title),
        air.P("Your go-to platform for blogging with Air."),
        air.H2("Latest Articles"),
        air.Ul(
            *[
                air.Li(
                    air.A(
                        article["attributes"]["title"],
                        href=f'/{article["attributes"]["slug"]}',
                        style="font-size: 1.2em; font-weight: bold;"
                    ),
                    air.Br(),
                    air.Small(article["attributes"]["description"]),
                    air.Br(),
                    air.Time(
                        f'Published: {article["attributes"]["date"]}', 
                        datetime=str(article["attributes"]["date"]),
                        style="color: #666;"
                    )
                )
                for article in articles
            ]
        )
    )


@app.get("/{slug}")
def article_detail(slug: str):
    """Display a single article."""
    article = get_article(slug)
    if not article:
        return air.layouts.mvpcss(
            air.H1("Article not found"),
            air.P("The requested article could not be found.")
        )
    
    # Convert markdown content to HTML
    html_content = markdown.markdown(article["body"])
    
    return air.layouts.mvpcss(
        air.Title(article["attributes"]["title"]),
        air.Article(
            air.H1(article["attributes"]["title"]),
            air.Time(
                f'Published: {article["attributes"]["date"]}',
                datetime=str(article["attributes"]["date"])
            ),
            air.P(f"By {article['attributes']['author']}"),
            air.Div(air.Raw(html_content))
        ),
        air.Nav(
            air.A("← Back to Home", href="/")
        )
    )


@app.page
def contact():
    """Contact form page."""
    return air.layouts.mvpcss(
        air.Title("Contact Us"),
        air.H1("Contact Us"),
        air.Form(
            air.Div(
                air.Label("Name", for_="name"),
                air.Input(type="text", name="name", required=True),
            ),
            air.Div(
                air.Label("Email", for_="email"),
                air.Input(type="email", name="email", required=True),
            ),
            air.Div(
                air.Label("Message", for_="message"),
                air.Textarea(name="message", required=True, rows=5),
            ),
            air.Button("Submit", type="submit"),
            method="POST",
            action="/contact",
            style="display: flex; flex-direction: column; gap: 1rem;"
        ),
        air.Nav(
            air.A("← Back to Home", href="/")
        )
    )


@app.post("/contact")
async def contact_handler(request: air.Request):
    """Handle form submission."""
    form_data = await request.form()
    
    # In a real application, you would process the form data here
    # (e.g., save to database, send email, etc.)
    
    name = form_data.get("name")
    email = form_data.get("email")
    message = form_data.get("message")
    
    return air.layouts.mvpcss(
        air.H1("Thank You!"),
        air.P(f"We have received your message, {name}!"),
        air.P("We'll get back to you soon."),
        air.Nav(
            air.A("← Back to Home", href="/"),
            air.Span(" | ", style="margin: 0 10px;"),
            air.A("Send Another Message", href="/contact")
        )
    )
```

### Adding an API Endpoint

Let's add a REST API endpoint to access our articles programmatically:

```python title="main.py"
from pathlib import Path
from frontmatter import Frontmatter
import markdown
from datetime import datetime
from typing import List
import air


def get_articles() -> list[dict]:
    """Read all markdown files in the articles directory and return their content."""
    articles = []
    for path in Path("articles").glob("*.md"):
        articles.append(Frontmatter.read_file(path))
    return sorted(articles, key=lambda x: x["attributes"]["date"], reverse=True)


def get_article(slug: str) -> dict | None:
    """Get a specific article by its slug."""
    for article in get_articles():
        if article["attributes"]["slug"] == slug:
            return article
    return None


app = air.Air()

@app.page
def index():
    title = "AirBlog!"
    articles = get_articles()
    return air.layouts.mvpcss(
        air.Header(
            air.Nav(
                air.A("AirBlog", href="/", style="font-size: 1.5em; font-weight: bold;"),
                air.Span(" | ", style="margin: 0 10px;"),
                air.A("Contact", href="/contact"),
                air.Span(" | ", style="margin: 0 10px;"),
                air.A("API", href="/api/docs", target="_blank")
            )
        ),
        air.Head(air.Title(title)),
        air.H1(title),
        air.P("Your go-to platform for blogging with Air."),
        air.H2("Latest Articles"),
        air.Ul(
            *[
                air.Li(
                    air.A(
                        article["attributes"]["title"],
                        href=f'/{article["attributes"]["slug"]}',
                        style="font-size: 1.2em; font-weight: bold;"
                    ),
                    air.Br(),
                    air.Small(article["attributes"]["description"]),
                    air.Br(),
                    air.Time(
                        f'Published: {article["attributes"]["date"]}', 
                        datetime=str(article["attributes"]["date"]),
                        style="color: #666;"
                    )
                )
                for article in articles
            ]
        )
    )


@app.get("/{slug}")
def article_detail(slug: str):
    """Display a single article."""
    article = get_article(slug)
    if not article:
        return air.layouts.mvpcss(
            air.H1("Article not found"),
            air.P("The requested article could not be found.")
        )
    
    # Convert markdown content to HTML
    html_content = markdown.markdown(article["body"])
    
    return air.layouts.mvpcss(
        air.Title(article["attributes"]["title"]),
        air.Article(
            air.H1(article["attributes"]["title"]),
            air.Time(
                f'Published: {article["attributes"]["date"]}',
                datetime=str(article["attributes"]["date"])
            ),
            air.P(f"By {article['attributes']['author']}"),
            air.Div(air.Raw(html_content))
        ),
        air.Nav(
            air.A("← Back to Home", href="/")
        )
    )


@app.page
def contact():
    """Contact form page."""
    return air.layouts.mvpcss(
        air.Title("Contact Us"),
        air.H1("Contact Us"),
        air.Form(
            air.Div(
                air.Label("Name", for_="name"),
                air.Input(type="text", name="name", required=True),
            ),
            air.Div(
                air.Label("Email", for_="email"),
                air.Input(type="email", name="email", required=True),
            ),
            air.Div(
                air.Label("Message", for_="message"),
                air.Textarea(name="message", required=True, rows=5),
            ),
            air.Button("Submit", type="submit"),
            method="POST",
            action="/contact",
            style="display: flex; flex-direction: column; gap: 1rem;"
        ),
        air.Nav(
            air.A("← Back to Home", href="/")
        )
    )


@app.post("/contact")
async def contact_handler(request: air.Request):
    """Handle form submission."""
    form_data = await request.form()
    
    name = form_data.get("name")
    email = form_data.get("email")
    message = form_data.get("message")
    
    return air.layouts.mvpcss(
        air.H1("Thank You!"),
        air.P(f"We have received your message, {name}!"),
        air.P("We'll get back to you soon."),
        air.Nav(
            air.A("← Back to Home", href="/"),
            air.Span(" | ", style="margin: 0 10px;"),
            air.A("Send Another Message", href="/contact")
        )
    )


# API Endpoints
@app.get("/api/articles")
def api_articles():
    """Return all articles as JSON."""
    articles = get_articles()
    # Return only the attributes, not the full frontmatter object
    return {
        "articles": [
            {
                "title": article["attributes"]["title"],
                "slug": article["attributes"]["slug"],
                "description": article["attributes"]["description"],
                "date": article["attributes"]["date"],
                "author": article["attributes"]["author"],
                "tags": article["attributes"]["tags"]
            }
            for article in articles
        ]
    }


@app.get("/api/articles/{slug}")
def api_article_detail(slug: str):
    """Return a specific article as JSON."""
    article = get_article(slug)
    if not article:
        return air.responses.JSONResponse(
            {"error": "Article not found"}, 
            status_code=404
        )
    
    return {
        "title": article["attributes"]["title"],
        "slug": article["attributes"]["slug"],
        "description": article["attributes"]["description"],
        "date": article["attributes"]["date"],
        "author": article["attributes"]["author"],
        "tags": article["attributes"]["tags"],
        "content": article["body"]
    }

```

---

## Advanced Routing

Air provides multiple ways to define routes, making it easy to handle various URL patterns and request methods.

### HTTP Methods

In addition to `@app.get`, Air supports all standard HTTP methods:

```python
@app.get("/{slug}")          # GET requests
@app.post("/{slug}")         # POST requests
@app.put("/{slug}")          # PUT requests
@app.delete("/{slug}")       # DELETE requests
@app.patch("/{slug}")        # PATCH requests
@app.head("/{slug}")         # HEAD requests
@app.options("/{slug}")      # OPTIONS requests
```

### Path Parameters

Path parameters are values extracted from the URL path:

```python
@app.get('/users/{user_id}/posts/{post_id}')
def post_detail(user_id: int, post_id: int):
    # Process user_id and post_id
    return air.P(f"Post {post_id} for user {user_id}")
```

### Query Parameters

Query parameters are values passed in the URL after `?`:

```python
@app.get('/search')
def search(query: str, page: int = 1, limit: int = 10):
    # Process the search parameters
    return air.P(f"Searching for '{query}' on page {page}")
```

### Mixed Parameters

You can combine path and query parameters:

```python
@app.get('/users/{user_id}')
def user_detail(user_id: int, include_posts: bool = False):
    # user_id from path, include_posts from query string
    if include_posts:
        return air.P(f"User {user_id} with posts")
    return air.P(f"User {user_id} without posts")
```

### Request Data

You can receive different types of request data:

```python
# Form data (from POST requests with Content-Type: application/x-www-form-urlencoded)
@app.post('/submit')
async def handle_form(request: air.Request):
    form_data = await request.form()
    return air.P(f"Form data: {form_data}")

# JSON data (from POST requests with Content-Type: application/json)
@app.post('/api/data')
async def handle_json(request: air.Request):
    json_data = await request.json()
    return air.P(f"JSON data: {json_data}")
    
# Raw body data
@app.post('/raw')
async def handle_raw(request: air.Request):
    body = await request.body()
    return air.P(f"Body: {body}")
```

### Path Separator Configuration

Air uses hyphens as path separators by default, but you can configure this:

```python
app = air.Air(path_separator="/")  # Use slashes instead of hyphens

@app.page
def my_page():  # Will route to /my/page instead of /my-page
    return air.P("This uses slash separators")
```

---

## Forms and Data Validation

Air provides powerful form handling capabilities with built-in validation using Pydantic.

### Basic Form Handling

Basic form handling in Air follows the Starlette pattern:

```python
@app.post("/submit-form")
async def submit_form(request: air.Request):
    form_data = await request.form()
    name = form_data.get("name")
    email = form_data.get("email")
    return air.P(f"Hello {name}, your email is {email}")
```

### Air Forms with Pydantic

Air provides `AirForm` and `AirField` for more powerful form handling with Pydantic validation:

```python
from pydantic import BaseModel, Field
from air import AirForm, AirField


class ContactModel(BaseModel):
    name: str = Field(..., min_length=2, max_length=50, description="Your name")
    email: str = AirField(type="email", label="Email Address", required=True)
    subject: str = Field(..., min_length=5, max_length=100, description="Subject of your message")
    message: str = Field(..., min_length=10, max_length=1000, description="Your message")


class ContactForm(AirForm):
    model = ContactModel


# Create an instance of the form
contact_form = ContactForm()


@app.page
def contact():
    """Contact form page with validation."""
    return air.layouts.mvpcss(
        air.Title("Contact Us"),
        air.H1("Contact Us"),
        air.Form(
            contact_form.render(),  # Render the form
            method="POST",
            action="/contact"
        ),
        air.Nav(
            air.A("← Back to Home", href="/")
        )
    )


@app.post("/contact")
async def contact_handler(request: air.Request):
    """Handle form submission with validation."""
    form_data = await request.form()
    
    # Validate the form
    if contact_form.validate(form_data):
        # Process valid data
        validated_data = contact_form.model.model_dump()
        return air.layouts.mvpcss(
            air.H1("Thank You!"),
            air.P(f"Your message has been sent, {validated_data['name']}!")
        )
    else:
        # Form has errors, re-render with errors
        return air.layouts.mvpcss(
            air.Title("Contact Us - Error"),
            air.H1("Contact Us"),
            air.P("Please correct the errors below:"),
            air.Form(
                contact_form.render(),  # Renders errors too
                method="POST",
                action="/contact"
            ),
            air.Nav(
                air.A("← Back to Home", href="/")
            )
        )
```

### Form Field Types and Validation

Air Forms support various field types with automatic validation:

```python
class UserForm(AirForm):
    class model(BaseModel):
        # Text fields
        name: str = Field(..., min_length=2, max_length=50)
        bio: str | None = Field(None, max_length=200)
        
        # Email field with validation
        email: str = AirField(type="email", label="Email Address")
        
        # Number fields
        age: int = Field(..., ge=13, le=120, description="Your age")
        score: float = Field(..., ge=0.0, le=100.0, description="Score")
        
        # Boolean fields (checkboxes)
        agreed_to_terms: bool = AirField(type="checkbox", required=True, label="Agree to terms")
        
        # Choice fields (dropdowns)
        gender: str = AirField(
            type="select", 
            choices=["male", "female", "other"],
            label="Gender"
        )
        
        # Date fields
        birth_date: str = AirField(type="date", label="Birth Date")
        
        # URL fields
        website: str | None = AirField(type="url", label="Website")
```

### Custom Validation

You can add custom validation methods:

```python
from pydantic import BaseModel, Field, field_validator


class RegistrationForm(AirForm):
    class model(BaseModel):
        username: str = Field(..., min_length=3, max_length=30)
        email: str = AirField(type="email", label="Email Address")
        password: str = Field(..., min_length=8)
        confirm_password: str = Field(..., min_length=8)
        
        @field_validator('username')
        def validate_username(cls, v):
            if ' ' in v:
                raise ValueError('Username cannot contain spaces')
            return v
            
        @field_validator('confirm_password')
        def passwords_match(cls, v, info):
            if v != info.data.get('password'):
                raise ValueError('Passwords do not match')
            return v
```

---

## Working with Databases

Air is database-agnostic and works with any Python database library. Here's how to integrate common database solutions:

### Using SQLAlchemy

Let's add database functionality to our blog:

```bash
uv add sqlalchemy "psycopg2-binary"
```

```python
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime

# Database setup
DATABASE_URL = "sqlite:///./airblog.db"
engine = create_engine(DATABASE_URL)
Base = declarative_base()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Database models
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    posts = relationship("Post", back_populates="author")

class Post(Base):
    __tablename__ = "posts"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    slug = Column(String, unique=True, index=True)
    content = Column(Text)
    author_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    author = relationship("User", back_populates="posts")

# Create tables
Base.metadata.create_all(bind=engine)

# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Now you can use database models in your routes
@app.get("/users")
def get_users():
    db = SessionLocal()
    users = db.query(User).all()
    db.close()
    return {"users": [{"id": u.id, "username": u.username} for u in users]}
```

### Using Tortoise ORM

Alternatively, you can use async ORMs like Tortoise ORM:

```bash
uv add "tortoise-orm[asyncpg]"
```

```python
from tortoise.models import Model
from tortoise import fields
from tortoise import Tortoise


class User(Model):
    id = fields.IntField(pk=True)
    username = fields.CharField(max_length=50, unique=True)
    email = fields.CharField(max_length=100, unique=True)
    created_at = fields.DatetimeField(auto_now_add=True)


class Post(Model):
    id = fields.IntField(pk=True)
    title = fields.CharField(max_length=200)
    content = fields.TextField()
    author = fields.ForeignKeyField('models.User', related_name='posts')
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)


# Initialize database
async def init_db():
    await Tortoise.init(
        db_url='sqlite://airblog.db',
        modules={'models': ['__main__']}  # Use your actual module path
    )
    await Tortoise.generate_schemas()
```

---

## API Development

Air makes it easy to create powerful REST APIs alongside your HTML pages.

### JSON Responses

Air automatically handles JSON responses when you return Python dictionaries:

```python
@app.get("/api/users")
def get_users():
    # Return Python data structure, Air converts to JSON
    return {
        "users": [
            {"id": 1, "name": "John", "email": "john@example.com"},
            {"id": 2, "name": "Jane", "email": "jane@example.com"}
        ]
    }

@app.get("/api/users/{user_id}")
def get_user(user_id: int):
    # Return single user
    return {"id": user_id, "name": "John", "email": "john@example.com"}
```

### Custom JSON Responses

For more control, use FastAPI's JSONResponse:

```python
from fastapi.responses import JSONResponse

@app.get("/api/status")
def get_status():
    return JSONResponse(
        content={"status": "ok", "timestamp": datetime.now().isoformat()},
        headers={"X-API-Version": "1.0"}
    )
```

### Request Bodies

Handle JSON request bodies:

```python
from pydantic import BaseModel


class UserCreate(BaseModel):
    name: str
    email: str
    age: int


@app.post("/api/users")
def create_user(user: UserCreate):
    # user is automatically validated against UserCreate schema
    return {
        "id": 123,  # In real app, this would be from database
        "name": user.name,
        "email": user.email,
        "age": user.age
    }
```

### API Documentation

Air integrates with FastAPI's automatic API documentation. Access it at `/docs` and `/redoc` (if enabled).

### Combining HTML and API

You can easily serve both HTML pages and API endpoints from the same application:

```python
# HTML page
@app.page
def dashboard():
    return air.layouts.mvpcss(
        air.Title("Dashboard"),
        air.H1("Dashboard"),
        # Load data via API call in JavaScript
        air.Div(id="api-data"),
        air.Script(
            """
            fetch('/api/user-data')
                .then(response => response.json())
                .then(data => {
                    document.getElementById('api-data').innerHTML = JSON.stringify(data);
                });
            """,
            type="module"
        )
    )

# API endpoint
@app.get("/api/user-data")
def get_user_data():
    return {"message": "Hello from API", "timestamp": datetime.now()}
```

---

## HTMX and Interactive Interfaces

HTMX allows you to create dynamic, interactive web applications without writing JavaScript.

### Installing HTMX Support

HTMX is included by default in Air's built-in layouts. Let's create an interactive example:

```python
@app.page
def counter_demo():
    """Demo of HTMX counter."""
    return air.layouts.mvpcss(
        air.Title("HTMX Counter"),
        air.H1("HTMX Counter Demo"),
        air.Div(
            air.Button("Increment", hx_post="/increment", hx_target="#counter", hx_swap="innerHTML"),
            air.Button("Decrement", hx_post="/decrement", hx_target="#counter", hx_swap="innerHTML"),
            air.Button("Reset", hx_post="/reset", hx_target="#counter", hx_swap="innerHTML"),
            air.Div(0, id="counter", style="font-size: 2em; margin: 1rem 0;"),
        ),
        air.A("← Back to Home", href="/")
    )


# Store counter value in memory (in production, use database or Redis)
counter_value = 0

@app.post("/increment")
def increment():
    global counter_value
    counter_value += 1
    return air.Div(counter_value, id="counter", style="font-size: 2em; margin: 1rem 0;")

@app.post("/decrement")
def decrement():
    global counter_value
    counter_value -= 1
    return air.Div(counter_value, id="counter", style="font-size: 2em; margin: 1rem 0;")

@app.post("/reset")
def reset():
    global counter_value
    counter_value = 0
    return air.Div(counter_value, id="counter", style="font-size: 2em; margin: 1rem 0;")
```

### Advanced HTMX Features

HTMX attributes can be added to Air Tags:

```python
air.Div(
    "Content",
    hx_get="/api/data",           # Make GET request to /api/data
    hx_target="#result",          # Update element with id="result"
    hx_swap="innerHTML",          # Replace innerHTML of target
    hx_trigger="click",           # Trigger on click
    hx_indicator="#spinner"       # Show spinner while loading
)

# Form with HTMX
air.Form(
    air.Input(name="search", placeholder="Search..."),
    air.Button("Search", type="submit"),
    hx_post="/search",            # POST to /search
    hx_target="#results",         # Update #results div
    hx_indicator=".htmx-indicator" # Show loading indicator
)
```

### Server-Sent Events (SSE)

Air supports Server-Sent Events for real-time updates:

```python
import asyncio
import random


@app.page
def sse_demo():
    """Server-Sent Events demo."""
    return air.layouts.mvpcss(
        air.Title("SSE Demo"),
        air.H1("Server-Sent Events Demo"),
        air.Div(id="events", style="height: 200px; overflow-y: scroll; border: 1px solid #ccc; padding: 10px;"),
        air.Script(
            """
            const eventSource = new EventSource('/events');
            const eventsDiv = document.getElementById('events');
            
            eventSource.onmessage = function(event) {
                const p = document.createElement('p');
                p.textContent = event.data;
                eventsDiv.appendChild(p);
                eventsDiv.scrollTop = eventsDiv.scrollHeight;
            };
            """,
            type="module"
        ),
        air.A("← Back to Home", href="/")
    )


@app.get("/events")
async def events():
    """SSE endpoint."""
    async def event_generator():
        for i in range(100):
            await asyncio.sleep(2)  # Wait 2 seconds
            yield air.Raw(f"data: Event {i} at {datetime.now()}\n\n")
    
    return air.SSEResponse(event_generator())
```

---

## Authentication and Security

### Session Management

Air provides session middleware for managing user sessions:

```python
import secrets

# Create a secret key for signing sessions
SECRET_KEY = secrets.token_urlsafe(32)

# Add session middleware
app.add_middleware(
    air.SessionMiddleware,
    secret_key=SECRET_KEY
)

@app.get("/login")
def login_page():
    return air.layouts.mvpcss(
        air.Title("Login"),
        air.H1("Login"),
        air.Form(
            air.Label("Username", for_="username"),
            air.Input(type="text", name="username", id="username"),
            air.Label("Password", for_="password"),
            air.Input(type="password", name="password", id="password"),
            air.Button("Login", type="submit"),
            method="POST",
            action="/login"
        )
    )

@app.post("/login")
async def login(request: air.Request):
    form_data = await request.form()
    username = form_data.get("username")
    password = form_data.get("password")
    
    # In real app, verify credentials against database
    if verify_credentials(username, password):
        # Set session data
        request.session["user_id"] = get_user_id(username)
        request.session["logged_in"] = True
        return air.RedirectResponse("/", status_code=303)
    else:
        return air.layouts.mvpcss(
            air.H1("Login Failed"),
            air.P("Invalid credentials. Please try again."),
            air.A("Try Again", href="/login")
        )

def require_login(func):
    """Decorator to require login for routes."""
    def wrapper(*args, **kwargs):
        request = kwargs.get('request') or next((arg for arg in args if isinstance(arg, air.Request)), None)
        if not request or not request.session.get("logged_in"):
            return air.RedirectResponse("/login", status_code=303)
        return func(*args, **kwargs)
    return wrapper
```

### Password Hashing

Use a library like `passlib` for secure password handling:

```bash
uv add passlib[bcrypt]
```

```python
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)
```

### Cross-Site Request Forgery (CSRF) Protection

For production applications, implement CSRF protection:

```python
import secrets

def generate_csrf_token():
    return secrets.token_urlsafe(32)

@app.get("/form-with-csrf")
def form_with_csrf(request: air.Request):
    csrf_token = generate_csrf_token()
    request.session["csrf_token"] = csrf_token
    
    return air.layouts.mvpcss(
        air.Form(
            air.Input(type="hidden", name="csrf_token", value=csrf_token),
            air.Input(type="text", name="data"),
            air.Button("Submit", type="submit"),
            method="POST",
            action="/process-data"
        )
    )
```

---

## Testing

### Unit Testing

Air applications can be tested using FastAPI's test client:

```python
import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_homepage():
    response = client.get("/")
    assert response.status_code == 200
    assert "AirBlog!" in response.text

def test_article_list():
    response = client.get("/api/articles")
    assert response.status_code == 200
    data = response.json()
    assert "articles" in data

def test_contact_form():
    response = client.post("/contact", data={
        "name": "Test User",
        "email": "test@example.com",
        "message": "Hello, world!"
    })
    assert response.status_code == 200
    assert "Thank You!" in response.text
```

### Testing with HTMX

Test HTMX endpoints:

```python
def test_htmx_increment():
    # Set initial value
    global counter_value
    counter_value = 0
    
    response = client.post("/increment")
    assert response.status_code == 200
    assert "1" in response.text

def test_htmx_headers():
    """Test with HTMX-specific headers."""
    response = client.post("/increment", headers={
        "HX-Request": "true",  # HTMX makes this header
        "HX-Target": "counter"
    })
    assert response.status_code == 200
```

---

## Deployment

### Production Deployment

Deploy your Air application just like any FastAPI application:

```bash
# Install gunicorn for production
uv add gunicorn

# Run with gunicorn
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### Docker Deployment

Create a `Dockerfile`:

```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml uv.lock ./

RUN pip install uv && uv sync --system

COPY . .

EXPOSE 8000

CMD ["gunicorn", "main:app", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000"]
```

### Environment Configuration

Use environment variables for configuration:

```python
import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///./airblog.db")
    secret_key: str = os.getenv("SECRET_KEY", "dev-secret-key")
    debug: bool = os.getenv("DEBUG", "False").lower() == "true"

settings = Settings()
```

### Scaling Considerations

For production applications, consider:

1. **Database Connection Pooling**: Use connection pools for database access
2. **Caching**: Implement caching with Redis or similar
3. **Static Files**: Serve static files through a CDN or reverse proxy
4. **Load Balancing**: Scale across multiple instances
5. **Monitoring**: Add logging and monitoring tools

---

## Advanced Patterns and Best Practices

### Application Structure

Organize your application into modules:

```
airblog/
├── main.py              # Application entry point
├── config.py            # Configuration settings
├── models.py            # Database models
├── schemas.py           # Pydantic schemas
├── database.py          # Database setup
├── routers/             # Route handlers
│   ├── web.py           # Web page routes
│   ├── api.py           # API routes
│   └── auth.py          # Authentication routes
├── templates/           # Jinja templates (if using)
└── static/              # Static files (CSS, JS, images)
```

### Separation of Concerns

Separate your routes into different modules:

```python
# routers/web.py
from fastapi import APIRouter
import air

web_router = APIRouter()

@web_router.page
def index():
    return air.P("Web page route")

# routers/api.py
from fastapi import APIRouter

api_router = APIRouter()

@api_router.get("/api/status")
def api_status():
    return {"status": "ok"}

# main.py
from fastapi import FastAPI
import air

app = air.Air()
app.include_router(web_router)
app.include_router(api_router, prefix="/api")
```

### Template Integration

While Air Tags are powerful, you can also use Jinja2 templates:

```python
from air import JinjaRenderer

jinja = JinjaRenderer(directory="templates")

@app.get("/jinja-page")
def jinja_page(request: air.Request):
    return jinja(request, "home.html", {"title": "Jinja Page", "articles": get_articles()})
```

### Background Tasks

Handle background tasks:

```python
@app.post("/submit-form")
async def submit_form_with_background_task(request: air.Request, background_tasks: air.BackgroundTasks):
    form_data = await request.form()
    
    # Process form in background
    background_tasks.add_task(send_email, form_data.get("email"), form_data.get("message"))
    
    return air.P("Form submitted successfully!")
```

### Error Handling

Add custom exception handlers:

```python
from fastapi import Request
from fastapi.responses import HTMLResponse

@app.exception_handler(404)
async def not_found_handler(request: Request, exc):
    return air.layouts.mvpcss(
        air.H1("Page Not Found"),
        air.P("The requested page could not be found."),
        air.A("← Back to Home", href="/")
    )
```

### Performance Optimization

1. **Caching**: Use FastAPI's caching mechanisms
2. **Database Optimization**: Use proper indexing and query optimization
3. **Static Asset Optimization**: Minimize CSS/JS and use CDNs
4. **Response Compression**: Enable gzip compression

---

## Conclusion

Congratulations! You've completed **The Air Web Framework: A Complete Guide**. You now have a comprehensive understanding of how to build modern web applications using Air.

### Key Takeaways

1. **Air Tags** provide a Pythonic way to generate HTML with full type safety
2. **Layouts** automatically handle document structure and head/body separation
3. **Routing** is intuitive and supports both simple and complex URL patterns
4. **Forms** are validated with Pydantic for robust data handling
5. **APIs** can be built alongside HTML pages in the same application
6. **HTMX** enables rich interactive experiences without JavaScript
7. **Security** is built-in with session management and validation
8. **Testing** is straightforward with FastAPI's test client

### Next Steps

1. **Build your own project**: Apply what you've learned to create your own application
2. **Explore the ecosystem**: Check out FastAPI, Starlette, and Pydantic documentation
3. **Join the community**: Contribute to Air or ask questions in the community
4. **Performance tune**: Optimize your applications for production use
5. **Learn advanced topics**: Explore databases, authentication, and deployment in depth

The Air framework is designed to make web development more enjoyable and productive. Its combination of Python's elegance with FastAPI's power provides a solid foundation for building modern web applications.

Happy coding!