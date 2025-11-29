# Layouts

Layouts in Air provide a way to structure complete HTML documents without the repetitive boilerplate. Air's layout system automatically handles the separation of head and body content and makes it easy to create your own custom layouts.

> ## Note
>
> This document covers how **Layouts** work. The full reference for them is the [Layouts reference](https://feldroy.github.io/air/api/layouts/).

## Understanding Air's Layout Philosophy

Air's layout functions automatically sort your tags into the right places using intelligent filtering. This allows you eliminate repetitive `air.Html`, `air.Body`, and `air.Head` boilerplate.

```
# Verbose Way
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

# Air Layouts
air.layouts.mvpcss(
    air.Title("My App"),           # Automatically goes to <head>
    air.Link(rel="stylesheet", href="style.css"),  # Also goes to <head>
    air.H1("Welcome"),             # Goes to <body>
    air.P("Content here")          # Also goes to <body>
    )
```

## The Tag Filtering System

Air layouts use two core functions to organize content:

- `filter_head_tags`: Returns only tags in `(Title, Style, Meta, Link, Script, Base)`
- `filter_body_tags`: Returns all tags except `(Title, Style, Meta, Link, Script, Base)`

### Why This Matters

This automatic separation means you can focus on your content and let Air handle the document structure:

```
@app.get("/")
def home():
    return air.layouts.mvpcss(
        # Mix head and body tags freely - Air sorts them
        air.Title("Dashboard"),
        air.H1("Welcome to the Dashboard"),
        air.Meta(name="description", content="User dashboard"),
        air.P("Your stats here"),
        air.Script(src="dashboard.js")
    )
```

Air transforms this into proper HTML structure automatically.

## Built-in Minimal Layouts

Air provides minimal ready-to-use layouts for rapid prototyping, `mvpcss` and `picocss` for MVP.css and PicoCSS respectively. They both work and are used in the exact same way.

```
import air

@app.get("/")
def home():
    return air.layouts.picocss( # or mvpcss
        air.Title("My App"),
        air.H1("Welcome"),
        air.P("This automatically looks great!"),
        air.Button("Get Started")
    )
```

**What you get:**

- [MVP.css](https://andybrewer.github.io/mvp/) styling or [PicoCSS](https://picocss.com/)
- HTMX included by default for interactivity
- Container wrapper for proper spacing

**Perfect for:**

- Prototypes and demos
- Internal tools and dashboards
- Quick proofs of concept
- Learning Air basics

## Beyond Built-in Layouts

The included layouts are designed for **quick prototyping**, not production commercial applications. Custom layouts give you complete control while preserving Air's automatic tag filtering benefits.

Here's the foundational pattern for any Air layout:

```
import air

def my_layout(*children, **kwargs):
    """My custom layout function."""
    # 1. Separate head and body content
    head_tags = air.layouts.filter_head_tags(children)
    body_tags = air.layouts.filter_body_tags(children)

    # 2. Build your custom structure
    return air.Html(
        air.Head(
            # Your custom head content
            ...
            *head_tags  # User's head tags
        ),
        air.Body(
            # Your custom body structure
            ... # Header content
            air.Main(*body_tags),  # User's body content
            ... # Footer Content
        ),
    ).render()
```

**Key principles:**

1. **Always filter tags** using Air's helper functions
1. **Use `*head_tags` and `*body_tags`** to include user content
1. **Return `.render()`** to get the final HTML string
