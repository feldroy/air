# The app.page decorator

For simple HTTP GET requests, Air provides the handy @app.page shortcut. It converts the name of the function to a URL, where underscores are replaced with dashes and `index` is replaced with '/'.

```python
import air

app = air.Air()


@app.page 
def index():
    # Same as route app.get('/')
    return air.H1('Welcome to our site!')

@app.page
def dashboard():
    # Same as route app.get('/dashboard')
    return air.H1('Dashboard')

@app.page
def show_item():
    # same as app.get('/get-item')
    return air.H1('Showing an item')
```
