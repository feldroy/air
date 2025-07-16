# Using Jinja with Air

We love Jinja. Proven and fast, its our go-to for when we want to manually craft templates containing programmatic content. To that end, we've ensured Air works great at combining Jinja and Air Tags together.

!!! note

    This document covers the concepts and how Jinja2 works in Air. The full reference for the tooling can be found at the [Templates API Reference](../api/templates.md).

!!! note "Jinja or Jinja2?"

    While the package is listed on [PyPI as Jinja2](https://pypi.org/project/jinja2/), that package and the [official Jinja docs](https://jinja.palletsprojects.com/) refers to Jinja as just "Jinja". Also, Jinja was released in 2008 and is well into the 3.x release cycle. If we want to lean into pedantry, we are arguably using Jinja 5 (base plus major releases cycles of 0.x, 1.x, 2.x, and 3.x)

    In any case, for the sake of brevity and to match the Jinja documentation, in the Air documentation we use the term "Jinja".



## Using Jinja for the HTML Layout

Air Tags are powerful but for those of us with a lot of experience with HTML, sometimes its easy to construct layouts using Jinja. As it is closer in look-and-feel to HTML for some of us that makes ensuring the end result looks good is easier. 

Here's a simple Jinja layout file:

```html+jinja title="templates/base.html"
<!doctype html>
<html>
    <head>
        <link
            rel="stylesheet"
            href="https://cdn.jsdelivr.net/npm/@picocss/pico@2/css/pico.min.css"></link>
        <script
            src="https://cdn.jsdelivr.net/npm/htmx.org@2.0.6/dist/htmx.min.js" 
            integrity="sha384-Akqfrbj/HpNVo8k11SXBb6TlBWmXXlYQrCSqEWmyKJe+hDm3Z/B2WVG4smwBkRVm"
            crossorigin="anonymous"></script>
        <title>{{title}}</title>
    </head>
    <body>  
        <main class="container">
        {# We need to safe the content, which can be 
            a security risk. We'll cover mitigation
            of such issues later on this page.
        #}
        {{content|safe}}
        </main>
    </body>
</html>
```

If you've used Jinja before this should look familiar. Now let's add in our Air Tags-powered content, which we'll do from the view.

```python title="main.py"
import air

app = Air()

# Set the Jinja render function
jinja = air.Jinja2Renderer(directory="tests/templates")

@app.get('/')
def index(request: Request):
    content = air.Main(
        air.h2('Does Jinja work with Air Tags?')
        air.P("Jinja works great with Air Tags")
    )
    return jinja(
        request,
        name="base.html",
        title="FAQ",
        content=content.render(),
    )
```

When run, this will look like this:

TODO: ADD SCREEN CAPTURE

!!! note "Why don't we call the `jinja()` function `render()`?"

    Because Air uses `.render()` as a method name in a lot of places, especially with Air Tags. So even though `render()` instead of `jinja()` is more semantically correct, to avoid confusion and collision, we use `jinja2()` instead.

    When several different things on the same page are called "render":

    ```python
    return render(
        request,
        name="base.html",
        title="FAQ",
        content=content.render(),
    )
    ```