import air


def test_atag_no_attrs_no_children():
    assert air.svg.A().render() == "<a></a>"


def test_cased_tag_no_children():
    assert air.svg.AnimateMotion().render() == "<animateMotion></animateMotion>"


def test_cased_tags_with_children():
    assert (
        air.svg.AnimateMotion(air.svg.ClipPath()).render()
        == "<animateMotion><clipPath></clipPath></animateMotion>"
    )
