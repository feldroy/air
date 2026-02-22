import air


def test_jsonable_encoder_converts_basetag_to_html():
    """Verify BaseTag registration in FastAPI's encoder registry.

    Air registers BaseTag in fastapi.encoders.ENCODERS_BY_TYPE so that
    jsonable_encoder calls str(tag) instead of vars(tag). This eliminates
    the need for endpoint wrappers. If this test fails after a FastAPI
    upgrade, the encoder registry mechanism has changed.
    """
    from fastapi.encoders import jsonable_encoder

    assert jsonable_encoder(air.H1("Hello")) == "<h1>Hello</h1>"
    assert jsonable_encoder(air.Html(air.H1("Hi"))).startswith("<!doctype html>")
