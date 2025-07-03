# Quickstart

## A Minimal Application

A minimal Air application:

=== "Air Tags"

    ```python title="main.py"
    import air

    app = air.Air()

    @app.get('/')
    async def index():
        return air.H1('Hello, world')
    ```

    So what does this code do?

    1. First we import the air project.
    2. Next we instantiate the Air app. `air.Air` is just a conveinance wrapper around `fastapi.FastAPI` that sets the `default_response_class` to be `air.TagResponse`
    3. We define a GET route using `@api.get`, with comes with a response class of `TagResponse`. Now, when we return Air Tags, they are automatically rendered as HTML
    4. We return `air.H1`, which renders as an `<h1></h1>` tag. The response type is `text/html`, so browsers display web pages.

=== "Jinja2"


    ```python title="main.py"
    import air    
    from fastapi import Request

    app = Air()
    render = air.Jinja2Renderer(directory="templates")

    @app.get('/')
    async def index(request: Request):
        return render(
            request,
            name="home.html"
        )       
    ```

    ```jinja title="templates/home.html"
    <h1>Hello, world</h1>
    ```

    So what does this code do?

    1. First we import the air project and a few select things from FastAPI.
    2. Next we instantiate the Air app. `air.Air` is just a convenience wrapper around `fastapi.FastAPI` that sets the `default_response_class` to be `air.TagResponse`
    3. We use `Jinja2Renderer` factory to configure a `render()` shortcut. This is easier to remember and faster to type than `template.TemplateResponse`.
    4. We define a GET route using `@api.get`. Unlike normal FastAPI projects we don't need to set the `response_class` to HtmlResponse. That's because the `air.Air` wrapper handles that for us.
    5. Our return calls `render()`, which reads the specified Jinja2 template and then produces the result as an `<h1></h1>` tag. The response type is `text/html`, so browsers display web pages

## Running the Application

To run your FastAPI application with uvicorn:

```bash
uvicorn main:app --reload
```

Where:

- `main` is the name of your Python file (main.py)
- `app` is the name of your FastAPI instance
- `--reload` enables auto-reloading when you make changes to your code (useful for development)

Once the server is running, open your browser and navigate to:

- **[http://localhost:8000](http://localhost:8000)** - Your application

## The `app.page` decorator

For simple HTTP GET requests, Air provides the handy `@app.page` shortcut. 


=== "Air Tags"

    ```python title="main.py"
    import air

    app = air.Air()


    @air.page
    def dashboard():
        return H1('Dashboard')
    ```


=== "Jinja2"


    ```python title="main.py"
    import air    
    from fastapi import Request

    app = Air()
    render = air.Jinja2Renderer(directory="templates")

    @air.page
    async def dashboard(request: Request):
        return render(
            request,
            name="dashboard.html"
        )       
    ```

    ```jinja title="templates/home.html"
    <h1>Dashboard</h1>
    ```