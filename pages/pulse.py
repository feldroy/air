import json
from collections import Counter
from datetime import datetime, timedelta, timezone
from functools import cache
from os import getenv

import air
import httpx


@cache
def get_commit_frequency(repo: str) -> dict:
    """
    Fetches the frequency of commits for the past 30 days for a GitHub repository using HTTPX.

    Args:
        repo (str): The GitHub repository in the format 'owner/repo'.

    Returns:
        dict: A dictionary where keys are dates (YYYY-MM-DD) and values are commit counts.
    """
    base_url = f"https://api.github.com/repos/{repo}/commits"
    since = (datetime.now(timezone.utc) - timedelta(days=30)).isoformat() + "Z"
    params = {"since": since, "per_page": 100, "page": 1}
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {getenv('GITHUB_TOKEN')}",
        "X-GitHub-Api-Version": "2022-11-28",  # optional but recommended
    }

    commit_dates = []

    with httpx.Client() as client:
        while True:
            response = client.get(base_url, params=params, headers=headers)
            if response.status_code != 200:
                raise Exception(
                    f"GitHub API error: {response.status_code} - {response.json().get('message', '')}"
                )

            commits = response.json()
            if not commits:
                break

            for commit in commits:
                date_str = commit["commit"]["committer"]["date"][:10]
                commit_dates.append(date_str)

            params["page"] += 1

    # Count and sort dates ascending
    return dict(sorted(Counter(commit_dates).items()))


def chart_setup(data):
    return json.dumps(
        {
            "data": [
                {
                    "x": list(data.keys())[0],
                    "y": list(data.values())[0],
                    "type": "scatter",
                    "fill": "tozeroy",
                },
            ],
            "title": "Fun charts with Plotly and Air",
            "description": "This is a demonstration of how to build a chart using Plotly and Air",
            "type": "scatter",
        }
    )


def get_frames(data):
    frames = []
    for key, value in data.items():
        frames.append(dict(name=key, data=[dict(y=value)]))
    return json.dumps(frames)


layout = json.dumps(
    {
        "title": "Animated Scatter Plot",
        "xaxis": {"range": [0, 31], "autorange": False},
        "yaxis": {"range": [0, 50], "autorange": False},
    }
)


def render(request: air.Request):
    initial_data = chart_setup(get_commit_frequency("feldroy/air"))
    frames = get_frames(get_commit_frequency("feldroy/air"))
    return air.Children(
        air.Article(air.P(initial_data)),
        air.Article(air.P(frames)),
        air.Div(id="scatterChart"),
        air.Children(
            # Call the Plotly library to plot the library
            air.Script(
                f"""const data = {initial_data};
                Plotly.newPlot('scatterChart', data, {layout})
                .then(() => {{
                    Plotly.addFrames('scatterChart', {frames});

                    // Animate all frames automatically
                    Plotly.animate('scatterChart', null, {{
                        frame: {{ duration: 500, redraw: true }},
                        transition: {{ duration: 300 }},
                        mode: 'immediate'
                    }});
                }});
                """,
            )
        ),
    )
