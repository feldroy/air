Utils

## compute_page_path

```
compute_page_path(endpoint_name, separator='-')
```

index -> '/', otherwise '/name-with-dashes'.

Source code in `src/air/utils.py`

```
def compute_page_path(endpoint_name: str, separator: Literal["/", "-"] = "-") -> str:
    """index -> '/', otherwise '/name-with-dashes'."""
    return "/" if endpoint_name == "index" else f"/{endpoint_name.replace('_', separator)}"
```
