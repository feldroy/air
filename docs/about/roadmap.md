# Roadmap: Road to the Beta Release

<a href="https://github.com/orgs/feldroy/projects/2" target="_blank">Air Beta Release Project Board</a>

We're really proud of what we've accomplished with Air. In a few short months we've taken a sketch of an idea and built out a new web framework that is both new and exciting, yet able to plug effortlessly into the FastAPI ecosystem.

Through our own experiences and feedback from users we can say the following is working out quite well:

- **Air Tags** are really popular and most people enjoy the API. That it plugs so well into IDEs and LLMs is a super power. Performance could be better, but optimization will happen once Air reaches Beta
- **AirResponse** makes writing views powered by Jinja or Air Tags easy and fast. Like Air Tags the API feature for this is complete
- **Examples** in all the doc strings makes it much easier for both humans and LLMs. This is an ongoing effort
- **Jinja + Air Tags** base templates for layout and Air Tags for content is a really sweet pattern we should talk about more. Unfortunately Jinja inside of Air Tags is a challenge not yet solved
- **Ecosystem** Leaning into FastAPI-isms means its easy to plug into the large and vibrant FastAPI ecosystem. Deployment is also easy - Air deploys precisely the same way as FastAPI

For all of these accomplishments we've got a ways to go before I feel confident about taking Air from Alpha to Beta. It's not just a matter of stability, it is also features that I believe are core to the vision. I want the project to be easier and more powerful for app builders and end users alike.

## Timeline

TLDR: When we feel Air is ready

While it would be nice to have Air be a Beta project today there's something to be said about having the freedom to make breaking changes or to backtrack from designs when we must. It's easier to fix mistakes now than later when there are more projects that could be broken by us making breaking changes. By staying in alpha longer it gives us the opportunity to validate our ideas .

## Headlines

Here is what is planned for the Beta release, which is tracked on the <a href="https://github.com/orgs/feldroy/projects/2" target="_blank">Air Beta Release Project board</a>:

### Air Forms

Forms are a core part of any web framework. While the foundations for forms are in place with Air Tags, there is still a lot of work to be done. Part of it is that form libraries have to support a lot of edge cases. This includes:

- [x] Form validation - Ensure error messages are clear and helpful
- [ ] CSRF protection - Implement CSRF protection for forms
- [ ] Integration with FastAPI's dependency injection - This is coded but it is not stable yet
[ ] - Default widget cleanup - It is working but the code is ungainly and hard to extend

### Accessibility Improvements

There are a number of accessibility improvements that we can make, mostly for built-in layouts module and project documentation. This includes:

- [x] Light/Dark Modes for Air itself - Air layouts should support both light and dark modes out of the box, as well as the ability to switch between them
- [x] Light/Dark Modes for the docs
- [ ] Mobile and cross platform form support - Air layouts should resize tags to look perfect on any screen and will have a mobile version and a desktop version. We think this is already part of the MVPCSS framework but it needs to be tested and documented
- [ ] Confirm fonts resizing works properly

### Bringing AirMarkdown Into Air Core

AirMarkdown is currently a separate package. While it works, it is extremely challenging to alter the configuration. In trying to fix it we discovered that the architecture of AirMarkdown is not quite right, and when combined with the extra layer of abstraction in having it as a separate package makes it hard to correct. 

Our plan is to bring AirMarkdown into Air core with an optional dependency group, and redesign the architecture to make it more flexible and easier to configure. Then we'll extract it again once we're happy with the result.

### AirBlog Tutorial

In writing the blog tutorial we discovered a number of gaps in the documentation as well as bugs and missing features in Air itself. In our own professional work we often just hop over these by leaning into hard-won knowledge, but we can't expect new users to do the same. Especially when existing documentation for both FastAPI and Air on certain topics (Async SQLModel and SQLAlchemy come to mind) is either sparse or wrong.

The goal is to finish the blog tutorial, as that forces us to have Air be more user friendly.

### Authentication and Authorization

We want to make it easier to add authentication and authorization and user constructs to Air applications while preserving interoperability with the FastAPI dependency injection-based ecosystem. This includes:

- [ ] User models - Provide a base user model that can be extended
- [x] Authentication - Provide helper tools to make authentication easier, including OAuth2. FastAPI is of great help here, at this point we think we just need to document how to use it with Air
- [ ] Authorization - Provide helper tools to make authorization easier, including role-based access control

### AirComponents

This will be a layout library that provides elegant defaults for making awesome layouts.

Tools like [shadcn](https://ui.shadcn.com/) and other Tailwind-powered projects are really powerful, but require an understanding of CSS (or tailwind) to be able to use. AirComponents will address this through intelligent defaults so those of us who don't know CSS can use it to make incredible looking sites. Yet AirComponents will be built so that it can be easily modified to support all kinds of usecases.

AirComponents may be a separate repo and package, managed in its own [GitHub repo](https://github.com/feldroy/AirComponents). That will allow for faster velocity and provide room for playing with architecture and design. 

## What's already been completed

### Air Tag API

The Air Tag API is complete and stable. This is based off working projects as well as experiences in other frameworks. There are no planned breaking changes to this API, just incremental improvements including bugfixes, more helpful error messages, and finished stock tag documentation.

### AirResponse/Application/Router

The AirResponse, Application and Router APIs are mostly complete. There should be no breaking changes to these APIs, rather adding polish, addressing bugs, and improving error handling.

What we really like is that AirResponse is so flexible. It can return Jinja templates, Air Tags, or even raw HTML strings. This means that users can incrementally adopt Air Tags into existing FastAPI/Jinja projects. Or use other HTML renderers, just so long as they return a string or have a `.render()` method that returns a string.

### Air ORM (Powered by SQLModel/SQLAlchemy)

In working on the blog tutorial as well as professional projects it has become clear that tying Air to SQLModel/SQLAlchemy is really powerful. However, the configuration is a bit clunky and documentation for it is almost non-existent or full of errors. This means that humans and LLMs alike struggle to understand how to use it.

The goal is Air ORM is include helper tools to make using SQLModel/SQLAlchemy easier, as well as better documentation and examples.