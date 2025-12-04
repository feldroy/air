# Charts

Air is great for building charts. Using [plotly](https://plotly.com/javascript/), here's a simple chart example.

```
import air
import json

app = air.Air()


@app.get("/")
def index():
    title = "Air Chart Demo"
    data = json.dumps(
        {
            "data": [
                {"x": [0, 4, 5, 7, 8, 10], "y": [2, 9, 0, 4, 3, 6], "type": "scatter"},
                {"x": [0, 1, 2, 4, 8, 10], "y": [9, 2, 4, 3, 5, 0], "type": "scatter"},
            ],
            "title": "Fun charts with Plotly and Air",
            "description": "This is a demonstration of how to build a chart using Plotly and Air",
            "type": "scatter",
        }
    )
    return air.layouts.mvpcss(
        air.Script(src="https://cdn.plot.ly/plotly-3.0.1.min.js"),
        air.Title(title),
        air.H1(title),
        air.Article(
            air.P(
                "Made with ",
                air.A("Air", href="https://github.com/feldroy/air"),
                " and ",
                air.A("Plotly", href="https://plotly.com/javascript/"),
            ),
            air.Div(id="chart"),
            air.Script(f"var data = {data}; Plotly.newPlot('chart', data);"),
        ),
    )
```

Air makes it possible to build charts that pull data from servers and animate the results. Here's an example being supplied with random numbers for the Air server.

```
air.Children(
    air.Div(id="randomChart"),
    air.Script("""
        var data = {"data": [{"x": [0, 4, 5, 7, 8, 10], "y": [2, 9, 0, 4, 3, 6], "type": "scatter"}, {"x": [0, 1, 2, 4, 8, 10], "y": [9, 2, 4, 3, 5, 0], "type": "scatter"}], "title": "Fun charts with Plotly and Air", "description": "This is a demonstration of how to build a chart using Plotly and Air", "type": "scatter"};
        Plotly.newPlot('randomChart', data);""",
        # ID is used to help HTMX know where to replace data
        id="dataSource",
        # Trigger HTMX to call new data every 2 seconds
        hx_trigger="every 2s",
        # Use HTMX to fetch new info from the /data route
        hx_get="/data",
        # When the data is fetched, replace the whole tag
        hx_swap="outerHTML",
    )
)
```
