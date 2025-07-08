# Alternatives, Inspiration, and Comparisons

Air was built on the shoulders of giants. Here we discuss what inspired Air and how Air compares to alternatives.

## Previous tools

### Django

Generally tied with FastAPI for popularity, Django comes with the stability of 20 years of use. 

Django is tightly coupled to relational databases (MySQL, PostgreSQL, SQLite, etc). Notably, third-party bridges to non-SQL engineers tend to have relatively short lifespans, typically measuring a few years.

Django pioneered high-quality, accessible documentation. That and its pluggable SQL-powered design really helped in the development of a vibrant ecosystem of third-party packages.

!!! note "Inspires Air to"

 1. Incorporate an HTML form validation system powered by pydantic
 2. Add a pluggable system for supporting an ecosystem of third-party packages
 3. Include user management as an early pluggable package.

### Flask

Flask is a small, atomic web framework that first appeared as an April Fool's Day prank. It is simple, easy to learn, and commonly used by API providers to show how to build Python integrations. The `Flask quickstart` is a powerful general reference for anyone with a web dev background.

Flask refuses to tie itself to much of anything, including database design. 

Of note is that core Flask uses a flat namespace. Instead of having to learn long library paths, Flask brings nearly everything into a global `flask` namespace.

!!! note "Inspires Air to"

 1. When possible, use the `air` namespace to simplify imports
 2. Stay simple and easy to learn
 3. Have a good quickstart document that provides an overview of performing common tasks.



### FastHTML

FastHTML is designed to build out web pages quickly. It provides an intuitive API that allows developers to build dynamic web apps without having to ever leave Python. 

While it wasn't the first framework to abstract HTML tags as Python objects, FastHTML's method of integrating the generation of HTML with return values from views allows for rapid development of both full pages and snippets. This, in turn, lends itself to easy usage with HTMX, meaning the rendered HTML is much simpler and easier to interpret than other frameworks that lean on heavy frontend tools like React.

This is in line with FastHTML's pattern of providing a lot of syntactical sugar for developers to lean on.

!!! note "Inspired Air to"

 1. Have an abstraction of HTML as Python objects, which in Air parlance is "Air Tags"
 2. Bundle Air's `AirResponse` to the `Air()` app factory for an easier, more intuitive design.


## Used by Air

### FastAPI

The most popular Python framework, FastAPI is a proven tool for building APIs. Odds are you came here because you wanted improved web page generation with FastAPI. 

FastAPI uses types to provide an intuitive and explicit API. Behaviors are sometimes controlled by types rather than configuration. A pleasant result of this is how nicely code completion works for FastAPI projects. This is a pattern we are emulating in Air.

The FastAPI project has superlative, engaging documentation. There's a sense of positivity in the prose that is infectious. Of note is how the project explains its inspiration, which in turn inspired this document.


!!! note "Air uses FastAPI to"

 1. Provide an application server
 2. Inspire us to have superlative documentation
 3. Stay positive - we're in this to support each other and have fun    
 4. Lean into types for better IDE and AI integrations.

 ### Pydantic

Pydantic is the most widely used data validation library for Python. We love using it to confirm the structure and quality of data.

One of the core components of FastAPI, Pydantic also uses types to provide an intuitive and explicit API. From simple to complex use cases, Pydantic handles everything and thanks to its Rust-powered backend, does so excellently at scale.

What we like about Pydantic's documention is the clean, intuitive structure of it. All the objects are well-documented, something that Air is working towards copying.


!!! note "Air uses Pydantic to"

 1. Power the form validation system
 2. Inspire us to better organize our documentation
 3. Lean into types for better IDE and AI integrations.