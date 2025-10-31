# Air Tags and Layouts

## Air Tags: An Approachable Entry Point to Air

Air Tags are strongly-typed Python classes that generate HTML elements. Instead of working with separate Jinja templates, you work with Python objects that provide type safety and IDE autocompletion. They really shine in the HTMX-era need to send small fragments of HTML from views, reducing the need to have dozens of tiny Jinja templates. By being written in Python they mean developers don't need leave Python and context switch to Jinja, reducing cognitive load and allowing for more fluid development. 

!!! note "What about Jinja?"

    While Air Tags are the preferred way to build HTML in Air, Air also supports Jinja templates for teams that prefer that approach. In fact, a popular Air pattern that has emerged is to use Jinja for page layouts while Air Tags are used for individual view responses.

### Basic Tag Usage

```python
import air

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

### Special Characters in Attributes

To get around that in Python we can't begin function arguments with special characters, we lean into how **Air Tags** is kwargs friendly.

```python
air.P('Hello', class_='plain', **{'@data': 6})
```

### Boolean Attributes

Boolean attributes in HTML can be represented in Air Tags by using `True`, `False`, or the strings `"true"` or `"false"`.

|Value|Behavior|
|---|---|---|
|True|Renders attribute name only (boolean style)|
|False|Omits attribute entirely|
|"true" (string)|Renders as attr="true"|

```python
# Renders as <option selected>Choice 1</option>
air.Option("Choice 1", selected=True)  
# Renders as <option>Choice 2</option>
air.Option("Choice 2", selected=False)  
# Renders as <option selected="true">Choice 3</option>
# Note: this isn't correct HTML for this tag,
#   but sometimes needed for specific use cases
air.Option("Choice 3", selected="true")  
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
2. **picocss**: Uses PicoCSS for slightly more sophisticated styling, deprecated

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
