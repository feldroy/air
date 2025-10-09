# API Development

!!! warning "Unreliable, incorrect advice lurks here"

    This chapter likely contains heavy AI edits on Daniel Roy Greenfeld's initial handwritten blog tutorial. AI has expanded sections, and Audrey M. Roy Greenfeld has not tested and rewritten those yet. 
    
    Please treat it as a very early draft, and DO NOT TRUST anything that this chapter says! We welcome your pull requests to help refine the material so it actually becomes useful.

Air makes it easy to create powerful REST APIs alongside your HTML pages.

## JSON Responses

Air automatically handles JSON responses when you return Python dictionaries:

```python
@app.get("/api/users")
def get_users():
    # Return Python data structure, Air converts to JSON
    return {
        "users": [
            {"id": 1, "name": "John", "email": "john@example.com"},
            {"id": 2, "name": "Jane", "email": "jane@example.com"}
        ]
    }

@app.get("/api/users/{user_id}")
def get_user(user_id: int):
    # Return single user
    return {"id": user_id, "name": "John", "email": "john@example.com"}
```

## Custom JSON Responses

For more control, use FastAPI's JSONResponse:

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
    return {
        "id": 123,  # In real app, this would be from database
        "name": user.name,
        "email": user.email,
        "age": user.age
    }
```

## API Documentation

Air integrates with FastAPI's automatic API documentation. Access it at `/docs` and `/redoc` (if enabled).

## Combining HTML and API

You can easily serve both HTML pages and API endpoints from the same application:

```python
# HTML page
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
@app.get("/api/user-data")
def get_user_data():
    return {"message": "Hello from API", "timestamp": datetime.now()}
```

Now would be a good time to commit your work:

```bash
git add .
git commit -m "Add API endpoints and development patterns"
```