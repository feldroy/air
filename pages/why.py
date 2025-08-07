from random import sample

import air
from air_markdown import TailwindTypographyMarkdown as Markdown


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


def render(request: air.Request):
    return air.Children(
        Markdown("# Don't use Air<br><br>"),
        air.P(
            air.I(
                reasons_not_to_use_air(),
                hx_trigger="every 3s",
                hx_get="/dontuseair",
                hx_swap="outerHTML",
            )
        ),
        Markdown("""
<br>                 
Air is a highly-unstable and experimental Python web framework. We have not officially launched it publicly yet. Every release could break your code. If you have to ask why you should use it, it's probably not for you.

We just started writing this thing. Don't judge it by what you see here. It's like looking at a painting that an artist started 5 minutes ago and saying, "Why are you even painting this? Why don't you go buy a painting?"

If you want to use Air, you can. But we don't recommend it. It's not enterprise-ready and will likely never be, at least definitely not before official launch. It'll likely infect you, your family, and your codebase with an evil web framework mind virus, distracting you to the point that you never ship because you're having too much fun playing with Air and contributing to the exciting Air ecosystem.

## Still Here?

Okay, here's why you might want to use Air:

- **Building in Public With Us Is Fun** - We're building Air in public. While not officially launched for real, we soft-launched it at Python Philippines on August 2, 2025 to find early volunteers for the core team. You can be part of the core team too, if you ask nicely and commit enough :)
- **Powered by FastAPI** - Designed to work with FastAPI so you can serve your API and web pages from one app
- **Fast to code** - Tons of intuitive shortcuts and optimizations designed to expedite coding HTML with FastAPI
- **Air Tags** - Easy to write and performant HTML content generation using Python classes to render HTML
- **Jinja Friendly** - No need to write `response_class=HtmlResponse` and `templates.TemplateResponse` for every HTML view
- **Mix Jinja and Air Tags** - Jinja and Air Tags both are first class citizens. Use either or both in the same view!
- **HTMX friendly** - We love HTMX and provide utilities to use it with Air
- **HTML form validation powered by Pydantic** - We love using Pydantic to validate incoming data. Air Forms provide two ways to use Pydantic with HTML forms (dependency injection or from within views)
- **Built-in SVG support** - SVGs aren't an afterthought, they are part of core Air and can be accessed via the `air.svgs` namespace
- **Code formatting and linting (PEP8)** - To maintain code quality and consistency, Air enforces Ruff formatting and linting across its entire codebase
- **Easy to learn yet well documented** - Hopefully Air is so intuitive and well-typed you'll barely need to use the documentation. In case you do need to look something up we're taking our experience writing technical books and using it to make the best documentation we can.
- **Ecosystem-Focused** - Air is developed with an ecosystem-first approach. Django achieved its success largely because of its Django package ecosystem. Contributing to Air means contributing not just to the core package but to any Air package.

Actually, there are a lot more reasons, but we got tired of editing this page and wanted to get back to coding.

**Link: [Alternatives, Inspiration, and Comparisons to Air](https://airdocs.fastapicloud.dev/about/alternatives)**

**Link: [How to help Air or get help](https://airdocs.fastapicloud.dev/about/help_air)**

**Documentation**: <a href="https://airdocs.fastapicloud.dev/" target="_blank">airdocs.fastapicloud.dev</a>

**Source Code**: <a href="https://github.com/feldroy/air" target="_blank">github.com/feldroy/air</a>"""),
    )
