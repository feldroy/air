import json
import random

import air
from air_markdown import TailwindTypographyMarkdown as Markdown


def sorted_random_list():
    return [0] + sorted(random.sample(range(1, 9), 4)) + [10]


def generate_data():
    return json.dumps(
        {
            "data": [
                {
                    "x": sorted_random_list(),
                    "y": random.sample(range(10), 6),
                    "type": "scatter",
                },
                {
                    "x": sorted_random_list(),
                    "y": random.sample(range(10), 6),
                    "type": "scatter",
                },
            ],
            "title": "Fun charts with Plotly and Air",
            "description": "This is a demonstration of how to build a chart using Plotly and Air",
            "type": "scatter",
        }
    )


def render(request: air.Request):
    data = generate_data()
    return air.Children(
        air.Title("Air: The New FastAPI-Powered Python Web Framework (2025)"),
        Markdown("# Air loves charts!"),
        air.Div(id="randomChart"),
        air.Children(
            # Call the Plotly library to plot the library
            air.Script(
                f"var data = {data}; Plotly.newPlot('randomChart', data);",
                # Used to help HTMX know where to replace data
                id="dataSource",
                # Trigger HTMX to call new data every 2 seconds
                hx_trigger="every 2s",
                # Use HTMX to fetch new info from the /data route
                hx_get="/data",
                # When the data is fetched, replace the whole tag
                hx_swap="outerHTML",
            )
        ),
    )
