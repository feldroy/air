# Air Reference

Here is the Air reference documentation. It explains how to do things, as well as providing reference details for nearly every object in the Air code.

- [Applications](../api/applications.md) - The app instantiator for Air
- [Background Tasks](../api/background.md) - Background tasks for Air
- [Exception Handlers](../api/exception_handlers.md) - Exceptions are returned to the user, specifically 404 and 500
- [Exceptions](../api/exceptions.md) - Sometimes it's good to know exactly what is breaking
- [Ext](../api/ext/index.md) - Functionality for Air that requires extra dependencies
    - [Auth](../api/ext/auth.md) - Authentication tools for OAuth and eventually email and magic link.
    - [SQLModel](../api/ext/sqlmodel.md) - Utilities for connecting to relational databases like PostgreSQL, MySQL, and SQLite for use with SQLModel. SQLAlchemy can also be used through this module, but this does require the `sqlmodel` dependency.
- [Forms](../api/forms.md) - Receive and validate data from users on web pages
- [Layouts](../api/layouts.md) - Utilities for building layout functions and two example layouts for css microframeworks (mvcss and picocss)
- [Middleware](../api/middleware.md) - Middleware for Air
- [Requests](../api/requests.md) - HTMX utility function that can be used with dependency injection
- [Responses](../api/responses.md) - AirResponse for normal responses and SSEResponse for Server Sent Events
- [Routing](../api/routing.md) - For compositing multiple apps inside each other
- [SVG](../api/svg/index.md) - Reference for all the entire SVG tags specification, all of which are supported by Air
- [Tags](../api/tags/index.md) - Reference for all the entire HTML tags specification, all of which are supported by Air
- [Templating](../api/templating.md) - Describes Jinja and Air Tag renderers for use in both projects and third-party installable packages
- [Utils](../api/utils.md) - Utilities that don't fall into one of the above categories