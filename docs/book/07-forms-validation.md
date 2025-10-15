# Forms and Data Validation

!!! warning "First draft!"
    
    Please treat this as a very early draft, and be careful with anything that this chapter says! We welcome your pull requests to help refine the material so it actually becomes useful.

Air provides powerful form handling capabilities with built-in validation using Pydantic.

## Basic Form Handling

Basic form handling in Air follows the Starlette pattern:

```python
@app.post("/submit-form")
async def submit_form(request: air.Request):
    form_data = await request.form()
    name = form_data.get("name")
    email = form_data.get("email")
    return air.P(f"Hello {name}, your email is {email}")
```

## Air Forms with Pydantic

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

## Form Field Types and Validation

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

## Custom Validation

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

## API Documentation and Reference

Air provides comprehensive API documentation. Here's a reference for the most important classes and functions:

### Core Application

- `air.Air()`: Main application class that extends FastAPI
- `@app.page`: Decorator for simple page routes (converts function name to URL)
- `@app.get`, `@app.post`, etc.: Standard FastAPI route decorators
- `app.add_middleware()`: Add middleware like session handling

### Layouts

- `air.layouts.mvpcss()`: MVP.css layout with HTMX
- `air.layouts.picocss()`: PicoCSS layout with HTMX
- `air.layouts.filter_head_tags()`: Filter tags for head section
- `air.layouts.filter_body_tags()`: Filter tags for body section

### Tags

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

### Forms

- `AirForm`: Pydantic-based form class
- `AirField`: Enhanced Pydantic fields with HTML attributes
- `form.render()`: Render form with validation errors
- `form.validate()`: Validate form data

### Responses

- `AirResponse`: Default HTML response class (alias for `TagResponse`)
- `SSEResponse`: Server-Sent Events response
- `RedirectResponse`: Redirect response
- `JSONResponse`: JSON response (from FastAPI)

### Utilities

- `Request`: Request object with session support
- `BackgroundTasks`: Handle background tasks
- `is_htmx_request`: Dependency to detect HTMX requests

## Best Practices

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