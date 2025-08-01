[](){ #air-tags }

# Air Tags

**Air Tags**, sometimes shortend to **Tags**, are Python classes that render HTML. They can be combined to render web pages or small components. **Air Tags** are typed and documented, working well with any code completion tool. They are designed to be an easy to write and performant HTML content generation system using Python classes to render HTML.

!!! note

    This document covers how **Air Tags** work. The full reference for them is the [Tag API Reference][tags].

## How **Air Tags** work

Used individually or combined into a greater whole, every Air Tag includes a `render()` method. When the render method is called, it returns the HTML representation of the Air Tag, as well as all the children of the Air Tag.

This example:

```python
>>> from air import Article, H1, P
>>> content = Article(
...     H1("Air Tags"),
...     P("Air Tags are a fast, expressive way to generate HTML.",
...             class_="subtitle")
... )
>>> content
<air.tags.Article at 0x1052f2cf0>
>>> content.render()
```

This is the output of the `render()` method for the example above:

```html
<article>
    <h1>Air Tags</h1>
    <p class="subtitle">Air Tags are a fast, expressive way to generate HTML.</p>
</article>
```

## Attributes

**Air Tags** convert keyword arguments into attributes. So:

```python+html
air.P('Hello', id="mine")
```

renders as:

```html
<p id="mine">Hello</p>
```

Lets take a look at some additional scenarios.

### Setting the `class` attribute

In Python `class` is a protected word. To set the `class` attribute in **Air Tags**, use the `class_` keyword.

```python
air.P('Hello', class_='plain')
```

renders as

```html
<p class="plain">Hello</p>
```

### Setting the `for` attribute

In Python `for` is a protected word. To set the `for` attribute in **Air Tags**, use the `for_` keyword.

```python
air.Label(
    'Email',
    air.Input(name='email', type='email')
    for_='email'
)
```

renders as

```html
<label for="email">
    Email
    <input name="email" type="email" />
</label>
```

### Attributes starting with special characters

To get around that in Python we can't begin function arguments with special characters, we lean into how **Air Tags** is kwargs friendly.

```python
air.P('Hello', class_='plain', **{'@data': 6})
```

Renders as:

```html
<p class="plain" @data="6">Hello</p>
```


### Single word attributes

To set or hide single word attributes like `@selected`, set the tag to `True` or `False` respectively. 

```python
air.Select(
    air.Option('South America', value='SA', selected=True),
    air.Option('North America', value='NA', selected=False)
)
```

Renders as:

```html
<select>
    <option value="SA" selected>South America</option>
    <option value="NA">North America</option>
</select>
```

If you need an value set to `true`, use `"true"` in Python. For example:

```python
air.P("Air makes FastAPI web pages easy", draggable="true")
```

Renders as:

```html
<p draggable="true">Air makes FastAPI web pages easy</p>
```

## Works well with SVGs

Unlike HTML, SVG tags are case-sensitive. You can access SVG tags by importing them from the `air.svg` module. Here's a simple example:

```python
from air import svg

svg.Svg(
    svg.Circle(cx='50', cy='50', r='40', fill='blue'),
    width='100',
    height='100'
)
```

This will render the following SVG:

```html
<svg width="100" height="100">
  <circle cx="50" cy="50" r="40" fill="blue" />
</svg>
```

## Custom Air Tags

The best way to define your own **Air Tags** is to subclass the `air.Tag` class. Here's a simple example:


```python
from air import Tag

class Tasty(Tag):
    pass
```

Let's instantiate this class and call its `render()` method:

```python
Tasty('Ice Cream', class_='dessert').render()
```

This will produce the following HTML:

```html
<awesome class="desert">Ice Cream</awesome>
```

## Functions as Custom **Air Tags** 

Subclasses are not the only way to create custom Air Tags. You can also use functions to create Air Tags. This is particularly useful for putting together components quickly without needing to define a class. Here's an example of a function that creates a custom Air Tag for a [picocss card](https://picocss.com/docs/card):

```python
def card(*content, header:str, footer:str):
    return air.Article(
        air.Header(header),
        *content,
        air.Footer(footer)
    )
```

We can use this function to create a card:

```python
card(
    air.P("This is a card with some content."),
    air.P("It can have multiple paragraphs."),
    header="Card Header",
    footer="Card Footer",
).render()
```

Which produces the following HTML:

```html
<article>
    <header>Card Header</header>
    <p>This is a card with some content.</p>
    <p>It can have multiple paragraphs.</p>
    <footer>Card Footer</footer>
</article>
```

## Returning Multiple Children (used in HTMX)

When using HTMX to add reactivity to pages, it is common to return several **Air Tags** so that HTMX can then replace existing DOM elements with new ones. **Air Tags** are heirchical, you need a base tag that just serves as a wrapper that doesn't generate any HTML. That tag is the `air.Tags`. Here's how to use it:


```python
import

@app.post('/cart/add/{product_id}/')
def update_cart(request: air.Request, product_id: int):
    "This is a simplified update cart view"
    # air.Tags renders the child tags without adding anything of its own
    return air.Tags(
        # Mark that an item has been added to the cart
        Button('Added!', hx_post='/cart/add/{{product.id}}', hx_swap_oob='true', id='add-button'),

        # Cart icon quantity changed
        A(f'Cart {count}', id='cart-icon', href='/cart', hx_trigger='polling 30s', hx_get='/cart-icon', hx_swap_oob='true'),
    )
```

This will generate HTML that looks something like this, without any wrapping text around the elements we are passing to the user's browser:


```html
<!-- Mark that an item has been added to the cart -->
<button
    hx-post="/cart/add/35"
    hx-swap-oob="true"
    id="add-button"
    >Added!</button>
<!-- Cart icon quantity changed -->
<a id="cart-icon" href="/cart"
    hx-trigger="polling 30s" hx-get="/cart-icon" hx-swap-oob="true"
     >Cart 2</a>
```

## Converting HTML to Air Tags

The easiest way to do that is with the [air-convert](https://pypi.org/project/air-convert/) package. 

## Converting HTML to Air Tags

The easiest way to do that is with the [air-convert](https://pypi.org/project/air-convert/) package. 

```sh
pip install air-convert
```

```python
from air_convert import html_to_airtags
html_to_airtags("""
<html>
    <body>
        <main>
            <h1 class="header">Hello, World</h1>
        </main>
    </body>
</html>""")
```

This generates:

```python
air.Html(
    air.Body(
        air.Main(
            air.H1('Hello, World', class_='header')
        )
    )
)
```

Removal of the `air.` prefix is done with the `air_prefix` boolean:

```python
html = """
<html>
    <body>
        <main>
            <h1 class="header">Hello, World</h1>
        </main>
    </body>
</html>"""
print(air.html_to_airtags(html, air_prefix=False))
```

This will generate:

```python
Html(
    Body(
        Main(
            H1('Hello, World', class_='header')
        )
    )
)
```