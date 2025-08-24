from time import time

from fastapi.testclient import TestClient

import air


def test_session_middleware():
    app = air.Air()
    app.add_middleware(air.SessionMiddleware, secret_key="change-me")

    @app.page
    async def check(request: air.Request):
        return air.layouts.mvpcss(
            air.H1(request.session.get("timestamp")),
        )

    @app.page
    async def reset(request: air.Request):
        request.session.pop("timestamp")
        return air.P("Reset")

    @app.get("/{timestamp}")
    async def home(request: air.Request, timestamp: int):
        request.session["timestamp"] = timestamp
        return air.layouts.mvpcss(
            air.H1(request.session.get("timestamp")),
        )

    client = TestClient(app)

    response = client.get("/123456")
    assert response.status_code == 200
    assert "123456" in response.text

    response = client.get("/check")
    assert response.status_code == 200
    assert "123456" in response.text

    response = client.get("/reset")
    response = client.get("/check")
    assert response.status_code == 200
    assert "123456" not in response.text
    assert "None" in response.text

    response = client.get("/654321")
    assert response.status_code == 200
    assert "654321" in response.text

    response = client.get("/check")
    assert response.status_code == 200
    assert "654321" in response.text


def test_user_middleware():

    app = air.Air()
    app.add_middleware(air.UserMiddleware)    
    app.add_middleware(air.SessionMiddleware, secret_key='change-me')    

    @app.page
    async def index(request: air.Request):
        return air.H1(str(getattr(request.state.user, 'login_time', 'None')))
    
    @app.get('/{login_time}')
    async def add_user(request: air.Request, login_time:int):
        request.state.user.login_time = login_time
        return air.H1(f'Time: {login_time}')
                

    client = TestClient(app)

    response = client.get("/123456")
    assert response.status_code == 200
    assert "123456" in response.text


    response = client.get("/")    
    assert response.status_code == 200
    assert "123456" in response.text    