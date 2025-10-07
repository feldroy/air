# Getting Started

## Prerequisites

Before we begin, you'll need:

1. **Python 3.12 or higher** (3.14 is recommended): The programming language we'll use. You can check your Python version with `python --version` or `python3 --version`.
2. **[uv](https://docs.astral.sh/uv/getting-started/installation/#installing-uv)**: A modern Python package and project manager that streamlines dependency management.
3. **A code editor**: [VS Code](https://code.visualstudio.com/) is recommended, though any Python-capable editor works.
4. **Basic command line familiarity**: Comfort with terminal commands like `cd`, `ls`/`dir`, etc.

## Installing Air

Let's start by creating a new project:

```bash
uv init myblog
```

This initializes a new Python project in a directory called `myblog`.

Familiarize yourself with the contents of a project created by `uv init`, if you're not already familiar:

```
myblog
├── .git
│   └── ...
├── .gitignore
├── .python-version
├── main.py
├── pyproject.toml
└── README.md
```

Here's what each file is:

- **`.git`**: Git repository directory that tracks changes to your project
- **`.gitignore`**: Specifies files and directories that Git should ignore
- **`.python-version`**: Specifies the Python version to use for this project
- **`main.py`**: The main Python file where you'll write your application code
- **`pyproject.toml`**: Project configuration file that includes dependencies and build settings
- **`README.md`**: Documentation file for your project

Now would be a good time to commit your work:

```bash
git add .
git commit -m "Initialize myblog project with uv"
```

Navigate to the project directory:

```bash
cd myblog
```

Open it in Visual Studio Code:

```bash
code .
```

Press `Ctrl+`` (backtick) to open a terminal in Visual Studio Code.

Set up a virtual environment for project isolation:

```bash
uv venv
```

Activate the virtual environment:

```bash
# On Mac/Linux:
source .venv/bin/activate

# On Windows:
.venv\Scripts\activate
```

Install Air with standard dependencies:

```bash
uv add "air[standard]"
```

This installs Air along with its recommended extensions for web development.

## Your First Air App

Replace the contents of `main.py` with:

```python title="main.py"
import air

app = air.Air()

@app.page
def index():
    title = "My Blog"  # TODO: Change this to your own blog title!
    return air.layouts.mvpcss(
        air.Head(air.Title(title)),
        air.H1(title),
        air.P("Welcome to my awesome Air-powered blog."),
    )
```

This creates a simple web application with:

- `import air`: Imports the Air framework
- `app = air.Air()`: Creates a new Air application instance
- `@app.page`: Decorator that maps the function to the root path `/`
- The function returns a complete HTML document using Air's layout system

!!! tip "Make It Yours!"
    This tutorial will be a lot more fun if you use it to make a real blog for yourself! Change that `"My Blog"` title to something that reflects your personality or interests. Here are some fun examples to get your creative juices flowing:
    
    - `"Carla's Tech Adventures"` or `"John's Culinary Journey"`
    - `"The Daily Musings of a Cat Lover"`
    - `"Code & Coffee"` or `"Python Ponderings"`
    - `"Creative Uma's Awesome Blog"` or `"Sony's Random Thoughts About Board Games"`
    - Get creative: `"The Midnight Coder's Chronicles"` or `"From Zero to Hero"`
    
    Don't forget to also update the paragraph text to match your personal style - maybe `"Welcome to my corner of the internet where I share my passion for [your topic]!"` or `"Thanks for stopping by my digital space!"`

Run the development server:

```bash
fastapi dev
```

Visit your application at: <a href="http://localhost:8000/" target="_blank">http://localhost:8000/</a>

!!! question "Why are we using fastapi to run Air?"

    Air is built on top of FastAPI, so we use the `fastapi` CLI command to run our Air application. This allows us to leverage FastAPI's powerful features while enjoying the simplicity and elegance of Air for building our web pages.

## Understanding Your First Application

Let's break down what's happening in this code:

1. **Import**: `import air` imports the Air framework
2. **App Creation**: `app = air.Air()` creates a new Air application instance
3. **Decorator**: `@app.page` is a decorator that tells Air to handle requests to the root path (`/`)
4. **Function**: `index()` is the function that processes the request and returns the response
5. **Layout**: `air.layouts.mvpcss()` provides a complete HTML document structure with basic styling

The `mvpcss` layout function automatically:

- Wraps content in proper HTML structure
- Includes MVP.css for basic styling
- Includes HTMX for interactive features
- Separates head and body content automatically

!!! info "More on Layouts"
    We'll explore layouts in much more detail in the [Air Tags and Layouts](04-air-tags-and-layouts.md) section, including how to create your own custom layouts.

**Air Tags**: The HTML elements you see in the code (`H1`, `P`, etc.) are called "Air Tags". These are Python classes that generate HTML. Each tag (like `H1`, `P`, `Div`) corresponds to an HTML element. When you create an instance of an Air Tag, it renders to the corresponding HTML:

```python
air.H1("Hello, World!")  # Renders as <h1>Hello, World!</h1>
air.P("This is a paragraph")  # Renders as <p>This is a paragraph</p>
```

Air Tags are type-safe and provide IDE autocompletion, making it easier to write correct HTML.

!!! info "More on Air Tags"
    We'll dive deeper into Air Tags, their attributes, and advanced usage in the [Air Tags and Layouts](04-air-tags-and-layouts.md) section.

Now would be a good time to commit your work:

```bash
git add .
git commit -m "Add minimal Air app with index page"
```