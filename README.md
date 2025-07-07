# airdocs

## Install

```sh
gh repo clone feldroy/airdocs
cd airdocs
uv venv
source .venv/bin/activate
uv add --editable ../air
uv add --editable ../EidosUI
uv run fastapi dev main.py
```