"""Tests for package-level attributes."""

from importlib.metadata import version

import air


def test_version_is_accessible() -> None:
    """Test that air.__version__ is accessible and valid."""
    assert hasattr(air, "__version__")
    assert isinstance(air.__version__, str)
    assert len(air.__version__) > 0
    # Should be a valid version format (e.g., "0.45.0" or "0.0.0.dev0")
    assert "." in air.__version__


def test_version_matches_installed_metadata() -> None:
    """Test that air.__version__ matches the installed package metadata."""
    assert air.__version__ == version("air")
