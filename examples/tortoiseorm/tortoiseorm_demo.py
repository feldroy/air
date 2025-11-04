# /// script
# dependencies = [
#   "air[standard]",
#   "asyncpg",
#   "tortoise-orm[asyncpg]",
# ]
# ///
"""
The Tortoise ORM demo from https://tortoise.github.io/getting_started.html#tutorial adapted for Air.

Usage:
    # Change username to your local Postgres user in main(), then:
    createdb tortoisedemo
    uv run tortoiseorm_demo.py

    # To setup migrations with Aerich, which creates pyproject.toml and migrations/ folder:
    uvx --with asyncpg "aerich[toml]" init -t config.TORTOISE_ORM

    # To create initial migration:
    uvx --with asyncpg "aerich[toml]" init-db
"""

import air
from tortoise import Tortoise, run_async
from models import Tournament, Event, Team

app = air.Air()

TORTOISE_ORM = {
    "connections": {"default": "postgres://arg@localhost:5432/tortoisedemo"},
    "apps": {
        "models": {
            "models": ["models"],
            "default_connection": "default",
        }
    },
}


@app.page
async def index(request: air.Request):
    """Render tournaments, their events and participating teams."""
    # Prefetch related events and participants so we can render without extra awaits
    tournaments = await Tournament.all().prefetch_related("events__participants")

    def render_tournament(t):
        return air.Article(
            air.H2(t.name),
            air.Ul(*[
                air.Li(
                    air.Strong(e.name),
                    air.Br(),
                    "Teams: ",
                    air.Span(", ".join([team.name for team in getattr(e, "participants", [])]))
                    if getattr(e, "participants", None) is not None
                    else "(no teams)",
                )
                for e in getattr(t, "events", [])
            ]),
        )

    return air.layouts.mvpcss(
        air.Title("Tortoise ORM demo"),
        air.Header(
            air.H1("Tournaments"),
            air.P("Below are tournaments with their events and participating teams."),
        ),
        air.Section(*[render_tournament(t) for t in tournaments]),
    )


async def main():
    await Tortoise.init(db_url="postgres://arg@localhost:5432/tortoisedemo", modules={"models": ["__main__"]})
    await Tortoise.generate_schemas()
    await seed_data()


async def seed_data():
    """Create sample tournaments, events and teams if DB is empty."""
    if await Tournament.all().count() > 0:
        return

    red = await Team.create(name="Red Rockets")
    blue = await Team.create(name="Blue Blazers")
    green = await Team.create(name="Green Giants")

    t1 = await Tournament.create(name="Autumn Open")
    e1 = await Event.create(name="Singles", tournament=t1)
    e2 = await Event.create(name="Doubles", tournament=t1)
    await e1.participants.add(red, blue)
    await e2.participants.add(blue, green)

    t2 = await Tournament.create(name="Spring Invitational")
    e3 = await Event.create(name="Team Relay", tournament=t2)
    await e3.participants.add(red, green)

    print("Seeded demo data: 2 tournaments, 3 events, 3 teams")

    return


if __name__ == "__main__":
    import uvicorn
    run_async(main())
    uvicorn.run(app)
