import air


def test_atag_no_attrs_no_children() -> None:
    assert air.svg.A().render() == "<a></a>"


def test_atag_with_all_attributes() -> None:
    link = air.svg.A(
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


def test_cased_tag_no_children() -> None:
    assert air.svg.AnimateMotion().render() == "<animateMotion></animateMotion>"


def test_cased_tags_with_children() -> None:
    assert air.svg.AnimateMotion(air.svg.ClipPath()).render() == "<animateMotion><clipPath></clipPath></animateMotion>"


# Test basic shapes with attributes
def test_circle_with_attributes() -> None:
    circle = air.svg.Circle(cx=50, cy=50, r=25, class_="my-circle")
    expected = '<circle cx="50" cy="50" r="25" class="my-circle"></circle>'
    assert circle.render() == expected


def test_rect_with_all_attributes() -> None:
    rect = air.svg.Rect(x=10, y=20, width=100, height=50, rx=5, ry=3, pathLength=300)
    expected = '<rect x="10" y="20" width="100" height="50" rx="5" ry="3" pathLength="300"></rect>'
    assert rect.render() == expected


def test_ellipse_coordinates() -> None:
    ellipse = air.svg.Ellipse(cx=100, cy=75, rx=40, ry=20)
    expected = '<ellipse cx="100" cy="75" rx="40" ry="20"></ellipse>'
    assert ellipse.render() == expected


def test_line_coordinates() -> None:
    line = air.svg.Line(x1=0, y1=0, x2=100, y2=100, style="stroke: black;")
    expected = '<line x1="0" y1="0" x2="100" y2="100" style="stroke: black;"></line>'
    assert line.render() == expected


def test_path_with_data() -> None:
    path = air.svg.Path(d="M10 10 L90 90 Z", pathLength=113)
    expected = '<path d="M10 10 L90 90 Z" pathLength="113"></path>'
    assert path.render() == expected


# Test SVG container elements
def test_svg_with_viewbox() -> None:
    svg = air.svg.Svg(width=200, height=200, viewBox="0 0 200 200", id="main-svg")
    expected = '<svg width="200" height="200" viewBox="0 0 200 200" id="main-svg"></svg>'
    assert svg.render() == expected


def test_group_with_children() -> None:
    group = air.svg.G(
        air.svg.Circle(r=10),
        air.svg.Rect(width=20, height=20),
        class_="shape-group",
        id="group1",
    )
    expected = '<g class="shape-group" id="group1"><circle r="10"></circle><rect width="20" height="20"></rect></g>'
    assert group.render() == expected


# Test text elements
def test_text_with_positioning() -> None:
    text = air.svg.Text("Hello SVG", x=50, y=100, dx=5, dy=-10, textLength=80)
    expected = '<text x="50" y="100" dx="5" dy="-10" textLength="80">Hello SVG</text>'
    assert text.render() == expected


def test_tspan_in_text() -> None:
    tspan = air.svg.Tspan("emphasized", dy=5, class_="emphasis")
    text = air.svg.Text("Normal ", tspan, " text", x=10, y=20)
    expected = '<text x="10" y="20">Normal <tspan dy="5" class="emphasis">emphasized</tspan> text</text>'
    assert text.render() == expected


# Test gradients
def test_linear_gradient_with_stops() -> None:
    stop1 = air.svg.Stop(offset="0%", stop_color="red")
    stop2 = air.svg.Stop(offset="100%", stop_color="blue", stop_opacity=0.8)
    gradient = air.svg.LinearGradient(stop1, stop2, x1="0%", y1="0%", x2="100%", y2="0%", id="myGradient")
    expected = '<linearGradient x1="0%" y1="0%" x2="100%" y2="0%" id="myGradient"><stop offset="0%" stop-color="red"></stop><stop offset="100%" stop-color="blue" stop-opacity="0.8"></stop></linearGradient>'
    assert gradient.render() == expected


def test_radial_gradient() -> None:
    gradient = air.svg.RadialGradient(
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
def test_filter_with_effects() -> None:
    blur = air.svg.FeGaussianBlur(in_="SourceGraphic", stdDeviation=2, result="blur")
    offset = air.svg.FeOffset(in_="blur", dx=3, dy=3, result="offset")
    filter_elem = air.svg.Filter(blur, offset, x="-20%", y="-20%", width="140%", height="140%", id="drop-shadow")
    expected = '<filter x="-20%" y="-20%" width="140%" height="140%" id="drop-shadow"><feGaussianBlur in-="SourceGraphic" stdDeviation="2" result="blur"></feGaussianBlur><feOffset in-="blur" dx="3" dy="3" result="offset"></feOffset></filter>'
    assert filter_elem.render() == expected


def test_fe_distant_light() -> None:
    light = air.svg.FeDistantLight(azimuth=45, elevation=60)
    expected = '<feDistantLight azimuth="45" elevation="60"></feDistantLight>'
    assert light.render() == expected


def test_fe_drop_shadow() -> None:
    shadow = air.svg.FeDropShadow(dx=2, dy=2, stdDeviation=1, flood_color="black", flood_opacity=0.3)
    expected = '<feDropShadow dx="2" dy="2" stdDeviation="1" flood-color="black" flood-opacity="0.3"></feDropShadow>'
    assert shadow.render() == expected


# Test animation elements
def test_animate_with_values() -> None:
    animate = air.svg.Animate(attributeName="opacity", values="0;1;0", dur="2s", repeatCount="indefinite")
    expected = '<animate attributeName="opacity" values="0;1;0" dur="2s" repeatCount="indefinite"></animate>'
    assert animate.render() == expected


def test_animate_motion_with_path() -> None:
    motion = air.svg.AnimateMotion(path="M10,10 L90,90", dur="3s", rotate="auto")
    expected = '<animateMotion path="M10,10 L90,90" rotate="auto" dur="3s"></animateMotion>'
    assert motion.render() == expected


# Test marker and mask elements
def test_marker_definition() -> None:
    marker = air.svg.Marker(
        air.svg.Path(d="M0,0 L10,5 L0,10 Z"),
        markerWidth=10,
        markerHeight=10,
        refX=0,
        refY=5,
        orient="auto",
        id="arrow",
    )
    expected = '<marker markerWidth="10" markerHeight="10" refX="0" refY="5" orient="auto" id="arrow"><path d="M0,0 L10,5 L0,10 Z"></path></marker>'
    assert marker.render() == expected


def test_mask_with_content() -> None:
    mask = air.svg.Mask(
        air.svg.Rect(width="100%", height="100%", style="fill: white;"),
        air.svg.Circle(cx=50, cy=50, r=30, style="fill: black;"),
        id="hole-mask",
    )
    expected = '<mask id="hole-mask"><rect width="100%" height="100%" style="fill: white;"></rect><circle cx="50" cy="50" r="30" style="fill: black;"></circle></mask>'
    assert mask.render() == expected


# Test complex SVG structure
def test_complex_svg_structure() -> None:
    # Create a complete SVG with multiple elements
    defs = air.svg.Defs(
        air.svg.LinearGradient(
            air.svg.Stop(offset="0%", stop_color="red"),
            air.svg.Stop(offset="100%", stop_color="blue"),
            id="grad1",
        )
    )

    content = air.svg.G(
        air.svg.Circle(cx=50, cy=50, r=40, style="fill: url(#grad1);"),
        air.svg.Text("SVG", x=35, y=55, style="font-family: Arial;"),
        class_="main-content",
    )

    svg = air.svg.Svg(
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
def test_none_attributes_filtered() -> None:
    # None values should not appear in rendered output
    circle = air.svg.Circle(cx=50, cy=50, r=25, pathLength=None, class_=None)
    expected = '<circle cx="50" cy="50" r="25"></circle>'
    assert circle.render() == expected


# Test mixed type attributes
def test_mixed_type_attributes() -> None:
    # Test that both string and numeric values work
    rect = air.svg.Rect(x="10px", y=20, width="50%", height=30.5)
    expected = '<rect x="10px" y="20" width="50%" height="30.5"></rect>'
    assert rect.render() == expected


# Test experimental attributes
def test_image_with_experimental_attributes() -> None:
    # Test fetchpriority experimental attribute
    image = air.svg.Image(
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


def test_script_with_experimental_attributes() -> None:
    # Test fetchpriority experimental attribute
    script = air.svg.Script(
        type="application/javascript",
        href="script.js",
        fetchpriority="low",
        crossorigin="use-credentials",
    )
    expected = '<script type="application/javascript" href="script.js" crossorigin="use-credentials" fetchpriority="low"></script>'
    assert script.render() == expected


def test_animate_with_extended_attributes() -> None:
    # Test the additional animation attributes
    animate = air.svg.Animate(
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
        calcMode="linear",
    )
    expected = '<animate attributeName="opacity" attributeType="CSS" dur="2s" repeatCount="3" repeatDur="10s" from-="0" to="1" by="0.5" begin="1s" end="5s" calcMode="linear"></animate>'
    assert animate.render() == expected


# Test missing classes for coverage
def test_animate_transform() -> None:
    transform = air.svg.AnimateTransform(type="rotate", from_="0", to="360", dur="2s", repeatCount="indefinite")
    expected = (
        '<animateTransform type="rotate" from-="0" to="360" dur="2s" repeatCount="indefinite"></animateTransform>'
    )
    assert transform.render() == expected


def test_desc() -> None:
    desc = air.svg.Desc("This is a description")
    expected = "<desc>This is a description</desc>"
    assert desc.render() == expected


def test_fe_blend() -> None:
    blend = air.svg.FeBlend(in_="SourceGraphic", in2="SourceAlpha", mode="multiply")
    expected = '<feBlend in-="SourceGraphic" in2="SourceAlpha" mode="multiply"></feBlend>'
    assert blend.render() == expected


def test_fe_color_matrix() -> None:
    matrix = air.svg.FeColorMatrix(type="matrix", values="1 0 0 0 0 0 1 0 0 0 0 0 1 0 0 0 0 0 1 0")
    expected = '<feColorMatrix type="matrix" values="1 0 0 0 0 0 1 0 0 0 0 0 1 0 0 0 0 0 1 0"></feColorMatrix>'
    assert matrix.render() == expected


def test_fe_component_transfer() -> None:
    transfer = air.svg.FeComponentTransfer(in_="SourceGraphic")
    expected = '<feComponentTransfer in-="SourceGraphic"></feComponentTransfer>'
    assert transfer.render() == expected


def test_fe_composite() -> None:
    composite = air.svg.FeComposite(in_="SourceGraphic", in2="SourceAlpha", operator="over")
    expected = '<feComposite in-="SourceGraphic" in2="SourceAlpha" operator="over"></feComposite>'
    assert composite.render() == expected


def test_fe_convolve_matrix() -> None:
    convolve = air.svg.FeConvolveMatrix(order="3", kernelMatrix="0 -1 0 -1 5 -1 0 -1 0")
    expected = '<feConvolveMatrix order="3" kernelMatrix="0 -1 0 -1 5 -1 0 -1 0"></feConvolveMatrix>'
    assert convolve.render() == expected


def test_fe_diffuse_lighting() -> None:
    lighting = air.svg.FeDiffuseLighting(in_="SourceGraphic", surfaceScale=1)
    expected = '<feDiffuseLighting in-="SourceGraphic" surfaceScale="1"></feDiffuseLighting>'
    assert lighting.render() == expected


def test_fe_displacement_map() -> None:
    displacement = air.svg.FeDisplacementMap(in_="SourceGraphic", in2="displacement", scale=10, xChannelSelector="R")
    expected = (
        '<feDisplacementMap in-="SourceGraphic" in2="displacement" scale="10" xChannelSelector="R"></feDisplacementMap>'
    )
    assert displacement.render() == expected


def test_fe_flood() -> None:
    flood = air.svg.FeFlood(flood_color="red", flood_opacity=0.5)
    expected = '<feFlood flood-color="red" flood-opacity="0.5"></feFlood>'
    assert flood.render() == expected


def test_fe_func_a() -> None:
    func_a = air.svg.FeFuncA(type="linear", slope=0.5)
    expected = '<feFuncA type="linear" slope="0.5"></feFuncA>'
    assert func_a.render() == expected


def test_fe_func_b() -> None:
    func_b = air.svg.FeFuncB(type="discrete", tableValues="0 0.5 1")
    expected = '<feFuncB type="discrete" tableValues="0 0.5 1"></feFuncB>'
    assert func_b.render() == expected


def test_fe_func_g() -> None:
    func_g = air.svg.FeFuncG(type="gamma", amplitude=2, exponent=3)
    expected = '<feFuncG type="gamma" amplitude="2" exponent="3"></feFuncG>'
    assert func_g.render() == expected


def test_fe_func_r() -> None:
    func_r = air.svg.FeFuncR(type="identity")
    expected = '<feFuncR type="identity"></feFuncR>'
    assert func_r.render() == expected


def test_fe_image() -> None:
    image = air.svg.FeImage(href="image.jpg", preserveAspectRatio="xMidYMid meet")
    expected = '<feImage href="image.jpg" preserveAspectRatio="xMidYMid meet"></feImage>'
    assert image.render() == expected


def test_fe_merge() -> None:
    merge = air.svg.FeMerge(result="merge1")
    expected = '<feMerge result="merge1"></feMerge>'
    assert merge.render() == expected


def test_fe_merge_node() -> None:
    merge_node = air.svg.FeMergeNode(in_="SourceGraphic")
    expected = '<feMergeNode in-="SourceGraphic"></feMergeNode>'
    assert merge_node.render() == expected


def test_fe_morphology() -> None:
    morphology = air.svg.FeMorphology(operator="dilate", radius=2)
    expected = '<feMorphology operator="dilate" radius="2"></feMorphology>'
    assert morphology.render() == expected


def test_fe_point_light() -> None:
    point_light = air.svg.FePointLight(x=100, y=100, z=50)
    expected = '<fePointLight x="100" y="100" z="50"></fePointLight>'
    assert point_light.render() == expected


def test_fe_specular_lighting() -> None:
    specular = air.svg.FeSpecularLighting(in_="SourceGraphic", surfaceScale=1, specularConstant=1.5)
    expected = '<feSpecularLighting in-="SourceGraphic" surfaceScale="1" specularConstant="1.5"></feSpecularLighting>'
    assert specular.render() == expected


def test_fe_spot_light() -> None:
    spot_light = air.svg.FeSpotLight(x=100, y=100, z=50, pointsAtX=0, pointsAtY=0, pointsAtZ=0)
    expected = '<feSpotLight x="100" y="100" z="50" pointsAtX="0" pointsAtY="0" pointsAtZ="0"></feSpotLight>'
    assert spot_light.render() == expected


def test_fe_tile() -> None:
    tile = air.svg.FeTile(in_="SourceGraphic", result="tile1")
    expected = '<feTile in-="SourceGraphic" result="tile1"></feTile>'
    assert tile.render() == expected


def test_fe_turbulence() -> None:
    turbulence = air.svg.FeTurbulence(baseFrequency="0.9", numOctaves=4, type="fractalNoise")
    expected = '<feTurbulence baseFrequency="0.9" numOctaves="4" type="fractalNoise"></feTurbulence>'
    assert turbulence.render() == expected


def test_foreign_object() -> None:
    foreign = air.svg.ForeignObject(x=20, y=20, width=160, height=160)
    expected = '<foreignObject x="20" y="20" width="160" height="160"></foreignObject>'
    assert foreign.render() == expected


def test_metadata() -> None:
    metadata = air.svg.Metadata("Dublin Core metadata")
    expected = "<metadata>Dublin Core metadata</metadata>"
    assert metadata.render() == expected


def test_mpath() -> None:
    mpath = air.svg.Mpath(href="#path1")
    expected = '<mpath href="#path1"></mpath>'
    assert mpath.render() == expected


def test_pattern() -> None:
    pattern = air.svg.Pattern(x=0, y=0, width=20, height=20, patternUnits="userSpaceOnUse", id="pattern1")
    expected = '<pattern x="0" y="0" width="20" height="20" patternUnits="userSpaceOnUse" id="pattern1"></pattern>'
    assert pattern.render() == expected


def test_polygon() -> None:
    polygon = air.svg.Polygon(points="200,10 250,190 160,210")
    expected = '<polygon points="200,10 250,190 160,210"></polygon>'
    assert polygon.render() == expected


def test_polyline() -> None:
    polyline = air.svg.Polyline(points="20,20 40,25 60,40 80,120 120,140 200,180")
    expected = '<polyline points="20,20 40,25 60,40 80,120 120,140 200,180"></polyline>'
    assert polyline.render() == expected


def test_set() -> None:
    set_elem = air.svg.Set(attributeName="fill", to="red", begin="2s", dur="1s")
    expected = '<set to="red" attributeName="fill" begin="2s" dur="1s"></set>'
    assert set_elem.render() == expected


def test_style() -> None:
    style = air.svg.Style("circle { fill: red; }", type="text/css")
    expected = '<style type="text/css">circle { fill: red; }</style>'
    assert style.render() == expected


def test_switch() -> None:
    switch = air.svg.Switch(id="switch1")
    expected = '<switch id="switch1"></switch>'
    assert switch.render() == expected


def test_symbol() -> None:
    symbol = air.svg.Symbol(viewBox="0 0 150 110", id="symbol1")
    expected = '<symbol viewBox="0 0 150 110" id="symbol1"></symbol>'
    assert symbol.render() == expected


def test_text_path() -> None:
    text_path = air.svg.TextPath("Text along path", href="#path1", startOffset="20%")
    expected = '<textPath href="#path1" startOffset="20%">Text along path</textPath>'
    assert text_path.render() == expected


def test_title() -> None:
    title = air.svg.Title("SVG Title")
    expected = "<title>SVG Title</title>"
    assert title.render() == expected


def test_use() -> None:
    use = air.svg.Use(href="#rect1", x=10, y=10)
    expected = '<use href="#rect1" x="10" y="10"></use>'
    assert use.render() == expected


def test_view() -> None:
    view = air.svg.View(viewBox="0 0 100 100", id="view1")
    expected = '<view viewBox="0 0 100 100" id="view1"></view>'
    assert view.render() == expected
