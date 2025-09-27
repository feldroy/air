# Tutorial

Welcome! If you're looking to build a modern web app that combines beautiful HTML pages with a powerful REST API, you're in the right place. Air is a friendly layer over FastAPI, making it easy to create both interactive sites and robust APIs—all in one seamless app.

## Project AirBlog

We're going to create a markdown file-powered blogging platform called AirBlog. It will have:

1. A web interface for reading blog posts.
2. A REST API for programmatic access to blog posts.

## Prerequisites:

1. Make sure you have [uv](https://docs.astral.sh/uv/getting-started/installation/#installing-uv) installed. This will handle installing Python, setting up a virtual environment, installing dependencies, and running your app.
2. Ensure you have a code editor like [VS Code](https://code.visualstudio.com/) installed.

## Starting the project

At the command line, create your project using the following command:

```bash
uv init airblog
```

Enter the new directory:

```bashbash
cd airblog
```

Initialize a virtual environment in which we can install dependencies:

```bash
uv venv
```

Depending on your operating system, you will need to activate the virtual environment. Fortunately, `uv` makes this easy by providing instructions for your operating system on how to activate the virtual environment. Follow the instructions provided by `uv` to activate the virtual environment.

## Breathing in some air: Installing your first dependency

Now that we have our virtual environment activated, let's install Air:

```bash
uv add "air[standard]"
```

Done! Now we can start writing some code!


## Creating the homepage

!!! tip "To learn best, write out the code!"

    It's important to write out the code yourself, rather than copy-pasting. This helps you learn better and get familiar with the syntax. Just like you can't build muscles by watching others exercise, you can't learn programming effectively by copy-pasting code. So take your time, type it out, and enjoy the learning process!

Remove the existing `main.py` file and create a new one. For now we'll keep things extremely simple:

```python title="main.py"
import air

app = air.Air()

@app.page
def index():
    title = "AirBlog!"
    return air.layouts.mvpcss(
        air.Head(air.Title(title)),
        air.H1(title),
        air.P("Your go-to platform for blogging with Air."),
    )
```

Let's see what this looks like. Run the following command to start the development server:

```bash
fastapi dev
```

Open your page by clicking this link: <a href="http://localhost:8000/" target="_blank">http://localhost:8000/</a>

!!! question "Why are we using fastapi to run Air?"

    Air is built on top of FastAPI, so we use the `fastapi` CLI command to run our Air application. This allows us to leverage FastAPI's powerful features while enjoying the simplicity and elegance of Air for building our web pages.

## Creating some articles

Create a new directory called `articles` in the root of your project. Inside this directory, create a new file called `hello-world.md` with the following content:

````markdown title="articles/hello-world.md"
---
title: Hello World
description: A simple example of an Air application that responds with "Hello, World!".
slug: hello-world
published: true
date: 2025-09-26
author: Daniel Roy Greenfeld
tags:
- example
- beginner
- tutorial
---

Let's create a simple AirBlog application powered by Markdown.

```python
for i in range(10):
    print("Hello, World!")
```
````

The file has two sections, the first one is called "frontmatter" and is delimited by `---` lines. This section contains metadata about the article, such as its title, description, slug (used in the URL), publication status, date, author, and tags. The second section is the main content of the article, written in Markdown format.

Create another file called `markdown-features.md` with the following content:

```markdown title="articles/markdown-features.md"
---
title: Markdown features
description: A page for showing off all the things markdown renders to.
slug: markdown-features
published: true
date: 2025-09-27
author: Daniel Roy Greenfeld
tags:
- example
- beginner
- tutorial
- markdown
---

# H1 title

A paragraph with **bold** text, *italic* text, and `inline code`.

# H2 title

A list of items:

- one
- two
- three

# H3 title

A numbered list:

1. First item
2. Second item
3. Third item

A blockquote:

> This is a blockquote.
```

## Getting articles into our app

To read the articles from the `articles` directory, we'll use the pathlib and frontmatter libraries. The first one is part of the Python standard library, and the second one we need to install. Let's install it now:

```bash
uv add python-frontmatter
```

Now, let's modify our `main.py` file to read the articles and display them on the homepage. Add the shaded lines of code to your `main.py` file:

```python title="main.py" linenums="1" hl_lines="1-23 8-16"
from pathlib import Path
from frontmatter import Frontmatter

import air


def get_articles() -> list[dict]:
    articles = []
    # Read all markdown files in the articles directory
    for path in Path("airblog-articles").glob("*.md"):
        # Parse the frontmatter and content of each file
        # then add it to the articles list
        articles.append(Frontmatter.read_file(path))
    # Sort articles by date in descending date order
    return sorted(articles, key=lambda x: x["attributes"]["date"], reverse=True)


app = air.Air()

@app.page
def index():
    title = "AirBlog!")
    return air.layouts.mvpcss(
        air.Head(air.Title(title)),
        air.H1(title),
        air.P("Your go-to platform for blogging with Air."),
    )
```

At the command line, use Python's interactive shell (also known as REPL) to check that the `get_articles` function works as expected.

```python
python
>>> from main import get_articles
>>> get_articles()
[{'attributes': {'title': 'Markdown features',
   'description': 'A page for showing off all the things markdown renders to.',
   'slug': 'markdown-features',
   'published': True,
   'date': datetime.date(2025, 9, 27),
   'author': 'Daniel Roy Greenfeld',
   'tags': ['example', 'beginner', 'tutorial', 'markdown']},
  'body': '# H1 title\n\nA paragraph with **bold** text, *italic* text, and `inline code`.\n\n# H2 title\n\nA list of items:\n\n- one\n- two\n- three\n\n#\xa0H3 title\n\nA numbered list:\n\n1. First item\n2. Second item\n3. Third item\n\nA blockquote:\n\n> This is a blockquote.',
  'frontmatter': '\ntitle: Markdown features\ndescription: A page for showing off all the things markdown renders to.\nslug: markdown-features\npublished: true\ndate: 2025-09-27\nauthor: Daniel Roy Greenfeld\ntags:\n- example\n- beginner\n- tutorial\n- markdown\n'},
 {'attributes': {'title': 'Hello World',
   'description': 'A simple example of an Air application that responds with "Hello, World!".',
   'slug': 'hello-world',
   'published': True,
   'date': datetime.date(2025, 9, 26),
   'author': 'Daniel Roy Greenfeld',
   'tags': ['example', 'beginner', 'tutorial']},
  'body': 'Let\'s create a simple AirBlog application powered by Markdown.\n\n```python\nfor i in range(10):\n    print("Hello, World!")\n```',
  'frontmatter': '\ntitle: Hello World\ndescription: A simple example of an Air application that responds with "Hello, World!".\nslug: hello-world\npublished: true\ndate: 2025-09-26\nauthor: Daniel Roy Greenfeld\ntags:\n- example\n- beginner\n- tutorial\n'}]
```

What's happened is that we used `pathlib.Path` to find all the markdown files in the `articles` directory, then we used `frontmatter` to read each file and parse its frontmatter and body content. Finally, we sorted the articles by date in descending order.

Now, let's update the `index` function to display the list of articles on the homepage. Modify the `index` function in your `main.py` file as follows:

```python title="main.py" linenums="1" hl_lines="27-39"
from pathlib import Path
from frontmatter import Frontmatter

import air


def get_articles() -> list[dict]:
    articles = []
    # Read all markdown files in the articles directory
    for path in Path("airblog-articles").glob("*.md"):
        # Parse the frontmatter and content of each file
        # then add it to the articles list
        articles.append(Frontmatter.read_file(path))
    # Sort articles by date in descending date order
    return sorted(articles, key=lambda x: x["attributes"]["date"], reverse=True)


app = air.Air()

@app.page
def index():
    title = "AirBlog!")
    return air.layouts.mvpcss(
        air.Head(air.Title(title)),
        air.H1(title),
        air.P("Your go-to platform for blogging with Air."),
        air.Ul(
            *[
                air.Li(
                    air.A(
                        article["attributes"]["title"],
                        href=f'/{article["attributes"]["slug"]}',
                    ),
                    air.Br(),
                    article["attributes"]["description"],
                )
                for article in get_articles()
            ]
        )
    )
```
