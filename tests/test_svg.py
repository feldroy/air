import air


def test_atag_no_attrs_no_children():
    assert air.svg.A().render() == "<a></a>"


def test_atag_with_all_attributes():
    link = sg.A(
        "Link text",
        href="https://example.com",
        target="_blank",
        download="file.pdf",
        hreflang="en-US",
        ping="https://tracker.example.com",
        referrerpolicy="no-referrer",
        rel="noopener",
        type="application/pdf",
    )
    expected = '<a href="https://example.com" target="_blank" download="file.pdf" hreflang="en-US" ping="https://tracker.example.com" referrerpolicy="no-referrer" rel="noopener" type="application/pdf">Link text</a>'
    assert link.render() == expected


def test_cased_tag_no_children():
    assert air.svg.AnimateMotion().render() == "<animateMotion></animateMotion>"


def test_cased_tags_with_children():
    assert (
        air.svg.AnimateMotion(air.svg.ClipPath()).render()
        == "<animateMotion><clipPath></clipPath></animateMotion>"
    )


# Test basic shapes with attributes
def test_circle_with_attributes():
    circle = sg.Circle(cx=50, cy=50, r=25, class_="my-circle")
    expected = '<circle cx="50" cy="50" r="25" class="my-circle"></circle>'
    assert circle.render() == expected


def test_rect_with_all_attributes():
    rect = sg.Rect(x=10, y=20, width=100, height=50, rx=5, ry=3, pathLength=300)
    expected = '<rect x="10" y="20" width="100" height="50" rx="5" ry="3" pathLength="300"></rect>'
    assert rect.render() == expected


def test_ellipse_coordinates():
    ellipse = sg.Ellipse(cx=100, cy=75, rx=40, ry=20)
    expected = '<ellipse cx="100" cy="75" rx="40" ry="20"></ellipse>'
    assert ellipse.render() == expected


def test_line_coordinates():
    line = sg.Line(x1=0, y1=0, x2=100, y2=100, style="stroke: black;")
    expected = '<line x1="0" y1="0" x2="100" y2="100" style="stroke: black;"></line>'
    assert line.render() == expected


def test_path_with_data():
    path = sg.Path(d="M10 10 L90 90 Z", pathLength=113)
    expected = '<path d="M10 10 L90 90 Z" pathLength="113"></path>'
    assert path.render() == expected


# Test SVG container elements
def test_svg_with_viewbox():
    svg = sg.Svg(width=200, height=200, viewBox="0 0 200 200", id="main-svg")
    expected = (
        '<svg width="200" height="200" viewBox="0 0 200 200" id="main-svg"></svg>'
    )
    assert svg.render() == expected


def test_group_with_children():
    group = sg.G(
        sg.Circle(r=10), sg.Rect(width=20, height=20), class_="shape-group", id="group1"
    )
    expected = '<g class="shape-group" id="group1"><circle r="10"></circle><rect width="20" height="20"></rect></g>'
    assert group.render() == expected


# Test text elements
def test_text_with_positioning():
    text = sg.Text("Hello SVG", x=50, y=100, dx=5, dy=-10, textLength=80)
    expected = '<text x="50" y="100" dx="5" dy="-10" textLength="80">Hello SVG</text>'
    assert text.render() == expected


def test_tspan_in_text():
    tspan = sg.Tspan("emphasized", dy=5, class_="emphasis")
    text = sg.Text("Normal ", tspan, " text", x=10, y=20)
    expected = '<text x="10" y="20">Normal <tspan dy="5" class="emphasis">emphasized</tspan> text</text>'
    assert text.render() == expected


# Test gradients
def test_linear_gradient_with_stops():
    stop1 = sg.Stop(offset="0%", stop_color="red")
    stop2 = sg.Stop(offset="100%", stop_color="blue", stop_opacity=0.8)
    gradient = sg.LinearGradient(
        stop1, stop2, x1="0%", y1="0%", x2="100%", y2="0%", id="myGradient"
    )
    expected = '<linearGradient x1="0%" y1="0%" x2="100%" y2="0%" id="myGradient"><stop offset="0%" stop-color="red"></stop><stop offset="100%" stop-color="blue" stop-opacity="0.8"></stop></linearGradient>'
    assert gradient.render() == expected


def test_radial_gradient():
    gradient = sg.RadialGradient(
        cx="50%",
        cy="50%",
        r="50%",
        fx="25%",
        fy="25%",
        gradientUnits="objectBoundingBox",
    )
    expected = '<radialGradient cx="50%" cy="50%" r="50%" fx="25%" fy="25%" gradientUnits="objectBoundingBox"></radialGradient>'
    assert gradient.render() == expected


# Test filter elements
def test_filter_with_effects():
    blur = sg.FeGaussianBlur(in_="SourceGraphic", stdDeviation=2, result="blur")
    offset = sg.FeOffset(in_="blur", dx=3, dy=3, result="offset")
    filter_elem = sg.Filter(
        blur, offset, x="-20%", y="-20%", width="140%", height="140%", id="drop-shadow"
    )
    expected = '<filter x="-20%" y="-20%" width="140%" height="140%" id="drop-shadow"><feGaussianBlur in-="SourceGraphic" stdDeviation="2" result="blur"></feGaussianBlur><feOffset in-="blur" dx="3" dy="3" result="offset"></feOffset></filter>'
    assert filter_elem.render() == expected


def test_fe_distant_light():
    light = sg.FeDistantLight(azimuth=45, elevation=60)
    expected = '<feDistantLight azimuth="45" elevation="60"></feDistantLight>'
    assert light.render() == expected


def test_fe_drop_shadow():
    shadow = sg.FeDropShadow(
        dx=2, dy=2, stdDeviation=1, flood_color="black", flood_opacity=0.3
    )
    expected = '<feDropShadow dx="2" dy="2" stdDeviation="1" flood-color="black" flood-opacity="0.3"></feDropShadow>'
    assert shadow.render() == expected


# Test animation elements
def test_animate_with_values():
    animate = sg.Animate(
        attributeName="opacity", values="0;1;0", dur="2s", repeatCount="indefinite"
    )
    expected = '<animate attributeName="opacity" values="0;1;0" dur="2s" repeatCount="indefinite"></animate>'
    assert animate.render() == expected


def test_animate_motion_with_path():
    motion = sg.AnimateMotion(path="M10,10 L90,90", dur="3s", rotate="auto")
    expected = (
        '<animateMotion path="M10,10 L90,90" rotate="auto" dur="3s"></animateMotion>'
    )
    assert motion.render() == expected


# Test marker and mask elements
def test_marker_definition():
    marker = sg.Marker(
        sg.Path(d="M0,0 L10,5 L0,10 Z"),
        markerWidth=10,
        markerHeight=10,
        refX=0,
        refY=5,
        orient="auto",
        id="arrow",
    )
    expected = '<marker markerWidth="10" markerHeight="10" refX="0" refY="5" orient="auto" id="arrow"><path d="M0,0 L10,5 L0,10 Z"></path></marker>'
    assert marker.render() == expected


def test_mask_with_content():
    mask = sg.Mask(
        sg.Rect(width="100%", height="100%", style="fill: white;"),
        sg.Circle(cx=50, cy=50, r=30, style="fill: black;"),
        id="hole-mask",
    )
    expected = '<mask id="hole-mask"><rect width="100%" height="100%" style="fill: white;"></rect><circle cx="50" cy="50" r="30" style="fill: black;"></circle></mask>'
    assert mask.render() == expected


# Test complex SVG structure
def test_complex_svg_structure():
    # Create a complete SVG with multiple elements
    defs = sg.Defs(
        sg.LinearGradient(
            sg.Stop(offset="0%", stop_color="red"),
            sg.Stop(offset="100%", stop_color="blue"),
            id="grad1",
        )
    )

    content = sg.G(
        sg.Circle(cx=50, cy=50, r=40, style="fill: url(#grad1);"),
        sg.Text("SVG", x=35, y=55, style="font-family: Arial;"),
        class_="main-content",
    )

    svg = sg.Svg(
        defs,
        content,
        width=100,
        height=100,
        viewBox="0 0 100 100",
        xmlns="http://www.w3.org/2000/svg",
    )

    expected = '<svg xmlns="http://www.w3.org/2000/svg" width="100" height="100" viewBox="0 0 100 100"><defs><linearGradient id="grad1"><stop offset="0%" stop-color="red"></stop><stop offset="100%" stop-color="blue"></stop></linearGradient></defs><g class="main-content"><circle cx="50" cy="50" r="40" style="fill: url(#grad1);"></circle><text x="35" y="55" style="font-family: Arial;">SVG</text></g></svg>'
    assert svg.render() == expected


# Test attribute handling with None values
def test_none_attributes_filtered():
    # None values should not appear in rendered output
    circle = sg.Circle(cx=50, cy=50, r=25, pathLength=None, class_=None)
    expected = '<circle cx="50" cy="50" r="25"></circle>'
    assert circle.render() == expected


# Test mixed type attributes
def test_mixed_type_attributes():
    # Test that both string and numeric values work
    rect = sg.Rect(x="10px", y=20, width="50%", height=30.5)
    expected = '<rect x="10px" y="20" width="50%" height="30.5"></rect>'
    assert rect.render() == expected


# Test experimental attributes
def test_image_with_experimental_attributes():
    # Test fetchpriority experimental attribute
    image = sg.Image(
        x=10,
        y=20,
        width=100,
        height=80,
        href="image.jpg",
        fetchpriority="high",
        crossorigin="anonymous",
    )
    expected = '<image x="10" y="20" width="100" height="80" href="image.jpg" crossorigin="anonymous" fetchpriority="high"></image>'
    assert image.render() == expected


def test_script_with_experimental_attributes():
    # Test fetchpriority experimental attribute
    script = sg.Script(
        type="application/javascript",
        href="script.js",
        fetchpriority="low",
        crossorigin="use-credentials",
    )
    expected = '<script type="application/javascript" href="script.js" crossorigin="use-credentials" fetchpriority="low"></script>'
    assert script.render() == expected


def test_animate_with_extended_attributes():
    # Test the additional animation attributes
    animate = sg.Animate(
        attributeName="opacity",
        attributeType="CSS",
        from_="0",
        to="1", 
        by="0.5",
        dur="2s",
        begin="1s",
        end="5s",
        repeatCount="3",
        repeatDur="10s",
        calcMode="linear"
    )
    expected = '<animate attributeName="opacity" attributeType="CSS" dur="2s" repeatCount="3" repeatDur="10s" from-="0" to="1" by="0.5" begin="1s" end="5s" calcMode="linear"></animate>'
    assert animate.render() == expected
