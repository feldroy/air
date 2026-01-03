from air.utils import cached_signature


def my_func(a: int, b: str) -> None:
    pass


sig = cached_signature(my_func)
# Subsequent calls with same function use cached result
sig2 = cached_signature(my_func)  # Fast!
