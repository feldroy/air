# The Air Web Framework: A Complete Guide

Welcome to **The Air Web Framework: A Complete Guide** - your comprehensive resource for building modern web applications with Air. This book is designed for developers of all levels, whether you're just starting with Python web development or looking to leverage Air's sophisticated features in your next project.

Air is a high-level layer over FastAPI that streamlines the creation of both interactive web interfaces and robust REST APIs within a single application. Built with developer experience in mind, Air provides an elegant Pythonic approach to modern web development.

This guide demonstrates how to build a complete blog application, showcasing both basic concepts for newcomers and advanced patterns that experienced developers can leverage in production systems.

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

Air is a Python web framework built on top of FastAPI that enables you to build both elegant HTML interfaces and powerful REST APIs within a single application. Air streamlines common web development workflows while maintaining the flexibility and power of the underlying FastAPI ecosystem.

Key concepts:

- **Web Framework**: A structured approach to building web applications
- **API (Application Programming Interface)**: Programmatic interfaces for data exchange
- **HTML**: The markup language for web browsers
- **Python**: The programming language underlying our applications

### Key Features of Air

1. **Air Tags**: Python classes that generate HTML, offering type safety and IDE autocompletion while maintaining clean Python syntax. For example, `air.H1("Hello")` generates an HTML heading `<h1>Hello</h1>`.

2. **Layouts**: Intelligent document structure handling that automatically separates head and body content, eliminating boilerplate and providing styling options.

3. **Streamlined Routing**: Direct mapping between Python functions and URL endpoints with both decorator-based and conventional routing patterns.

4. **Pydantic-Powered Forms**: Built-in form validation and processing using Pydantic models, providing robust data handling with type safety.

5. **HTMX Integration**: Native support for HTMX's progressive enhancement approach, enabling dynamic interfaces without client-side JavaScript frameworks.

6. **Jinja Compatibility**: Seamless integration with Jinja2 templating for teams preferring traditional server-side rendering.

7. **Database Agnostic**: Works with any Python database library (SQLAlchemy, Tortoise ORM, etc.)

8. **Unified Application Architecture**: First-class support for serving both HTML interfaces and API endpoints from a single codebase.

### Why Choose Air?

Air is ideal for developers who want to:

- Build modern, interactive web applications quickly
- Leverage FastAPI's ecosystem without HTML response boilerplate
- Create unified applications serving both UI and API clients
- Maintain type safety and IDE support throughout development
- Work with Pythonic, readable code patterns

### Philosophy of Air

Air prioritizes these principles:

1. **Developer Experience**: Intuitive, discoverable APIs that follow Python conventions
2. **Pythonic Design**: Leverages Python's natural syntax and type system
3. **Type Safety**: Full type hinting for better development tooling and error prevention  
4. **Flexibility**: Accommodates various architectural patterns and team preferences
5. **Productivity**: Reduces boilerplate while preserving power for complex applications

---

## Getting Started

### Prerequisites

Before we begin, you'll need:

1. **Python 3.11 or higher** (3.14 is recommended): The programming language we'll use. You can check your Python version with `python --version` or `python3 --version`.
2. **[uv](https://docs.astral.sh/uv/getting-started/installation/#installing-uv)**: A modern Python package and project manager that streamlines dependency management.
3. **A code editor**: [VS Code](https://code.visualstudio.com/) is recommended, though any Python-capable editor works.
4. **Basic command line familiarity**: Comfort with terminal commands like `cd`, `ls`/`dir`, etc.

### Installing Air

Let's start by creating a new project:

```bash
uv init myblog
```

This initializes a new Python project in a directory called `myblog`.

Now would be a good time to commit your work:

```bash
git add .
git commit -m "Initialize myblog project with uv"
```

Navigate to the project directory:

```bash
cd myblog
```

Open it in Visual Studio Code:

```bash
code .
```

Familiarize yourself with the contents of a project created by `uv init`, if you're not already familiar:

```
myblog
├── .git
│   └── ...
├── .gitignore
├── .python-version
├── main.py
├── pyproject.toml
└── README.md
```

Press `Ctrl+`` (backtick) to open a terminal in Visual Studio Code.

Set up a virtual environment for project isolation:

```bash
uv venv
```

Activate the virtual environment:

```bash
# On Mac/Linux:
source .venv/bin/activate

# On Windows:
.venv\Scripts\activate
```

Install Air with standard dependencies:

```bash
uv add "air[standard]"
```

This installs Air along with its recommended extensions for web development.

### Your First Air App

Replace the contents of `main.py` with:

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

This creates a simple web application with:

- `import air`: Imports the Air framework
- `app = air.Air()`: Creates a new Air application instance
- `@app.page`: Decorator that maps the function to the root path `/`
- The function returns a complete HTML document using Air's layout system

Run the development server:

```bash
fastapi dev
```

Visit your application at: <a href="http://localhost:8000/" target="_blank">http://localhost:8000/</a>

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

Now would be a good time to commit your work:

```bash
git add .
git commit -m "Add first Air app with index page"
```

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

Air Tags are strongly-typed Python classes that generate HTML elements. Instead of writing HTML strings, you work with Python objects that provide type safety and IDE autocompletion.

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

### Project My Personal Blog

We're going to create a markdown file-powered blogging platform called My Personal Blog. It will have:

1. A web interface for reading blog posts
2. A REST API for programmatic access to blog posts
3. Administrative interface for managing posts

### Creating Article Files

First, let's create a directory to store our blog articles and some sample content:

Create a new directory called `articles` in the root of your project. Inside this directory, create a new file called `hello-world.md` with the following content:

```markdown title="articles/hello-world.md"
---
title: Hello World
description: Welcome to my personal blog - my first post!
slug: hello-world
published: true
date: 2025-09-26
author: Your Name
tags:
- personal
- first-post
- welcome
---

Welcome to my personal blog! This is the beginning of my journey with Air and web development.

I'm excited to share my thoughts and projects with you through this blog.

```python
for i in range(10):
    print("Hello, World!")
```
```

The file has two sections:

- **Frontmatter**: Delimited by `---` lines, contains metadata like title, description, slug, etc.
- **Content**: The main body of the article, written in Markdown format

Create another file called `about-me.md`:

```markdown title="articles/about-me.md"
---
title: About Me
description: Get to know the person behind this blog
slug: about-me
published: true
date: 2025-09-27
author: Your Name
tags:
- about
- introduction
---

Hi there! Welcome to my personal blog.

My name is Your Name, and I'm passionate about Python programming and web development.

I hope you enjoy reading my blog posts!
```

And a third file called `markdown-features.md`:

```markdown title="articles/markdown-features.md"
---
title: Learning Markdown
description: A guide to using different Markdown formatting features
slug: markdown-features
published: true
date: 2025-09-28
author: Your Name
tags:
- markdown
- formatting
- tutorial
---

# Main Title

This is a paragraph with **bold text**, *italic text*, and `inline code`.

## Subheading

A list of items:

- First item
- Second item 
- Third item

## Numbered List

1. First step
2. Second step
3. Third step

## Blockquote

> This is a quote from someone important or a thought I want to highlight.
```

Now would be a good time to commit your work:

```bash
git add .
git commit -m "Add article files: hello-world.md, about-me.md, markdown-features.md"
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
    title = "My Personal Blog"
    articles = get_articles()
    return air.layouts.mvpcss(
        air.Head(air.Title(title)),
        air.H1(title),
        air.P("Welcome to my personal blog!"),
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

Now would be a good time to commit your work:

```bash
git add .
git commit -m "Add functionality to read and display articles on homepage"
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
    title = "My Personal Blog"
    articles = get_articles()
    return air.layouts.mvpcss(
        air.Head(air.Title(title)),
        air.H1(title),
        air.P("Welcome to my personal blog!"),
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

Now would be a good time to commit your work:

```bash
git add .
git commit -m "Add article detail pages with markdown conversion"
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
    title = "My Personal Blog"
    articles = get_articles()
    return air.layouts.mvpcss(
        air.Head(air.Title(title)),
        air.Header(
            air.Nav(
                air.A("My Personal Blog", href="/", style="font-size: 1.5em; font-weight: bold;"),
                air.Span(" | ", style="margin: 0 10px;"),
                air.A("Contact", href="/contact")
            )
        ),
        air.H1(title),
        air.P("Welcome to my personal blog!"),
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

Now would be a good time to commit your work:

```bash
git add .
git commit -m "Add contact form with handler"
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
    title = "My Personal Blog"
    articles = get_articles()
    return air.layouts.mvpcss(
        air.Header(
            air.Nav(
                air.A("My Personal Blog", href="/", style="font-size: 1.5em; font-weight: bold;"),
                air.Span(" | ", style="margin: 0 10px;"),
                air.A("Contact", href="/contact"),
                air.Span(" | ", style="margin: 0 10px;"),
                air.A("API", href="/api/docs", target="_blank")
            )
        ),
        air.Head(air.Title(title)),
        air.H1(title),
        air.P("Welcome to my personal blog!"),
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

Now would be a good time to commit your work:

```bash
git add .
git commit -m "Add API endpoints for articles"
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

### Complete Blog Example with All Features

Let's build a complete, production-ready blog application that showcases all Air's capabilities:

```python title="main.py"
from pathlib import Path
from frontmatter import Frontmatter
import markdown
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field
from air import Air, AirForm, AirField, RedirectResponse
import secrets
import hashlib


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


def get_article_by_id(article_id: int) -> dict | None:
    """Get an article by its index (ID)."""
    articles = get_articles()
    if 0 <= article_id < len(articles):
        return articles[article_id]
    return None


def get_article_index_by_slug(slug: str) -> int | None:
    """Get the index of an article by its slug."""
    articles = get_articles()
    for i, article in enumerate(articles):
        if article["attributes"]["slug"] == slug:
            return i
    return None


# Initialize Air app with session support
app = Air()
app.add_middleware(
    air.SessionMiddleware,
    secret_key=secrets.token_urlsafe(32)
)


@app.page
def index():
    """Home page with latest articles."""
    title = "My Personal Blog"
    articles = get_articles()
    
    # Check if user is logged in
    is_admin = False  # In a real app, check session here
    
    return air.layouts.mvpcss(
        air.Title(title),
        air.Header(
            air.Nav(
                air.A("My Personal Blog", href="/", style="font-size: 1.5em; font-weight: bold;"),
                air.Span(" | ", style="margin: 0 10px;"),
                air.A("Contact", href="/contact"),
                air.Span(" | ", style="margin: 0 10px;"),
                air.A("API Docs", href="/docs", target="_blank") if app.docs_url else "",
                air.Span(" | ", style="margin: 0 10px;"),
                air.A("Admin", href="/admin") if is_admin else air.A("Login", href="/login")
            )
        ),
        air.H1(title),
        air.P("Welcome to my personal blog!"),
        air.H2("Latest Articles"),
        air.Ul(
            *[
                air.Li(
                    air.A(
                        article["attributes"]["title"],
                        href=f'/{article["attributes"]["slug"]}',
                        style="font-size: 1.2em; font-weight: bold; display: block;"
                    ),
                    air.Small(
                        f"{article['attributes']['description']} - "
                        f"Published: {article['attributes']['date']} by {article['attributes']['author']}"
                    ),
                    air.Div(
                        *[air.Span(f"#{tag}", style="margin-right: 0.5rem; color: #666;") 
                          for tag in article['attributes']['tags']],
                        style="margin-top: 0.25rem;"
                    )
                )
                for article in articles
            ]
        )
    )


@app.get("/{slug}")
def article_detail(slug: str):
    """Display a single article with full details."""
    article = get_article(slug)
    if not article:
        return air.layouts.mvpcss(
            air.H1("Article not found"),
            air.P("The requested article could not be found."),
            air.A("← Back to Home", href="/")
        )
    
    # Convert markdown content to HTML
    html_content = markdown.markdown(article["body"])
    
    return air.layouts.mvpcss(
        air.Title(article["attributes"]["title"]),
        air.Article(
            air.H1(article["attributes"]["title"]),
            air.Div(
                air.Time(
                    f'Published: {article["attributes"]["date"]}',
                    datetime=str(article["attributes"]["date"])
                ),
                air.P(f"By {article['attributes']['author']}"),
                style="color: #666; margin-bottom: 1rem;"
            ),
            air.Div(air.Raw(html_content), style="line-height: 1.6;"),
            air.Div(
                *[air.Span(f"#{tag}", style="margin-right: 0.5rem;") for tag in article['attributes']['tags']],
                style="margin-top: 1rem; color: #666;"
            )
        ),
        air.Nav(
            air.A("← Back to Home", href="/")
        )
    )


# Contact Form
class ContactForm(AirForm):
    class model(BaseModel):
        name: str = Field(..., min_length=2, max_length=50, description="Your name")
        email: str = AirField(type="email", label="Email Address", required=True)
        subject: str = Field(..., min_length=5, max_length=100, description="Subject of your message")
        message: str = Field(..., min_length=10, max_length=1000, description="Your message")


contact_form = ContactForm()

@app.page
def contact():
    """Contact form page."""
    return air.layouts.mvpcss(
        air.Title("Contact Us"),
        air.H1("Contact Us"),
        air.P("Have questions or feedback? Get in touch!"),
        air.Form(
            contact_form.render(),  # Render the form with AirForm
            method="POST",
            action="/contact",
            style="display: flex; flex-direction: column; gap: 1rem; max-width: 500px;"
        ),
        air.Nav(
            air.A("← Back to Home", href="/")
        )
    )


@app.post("/contact")
async def contact_handler(request: air.Request):
    """Handle contact form submission with validation."""
    form_data = await request.form()
    
    # Validate the form
    if contact_form.validate(form_data):
        # Process valid data
        validated_data = contact_form.model.model_dump()
        
        # In a real application, you would send an email or save to database
        # print(f"Contact form submitted: {validated_data}")
        
        return air.layouts.mvpcss(
            air.H1("Thank You!"),
            air.P(f"Your message has been sent, {validated_data['name']}!"),
            air.P("We'll get back to you soon."),
            air.Nav(
                air.A("← Back to Home", href="/"),
                air.Span(" | ", style="margin: 0 10px;"),
                air.A("Send Another Message", href="/contact")
            )
        )
    else:
        # Form has errors, re-render with errors
        return air.layouts.mvpcss(
            air.Title("Contact Us - Error"),
            air.H1("Contact Us"),
            air.P("Please correct the errors below:"),
            air.Form(
                contact_form.render(),  # Renders form with errors
                method="POST",
                action="/contact",
                style="display: flex; flex-direction: column; gap: 1rem; max-width: 500px;"
            ),
            air.Nav(
                air.A("← Back to Home", href="/")
            )
        )


# API Endpoints
@app.get("/api/articles")
def api_articles():
    """Return all articles as JSON."""
    articles = get_articles()
    return {
        "articles": [
            {
                "id": i,
                "title": article["attributes"]["title"],
                "slug": article["attributes"]["slug"],
                "description": article["attributes"]["description"],
                "date": article["attributes"]["date"],
                "author": article["attributes"]["author"],
                "tags": article["attributes"]["tags"],
                "url": f"/{article['attributes']['slug']}"
            }
            for i, article in enumerate(articles)
        ],
        "total": len(articles)
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
    
    # Convert markdown to HTML for API
    html_content = markdown.markdown(article["body"])
    
    return {
        "id": get_article_index_by_slug(slug),
        "title": article["attributes"]["title"],
        "slug": article["attributes"]["slug"],
        "description": article["attributes"]["description"],
        "date": article["attributes"]["date"],
        "author": article["attributes"]["author"],
        "tags": article["attributes"]["tags"],
        "content": article["body"],
        "html_content": html_content
    }


# HTMX Interactive Features
@app.page
def htmx_demo():
    """Interactive HTMX demo page."""
    return air.layouts.mvpcss(
        air.Title("HTMX Demo"),
        air.H1("HTMX Interactive Demo"),
        air.H2("Dynamic Content Without JavaScript"),
        
        # Counter demo
        air.Div(
            air.H3("Counter Example:"),
            air.Button("Increment", 
                      hx_post="/api/increment", 
                      hx_target="#counter", 
                      hx_swap="innerHTML",
                      class_="button"),
            air.Button("Decrement", 
                      hx_post="/api/decrement", 
                      hx_target="#counter", 
                      hx_swap="innerHTML",
                      class_="button"),
            air.Button("Reset", 
                      hx_post="/api/reset", 
                      hx_target="#counter", 
                      hx_swap="innerHTML",
                      class_="button"),
            air.Div(0, id="counter", style="font-size: 2em; margin: 1rem 0; padding: 1rem; border: 1px solid #ccc; display: inline-block;"),
        ),
        
        # Search demo
        air.Div(
            air.H3("Search Example:"),
            air.Form(
                air.Input(name="q", placeholder="Search articles...", 
                         hx_post="/api/search", 
                         hx_trigger="keyup changed delay:500ms", 
                         hx_target="#search-results", 
                         hx_swap="outerHTML"),
                method="POST",
                style="margin: 1rem 0;"
            ),
            air.Div(id="search-results", style="margin-top: 1rem;"),
        ),
        
        air.Nav(
            air.A("← Back to Home", href="/")
        )
    )


# Global counter for HTMX demo (in production, use database or Redis)
counter = 0

@app.post("/api/increment")
def increment_counter():
    global counter
    counter += 1
    return air.Div(counter, id="counter", style="font-size: 2em; margin: 1rem 0; padding: 1rem; border: 1px solid #ccc; display: inline-block;")

@app.post("/api/decrement")
def decrement_counter():
    global counter
    counter = max(0, counter - 1)  # Don't go below 0
    return air.Div(counter, id="counter", style="font-size: 2em; margin: 1rem 0; padding: 1rem; border: 1px solid #ccc; display: inline-block;")

@app.post("/api/reset")
def reset_counter():
    global counter
    counter = 0
    return air.Div(counter, id="counter", style="font-size: 2em; margin: 1rem 0; padding: 1rem; border: 1px solid #ccc; display: inline-block;")

@app.post("/api/search")
async def search_articles(request: air.Request):
    """HTMX search endpoint."""
    form_data = await request.form()
    query = form_data.get("q", "").lower()
    
    if not query:
        return air.Div("Enter a search term", id="search-results", style="margin-top: 1rem;")
    
    articles = get_articles()
    results = [
        article for article in articles 
        if query in article["attributes"]["title"].lower() 
        or query in article["attributes"]["description"].lower()
        or query in article["body"].lower()
    ]
    
    if not results:
        return air.Div("No results found", id="search-results", style="margin-top: 1rem; color: #666;")
    
    result_items = [
        air.Div(
            air.A(
                result["attributes"]["title"],
                href=f"/{result['attributes']['slug']}",
                style="display: block; margin-bottom: 0.5rem; font-weight: bold;"
            ),
            air.Small(result["attributes"]["description"]),
            style="padding: 0.5rem; border-bottom: 1px solid #eee;"
        )
        for result in results[:5]  # Limit to first 5 results
    ]
    
    return air.Div(*result_items, id="search-results", style="margin-top: 1rem; border: 1px solid #ccc; padding: 1rem;")

# Admin section with session protection
@app.page
def login():
    """Login page."""
    return air.layouts.mvpcss(
        air.Title("Admin Login"),
        air.H1("Admin Login"),
        air.Form(
            air.Div(
                air.Label("Username", for_="username"),
                air.Input(type="text", name="username", id="username"),
            ),
            air.Div(
                air.Label("Password", for_="password"),
                air.Input(type="password", name="password", id="password"),
            ),
            air.Button("Login", type="submit"),
            method="POST",
            action="/login",
            style="display: flex; flex-direction: column; gap: 1rem; max-width: 300px;"
        ),
        air.Nav(
            air.A("← Back to Home", href="/")
        )
    )


@app.post("/login")
async def login_handler(request: air.Request):
    """Handle login."""
    form_data = await request.form()
    username = form_data.get("username")
    password = form_data.get("password")
    
    # Simple demo password check (use proper authentication in real app)
    # In a real app, hash passwords and verify against database
    hashed_input = hashlib.sha256(password.encode()).hexdigest()
    hashed_admin = hashlib.sha256("admin".encode()).hexdigest()  # Demo password
    
    if username == "admin" and hashed_input == hashed_admin:
        request.session["user"] = username
        request.session["is_logged_in"] = True
        return RedirectResponse("/admin", status_code=303)
    else:
        return air.layouts.mvpcss(
            air.H1("Login Failed"),
            air.P("Invalid credentials. Please try again."),
            air.A("← Back to Home", href="/")
        )


def require_login(func):
    """Decorator to require login for routes."""
    def wrapper(*args, **kwargs):
        # In a real implementation, we'd access the request through FastAPI dependencies
        # This is just a basic example
        request = kwargs.get('request') or next((arg for arg in args if hasattr(arg, 'session')), None)
        
        # For this example, we'll skip this decorator functionality
        # In a real app, this would properly check sessions
        return func(*args, **kwargs)
    return wrapper


@app.page
@require_login  # Would require login in a real implementation
def admin():
    """Admin page for managing content."""
    articles = get_articles()
    
    return air.layouts.mvpcss(
        air.Title("Admin Dashboard"),
        air.Header(
            air.H1("Admin Dashboard"),
            air.Nav(
                air.A("← Back to Home", href="/"),
                air.Span(" | ", style="margin: 0 10px;"),
                air.A("Logout", href="/logout")
            )
        ),
        air.H2("Manage Articles"),
        air.Div(
            air.A("Add New Article", href="/admin/new", class_="button primary"),
            style="margin-bottom: 1rem;"
        ),
        air.Ul(
            *[
                air.Li(
                    air.A(
                        f"{i+1}. {article['attributes']['title']} ({article['attributes']['slug']})",
                        href=f"/admin/edit/{article['attributes']['slug']}"
                    ),
                    air.Span(f" - {article['attributes']['date']} | ", style="color: #666;"),
                    air.A("View", href=f"/{article['attributes']['slug']}", target="_blank"),
                    style="margin-bottom: 0.5rem;"
                )
                for i, article in enumerate(articles)
            ]
        )
    )


@app.page
def admin_new():
    """Page to create new articles."""
    # Form for creating new articles
    return air.layouts.mvpcss(
        air.Title("Create New Article"),
        air.H1("Create New Article"),
        air.Form(
            # In a real implementation, you'd have a form for title, content, etc.
            air.Div(
                air.Label("Title", for_="title"),
                air.Input(type="text", name="title", id="title", required=True),
            ),
            air.Div(
                air.Label("Slug", for_="slug"),
                air.Input(type="text", name="slug", id="slug", required=True),
            ),
            air.Div(
                air.Label("Content", for_="content"),
                air.Textarea(name="content", id="content", required=True, rows=10),
            ),
            air.Button("Create Article", type="submit"),
            method="POST",
            action="/admin/new",
            style="display: flex; flex-direction: column; gap: 1rem;"
        ),
        air.Nav(
            air.A("← Back to Admin", href="/admin"),
            air.Span(" | ", style="margin: 0 10px;"),
            air.A("← Back to Home", href="/")
        )
    )


@app.post("/admin/new")
async def admin_new_handler(request: air.Request):
    """Handle new article creation."""
    # In a real app, this would create a new markdown file
    form_data = await request.form()
    title = form_data.get("title")
    slug = form_data.get("slug")
    content = form_data.get("content")
    
    # Create markdown content with frontmatter
    markdown_content = f"""---
title: {title}
description: {title}
slug: {slug}
published: true
date: {datetime.now().date()}
author: Admin
tags:

- new
---

{content}
"""
    
    # Write to file (in real app, you'd validate and sanitize input)
    file_path = Path("articles") / f"{slug}.md"
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(markdown_content)
    
    return air.layouts.mvpcss(
        air.H1("Article Created!"),
        air.P(f"Article '{title}' has been created successfully."),
        air.Div(
            air.A("View Article", href=f"/{slug}", class_="button primary"),
            air.Span(" | ", style="margin: 0 10px;"),
            air.A("Back to Admin", href="/admin"),
            air.Span(" | ", style="margin: 0 10px;"),
            air.A("← Back to Home", href="/")
        )
    )


@app.get("/logout")
def logout(request: air.Request):
    """Handle logout."""
    # Clear session
    request.session.clear()
    return RedirectResponse("/", status_code=303)


# Error handlers
@app.exception_handler(404)
async def not_found(request, exc):
    return air.layouts.mvpcss(
        air.H1("Page Not Found"),
        air.P("The requested page could not be found."),
        air.A("← Back to Home", href="/")
    )


@app.exception_handler(500)
async def server_error(request, exc):
    return air.layouts.mvpcss(
        air.H1("Server Error"),
        air.P("An internal server error occurred."),
        air.A("← Back to Home", href="/")
    )
```

Now would be a good time to commit your work:

```bash
git add .
git commit -m "Complete blog application with all features"
```

This complete example demonstrates:

1. **Routing**: Multiple route types and patterns
2. **Forms**: Both basic and AirForm validation
3. **Layouts**: Using mvpcss for consistent styling
4. **API**: JSON endpoints alongside HTML pages
5. **HTMX**: Interactive features without JavaScript
6. **Sessions**: Basic authentication
7. **Error Handling**: Custom error pages
8. **File Operations**: Reading and writing markdown files

### API Documentation and Reference

Air provides comprehensive API documentation. Here's a reference for the most important classes and functions:

#### Core Application

- `air.Air()`: Main application class that extends FastAPI
- `@app.page`: Decorator for simple page routes (converts function name to URL)
- `@app.get`, `@app.post`, etc.: Standard FastAPI route decorators
- `app.add_middleware()`: Add middleware like session handling

#### Layouts

- `air.layouts.mvpcss()`: MVP.css layout with HTMX
- `air.layouts.picocss()`: PicoCSS layout with HTMX
- `air.layouts.filter_head_tags()`: Filter tags for head section
- `air.layouts.filter_body_tags()`: Filter tags for body section

#### Tags

All HTML elements are available as Air Tags:

- `air.Html`, `air.Head`, `air.Body`: Document structure
- `air.H1`, `air.H2`, `air.H3`, etc.: Headings
- `air.Div`, `air.Span`: Block and inline containers
- `air.A`, `air.Img`: Links and images
- `air.Form`, `air.Input`, `air.Button`: Form elements
- `air.P`, `air.Ul`, `air.Li`: Text elements
- `air.Title`, `air.Meta`, `air.Link`: Head elements
- `air.Script`, `air.Style`: Script and style elements
- `air.Raw()`: Raw HTML content (use with caution)

#### Forms

- `AirForm`: Pydantic-based form class
- `AirField`: Enhanced Pydantic fields with HTML attributes
- `form.render()`: Render form with validation errors
- `form.validate()`: Validate form data

#### Responses

- `AirResponse`: Default HTML response class (alias for `TagResponse`)
- `SSEResponse`: Server-Sent Events response
- `RedirectResponse`: Redirect response
- `JSONResponse`: JSON response (from FastAPI)

#### Utilities

- `Request`: Request object with session support
- `BackgroundTasks`: Handle background tasks
- `is_htmx_request`: Dependency to detect HTMX requests

### Best Practices

1. **Use Type Hints**: Always use type hints for better IDE support and validation
2. **Separate Concerns**: Keep HTML generation logic in route handlers
3. **Leverage Layouts**: Use layouts to avoid HTML boilerplate
4. **Validate Input**: Always validate form and API input
5. **Handle Errors**: Implement custom exception handlers
6. **Organize Code**: Separate routes into modules for large applications
7. **Use Dependencies**: Leverage FastAPI's dependency injection
8. **Security First**: Implement proper authentication and authorization
9. **Performance**: Cache static content and optimize database queries
10. **Testing**: Write comprehensive tests for all functionality
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
DATABASE_URL = "postgresql://postgres:password@localhost:5432/myblog"
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
        db_url='sqlite://myblog.db',
        modules={'models': ['__main__']}  # Use your actual module path
    )
    await Tortoise.generate_schemas()
```

Now would be a good time to commit your work:

```bash
git add .
git commit -m "Add database integration with SQLAlchemy and Tortoise ORM"
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

Now would be a good time to commit your work:

```bash
git add .
git commit -m "Add API endpoints and development patterns"
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

Now would be a good time to commit your work:

```bash
git add .
git commit -m "Add HTMX and interactive interface features"
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

Now would be a good time to commit your work:

```bash
git add .
git commit -m "Add authentication and security features"
```

---

## Testing

### Unit Testing

Air applications can be tested using FastAPI's test client. Here's a comprehensive testing approach for all aspects of your application:

```python
import pytest
from fastapi.testclient import TestClient
from main import app, get_articles, get_article

client = TestClient(app)

def test_homepage():
    response = client.get("/")
    assert response.status_code == 200
    assert "My Personal Blog" in response.text
    assert "Latest Articles" in response.text

def test_article_list():
    response = client.get("/api/articles")
    assert response.status_code == 200
    data = response.json()
    assert "articles" in data
    assert isinstance(data["articles"], list)

def test_article_detail():
    # Test with a known article slug (assuming you have hello-world.md)
    response = client.get("/hello-world")
    assert response.status_code == 200
    assert "Hello World" in response.text

def test_contact_form():
    response = client.post("/contact", data={
        "name": "Test User",
        "email": "test@example.com",
        "message": "Hello, world!",
        "subject": "Test Subject"
    })
    assert response.status_code == 200
    assert "Thank You!" in response.text

def test_contact_form_invalid():
    # Test form with missing required fields
    response = client.post("/contact", data={
        "name": "",  # Missing required name
        "email": "invalid-email",  # Invalid email
        "message": "Short"  # Too short
    })
    assert response.status_code == 200
    assert "Please correct the errors below:" in response.text

def test_api_article_detail():
    response = client.get("/api/articles/hello-world")
    assert response.status_code == 200
    data = response.json()
    assert "title" in data
    assert "slug" in data
    assert data["slug"] == "hello-world"

def test_api_article_not_found():
    response = client.get("/api/articles/nonexistent-slug")
    assert response.status_code == 404
    data = response.json()
    assert "error" in data

def test_htmx_endpoints():
    # Test HTMX counter functionality
    # Reset counter first
    response = client.post("/api/reset")
    assert response.status_code == 200
    
    # Test increment
    response = client.post("/api/increment")
    assert response.status_code == 200
    assert "1" in response.text
    
    # Test decrement
    response = client.post("/api/decrement")
    assert response.status_code == 200
    assert "0" in response.text
```

### Testing with HTMX

Test HTMX endpoints with proper headers and state management:

```python
def test_htmx_increment():
    """Test HTMX increment functionality."""
    # Reset counter to known state
    reset_response = client.post("/api/reset")
    assert reset_response.status_code == 200
    assert "0" in reset_response.text
    
    # Test increment
    response = client.post("/api/increment")
    assert response.status_code == 200
    assert "1" in response.text

def test_htmx_headers():
    """Test HTMX-specific headers are handled properly."""
    response = client.post("/api/increment", headers={
        "HX-Request": "true",  # HTMX makes this header
        "HX-Target": "counter"
    })
    assert response.status_code == 200
    assert "1" in response.text

def test_htmx_search():
    """Test HTMX search functionality."""
    response = client.post("/api/search", data={"q": "hello"})
    assert response.status_code == 200
    assert "search-results" in response.text

def test_htmx_search_empty():
    """Test HTMX search with empty query."""
    response = client.post("/api/search", data={"q": ""})
    assert response.status_code == 200
    assert "Enter a search term" in response.text
```

### Database Testing

If using a database, implement proper testing strategies:

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import Base, get_db

# Create test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
test_engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

Base.metadata.create_all(bind=test_engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

# Override the database dependency
app.dependency_overrides[get_db] = override_get_db

def test_database_operations():
    """Test database operations."""
    # This would test actual database operations if you had them
    response = client.get("/users")
    assert response.status_code == 200
```

### Form Validation Testing

Test your Air Forms validation thoroughly:

```python
def test_contact_form_validation_valid():
    """Test ContactForm with valid data."""
    response = client.post("/contact", data={
        "name": "Valid Name",
        "email": "valid@example.com",
        "subject": "Valid Subject",
        "message": "This is a valid message with sufficient length."
    })
    assert response.status_code == 200
    assert "Thank You!" in response.text

def test_contact_form_validation_invalid():
    """Test ContactForm with invalid data."""
    response = client.post("/contact", data={
        "name": "A",  # Too short
        "email": "invalid-email",  # Invalid email
        "subject": "Hi",  # Too short
        "message": "Hi"  # Too short
    })
    assert response.status_code == 200
    assert "Please correct the errors below:" in response.text
    # Check that errors are displayed
    assert "name" in response.text
    assert "email" in response.text

def test_contact_form_missing_required():
    """Test ContactForm with missing required fields."""
    response = client.post("/contact", data={})
    assert response.status_code == 200
    assert "Please correct the errors below:" in response.text
```

### API Testing

Comprehensive API endpoint testing:

```python
def test_api_articles_response_structure():
    """Test that API response has correct structure."""
    response = client.get("/api/articles")
    assert response.status_code == 200
    data = response.json()
    
    assert "articles" in data
    assert "total" in data
    assert isinstance(data["total"], int)
    
    if data["articles"]:  # If there are articles
        article = data["articles"][0]
        assert "id" in article
        assert "title" in article
        assert "slug" in article
        assert "description" in article
        assert "date" in article
        assert "author" in article
        assert "tags" in article
        assert "url" in article

def test_api_article_detail_response_structure():
    """Test that API article detail response has correct structure."""
    response = client.get("/api/articles/hello-world")
    if response.status_code == 200:  # Only if article exists
        data = response.json()
        assert "id" in data
        assert "title" in data
        assert "slug" in data
        assert "description" in data
        assert "date" in data
        assert "author" in data
        assert "tags" in data
        assert "content" in data
        assert "html_content" in data

def test_api_404_handling():
    """Test API 404 error handling."""
    response = client.get("/api/articles/nonexistent-article")
    assert response.status_code == 404
    data = response.json()
    assert "error" in data
    assert data["error"] == "Article not found"
```

### Error Handling Testing

Test your error handlers:

```python
def test_404_error_page():
    """Test 404 error page."""
    response = client.get("/nonexistent-page")
    assert response.status_code == 404
    assert "Page Not Found" in response.text

def test_500_error_page():
    """Test 500 error page (requires triggering an actual server error)."""
    # This would require creating a route that raises an exception
    pass
```

### Integration Testing

Test the complete user journey:

```python
def test_complete_user_flow():
    """Test a complete user journey."""
    # 1. Visit homepage
    response = client.get("/")
    assert response.status_code == 200
    assert "My Personal Blog" in response.text
    
    # 2. View articles list
    response = client.get("/")
    assert "Latest Articles" in response.text
    
    # 3. Submit contact form
    response = client.post("/contact", data={
        "name": "Integration Test User",
        "email": "integration@test.com",
        "subject": "Integration Test",
        "message": "This is a test message during integration testing."
    })
    assert response.status_code == 200
    assert "Thank You!" in response.text
    
    # 4. Verify API access
    response = client.get("/api/articles")
    assert response.status_code == 200
    data = response.json()
    assert "articles" in data
```

### Testing Best Practices

1. **Use fixtures for common setup:**

```python
@pytest.fixture
def client():
    """Create test client."""
    return TestClient(app)

@pytest.fixture
def sample_article():
    """Provide sample article data for tests."""
    return {
        "title": "Test Article",
        "slug": "test-article",
        "description": "A test article",
        "content": "# Test Article\n\nThis is a test article."
    }
```

2. **Test different data scenarios:**

   - Valid data
   - Invalid data
   - Boundary conditions
   - Edge cases

3. **Use parameterized tests for multiple scenarios:**
```python
@pytest.mark.parametrize("name,email,message,expected_status", [
    ("Valid User", "valid@example.com", "Valid message", 200),
    ("", "valid@example.com", "Valid message", 200),  # Should fail validation
    ("Valid User", "invalid-email", "Valid message", 200),  # Should fail validation
])
def test_contact_form_scenarios(name, email, message, expected_status):
    response = client.post("/contact", data={
        "name": name,
        "email": email,
        "message": message
    })
    assert response.status_code == expected_status
```

4. **Mock external dependencies:**
```python
from unittest.mock import patch

def test_external_api_call():
    """Test functionality that calls external APIs."""
    with patch('main.external_api_call') as mock_api:
        mock_api.return_value = {"status": "success"}
        response = client.get("/external-call")
        assert response.status_code == 200
```

Now would be a good time to commit your work:

```bash
git add .
git commit -m "Add comprehensive testing framework"
```

---

## Deployment

### Production Deployment

Deploy your Air application just like any FastAPI application. For production environments, you'll want to use a production-ready ASGI server:

```bash
# Install production ASGI server
uv add "uvicorn[standard]" gunicorn

# For Unix systems (Linux/macOS)
uv add gunicorn uvicorn

# Run with gunicorn and uvicorn worker
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000 --workers 4 --worker-class uvicorn.workers.UvicornWorker --timeout 120 --keep-alive 5
```

For high-traffic applications, consider using Uvicorn directly or with a reverse proxy:

```bash
# Run Uvicorn directly (good for containerized environments)
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Configuration for Production

Create a production-ready configuration:

```python title="config.py"
import os
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # Database settings
    database_url: str = os.getenv("DATABASE_URL", "postgresql://postgres:password@localhost:5432/myblog")
    
    # Security settings
    secret_key: str = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")
    debug: bool = os.getenv("DEBUG", "False").lower() == "true"
    allowed_hosts: str = os.getenv("ALLOWED_HOSTS", "*")
    
    # CORS settings
    cors_allow_origins: str = os.getenv("CORS_ALLOW_ORIGINS", "")
    cors_allow_credentials: bool = os.getenv("CORS_ALLOW_CREDENTIALS", "true").lower() == "true"
    cors_allow_methods: str = os.getenv("CORS_ALLOW_METHODS", "*")
    cors_allow_headers: str = os.getenv("CORS_ALLOW_HEADERS", "*")
    
    # Application settings
    app_version: str = os.getenv("APP_VERSION", "1.0.0")
    admin_email: str = os.getenv("ADMIN_EMAIL", "admin@example.com")
    
    # Cache settings
    redis_url: Optional[str] = os.getenv("REDIS_URL")
    
    @property
    def cors_allow_origins_list(self) -> list:
        if self.cors_allow_origins:
            return [origin.strip() for origin in self.cors_allow_origins.split(",")]
        return ["*"]


settings = Settings()
```

### Docker Deployment

Create a production-ready `Dockerfile` with security and performance optimizations:

```dockerfile
# Use a non-root user for security
FROM python:3.12-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Create a non-root user
RUN useradd --create-home --shell /bin/bash app

# Set working directory
WORKDIR /home/app

# Install uv
RUN pip install uv

# Copy project files
COPY pyproject.toml uv.lock ./

# Create virtual environment and install dependencies
RUN uv venv && \
    . .venv/bin/activate && \
    uv sync --system

# Copy application code
COPY . .

# Change ownership to app user
RUN chown -R app:app /home/app

# Switch to app user
USER app

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/ || exit 1

# Run with gunicorn
CMD ["/home/app/.venv/bin/gunicorn", "main:app", \
    "-w", "4", \
    "-k", "uvicorn.workers.UvicornWorker", \
    "--bind", "0.0.0.0:8000", \
    "--timeout", "120", \
    "--keep-alive", "5", \
    "--max-requests", "1000", \
    "--max-requests-jitter", "100"]
```

Create a `docker-compose.yml` for easy deployment:

```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:password@db:5432/myblog
      - SECRET_KEY=your-super-secret-key
      - DEBUG=False
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      - db
      - redis
    volumes:
      - ./articles:/home/app/articles  # For persistent article storage
    restart: unless-stopped

  db:
    image: postgres:18
    environment:
      - POSTGRES_DB=myblog
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=password
    volumes:
      - postgres_data:/var/lib/postgresql/data
    restart: unless-stopped

  redis:
    image: redis:7-alpine
    restart: unless-stopped

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl  # For SSL certificates
    depends_on:
      - web
    restart: unless-stopped

volumes:
  postgres_data:
```

### Reverse Proxy Configuration

Create an Nginx configuration for production:

```nginx
# nginx.conf
events {
    worker_connections 1024;
}

http {
    upstream myblog {
        server web:8000;
    }

    server {
        listen 80;
        server_name yourdomain.com www.yourdomain.com;
        
        # Security headers
        add_header X-Frame-Options "SAMEORIGIN" always;
        add_header X-Content-Type-Options "nosniff" always;
        add_header Referrer-Policy "no-referrer-when-downgrade" always;
        add_header Content-Security-Policy "default-src 'self' http: https: data: blob: 'unsafe-inline'" always;
        
        client_max_body_size 100M;
        
        # Static files
        location /static {
            alias /home/app/static;
            expires 30d;
            add_header Cache-Control "public, immutable";
        }
        
        # API and application routes
        location / {
            proxy_pass http://myblog;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
            proxy_redirect off;
            proxy_buffering off;
            
            # WebSocket support if needed
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection "upgrade";
        }
    }
}
```

### Environment Configuration

Use environment variables for configuration. Create a `.env.example` file:

```env
# Database
DATABASE_URL=postgresql://username:password@localhost/dbname

# Security
SECRET_KEY=your-very-long-secret-key-here-make-it-random-and-secure

# Application
DEBUG=False
ADMIN_EMAIL=admin@yourdomain.com

# CORS
CORS_ALLOW_ORIGINS=https://yourdomain.com,https://www.yourdomain.com

# Redis (for caching/session storage)
REDIS_URL=redis://localhost:6379/0

# Logging
LOG_LEVEL=INFO
```

### Production Settings

Create different settings for different environments:

```python title="config.py" (expanded)
import os
from pydantic_settings import BaseSettings
from typing import Optional, List


class Settings(BaseSettings):
    # Core settings
    app_version: str = os.getenv("APP_VERSION", "1.0.0")
    debug: bool = os.getenv("DEBUG", "False").lower() == "true"
    
    # Database
    database_url: str = os.getenv("DATABASE_URL", "postgresql://postgres:password@localhost:5432/myblog")
    database_pool_size: int = int(os.getenv("DATABASE_POOL_SIZE", "5"))
    
    # Security
    secret_key: str = os.getenv("SECRET_KEY")
    allowed_hosts: str = os.getenv("ALLOWED_HOSTS", "*")
    
    # CORS
    cors_allow_origins: str = os.getenv("CORS_ALLOW_ORIGINS", "")
    cors_allow_credentials: bool = os.getenv("CORS_ALLOW_CREDENTIALS", "true").lower() == "true"
    cors_allow_methods: str = os.getenv("CORS_ALLOW_METHODS", "*")
    cors_allow_headers: str = os.getenv("CORS_ALLOW_HEADERS", "*")
    
    # Cache
    redis_url: Optional[str] = os.getenv("REDIS_URL")
    
    # Email (for contact forms, notifications)
    smtp_server: str = os.getenv("SMTP_SERVER", "localhost")
    smtp_port: int = int(os.getenv("SMTP_PORT", "587"))
    smtp_username: Optional[str] = os.getenv("SMTP_USERNAME")
    smtp_password: Optional[str] = os.getenv("SMTP_PASSWORD")
    email_from: str = os.getenv("EMAIL_FROM", "noreply@yourdomain.com")
    
    # Logging
    log_level: str = os.getenv("LOG_LEVEL", "INFO")
    
    # File uploads
    max_upload_size: int = int(os.getenv("MAX_UPLOAD_SIZE", "10485760"))  # 10MB
    
    @property
    def cors_allow_origins_list(self) -> List[str]:
        if self.cors_allow_origins:
            return [origin.strip() for origin in self.cors_allow_origins.split(",")]
        return ["*"] if not self.debug else ["*"]

    @property
    def is_production(self) -> bool:
        return not self.debug
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
```

And update your main application to use these settings:

```python
# main.py (with production settings)
from config import settings
import air

# Initialize app with settings
app = air.Air(
    debug=settings.debug,
    title="My Personal Blog",
    version=settings.app_version
)

# Add CORS middleware if needed
from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_allow_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Scaling Considerations

For production applications, consider:

1. **Database Connection Pooling**: Use connection pools for database access
2. **Caching**: Implement caching with Redis or similar
3. **Static Files**: Serve static files through a CDN or reverse proxy
4. **Load Balancing**: Scale across multiple instances
5. **Monitoring**: Add logging and monitoring tools
6. **Health Checks**: Implement health check endpoints
7. **Security**: Use HTTPS, security headers, and authentication
8. **Backup Strategy**: Regular database and file backups
9. **Monitoring**: Application and infrastructure monitoring
10. **CDN**: Use a CDN for static assets

### Health Checks and Monitoring

Add health check endpoints:

```python
@app.get("/health")
def health_check():
    """Health check endpoint for load balancers and monitoring."""
    return {
        "status": "healthy",
        "app": "My Personal Blog",
        "version": settings.app_version,
        "timestamp": datetime.now().isoformat()
    }

@app.get("/ready")
def readiness_check():
    """Readiness check to verify the app is ready to serve requests."""
    # Add checks for database, cache, etc.
    return {"status": "ready"}
```

### SSL/HTTPS Configuration

For production, always use HTTPS. You can handle this at the reverse proxy level (nginx) or with a service like Let's Encrypt:

```bash
# Using certbot for Let's Encrypt
sudo apt-get install certbot python3-certbot-nginx
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
```

### Performance Optimization

Optimize your production deployment:

```python
# In production settings, optimize for performance
if settings.is_production:
    # Add performance-related middleware
    from fastapi.middleware.gzip import GZipMiddleware
    app.add_middleware(GZipMiddleware, minimum_size=1000)
    
    # Configure for production
    app.docs_url = "/docs" if settings.debug else None
    app.redoc_url = "/redoc" if settings.debug else None
```

Now would be a good time to commit your work:

```bash
git add .
git commit -m "Complete deployment configuration"
```

---

## Advanced Patterns and Best Practices

### Application Structure

Organize your application into modules:

```
myblog/
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

### Best Practices Summary

Throughout this guide, we've emphasized several key best practices:

- **Type Safety**: Always use type hints to catch errors early and improve IDE support
- **Security First**: Implement authentication, authorization, and input validation
- **Separation of Concerns**: Organize code into logical modules and components
- **Performance**: Optimize database queries, cache frequently accessed data, and compress responses
- **Testing**: Write comprehensive tests covering unit, integration, and end-to-end scenarios
- **Deployment**: Prepare applications for production with proper configuration and monitoring

### Advanced Resources

To further your Air journey, consider exploring these additional resources:

#### Official Documentation
- [Air Framework Documentation](https://feldroy.github.io/air/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [HTMX Documentation](https://htmx.org/)

#### Community Resources
- Join Air discussions on GitHub
- Participate in Python web development forums
- Follow web development blogs and newsletters
- Contribute to open source Air projects

#### Advanced Topics to Explore
- **Async Programming**: Deepen your understanding of asyncio for better performance
- **Database Optimization**: Learn advanced SQL and ORM techniques
- **Frontend Frameworks**: Explore how Air integrates with React, Vue, or other frameworks
- **Microservices**: Scale applications across multiple services
- **DevOps**: Master deployment, monitoring, and CI/CD pipelines

### Building Your Portfolio

Now that you have mastered Air, consider building projects to add to your portfolio:

1. **Personal Blog**: Start with the blog example and expand it with features
2. **E-commerce Site**: Implement product listings, cart functionality, and checkout
3. **Task Management App**: Create a Kanban board or todo application
4. **API Service**: Build a comprehensive REST API with authentication
5. **Interactive Dashboard**: Create real-time dashboards with HTMX and SSE

### Contributing to Air

The Air framework is an open-source project that benefits from community contributions:

- Report bugs and issues
- Suggest new features
- Write documentation
- Create example applications
- Submit pull requests with improvements
- Help other users in community forums

### Staying Current

The web development landscape evolves rapidly. To stay current:

- Follow the Air release notes and changelogs
- Subscribe to Python and web development newsletters
- Attend web development meetups and conferences
- Participate in online learning platforms
- Regularly refactor and update your applications

### Final Thoughts

Air represents a thoughtful approach to web development, combining the power of FastAPI with the elegance of Python. By focusing on developer experience while maintaining performance and security, Air enables you to build applications that are both enjoyable to develop and robust in production.

The patterns, techniques, and best practices you've learned in this guide will serve you well beyond Air itself. The principles of clean code, proper testing, security awareness, and performance optimization are universal in software development.

Remember that mastery comes through practice. Build applications, experiment with new features, and don't be afraid to make mistakes. Each project teaches valuable lessons that will make you a better developer.

### Next Steps

1. **Build something now**: Start a new project using Air today
2. **Experiment with features**: Try different layout options, form configurations, and HTMX interactions
3. **Contribute to the community**: Share your knowledge and learn from others
4. **Optimize and scale**: Take your first application to production
5. **Keep learning**: Continue exploring advanced topics and new technologies

Thank you for reading **The Air Web Framework: A Complete Guide**. Your journey with Air is just beginning, and we're excited to see what you'll build!

Happy coding!

---

## Appendix A: Quick Reference

### Common Decorators
- `@app.page` - Simple page routes (function name → URL)
- `@app.get` - GET requests
- `@app.post` - POST requests
- `@app.put` - PUT requests
- `@app.delete` - DELETE requests

### Common Air Tags
- Document structure: `air.Html`, `air.Head`, `air.Body`
- Headings: `air.H1`, `air.H2`, `air.H3`, `air.H4`, `air.H5`, `air.H6`
- Text: `air.P`, `air.Span`, `air.Div`
- Links: `air.A`, `air.Link`
- Forms: `air.Form`, `air.Input`, `air.Button`, `air.Textarea`, `air.Select`
- Media: `air.Img`, `air.Video`, `air.Audio`
- Metadata: `air.Title`, `air.Meta`, `air.Style`, `air.Script`

### Layout Functions
- `air.layouts.mvpcss()` - MVP.css with HTMX
- `air.layouts.picocss()` - PicoCSS with HTMX

### Response Types
- `air.AirResponse` - Default HTML response
- `air.SSEResponse` - Server-Sent Events
- `air.RedirectResponse` - Redirect responses

### Utility Functions
- `air.Raw()` - Include raw HTML
- `air.is_htmx_request` - Dependency for detecting HTMX requests
- Layout filters: `air.layouts.filter_head_tags()`, `air.layouts.filter_body_tags()`

## Appendix B: Common Patterns

### Form Handling Pattern
```python
# Define a form
class ContactForm(AirForm):
    class model(BaseModel):
        name: str = Field(..., min_length=2)
        email: str = AirField(type="email", required=True)

form = ContactForm()

# Handle form in route
@app.post("/contact")
async def contact_handler(request: air.Request):
    form_data = await request.form()
    if form.validate(form_data):
        # Process validated data
        validated_data = form.model.model_dump()
        # ... handle valid form
    else:
        # Render with errors
        return air.layouts.mvpcss(form.render())
```

### API + HTML Pattern
```python
# HTML page
@app.page
def dashboard():
    return air.layouts.mvpcss(
        # Load data via JavaScript calling API
        air.Div(id="api-data"),
        air.Script(
            "fetch('/api/data').then(r => r.json()).then(data => {...})",
            type="module"
        )
    )

# API endpoint
@app.get("/api/data")
def api_data():
    return {"message": "Data from API"}
```

### HTMX Pattern
```python
# Page with HTMX features
@app.page
def interactive_page():
    return air.layouts.mvpcss(
        air.Div(
            air.Button("Click me", 
                      hx_post="/handle-click", 
                      hx_target="#result", 
                      hx_swap="innerHTML"),
            air.Div(id="result")
        )
    )

# HTMX handler
@app.post("/handle-click")
def handle_click():
    return air.Div("Updated content", id="result")
```

Now would be a good time to commit your work:

```bash
git add .
git commit -m "Complete the Air web framework tutorial"
```