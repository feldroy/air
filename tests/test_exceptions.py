import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from fastapi.exceptions import HTTPException as FastAPIHTTPException
from air import HTTPException 

def test_init_signature_compat():
    e = HTTPException(status_code=418, detail="teapot", headers={"X-Foo": "Bar"})
    assert e.status_code == 418
    assert e.detail == "teapot"
    assert e.headers["X-Foo"] == "Bar"
    assert isinstance(e, FastAPIHTTPException)

@pytest.mark.parametrize(
    "status,detail",
    [
        (400, "bad request"),
        (401, {"msg": "unauthorized", "code": "UNAUTH"}),
        (404, ["not", "found"]),
        (422, {"errors": [{"loc": ["q"], "msg": "invalid"}]}),
    ],
)
def test_fastapi_integration_various_details(status, detail):
    app = FastAPI()

    @app.get("/boom")
    def boom():
        raise HTTPException(status_code=status, detail=detail)

    client = TestClient(app)
    r = client.get("/boom")
    assert r.status_code == status
    assert r.json()["detail"] == detail

def test_headers_passthrough():
    app = FastAPI()

    @app.get("/with-headers")
    def with_headers():
        raise HTTPException(
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
    app = FastAPI()

    @app.exception_handler(FastAPIHTTPException)
    async def custom_http_exception_handler(_, exc: FastAPIHTTPException):
        return PlainTextResponse(f"oops:{exc.status_code}:{exc.detail}", status_code=exc.status_code)

    from starlette.responses import PlainTextResponse

    @app.get("/handled")
    def handled():
        raise HTTPException(status_code=403, detail="nope")

    client = TestClient(app)
    r = client.get("/handled")
    assert r.status_code == 403
    assert r.text == "oops:403:nope"