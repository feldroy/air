import air.svg as sg


def test_atag_no_attrs_no_children():
    assert sg.A().render() == "<a></a>"


def test_cased_tag_no_children():
    assert sg.AnimateMotion().render() == "<animateMotion></animateMotion>"


def test_cased_tags_with_children():
    assert (
        sg.AnimateMotion(sg.ClipPath()).render()
        == "<animateMotion><clipPath></clipPath></animateMotion>"
    )
