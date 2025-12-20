# {{cookiecutter.name}}

An Air-powered project.

## Setup

{% if cookiecutter.orm == "PostgreSQL: asyncpg+dbmate" %}
This project uses the [asyncpg](https://pypi.org/project/asyncpg/) library to connect with PostgreSQL. Queries to the database will be written as PostgreSQL-flavored SQL. As `asyncpg` isn't ideal for database schema changes, this project uses [dbmate](https://github.com/amacneil/dbmate) to manage database migrations.

TODO add getting the basic environment ready

Instructions for installing dbmate: https://github.com/amacneil/dbmate?tab=readme-ov-file#installation
{% endif %}