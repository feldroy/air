import marimo

__generated_with = "0.14.10"
app = marimo.App(width="medium")


@app.cell
def _():
    import griffe

    return (griffe,)


@app.cell
def _(griffe):
    loader = griffe.GriffeLoader()
    return (loader,)


@app.cell
def _(loader):
    mod = loader.load("air.forms")
    return (mod,)


@app.cell
def _(mod):
    mod
    return


@app.cell
def _(mod):
    mod.all_members
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
