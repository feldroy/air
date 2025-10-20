# Advanced Patterns and Best Practices

!!! warning "First draft!"
    
    Please treat this as a very early draft, and be careful with anything that this chapter says! We welcome your pull requests to help refine the material so it actually becomes useful.

## Application Structure

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

## Separation of Concerns

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

## Template Integration

While Air Tags are powerful, you can also use Jinja2 templates:

```python
from air import JinjaRenderer

jinja = JinjaRenderer(directory="templates")

@app.get("/jinja-page")
def jinja_page(request: air.Request):
    return jinja(request, "home.html", {"title": "Jinja Page", "articles": get_articles()})
```

## Background Tasks

Handle background tasks:

```python
@app.post("/submit-form")
async def submit_form_with_background_task(request: air.Request, background_tasks: air.BackgroundTasks):
    form_data = await request.form()
    
    # Process form in background
    background_tasks.add_task(send_email, form_data.get("email"), form_data.get("message"))
    
    return air.P("Form submitted successfully!")
```

## Error Handling

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

## Performance Optimization

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
- **DevOps**: Deployment, monitoring, and CI/CD pipelines

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