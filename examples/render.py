from rich import print

from air import A, Div, Img, Link, P, Script

if __name__ == "__main__":
    link = Link(
        rel="stylesheet",
        href="https://cdn.jsdelivr.net/npm/@picocss/pico@2/css/pico.min.css",
    )
    script = Script(
        src="https://cdn.jsdelivr.net/npm/htmx.org@2.0.6/dist/htmx.min.js",
        integrity="sha384-Akqfrbj/HpNVo8k11SXBb6TlBWmXXlYQrCSqEWmyKJe+hDm3Z/B2WVG4smwBkRVm",
        crossorigin="anonymous",
    )
    a = A("Air", data_cloud=True, data_earth="true")
    img = Img(
        src="https://cdn.jsdelivr.net/dist/img.png",
        width=250,
        height=100,
        alt="My Img",
        cheched=False,
        selected=True,
        bar="foo",
    )
    div = Div(
        link,
        script,
        P(a, img),
        class_="class1",
        id="id1",
        style="style1",
        kwarg1="kwarg1",
        kwarg2="kwarg2",
        kwarg3="kwarg3",
    )

    print(div)
