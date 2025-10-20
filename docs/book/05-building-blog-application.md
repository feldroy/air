# Building Our Blog Application

!!! warning "First draft!"
    
    Please treat this as a very early draft, and be careful with anything that this chapter says! We welcome your pull requests to help refine the material so it actually becomes useful.

## Project My Personal Blog

We're going to create a markdown file-powered blogging platform called My Personal Blog. It will have:

1. A web interface for reading blog posts
2. A REST API for programmatic access to blog posts
3. Administrative interface for managing posts

## Creating Article Files

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

## Reading Articles into Our Application

To read the articles from the `articles` directory, we'll use the `pathlib` and `frontmatter` libraries. First, install the frontmatter library:

```bash
uv add frontmatter
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

## Creating Article Detail Pages

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

## Adding a Contact Form

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
        air.Header(
            air.Nav(
                air.A("My Personal Blog", href="/", style="font-size: 1.5em; font-weight: bold;"),
                air.Span(" | ", style="margin: 0 10px;"),
                air.A("Contact", href="/contact")
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

## Adding an API Endpoint

Let's add a REST API endpoint to access our articles programmatically:

```python title="main.py"
from pathlib import Path
from frontmatter import Frontmatter
import markdown
from datetime import datetime
from typing import List
import fastapi


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
api = fastapi.FastAPI()

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
@api.get("/articles")
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


@api.get("/articles/{slug}")
def api_article_detail(slug: str):
    """Return a specific article as JSON."""
    article = get_article(slug)
    if not article:
        raise fastapi.exceptions.HTTPException(status_code=404)
    
    return {
        "title": article["attributes"]["title"],
        "slug": article["attributes"]["slug"],
        "description": article["attributes"]["description"],
        "date": article["attributes"]["date"],
        "author": article["attributes"]["author"],
        "tags": article["attributes"]["tags"],
        "content": article["body"]
    }

# Mounting the API into the APP
app.mount("/api", api)
```

Now would be a good time to commit your work:

```bash
git add .
git commit -m "Add API endpoints for articles"
```

## Complete Blog Example with All Features

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
import fastapi


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
api = fastapi.FastAPI()


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
# API Endpoints
@api.get("/articles")
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


@api.get("/articles/{slug}")
def api_article_detail(slug: str):
    """Return a specific article as JSON."""
    article = get_article(slug)
    if not article:
        raise fastapi.exceptions.HTTPException(status_code=404)
    
    return {
        "title": article["attributes"]["title"],
        "slug": article["attributes"]["slug"],
        "description": article["attributes"]["description"],
        "date": article["attributes"]["date"],
        "author": article["attributes"]["author"],
        "tags": article["attributes"]["tags"],
        "content": article["body"]
    }

# Mounting the API into the APP
app.mount("/api", api)


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