# Advanced Routing and URL Management

!!! warning "First draft!"

    Please treat this as a very early draft, and be careful with anything that this chapter says! We welcome your pull requests to help refine the material so it actually becomes useful.

Air provides multiple ways to define routes, making it easy to handle various URL patterns and request methods.

## HTTP Methods

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

## Path Parameters

Path parameters are values extracted from the URL path:

```python
@app.get('/users/{user_id}/posts/{post_id}')
def post_detail(user_id: int, post_id: int):
    # Process user_id and post_id
    return air.P(f"Post {post_id} for user {user_id}")
```

## Query Parameters

Query parameters are values passed in the URL after `?`:

```python
@app.get('/search')
def search(query: str, page: int = 1, limit: int = 10):
    # Process the search parameters
    return air.P(f"Searching for '{query}' on page {page}")
```

## Mixed Parameters

You can combine path and query parameters:

```python
@app.get('/users/{user_id}')
def user_detail(user_id: int, include_posts: bool = False):
    # user_id from path, include_posts from query string
    if include_posts:
        return air.P(f"User {user_id} with posts")
    return air.P(f"User {user_id} without posts")
```

## Request Data

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

## Path Separator Configuration

Air uses hyphens as path separators by default, but you can configure this:

```python
app = air.Air(path_separator="/")  # Use slashes instead of hyphens

@app.page
def my_page():  # Will route to /my/page instead of /my-page
    return air.P("This uses slash separators")
```

## URL Generation

Route functions provide a `.url()` method for generating URLs programmatically, making it easy to create links and redirects without hardcoding URLs:

```python
@app.get('/users/{user_id}/posts/{post_id}')
def post_detail(user_id: int, post_id: int):
    return air.P(f"Post {post_id} for user {user_id}")

# Generate URL with path parameters
url = post_detail.url(user_id=123, post_id=456)
# Returns: "/users/123/posts/456"
```

This works with all route decorators including `.get()`, `.post()`, `.page()`, and is particularly useful for:

- Creating redirects
- Generating navigation links
- Building canonical URLs

### Using .url() for Redirects

```python
@app.get('/redirect-to-post')
def redirect_example():
    return air.RedirectResponse(post_detail.url(user_id=1, post_id=2))
```

### Using .url() in Templates

```python
@app.page
def navigation():
    return air.layouts.mvpcss(
        air.H1("Navigation"),
        air.Ul(
            air.Li(air.A("View Post 1", href=post_detail.url(user_id=1, post_id=2))),
            air.Li(air.A("View Post 2", href=post_detail.url(user_id=3, post_id=4)))
        )
    )
```

### Using .url() with @app.page

The `.url()` method also works with the `@app.page` decorator:

```python
@app.page
def about():
    return air.P("About us")

@app.page
def index():
    return air.layouts.mvpcss(
        air.H1("Home"),
        air.A("Learn more", href=about.url())
    )
```
