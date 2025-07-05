from typing import Annotated

from fastapi import Depends, Request
from fastapi.testclient import TestClient
import air

from pydantic import BaseModel, ValidationError


def test_simple_form():
    class CheeseModel(BaseModel):
        name: str
        age: int

    class AirForm:
        model = None
        data = None
        errors = None
        is_valid = None

        async def __call__(self, request: Request):
            data = await request.form()
            try:
                self.data = self.model(**data)
                self.is_valid = True
            except ValidationError as e:
                self.errors = e.errors()
                self.is_valid = False
            return self

    class CheeseForm(AirForm):
        model = CheeseModel

    app = air.Air()

    @app.post("/cheese")
    async def cheese_form(cheese: Annotated[CheeseForm, Depends(CheeseForm())]):
        if cheese.is_valid:
            return air.Html(air.H1(cheese.data.name))
        return air.Html(air.H1(air.RawHTML(str(len(cheese.errors)))))

    client = TestClient(app)

    # Test with valid form data
    response = client.post("/cheese", data={"name": "cheddar", "age": 5})
    assert response.status_code == 200
    assert response.headers["content-type"] == "text/html; charset=utf-8"
    assert response.text == "<!doctype html><html><h1>cheddar</h1></html>"

    # Test with invalid form data
    response = client.post("/cheese", data={})
    assert response.status_code == 200
    assert response.headers["content-type"] == "text/html; charset=utf-8"
    assert response.text == "<!doctype html><html><h1>2</h1></html>"
