# About

- [Read about what inspired Air and what it's built on](inspirations.md)
- [Helping Air and getting help about Air](help_air.md)
- [Air Beta Release Project Board](roadmap.md)

## Stories

### Daniel's Story

I first encountered FastAPI in late 2019. I immediately liked how it used types to define behavior.

In 2022 and 2023 I carefully reviewed all the Python web frameworks. From my perspective FastAPI won out over Django, Flask, Pyramid, and others. I even gave a series of talks on the subject.

In the middle of 2023, I was unhappy with how making web pages with FastAPI to support APIs felt clunky. It felt like a harder version of Flask. I talked to Sebastian Ramirez about it over the course of a week. I started thinking about making some kind of extension for FastAPI to make web pages easier, even wrote up a design document for it in December of 2023 titled "[FastHTML](https://docs.google.com/document/d/1CaAqTYmK7gXTHxkQ-SaMndJV7vev-34cvEBe1kKESQU/edit?usp=sharing)".

In early 2024 I noodled with the idea of a FastAPI for HTML, tentatively called "FastHTML". You can see one of my attempts here in a project called [fastapi-blog](https://github.com/pydanny/fastapi-blog). This particular project didn't go well, but allowed me to explore possible ideas for making a more friendly HTML API for developers. Alas, I was busy with work and family life and didn't have enough time to really focus on the project. I told Sebastian I was giving the effort a break.

Shortly after Sebastian Ramirez introduced me to Jeremy Howard of Answer.AI. Jeremy demonstrated a Starlette-descendant project, called, amusingly enough, 'FastHTML'. Like FastAPI, his FastHTML implementation was driven directly by Starlette. He eschewed Jinja2 templating for HTML, instead implementing FT Components, an elegant version of Python classes that can render as HTML. While I like Jinja2, I also liked his implementation of Python objects rendered to HTML. Excited about a shared vision I started contributing to his FastHTML.

In June of 2025 I started work on fastapi-tags, which is designed to bring fully typed Python classes that can render as HTML to FastAPI. After a couple weeks I realized I wanted to expand fastapi-tags to meet my original design document for building an HTML web page framework on top of FastAPI. The problem was that "fastapi-tags" didn't sound like a good framework name and "FastHTML" was already taken.

Fortunately for me, my wife Audrey had a static site generator project called "Air". She volunteered the name for the web framework, and thus this project was born.
