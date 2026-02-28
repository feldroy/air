# `def` vs `async def`

Air endpoints can be written with `def` or `async def`. Here's how to choose.

**Does the code inside your endpoint use `await`?**

- **No** → use `def`
- **Yes** → use `async def`

That's it. Here are examples of each.

## Endpoints without `await`

These all use `def`:

```python
@app.get("/users/{user_id}")
def user_detail(user_id: int):
    user = db.get_user(user_id)
    return air.H1(user.name)

@app.get("/about")
def about():
    return air.H1("About")

@app.get("/data")
def get_data():
    content = open("data.csv").read()
    return air.Pre(content)
```

## Endpoints with `await`

These use `async def`:

```python
@app.post("/submit")
async def handle_form(request: air.Request):
    form = await ContactForm.from_request(request)
    if form.is_valid:
        return air.H1(f"Hello, {form.data.name}!")
    return form.render()

@app.get("/external")
async def fetch_data():
    async with httpx.AsyncClient() as client:
        resp = await client.get("https://api.example.com/data")
    return air.H1(resp.text)
```

!!! warning
    If your endpoint doesn't use `await`, use `def`, not `async def`. Writing `async def` without `await` freezes your entire application until the call finishes.

    ```python
    # WRONG: freezes the server while reading
    @app.get("/data")
    async def get_data():
        return open("big_file.csv").read()

    # RIGHT: runs in a thread, other requests keep flowing
    @app.get("/data")
    def get_data():
        return open("big_file.csv").read()
    ```
