import random
from asyncio import sleep

import air

app = air.Air()


@app.page
def index():
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


async def lottery_generator():  # (6)!
    while True:
        lottery_numbers = ", ".join([str(random.randint(1, 40)) for x in range(6)])
        # Tags work seamlessly
        yield air.Aside(lottery_numbers)  # (7)!
        await sleep(1)


@app.page
async def lottery_numbers():
    return air.SSEResponse(lottery_generator())  # (9)!
