# Introduction to Air

## What is Air?

Air is a Python web framework built on top of FastAPI that enables you to build both elegant HTML interfaces and powerful REST APIs within a single application. Air streamlines common web development workflows while maintaining the flexibility and power of the underlying FastAPI ecosystem.

Key concepts:

- **Web Framework**: A structured approach to building web applications
- **API (Application Programming Interface)**: Programmatic interfaces for data exchange
- **HTML**: The markup language for web browsers
- **Python**: The programming language underlying our applications

## Key Features of Air

1. **Air Tags**: Python classes that generate HTML, offering type safety and IDE autocompletion while maintaining clean Python syntax. For example, `air.H1("Hello")` generates an HTML heading `<h1>Hello</h1>`.

2. **Layouts**: Intelligent document structure handling that automatically separates head and body content, eliminating boilerplate and providing styling options.

3. **Streamlined Routing**: Direct mapping between Python functions and URL endpoints with both decorator-based and conventional routing patterns.

4. **Pydantic-Powered Forms**: Built-in form validation and processing using Pydantic models, providing robust data handling with type safety.

5. **HTMX Integration**: Native support for HTMX's progressive enhancement approach, enabling dynamic interfaces without client-side JavaScript frameworks.

6. **Jinja Compatibility**: Seamless integration with Jinja2 templating for teams preferring traditional server-side rendering.

7. **Database Agnostic**: Works with any Python database library (SQLAlchemy, Tortoise ORM, etc.)

8. **Unified Application Architecture**: First-class support for serving both HTML interfaces and API endpoints from a single codebase.

## Why Choose Air?

Air is ideal for developers who want to:

- Build modern, interactive web applications quickly
- Leverage FastAPI's ecosystem without HTML response boilerplate
- Create unified applications serving both UI and API clients
- Maintain type safety and IDE support throughout development
- Work with Pythonic, readable code patterns

## Philosophy of Air

Air prioritizes these principles:

1. **Developer Experience**: Intuitive, discoverable APIs that follow Python conventions
2. **Pythonic Design**: Leverages Python's natural syntax and type system
3. **Type Safety**: Full type hinting for better development tooling and error prevention  
4. **Flexibility**: Accommodates various architectural patterns and team preferences
5. **Productivity**: Reduces boilerplate while preserving power for complex applications