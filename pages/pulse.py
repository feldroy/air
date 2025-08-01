import air
import httpx
from datetime import datetime, timedelta, timezone
from collections import Counter
import json

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
    headers = {"Accept": "application/vnd.github+json"}

    commit_dates = []

    with httpx.Client() as client:
        while True:
            response = client.get(base_url, params=params, headers=headers)
            if response.status_code != 200:
                raise Exception(f"GitHub API error: {response.status_code} - {response.json().get('message', '')}")
            
            commits = response.json()
            if not commits:
                break

            for commit in commits:
                date_str = commit['commit']['committer']['date'][:10]
                commit_dates.append(date_str)

            params["page"] += 1

    # Count and sort dates ascending
    return dict(sorted(Counter(commit_dates).items()))

def format_data(data):
    return {
            "data": [
                {
                    "x": list(data.keys()),
                    "y": list(data.values()),
                    "type": "scatter",
                    'fill': 'tozeroy',
                },
            ],
            "title": "Fun charts with Plotly and Air",
            "description": "This is a demonstration of how to build a chart using Plotly and Air",
            "type": "scatter",
        }

data_cached = json.dumps(format_data(get_commit_frequency('feldroy/air')))


def render(request: air.Request):

    return air.Children(
        air.Article(air.P(data_cached)),
        air.Div(id="pulseChart"),
        air.Children(
            # Call the Plotly library to plot the library
            air.Script(
                f"var data = {data_cached}; Plotly.newPlot('pulseChart', data);",
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