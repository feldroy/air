from importlib.metadata import version

import air


def test_version_attribute() -> None:
    """air.__version__ matches the installed package version."""
    assert air.__version__ == version("air")
