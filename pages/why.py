from random import sample

import air
from air_markdown.tags import AirMarkdown


def reasons_not_to_use_air():
    reasons = [
        "unless you like living on the edge",
        "unless you believe in unicorns",
        "unless you like early stage projects",
        "unless you want to try an early stage project",
        "if you are building something where lives depend on stability",
        "because there's no paid support",
        "as it is just another Python web framework",
        "when you could be using COBOL",
        "if you have a problem with dairy-themed documentation (although we do like spicy vegan cheese dips)",
        "it's better to stay under water",
        "because we're running out",
        "if you want a full stack framework",
        "if you want something not in alpha",
        "if you prefer semantic versioning",
        "because we're off to see the wizard",
        "if you dislike PEP8 and type annotations",
        "if you don't like HTMX",
        "when you need a stable, mature project",
        "if you want React to be your frontend instead of HTML"
    ]
    return f"... {sample(reasons, 1)[0]}"


def rotating_reasons():
    return air.P(
        air.I(
            reasons_not_to_use_air(),
            hx_trigger="every 3s",
            hx_get="/dontuseair",
            hx_swap="outerHTML",
        )
    )
