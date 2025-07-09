# Air Tags

Tags, also known as "Air Tags", are a fast, expressive way to generate HTML. Instead of a template language, Air Tags use Python classes to represent HTML elements. This allows leveraging Python's capabilities to generate content.

!!! note

    This document covers how Tags, or Air Tags work. The full reference for them is the [Tag API Reference](../api/tags.md).

## What are Air Tags?

**Air Tags** are Python classes that render HTML. They can be combined to render web pages or small components. Air Tags are typed and documented, working well with any code completion tool.

## How Air Tags work

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

The best way to define your own Air Tags is to subclass the `air.Tag` class. Here's a simple example:


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

## Functions as Custom Air Tags 

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