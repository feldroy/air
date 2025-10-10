# HTMX and Interactive Interfaces

!!! warning "Unreliable, incorrect advice lurks here"

    This chapter likely contains heavy AI edits on Daniel Roy Greenfeld's initial handwritten blog tutorial. AI has expanded sections, and Audrey M. Roy Greenfeld has not tested and rewritten those yet. 
    
    Please treat it as a very early draft, and DO NOT TRUST anything that this chapter says! We welcome your pull requests to help refine the material so it actually becomes useful.

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
import asyncio
import random


@app.page
def sse_demo():
    """Server-Sent Events demo."""
    return air.layouts.mvpcss(
        air.Title("SSE Demo"),
        air.H1("Server-Sent Events Demo"),
        air.Div(id="events", style="height: 200px; overflow-y: scroll; border: 1px solid #ccc; padding: 10px;"),
        air.Script(
            """
            const eventSource = new EventSource('/events');
            const eventsDiv = document.getElementById('events');
            
            eventSource.onmessage = function(event) {
                const p = document.createElement('p');
                p.textContent = event.data;
                eventsDiv.appendChild(p);
                eventsDiv.scrollTop = eventsDiv.scrollHeight;
            };
            """,
            type="module"
        ),
        air.A("← Back to Home", href="/")
    )


@app.get("/events")
async def events():
    """SSE endpoint."""
    async def event_generator():
        for i in range(100):
            await asyncio.sleep(2)  # Wait 2 seconds
            yield air.Raw(f"data: Event {i} at {datetime.now()}\\n\\n")
    
    return air.SSEResponse(event_generator())
```

Now would be a good time to commit your work:

```bash
git add .
git commit -m "Add HTMX and interactive interface features"
```