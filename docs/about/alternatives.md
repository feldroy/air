# Alternatives, Inspiration and Comparisons

Air was built on the shoulders of giants. Here we discuss what inspired Air and how Air compares to alternatives.

## Previous tools

### Django

Generally tied with FastAPI for popularity, Django comes with the stability of 20 years of use. 

Django is tightly coupled to relational databases (MySQL, PostgreSQL, Sqlite, etc) and third-party bridges to other databases tend to have relatively short lifespans typically measuring a few years.

Django is also notable in that it pioneered high quality, accessible documentation. That and it's pluggable SQL-powered design really helped in the development of a vibrant ecosystem of third-party packages.

!!! note "Inspires Air to"

    1. Incorporate an HTML form validation system powered by pydantic
    2. Add a pluggable system for supporting an ecosystem of third-party packages
    3. Include user management as an early pluggable package

### Flask

Flask is a small, atomic webframework that first appeared as an April Fool's Day prank. It is very simple, easy-to-learn, and commonly used by API providers to show how to build Python integrations. The `Flask quickstart` is a powerful general reference for anyone with a web dev background.

Flask refuses tie itself to much of anything, including database design. 

Of note is that core Flask uses a flat namespace. Instead of having to learn long library paths, Flask brings nearly everything into a global `flask` namespace.

!!! note "Inspires Air to"

    1. When possible, use the `air` namespace to simplify imports
    2. Stay simple and easy-to-learn
    3. Have a really good quickstart document



### FastHTML

FastHTML is designed to build out web pages quickly. It does this by providing an intuitive API that allows developers to build web apps without having to leave Python. From defining routes to views to writing HTML tags as Python functions or classes via its FT Components system.

While it wasn't the first framework to abstract out HTML tags as Python objects, FastHTML's method of integrating generation of HTML with return values from views allows for rapid development of both full pages and snippets. This in turn lends itself to easy using with HTMX.

This is inline with FastHTML's pattern of providing a lot of syntactal sugar for developers to lean on.

!!! note "Inspired Air to"

    1. Have an abstraction of HTML as Python objects, which in Air parlance is "Air Tags".
    2. Bundle Air's `TagResponse` to the `Air()` app factory for an easier, more intuitive design.


## Used by Air

### FastAPI

The reason for Air's existence is we wanted to help users of FastAPI to better leverage the framework to build the web pages that support their API implementations. While there's nothing wrong with using FastAPI to serve JSON for frontend apps, there's something to be said about reducing how many repos and languages are needed to support a project.

FastAPI uses types to the point of obsession. Behaviors are sometimes controlled by types rather than configuration. A pleasant result of this is how nicely code completion works for FastAPI projects. A pattern we are emulating



!!! note "Air uses FastAPI to"

    1. Have superlative documentation
    2. Stay positive - we're in this to support each other and have fun    
    3. Provide an intuitive and explicit API for people to build projects with\
    4. Lean into types for better IDE and AI integrations
