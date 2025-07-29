import air


def test_html_to_tags():
    sample = """
    <html>
        <body>
            <main>
                <h1 class="header">Hello, World</h1>
            </main>
        </body>
    </html>"""
    assert "air.H1" in air.html_to_airtags(sample)
    assert "H1" in air.html_to_airtags(sample)

    # Now test with no prefix
    assert "air.H1" not in air.html_to_airtags(sample, air_prefix=False)
    assert "H1" in air.html_to_airtags(sample, air_prefix=False)


def test_html_to_tags_multi_attrs():
    sample = """
    <form action="." method="post" class="searcho">
        <label for="search">
        Search:
        <input type="search" name="search" />
        </label>
    </form>
"""
    tags = air.html_to_airtags(sample)

    assert (
        tags
        == """air.Form(action=".", method="post", class_="searcho")(
    air.Label(for_="search")("Search:", air.Input(type="search", name="search"))
)
"""
    )


def test_