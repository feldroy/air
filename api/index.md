# Air Reference

Here is the Air reference documentation. It explains how to do things, as well as providing reference details for nearly every object in the Air code.

- [Applications](applications/) - The app instantiator for Air
- [Background Tasks](background/) - Background tasks for Air
- [Exception Handlers](exception_handlers/) - Exceptions are returned to the user, specifically 404 and 500
- [Exceptions](exceptions/) - Sometimes it's good to know exactly what is breaking
- [Ext](ext/) - Functionality for Air that requires extra dependencies
  - [Auth](ext/auth/) - Authentication tools for OAuth and eventually email and magic link.
  - [SQLModel](ext/sqlmodel/) - Utilities for connecting to relational databases like PostgreSQL, MySQL, and SQLite for use with SQLModel. SQLAlchemy can also be used through this module, but this does require the `sqlmodel` dependency.
- [Forms](forms/) - Receive and validate data from users on web pages
- [Layouts](layouts/) - Utilities for building layout functions and two example layouts for css microframeworks (mvcss and picocss)
- [Middleware](middleware/) - Middleware for Air
- [Requests](requests/) - HTMX utility function that can be used with dependency injection
- [Responses](responses/) - AirResponse for normal responses and SSEResponse for Server Sent Events
- [Routing](routing/) - For compositing multiple apps inside each other
- [SVG](svg/) - Reference for the entire SVG tags specification, all of which are supported by Air
- [Tags](tags/) - Reference for the entire HTML tags specification, all of which are supported by Air
- [Templating](templating/) - Describes Jinja and Air Tag renderers for use in both projects and third-party installable packages
- [Utils](utils/) - Utilities that don't fall into one of the above categories
