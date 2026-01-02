import hashlib
import json
from typing import Any


def generate_cache_key(func_name: str, *args: Any, **kwargs: Any) -> str:
    """Generate a unique cache key based on function name and arguments.

    Args:
        func_name (str): Name of the function
        *args: Positional arguments to include in the cache key
        **kwargs: Keyword arguments to include in the cache key

    Returns:
        str: constructed cache key
    """

    arg_str = json.dumps({"args": args, "kwargs": kwargs}, sort_keys=True)
    arg_hash = hashlib.md5(arg_str.encode()).hexdigest()

    return f"__air:{func_name}:{arg_hash}"
