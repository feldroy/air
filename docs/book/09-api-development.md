# API Development

!!! warning "First draft!"
    
    Please treat this as a very early draft, and be careful with anything that this chapter says! We welcome your pull requests to help refine the material so it actually becomes useful.

Air makes it easy to create powerful REST APIs alongside your HTML pages.

## JSON Responses

Unlike FastAPI, Air does not automatically handles JSON responses when you return Python dictionaries. Instead, we use FastAPI's `JSONResponse` class to return JSON.

```python
from fastapi.responses import JSONResponse

@app.get("/api/status")
def get_status():
    return JSONResponse(
        content={"status": "ok", "timestamp": datetime.now().isoformat()},
        headers={"X-API-Version": "1.0"}
    )
```

## Request Bodies

Handle JSON request bodies:

```python
from pydantic import BaseModel


class UserCreate(BaseModel):
    name: str
    email: str
    age: int


@app.post("/api/users")
def create_user(user: UserCreate):
    # user is automatically validated against UserCreate schema
    return JSONResponse({
        "id": 123,  # In real app, this would be from database
        "name": user.name,
        "email": user.email,
        "age": user.age
    })
```

## API Documentation

Air **does not** integrate with FastAPI's automatic API documentation. This is one reason why for API work we recommend instantiating a separate FastAPI app called `api`.

## Combining HTML and API

You can easily serve both HTML pages and API endpoints from the same application:

```python
# HTML page
app = air.Air()
api = fastapi.FastAPI()

@app.page
def dashboard():
    return air.layouts.mvpcss(
        air.Title("Dashboard"),
        air.H1("Dashboard"),
        # Load data via API call in JavaScript
        air.Div(id="api-data"),
        air.Script(
            """
            fetch('/api/user-data')
                .then(response => response.json())
                .then(data => {
                    document.getElementById('api-data').innerHTML = JSON.stringify(data);
                });
            """,
            type="module"
        )
    )

# API endpoint
@api.get("/user-data")
def get_user_data():
    return {"message": "Hello from API", "timestamp": datetime.now()}


app.mount('/api', api)
```

Now would be a good time to commit your work:

```bash
git add .
git commit -m "Add API endpoints and development patterns"
```