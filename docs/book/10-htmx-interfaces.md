# HTMX and Interactive Interfaces

!!! warning "First draft!"
    
    Please treat this as a very early draft, and be careful with anything that this chapter says! We welcome your pull requests to help refine the material so it actually becomes useful.

HTMX allows you to create dynamic, interactive web applications without writing JavaScript.

## Installing HTMX Support

HTMX is included by default in Air's built-in layouts. Let's create an interactive example:

```python
@app.page
def counter_demo():
    """Demo of HTMX counter."""
    return air.layouts.mvpcss(
        air.Title("HTMX Counter"),
        air.H1("HTMX Counter Demo"),
        air.Div(
            air.Button("Increment", hx_post="/increment", hx_target="#counter", hx_swap="innerHTML"),
            air.Button("Decrement", hx_post="/decrement", hx_target="#counter", hx_swap="innerHTML"),
            air.Button("Reset", hx_post="/reset", hx_target="#counter", hx_swap="innerHTML"),
            air.Div(0, id="counter", style="font-size: 2em; margin: 1rem 0;"),
        ),
        air.A("← Back to Home", href="/")
    )


# Store counter value in memory (in production, use database or Redis)
counter_value = 0

@app.post("/increment")
def increment():
    global counter_value
    counter_value += 1
    return air.Div(counter_value, id="counter", style="font-size: 2em; margin: 1rem 0;")

@app.post("/decrement")
def decrement():
    global counter_value
    counter_value -= 1
    return air.Div(counter_value, id="counter", style="font-size: 2em; margin: 1rem 0;")

@app.post("/reset")
def reset():
    global counter_value
    counter_value = 0
    return air.Div(counter_value, id="counter", style="font-size: 2em; margin: 1rem 0;")
```

## Advanced HTMX Features

HTMX attributes can be added to Air Tags:

```python
air.Div(
    "Content",
    hx_get="/api/data",           # Make GET request to /api/data
    hx_target="#result",          # Update element with id="result"
    hx_swap="innerHTML",          # Replace innerHTML of target
    hx_trigger="click",           # Trigger on click
    hx_indicator="#spinner"       # Show spinner while loading
)

# Form with HTMX
air.Form(
    air.Input(name="search", placeholder="Search..."),
    air.Button("Search", type="submit"),
    hx_post="/search",            # POST to /search
    hx_target="#results",         # Update #results div
    hx_indicator=".htmx-indicator" # Show loading indicator
)
```

## Server-Sent Events (SSE)

Air supports Server-Sent Events for real-time updates:

```python
import random
from asyncio import sleep

import air

app = air.Air()

@app.page
def index():
    return air.layouts.mvpcss(
        air.Script(src="https://unpkg.com/htmx-ext-sse@2.2.1/sse.js"), 
        air.Title("Server Sent Event Demo"),
        air.H1("Server Sent Event Demo"),
        air.P("Lottery number generator"),
        air.Section(
            hx_ext="sse",  
            sse_connect="/lottery-numbers", 
            hx_swap="beforeend show:bottom", 
            sse_swap="message", 
        ),
    )

async def lottery_generator():  
    while True:
        lottery_numbers = ", ".join([str(random.randint(1, 40)) for x in range(6)])
        # Tags work seamlessly
        yield air.Aside(lottery_numbers) 
        await sleep(1)


@app.page
async def lottery_numbers():
    return air.SSEResponse(lottery_generator())
```

Now would be a good time to commit your work:

```bash
git add .
git commit -m "Add HTMX and interactive interface features"
```