import pytest
from fastapi.exceptions import HTTPException as FastAPIHTTPException
from fastapi.testclient import TestClient

import air


def test_init_signature_compat():
    e = air.HTTPException(status_code=418, detail="teapot", headers={"X-Foo": "Bar"})
    assert e.status_code == 418
    assert e.detail == "teapot"
    assert isinstance(e, FastAPIHTTPException)


@pytest.mark.parametrize(
    "status,detail",
    [
        (400, "bad request"),
        (401, {"msg": "unauthorized", "code": "UNAUTH"}),
        (422, {"errors": [{"loc": ["q"], "msg": "invalid"}]}),
    ],
)
def test_fastapi_integration_various_details(status, detail):
    app = air.Air()

    @app.get("/boom")
    def boom():
        raise air.HTTPException(status_code=status, detail=detail)

    client = TestClient(app)
    r = client.get("/boom")
    assert r.status_code == status
    assert r.json()["detail"] == detail


def test_fastapi_integration_404():
    app = air.Air()

    @app.get("/")
    def boom():
        raise air.HTTPException(status_code=404)

    client = TestClient(app)
    r = client.get("/where?")
    assert r.status_code == 404
    assert "The requested resource was not found on this server." in r.text


def test_headers_passthrough():
    app = air.Air()

    @app.get("/with-headers")
    def with_headers():
        raise air.HTTPException(
            status_code=429,
            detail="too many requests",
            headers={"Retry-After": "5", "X-Foo": "Bar"},
        )

    client = TestClient(app)
    r = client.get("/with-headers")
    assert r.status_code == 429
    assert r.headers.get("Retry-After") == "5"
    assert r.headers.get("X-Foo") == "Bar"
    assert r.json() == {"detail": "too many requests"}


def test_custom_exception_handler_compat():
    app = air.Air()

    @app.exception_handler(FastAPIHTTPException)
    async def custom_http_exception_handler(_, exc: FastAPIHTTPException):
        return air.PlainTextResponse(f"oops:{exc.status_code}:{exc.detail}", status_code=exc.status_code)

    @app.get("/handled")
    def handled():
        raise air.HTTPException(status_code=403, detail="nope")

    client = TestClient(app)
    r = client.get("/handled")
    assert r.status_code == 403
    assert r.text == "oops:403:nope"
