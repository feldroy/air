from air import tags as tg


def test_tags():
    html = tg.Abbr("example").render()
    assert html == "<abbr>example</abbr>"
