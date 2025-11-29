# Minimal app

The "Hello, World" of Air is:

```
import air

app = air.Air()

@app.get("/")
async def index():
    return air.H1("Hello, Air!", style="color: blue;")
```
