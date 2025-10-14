# Air Tags and Layouts

!!! warning "First draft!"
    
    Please treat this as a very early draft, and be careful with anything that this chapter says! We welcome your pull requests to help refine the material so it actually becomes useful.

## Air Tags: An Approachable Entry Point to Air

Air Tags are strongly-typed Python classes that generate HTML elements. Instead of writing HTML strings, you work with Python objects that provide type safety and IDE autocompletion. Air Tags provide a beginner-friendly entry point to creating web interfaces in Air, but Air's architecture extends far beyond just tags to include routing, middleware, database integration, and API capabilities built on FastAPI and Starlette.

### Basic Tag Usage

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

### Nested Tags

Tags can be nested by passing child tags as arguments:

```python
air.Div(
    air.H2("Section Title"),
    air.P("Some content here"),
    air.Button("Submit", type="submit")
)
```

### Attributes and the Underscore Convention

In Air Tags, HTML attributes that conflict with Python keywords are suffixed with an underscore:

- `class` becomes `class_`
- `for` becomes `for_`
- `id` remains `id`
- `type` remains `type`

```python
air.Label("Username", for_="username-field")
air.Div(class_="container", id="main-content")
```

## Layouts: Structuring Complete Documents

Air's layout system automatically handles the separation of head and body content, eliminating boilerplate and making it easy to create complete HTML documents.

### How Layout Filtering Works

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

### Built-in Layouts

Air provides several built-in layouts for rapid prototyping:

1. **mvpcss**: Uses MVP.css for minimal styling
2. **picocss**: Uses PicoCSS for slightly more sophisticated styling

Both layouts include HTMX by default for interactive features.

### Creating Custom Layouts

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

## The App Object

The `air.Air()` object is the core of every Air application. It inherits from FastAPI but is configured with Air-specific defaults.

### Common Configuration Options

```python
app = air.Air(
    debug=True,  # Enable debug mode
    docs_url="/docs",  # Swagger UI endpoint
    redoc_url="/redoc",  # ReDoc endpoint
    path_separator="-"  # How to convert function names to URLs
)
```