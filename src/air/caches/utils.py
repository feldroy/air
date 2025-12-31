import hashlib
import json
from typing import Any


def _generate_cache_key(func_name: str, *args: tuple[Any], **kwargs: dict[str, Any]) -> str:
    """Generate a unique cache key based on function name and arguments.

    Args:
        func_name (str): Name of the function

    Returns:
        str: constructed cache key
    """

    arg_str = json.dumps({"args": args, "kwargs": kwargs}, sort_keys=True)
    arg_hash = hashlib.md5(arg_str.encode()).hexdigest()

    return f"__air:{func_name}:{arg_hash}"
