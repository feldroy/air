# Tutorial

Welcome! If you're looking to build a modern web app that combines beautiful HTML pages with a powerful REST API, you're in the right place. Air is a friendly layer over FastAPI, making it easy to create both interactive sites and robust APIs—all in one seamless app.

## Project AirBlog

We're going to create a simple blogging platform called AirBlog. It will have:

1. A web interface for reading and writing blog posts.
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
        air.Body(
            air.H1(title),
            air.P("Your go-to platform for blogging with Air."),
        ),
    )
```

Let's see what this looks like. Run the following command to start the development server:

```bash
fastapi dev
```

Open your page by clicking this link: <a href="http://localhost:8000/" target="_blank">http://localhost:8000/</a>

!!! question "Why are we using fastapi to start Air?"

    Air is built on top of FastAPI, so we use the `fastapi` command to run our Air application. This allows us to leverage FastAPI's powerful features while enjoying the simplicity and elegance of Air for building our web pages.

## Want to learn more?

TODO


