import inspect

from air.utils import cached_signature


def test_cached_signature() -> None:
    def my_func(a: int, b: str) -> None:
        pass

    sig = cached_signature(my_func)
    # Subsequent calls with same function use cached result
    sig2 = cached_signature(my_func)  # Fast!

    # Verify both signatures are the same
    assert sig == sig2
    assert isinstance(sig, inspect.Signature)
    assert len(sig.parameters) == 2
    assert "a" in sig.parameters
    assert "b" in sig.parameters
