We're really proud of what we've accomplished with Air. In a few short months we've taken a sketch of an idea and built out a new web framework that is both new and exciting, yet able to plug effortlessly into the FastAPI ecosystem.

Through our own experiences and feedback from users we can say the following is working out quite well:

- **Air Tags** are really popular and most people enjoy the API. That it plugs so well into IDEs and LLMs is a super power. Air Tags could be faster, but optimisation will happen once Air reaches Beta
- **AirResponse** makes writing views powered by Jinja or Air Tags easy and fast. Like Air Tags the API feature for this is complete
- **Examples** in all the doc strings makes it much easier for both humans and LLMs. This is an ongoing effort
- **Jinja + Air Tags** base templates for layout and Air Tags for content is a really sweet pattern we should talk about more. Unfortunately Jinja inside of Air Tags is a challenge not yet solved
- **Ecosystem** Leaning into FastAPI-isms means its easy to plug into the large and vibrant FastAPI ecosystem. Deployment is also easy - Air deploys precisely the same way as FastAPI. Nevertheless we should discuss the ecosystem more in documentation

For all of this we've got a ways to go before I feel confident about taking Air from Alpha to Beta. It's not just a matter of stability, it is also features that I believe are core to the vision. I want the project to be easier and more powerful for app builders and end users alive.

## Timeline to Beta

TLDR: When we feel Air is ready

While it would be nice to have Air be a Beta project there's something to be said about having the freedom to make breaking changes or to backtrack from designs when we must. It's easy to fix mistakes now then later when there are more projects that could be broken by us making breaking changes. By staying in alpha longer it gives us the opportunity to validate our ideas .

## Headlines

Here is what is planned for the Beta release:

### Accessibility Improvements


### Air Forms


### Bringing AirMarkdown Into Air Core

### Air ORM

### AirBlog Tutorial


## What's already been done

### Air Tag API

The Air Tag API is complete and stable. This is based off working projects as well as experiences in other frameworks. There are no planned breaking changes to this API, just incremental improvements like bugfixes, more helpful error messages, and finished stock tag documentation.

### AirResponse/Application/Router

The AirResponse, Application and Router APIs are mostly complete. There should be no breaking changes to these APIs, rather adding polish, addressing bugs, and improving error handling.
