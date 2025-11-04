TORTOISE_ORM = {
    "connections": {"default": "postgres://arg@localhost:5432/tortoisedemo"},  # or your DB URL
    "apps": {
        "models": {
            "models": ["models"],  # reference the models module
            "default_connection": "default",
        }
    },
}
