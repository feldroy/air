# Air Layouts: Building Beautiful Web Pages

Layouts in Air provide a powerful way to structure complete HTML documents without the repetitive boilerplate. Air's layout system automatically handles the separation of head and body content, includes popular CSS frameworks, and makes it easy to create your own custom layouts.

## Understanding Air's Layout Philosophy

Air layouts solve a fundamental problem: **mixing head and body tags is messy**. Instead of manually building `<html>`, `<head>`, and `<body>` structures, Air layouts automatically organize your content based on tag types.

```python
import air

# Instead of this verbose approach:
def old_way():
    return air.Html(
        air.Head(
            air.Title("My App"),
            air.Link(rel="stylesheet", href="style.css")
        ),
        air.Body(
            air.H1("Welcome"),
            air.P("Content here")
        )
    )

# Use layouts to write this:
def layout_way():
    return air.layouts.picocss(
        air.Title("My App"),           # Automatically goes to <head>
        air.Link(rel="stylesheet", href="style.css"),  # Also goes to <head>
        air.H1("Welcome"),             # Goes to <body>
        air.P("Content here")          # Also goes to <body>
    )
```

**The magic:** Air's layout functions automatically sort your tags into the right places using intelligent filtering.

## The Tag Filtering System

Air layouts use two core functions to organize content:

### `filter_head_tags()` and `filter_body_tags()`

These functions know which HTML tags belong in the document head versus body:

```python
import air.layouts as layouts

# These tags automatically go to <head>:
head_content = [
    air.Title("My Page"),
    air.Meta(charset="utf-8"),
    air.Link(rel="stylesheet", href="styles.css"),
    air.Script(src="app.js"),
    air.Style("body { margin: 0; }")
]

# These tags automatically go to <body>:
body_content = [
    air.H1("Welcome"),
    air.P("Hello world"),
    air.Div("Content"),
    air.Button("Click me")
]

# Air automatically separates them:
head_tags = layouts.filter_head_tags(head_content + body_content)
body_tags = layouts.filter_body_tags(head_content + body_content)
# head_tags = [Title, Meta, Link, Script, Style]
# body_tags = [H1, P, Div, Button]
```

**The HEAD_TAG_TYPES:** Air recognizes these tags as head content: `Title`, `Style`, `Meta`, `Link`, `Script`, and `Base`.

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
- [PicoCSS](https://picocss.com/) styling for instant beauty
- HTMX included by default for interactivity
- Responsive design that works on all devices
- Container wrapper for proper spacing
- Dark/light mode support

**Perfect for:**
- Prototypes and demos
- Internal tools and dashboards
- Quick proofs of concept
- Learning Air basics

### MVP.css Layout: Minimalist Elegance

The `mvpcss()` layout offers a cleaner, more minimal aesthetic:

```python
@app.get("/")
def home():
    return air.layouts.mvpcss(
        air.Title("Clean App"),
        air.H1("Minimal Design"),
        air.P("Sometimes less is more"),
        air.Button("Simple Action")
    )
```

**What you get:**
- [MVP.css](https://andybrewer.github.io/mvp/) for clean typography
- HTMX included for dynamic behavior
- No container wrapper (fuller width)
- Lighter visual weight

**Perfect for:**
- Documentation sites
- Blogs and content-focused apps
- When you want subtle styling
- Text-heavy applications

### Layout Options

Both layouts support these parameters:

```python
# Disable HTMX if you don't need it
air.layouts.picocss(
    air.H1("Static Page"),
    htmx=False
)

# Pass additional HTML attributes
air.layouts.picocss(
    air.H1("Custom Page"),
    lang="es",
    data_theme="dark"
)
```

## When to Move Beyond Built-in Layouts

The included layouts are designed for **quick prototyping**, not production applications. Consider creating custom layouts when:

- **Branding matters:** You need custom colors, fonts, or styling
- **Performance is critical:** You want to optimize CSS/JS loading
- **Complex layouts:** Multi-column, dashboard, or custom grid layouts
- **Design system:** You're building a consistent design language
- **Team standards:** Your organization has specific requirements

**Our recommendation:** Start with built-in layouts, then graduate to custom ones as your needs evolve.

## Creating Custom Layouts

Custom layouts give you complete control while preserving Air's automatic tag filtering benefits.

### Basic Custom Layout Pattern

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
            air.Meta(charset="utf-8"),
            air.Meta(name="viewport", content="width=device-width, initial-scale=1"),
            *head_tags  # User's head tags
        ),
        air.Body(
            # Your custom body structure
            air.Header("My Site"),
            air.Main(*body_tags),  # User's body content
            air.Footer("© 2024")
        ),
        **kwargs  # Pass through HTML attributes
    ).render()
```

**Key principles:**
1. **Always filter tags** using Air's helper functions
2. **Use `*head_tags` and `*body_tags`** to include user content
3. **Return `.render()`** to get the final HTML string
4. **Accept `**kwargs`** for HTML attributes

### Example: Bootstrap Layout

Let's create a layout using Bootstrap CSS framework:

```python
def bootstrap_layout(*children, htmx=True, **kwargs):
    """Bootstrap 5 layout with optional HTMX."""
    head_tags = air.layouts.filter_head_tags(children)
    body_tags = air.layouts.filter_body_tags(children)
    
    # Add HTMX if requested
    if htmx:
        head_tags.insert(0, air.Script(
            src="https://unpkg.com/htmx.org@1.9.10"
        ))
    
    return air.Html(
        air.Head(
            air.Meta(charset="utf-8"),
            air.Meta(name="viewport", content="width=device-width, initial-scale=1"),
            air.Link(
                href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css",
                rel="stylesheet"
            ),
            *head_tags
        ),
        air.Body(
            air.Div(
                *body_tags,
                class_="container"
            ),
            air.Script(
                src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"
            )
        ),
        **kwargs
    ).render()

# Usage
@app.get("/")
def home():
    return bootstrap_layout(
        air.Title("Bootstrap App"),
        air.H1("Hello Bootstrap", class_="text-primary"),
        air.Button("Primary Button", class_="btn btn-primary")
    )
```

### Example: Dashboard Layout

For more complex layouts, you can create sophisticated structures:

```python
def dashboard_layout(*children, title="Dashboard", **kwargs):
    """Multi-section dashboard layout."""
    head_tags = air.layouts.filter_head_tags(children)
    body_tags = air.layouts.filter_body_tags(children)
    
    return air.Html(
        air.Head(
            air.Meta(charset="utf-8"),
            air.Meta(name="viewport", content="width=device-width, initial-scale=1"),
            air.Title(title),
            air.Link(rel="stylesheet", href="/static/dashboard.css"),
            *head_tags
        ),
        air.Body(
            air.Header(
                air.Nav(
                    air.A("Dashboard", href="/"),
                    air.A("Users", href="/users"),
                    air.A("Settings", href="/settings"),
                    class_="navbar"
                ),
                class_="header"
            ),
            air.Main(
                air.Aside(
                    air.H3("Quick Stats"),
                    air.Div(id="stats-widget"),
                    class_="sidebar"
                ),
                air.Section(
                    *body_tags,  # Main content goes here
                    class_="content"
                ),
                class_="main-layout"
            ),
            air.Footer(
                air.P("© 2024 My Company"),
                class_="footer"
            ),
            air.Script(src="/static/dashboard.js")
        ),
        **kwargs
    ).render()

# Usage
@app.get("/users")
def users_page():
    return dashboard_layout(
        air.H1("User Management"),
        air.Table(
            air.Tr(air.Th("Name"), air.Th("Email")),
            air.Tr(air.Td("John"), air.Td("john@example.com"))
        ),
        title="Users - Dashboard"
    )
```

## Advanced Layout Patterns

### Conditional Content

Include different content based on parameters:

```python
def app_layout(*children, authenticated=False, **kwargs):
    head_tags = air.layouts.filter_head_tags(children)
    body_tags = air.layouts.filter_body_tags(children)
    
    # Different navigation for authenticated users
    nav_items = [
        air.A("Home", href="/")
    ]
    
    if authenticated:
        nav_items.extend([
            air.A("Dashboard", href="/dashboard"),
            air.A("Logout", href="/logout")
        ])
    else:
        nav_items.append(air.A("Login", href="/login"))
    
    return air.Html(
        air.Head(*head_tags),
        air.Body(
            air.Nav(*nav_items),
            air.Main(*body_tags)
        ),
        **kwargs
    ).render()
```

### Layout Composition

Build complex layouts by composing simpler ones:

```python
def base_layout(*children, **kwargs):
    """Base layout with common elements."""
    head_tags = air.layouts.filter_head_tags(children)
    body_tags = air.layouts.filter_body_tags(children)
    
    return air.Html(
        air.Head(
            air.Meta(charset="utf-8"),
            air.Link(rel="stylesheet", href="/static/base.css"),
            *head_tags
        ),
        air.Body(*body_tags),
        **kwargs
    )

def admin_layout(*children, **kwargs):
    """Admin layout extends base with admin-specific elements."""
    return base_layout(
        air.Style("""
        .admin-header { background: #dc3545; color: white; }
        """),
        air.Header("Admin Panel", class_="admin-header"),
        air.Main(*children),
        air.Footer("Admin Area"),
        **kwargs
    )
```

### Dynamic CSS/JS Loading

Load different assets based on the page:

```python
def dynamic_layout(*children, css_files=None, js_files=None, **kwargs):
    head_tags = air.layouts.filter_head_tags(children)
    body_tags = air.layouts.filter_body_tags(children)
    
    # Add custom CSS files
    if css_files:
        for css_file in css_files:
            head_tags.append(air.Link(rel="stylesheet", href=css_file))
    
    # Add custom JS files
    js_tags = []
    if js_files:
        for js_file in js_files:
            js_tags.append(air.Script(src=js_file))
    
    return air.Html(
        air.Head(*head_tags),
        air.Body(
            *body_tags,
            *js_tags  # JS at end of body for performance
        ),
        **kwargs
    ).render()

# Usage
@app.get("/charts")
def charts_page():
    return dynamic_layout(
        air.Title("Charts"),
        air.H1("Data Visualization"),
        air.Div(id="chart-container"),
        css_files=["/static/charts.css"],
        js_files=["/static/chart-lib.js", "/static/charts.js"]
    )
```

## Best Practices for Air Layouts

### 1. Start Simple, Evolve Gradually

```python
# ✅ Start with built-in layouts
@app.get("/prototype")
def prototype():
    return air.layouts.picocss(
        air.Title("Prototype"),
        air.H1("Quick and dirty")
    )

# ✅ Graduate to custom layouts when needed
@app.get("/production")
def production():
    return company_layout(
        air.Title("Production App"),
        air.H1("Polished and branded")
    )
```

### 2. Always Use Tag Filtering

```python
# ✅ Use Air's filtering functions
def good_layout(*children, **kwargs):
    head_tags = air.layouts.filter_head_tags(children)
    body_tags = air.layouts.filter_body_tags(children)
    return air.Html(
        air.Head(*head_tags),
        air.Body(*body_tags)
    ).render()

# ❌ Don't manually manage head/body separation
def bad_layout(head_content, body_content, **kwargs):
    return air.Html(
        air.Head(*head_content),  # Brittle and verbose
        air.Body(*body_content)
    ).render()
```

### 3. Make Layouts Configurable

```python
# ✅ Accept parameters for flexibility
def flexible_layout(*children, title="My App", theme="light", **kwargs):
    head_tags = air.layouts.filter_head_tags(children)
    body_tags = air.layouts.filter_body_tags(children)
    
    return air.Html(
        air.Head(
            air.Title(title),
            air.Link(rel="stylesheet", href=f"/static/themes/{theme}.css"),
            *head_tags
        ),
        air.Body(*body_tags, data_theme=theme),
        **kwargs
    ).render()
```

### 4. Handle Edge Cases Gracefully

```python
def robust_layout(*children, **kwargs):
    head_tags = air.layouts.filter_head_tags(children)
    body_tags = air.layouts.filter_body_tags(children)
    
    # Provide default title if none specified
    has_title = any(isinstance(tag, air.Title) for tag in head_tags)
    if not has_title:
        head_tags.insert(0, air.Title("My App"))
    
    # Handle empty body content
    if not body_tags:
        body_tags = [air.P("No content provided.")]
    
    return air.Html(
        air.Head(*head_tags),
        air.Body(*body_tags),
        **kwargs
    ).render()
```

### 5. Performance Considerations

```python
def optimized_layout(*children, **kwargs):
    head_tags = air.layouts.filter_head_tags(children)
    body_tags = air.layouts.filter_body_tags(children)
    
    return air.Html(
        air.Head(
            # Critical CSS inline for faster loading
            air.Style("""
            body { font-family: system-ui; margin: 0; }
            .container { max-width: 1200px; margin: 0 auto; }
            """),
            *head_tags,
            # Non-critical CSS loaded asynchronously
            air.Link(
                rel="preload",
                href="/static/app.css",
                as_="style",
                onload="this.onload=null;this.rel='stylesheet'"
            )
        ),
        air.Body(*body_tags),
        **kwargs
    ).render()
```

## Testing Layouts

Create simple tests to verify your layouts work correctly:

```python
def test_layout_separates_tags():
    """Test that layouts properly separate head and body tags."""
    result = my_layout(
        air.Title("Test"),
        air.H1("Header"),
        air.Meta(charset="utf-8"),
        air.P("Paragraph")
    )
    
    # Verify structure
    assert "<title>Test</title>" in result
    assert "<meta charset=\"utf-8\">" in result
    assert "<h1>Header</h1>" in result
    assert "<p>Paragraph</p>" in result
    
    # Verify proper placement
    assert result.index("<title>") < result.index("<h1>")
    assert result.index("<meta") < result.index("<p>")
```

## Integration with Air Components

Layouts work seamlessly with Air's component system:

```python
def UserCard(user):
    return air.Div(
        air.H3(user["name"]),
        air.P(user["email"]),
        class_="user-card"
    )

@app.get("/users")
def users_page():
    users = get_all_users()
    return air.layouts.picocss(
        air.Title("Users"),
        air.H1("All Users"),
        *[UserCard(user) for user in users]
    )
```

Layouts handle the document structure, while components handle the content structure - a perfect separation of concerns.

## Common Patterns

### Form Pages

```python
@app.get("/contact")
def contact_form():
    return air.layouts.picocss(
        air.Title("Contact Us"),
        air.H1("Get in Touch"),
        air.Form(
            air.Input(name="name", placeholder="Your Name", required=True),
            air.Textarea(name="message", placeholder="Your Message"),
            air.Button("Send Message", type="submit"),
            method="post",
            action="/contact"
        )
    )
```

### Error Pages

```python
@app.exception_handler(404)
def not_found(request, exc):
    return air.layouts.picocss(
        air.Title("Page Not Found"),
        air.H1("404 - Page Not Found"),
        air.P("The page you're looking for doesn't exist."),
        air.A("Return Home", href="/")
    )
```

### API Documentation

```python
@app.get("/docs")
def api_docs():
    return air.layouts.mvpcss(
        air.Title("API Documentation"),
        air.H1("API Reference"),
        air.H2("Authentication"),
        air.P("All requests require an API key..."),
        air.H2("Endpoints"),
        air.H3("GET /users"),
        air.P("Returns a list of users...")
    )
```

Air layouts provide the foundation for building beautiful, maintainable web applications. Start with the built-in layouts for rapid prototyping, then create custom layouts as your applications mature and your design requirements become more sophisticated.

The key insight: **layouts handle document structure, components handle content structure**. This separation lets you focus on building great user experiences while Air handles the HTML plumbing.
