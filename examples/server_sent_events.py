import random
from asyncio import sleep
from collections.abc import AsyncGenerator

import air

app = air.Air()


@app.page
def index() -> air.Html | air.Children:
    return air.layouts.mvpcss(
        air.Script(src="https://unpkg.com/htmx-ext-sse@2.2.1/sse.js"),  # (1)!
        air.Title("Server Sent Event Demo"),
        air.H1("Server Sent Event Demo"),
        air.P("Lottery number generator"),
        air.Section(
            hx_ext="sse",  # (2)!
            sse_connect="/lottery-numbers",  # (3)!
            hx_swap="beforeend show:bottom",  # (4)!
            sse_swap="message",  # (5)!
        ),
    )


async def lottery_generator() -> AsyncGenerator[str]:  # (6)!
    while True:
        lottery_numbers = ", ".join([str(random.randint(1, 40)) for x in range(6)])
        # Tags work seamlessly
        yield str(air.Aside(lottery_numbers))  # (7)!
        await sleep(1)


@app.page
async def lottery_numbers() -> air.SSEResponse:
    return air.SSEResponse(lottery_generator())  # (9)!
