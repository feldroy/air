import json
from typing import Annotated

from fastapi.testclient import TestClient

from air import H1, Air, AirRequest, Request, is_htmx_request


def test_is_htmx() -> None:
    """Test the is_htmx method, which only works if the response is wrapped."""

    app = Air()

    @app.get("/test")
    def test_endpoint(is_htmx: Annotated[bool, is_htmx_request]) -> H1:
        return H1(f"Is HTMX request: {is_htmx}")

    client = TestClient(app)

    response = client.get("/test", headers={"hx-request": "true"})
    assert response.status_code == 200
    assert response.headers["content-type"] == "text/html; charset=utf-8"
    assert response.text == "<h1>Is HTMX request: True</h1>"

    response = client.get("/test", headers={"hx-request": "false"})
    assert response.status_code == 200
    assert response.headers["content-type"] == "text/html; charset=utf-8"
    assert response.text == "<h1>Is HTMX request: False</h1>"

    response = client.get("/test")
    assert response.status_code == 200
    assert response.headers["content-type"] == "text/html; charset=utf-8"
    assert response.text == "<h1>Is HTMX request: False</h1>"


def test_request_htmx_method() -> None:
    app = Air()

    @app.get("/test")
    def test_endpoint(request: Request) -> H1:
        return H1(f"Is HTMX request: {request.htmx}")

    client = TestClient(app)

    response = client.get("/test", headers={"hx-request": "true"})
    assert response.status_code == 200
    assert response.headers["content-type"] == "text/html; charset=utf-8"
    assert response.text == "<h1>Is HTMX request: True</h1>"

    response = client.get("/test", headers={"hx-request": "false"})
    assert response.status_code == 200
    assert response.headers["content-type"] == "text/html; charset=utf-8"
    assert response.text == "<h1>Is HTMX request: False</h1>"

    response = client.get("/test")
    assert response.status_code == 200
    assert response.headers["content-type"] == "text/html; charset=utf-8"
    assert response.text == "<h1>Is HTMX request: False</h1>"


def test_htmx_boosted() -> None:
    app = Air()

    @app.get("/test")
    def test_endpoint(request: Request) -> H1:
        return H1(f"Is boosted: {request.htmx.boosted}")

    client = TestClient(app)

    response = client.get("/test", headers={"hx-boosted": "true"})
    assert response.text == "<h1>Is boosted: True</h1>"

    response = client.get("/test")
    assert response.text == "<h1>Is boosted: False</h1>"


def test_htmx_current_url() -> None:
    app = Air()

    @app.get("/test")
    def test_endpoint(request: Request) -> H1:
        return H1(f"Current URL: {request.htmx.current_url}")

    client = TestClient(app)

    response = client.get("/test", headers={"hx-current-url": "https://example.com/page"})
    assert response.text == "<h1>Current URL: https://example.com/page</h1>"

    response = client.get("/test")
    assert response.text == "<h1>Current URL: None</h1>"


def test_htmx_current_url_abs_path() -> None:
    app = Air()

    @app.get("/test")
    def test_endpoint(request: Request) -> H1:
        return H1(f"Abs path: {request.htmx.current_url_abs_path}")

    client = TestClient(app)

    response = client.get("/test", headers={"hx-current-url": "http://testserver/page?q=1"})
    assert response.text == "<h1>Abs path: /page?q=1</h1>"

    response = client.get("/test", headers={"hx-current-url": "https://other.com/page"})
    assert response.text == "<h1>Abs path: None</h1>"

    response = client.get("/test")
    assert response.text == "<h1>Abs path: None</h1>"


def test_htmx_history_restore_request() -> None:
    app = Air()

    @app.get("/test")
    def test_endpoint(request: Request) -> H1:
        return H1(f"History restore: {request.htmx.history_restore_request}")

    client = TestClient(app)

    response = client.get("/test", headers={"hx-history-restore-request": "true"})
    assert response.text == "<h1>History restore: True</h1>"

    response = client.get("/test")
    assert response.text == "<h1>History restore: False</h1>"


def test_htmx_prompt() -> None:
    app = Air()

    @app.get("/test")
    def test_endpoint(request: Request) -> H1:
        return H1(f"Prompt: {request.htmx.prompt}")

    client = TestClient(app)

    response = client.get("/test", headers={"hx-prompt": "user input"})
    assert response.text == "<h1>Prompt: user input</h1>"

    response = client.get("/test")
    assert response.text == "<h1>Prompt: None</h1>"


def test_htmx_target() -> None:
    app = Air()

    @app.get("/test")
    def test_endpoint(request: Request) -> H1:
        return H1(f"Target: {request.htmx.target}")

    client = TestClient(app)

    response = client.get("/test", headers={"hx-target": "my-div"})
    assert response.text == "<h1>Target: my-div</h1>"

    response = client.get("/test")
    assert response.text == "<h1>Target: None</h1>"


def test_htmx_trigger() -> None:
    app = Air()

    @app.get("/test")
    def test_endpoint(request: Request) -> H1:
        return H1(f"Trigger: {request.htmx.trigger}")

    client = TestClient(app)

    response = client.get("/test", headers={"hx-trigger": "button-id"})
    assert response.text == "<h1>Trigger: button-id</h1>"

    response = client.get("/test")
    assert response.text == "<h1>Trigger: None</h1>"


def test_htmx_trigger_name() -> None:
    app = Air()

    @app.get("/test")
    def test_endpoint(request: Request) -> H1:
        return H1(f"Trigger name: {request.htmx.trigger_name}")

    client = TestClient(app)

    response = client.get("/test", headers={"hx-trigger-name": "my-button"})
    assert response.text == "<h1>Trigger name: my-button</h1>"

    response = client.get("/test")
    assert response.text == "<h1>Trigger name: None</h1>"


def test_htmx_triggering_event() -> None:
    app = Air()

    @app.get("/test")
    def test_endpoint(request: AirRequest) -> H1:
        event = request.htmx.triggering_event
        if event:
            return H1(f"Event: {event['type']}")
        return H1("Event: None")

    client = TestClient(app)

    event_data = {"type": "click", "target": "button"}
    response = client.get("/test", headers={"triggering-event": json.dumps(event_data)})
    assert response.text == "<h1>Event: click</h1>"

    response = client.get("/test", headers={"triggering-event": "invalid json"})
    assert response.text == "<h1>Event: None</h1>"

    response = client.get("/test")
    assert response.text == "<h1>Event: None</h1>"
