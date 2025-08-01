import air


def render(request: air.Request):
    return air.Children(
        air.Div(
            air.Img(
                src="https://air-svgs.fastapicloud.dev/static/air-3color.svg",
                width="400",
                alt="Air logo",
                class_="mx-auto mb-6",
            ),
            air.H2(
                "The new Python web framework built on FastAPI.",
                class_="text-center text-2xl font-semibold text-gray-800 mb-2",
            ),
            air.Div(
                air.A(
                    "Air on GitHub",
                    href="https://github.com/feldroy/air",
                    class_="inline-block px-4 py-2 mr-3 rounded bg-blue-600 text-white hover:bg-blue-700 transition",
                ),
                air.A(
                    "Air Docs on GitHub",
                    href="https://github.com/feldroy/airdocs",
                    class_="inline-block px-4 py-2 rounded bg-gray-800 text-white hover:bg-gray-900 transition",
                ),
                class_="mt-4 flex flex-row justify-center",
            ),
            class_="flex flex-col items-center justify-center min-h-[60vh]",
        )
    )
