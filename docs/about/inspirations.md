# Inspirations

Air was built on the shoulders of giants. Here we discuss what inspired Air and the tools that serve as dependencies for Air.

## Previous tools

### [Django](https://djangoproject.com)

Generally tied with FastAPI for popularity, Django comes with the stability of 20 years of use.

Django is tightly coupled to relational databases (MySQL, PostgreSQL, SQLite, etc). Notably, third-party bridges to non-SQL engineers tend to have relatively short lifespans, typically measuring a few years.

Django pioneered high-quality, accessible documentation. That and its pluggable SQL-powered design really helped in the development of a vibrant ecosystem of third-party packages.

!!! note "Django inspires Air to"
    1. Incorporate an HTML form validation system powered by Pydantic
    2. Add a pluggable system for supporting an ecosystem of third-party packages
    3. Include user management as an early pluggable package.

### [Flask](https://flask.palletsprojects.com/)

Flask is a small, atomic web framework that first appeared as an April Fool's Day prank. It is simple, easy to learn, and commonly used by API providers to show how to build Python integrations. The `Flask quickstart` is a powerful general reference for anyone with a web dev background.

Flask refuses to tie itself to much of anything, including database design.

Of note is that core Flask uses a flat namespace. Instead of having to learn long library paths, Flask brings nearly everything into a global `flask` namespace.

!!! note "Flask inspires Air to"
    1. When possible, use the `air` namespace to simplify imports
    2. Stay simple and easy to learn
    3. Have a good quickstart document that provides an overview of performing common tasks.

### [htpy](https://htpy.dev/)

A standalone library for rendering Python objects as HTML, we considered using htpy instead of creating Air Tags. However, we prefer the parenthesis approach of Air Tags is more sound. In any case, htpy has a fantastic HTML to htpy CLI utility.

!!! note "htpy inspires Air to"
    Improve air-convert to support pipes better.

### [Dash](https://dash.plotly.com/)

Dash is designed to build out web pages quickly. Through its `html` package it provides an intuitive API that allows developers to build dynamic web apps without having to ever leave Python.

While it wasn't the first framework to abstract HTML tags as Python objects, Dash's method of integrating the generation of HTML with return values from views allows for rapid development of full pages and snippets. While a fascinating project, we feel its reliance on React means there's an extra layer of abstraction for developers to debug and deploy.

!!! note "Dash inspires Air to"
    1. Have an abstraction of HTML as Python objects, which in Air parlance is "Air Tags"
    2. Bundle Air's `AirResponse` to the `Air()` app factory for an easier, more intuitive design.

### [FastHTML](https://fastht.ml/)

FastHTML has some similarity with Dash, especially in its use of FT Components, its analogue of Dash HTML objects. Where FastHTML significantly differs from Dash is that it eschews React and other large frontend libraries in favor of using Python wherever possible. For reactivity it leans into the HTMX sphere. This means less abstraction, simpler HTML generation, and hence an easier debugging and deployment experience than Dash.

Of note is that FastHTML follows the Fastcore coding standard which is substantially different from PEP8.

The creators of Air have contributed a lot to FastHTML and elements of its ecosystem. We admire FastHTML's syntactical sugar and the velocity of onboarding new users.

!!! note "FastHTML inspires Air to"
    1. Support HTMX as a first class citizen of the framework
    2. Focus on syntactal sugar
    3. Know that we can build our own web framework

## Used by Air

### [FastAPI](https://fastapi.tiangolo.com/)

The most popular Python framework, FastAPI is a proven tool for building APIs. Odds are you came here because you wanted improved web page generation with FastAPI.

FastAPI uses types to provide an intuitive and explicit API. Behaviors are sometimes controlled by types rather than configuration. A pleasant result of this is how nicely code completion works for FastAPI projects. This is a pattern we are emulating in Air.

The FastAPI project has superlative, engaging documentation. There's a sense of positivity in the prose that is infectious. Of note is how the project explains its inspiration, which in turn inspired this document.

!!! note "Air uses FastAPI to"
    1. Provide a really nice layer on top of Starlette
    2. Inspire us to have superlative documentation
    3. Stay positive - we're in this to support each other and have fun
    4. Lean into types for better IDE and AI integrations.

    Anything you can do with with FastAPI, you can do with Air. Air is literally FastAPI with some extra features for working with HTML and HTMX.

### [Starlette](https://www.starlette.io/)

A light ASGI framework/toolkit, Starlette is the HTTP server that Air (and FastAPI) use to serve content. It is very simple and intuitive, meaning what FastAPI doesn't provide we can usually come up with something quickly in Starlette. Here's a short list of features:

- WebSocket support.
- In-process background tasks.
- Startup and shutdown events.
- Test client built on HTTPX.
- CORS, GZip, Static Files, Streaming responses.
- Session and Cookie support.
- 100% test coverage.
- 100% type annotated codebase.
- Few hard dependencies.

!!! note "Air uses Starlette to"
    Provide a solid foundation for being a web application server
    
    Anything you can do with Starlette, you can do with Air. In essence, Air builds off the idea of FastAPI being Starlette on steroids.

### [Pydantic](https://docs.pydantic.dev/)

Far and away Pydantic is the most widely used data validation library for Python. We love using it to confirm the structure and quality of data.

Pydantic uses types to provide an intuitive and explicit API. From simple to complex use cases, thanks to its Rust-powered backend, does so excellently at scale.

What we like about Pydantic's documentation is the clean, intuitive structure of it. All the objects are well-documented, something that Air is working towards copying.

!!! note "Air uses Pydantic to"
    1. Power the form validation system
    2. Inspire us to better organize our documentation
    3. Lean into types for better IDE and AI integrations.

### [Jinja](https://jinja.palletsprojects.com/)

An extremely popular template engine for Python, Jinja is nearly as old as Django. It provides a fast, secure, and designer-friendly way to generate HTML from template files. Its syntax is heavily inspired by Django's template language, but it offers more flexibility and a sandboxed execution environment.

While **Air Tags** could replace the need for a separate template language in many cases, we recognize the power and familiarity of Jinja. For example, creating base templates for sites is something many users and designers prefer to do in Jinja while leaning on Air Tags for content and HTMX response snippets. Therefore, Air provides first-class support for Jinja templates, allowing developers to choose the best tool for their specific needs.

!!! note "Air uses Jinja2 to"
    1. Provide a simple and powerful way to render dynamic HTML
    2. Support not just those familiar with Python with a means to render templates.
