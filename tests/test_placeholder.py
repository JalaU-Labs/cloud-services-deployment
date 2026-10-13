"""Placeholder test to verify pytest setup."""

from lab_cloud import __version__


def test_version() -> None:
    """Test that the package version is defined."""
    assert __version__ == "0.1.0"
