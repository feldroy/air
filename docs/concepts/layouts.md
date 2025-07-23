# Layouts

Layouts in Air provide a way to structure complete HTML documents without the repetitive boilerplate. Air's layout system automatically handles the separation of head and body content and makes it easy to create your own custom layouts.

## Understanding Air's Layout Philosophy

Air's layout functions automatically sort your tags into the right places using intelligent filtering.  This allows you eliminate repetitive `air.Html`, `air.Body`, and `air.Head` boilerplate.

```python
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
air.layouts.picocss(
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

```python
@app.get("/")
def home():
    return air.layouts.picocss(
        # Mix head and body tags freely - Air sorts them
        air.Title("Dashboard"),
        air.H1("Welcome to the Dashboard"),
        air.Meta(name="description", content="User dashboard"),
        air.P("Your stats here"),
        air.Script(src="dashboard.js")
    )
```

Air transforms this into proper HTML structure automatically.

## Built-in Layouts: Start Fast

Air provides two ready-to-use layouts for rapid prototyping:

### PicoCSS Layout: Modern and Clean

The `picocss()` layout provides a beautiful, modern interface with zero configuration:

```python
import air

@app.get("/")
def home():
    return air.layouts.picocss(
        air.Title("My App"),
        air.H1("Welcome"),
        air.P("This automatically looks great!"),
        air.Button("Get Started")
    )
```

**What you get:**
- [PicoCSS](https://picocss.com/) styling
- HTMX included by default for interactivity
- Container wrapper for proper spacing

**Perfect for:**
- Prototypes and demos
- Internal tools and dashboards
- Quick proofs of concept
- Learning Air basics

!!! note

    There is an additional built in layout `mvpcss` that works the exact same way but used MVP.css instead of Pico CSS

## How to Move Beyond Built-in Layouts

The included layouts are designed for **quick prototyping**, not production applications.  Custom layouts give you complete control while preserving Air's automatic tag filtering benefits.

Here's the foundational pattern for any Air layout:

```python
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
2. **Use `*head_tags` and `*body_tags`** to include user content
3. **Return `.render()`** to get the final HTML string
4. **Accept `**kwargs`** for HTML attributes