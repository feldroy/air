import air

app = air.Air()

@app.page
def index():
    return air.H1('hello world')
