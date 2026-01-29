"""Tests for package-level attributes."""

from importlib.metadata import PackageNotFoundError, version

import air


def test_version_matches_metadata() -> None:
    """Test that air.__version__ matches installed distribution metadata.

    When the package is installed, the version should match the metadata.
    When running from source (metadata not available), it should use the
    documented dev fallback of "0.0.0.dev0".
    """
    try:
        expected_version = version("air")
        assert air.__version__ == expected_version
    except PackageNotFoundError:
        # If metadata is not available (e.g., running from source),
        # verify the documented dev fallback
        assert air.__version__ == "0.0.0.dev0"
