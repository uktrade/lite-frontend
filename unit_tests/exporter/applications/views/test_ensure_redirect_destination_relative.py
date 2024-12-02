import pytest
from lite_forms.views import ensure_redirect_destination_relative, UnsafeRedirectDestination


def test_ensure_redirect_destination_relative_valid():
    try:
        ensure_redirect_destination_relative("/valid/path")
    except UnsafeRedirectDestination:
        pytest.fail("UnsafeRedirectDestination was raised unexpectedly!")


def test_ensure_redirect_destination_relative_backslashes_valid():
    try:
        ensure_redirect_destination_relative("\\valid\path")
    except UnsafeRedirectDestination:
        pytest.fail("UnsafeRedirectDestination was raised unexpectedly!")


def test_ensure_redirect_destination_relative_invalid():
    with pytest.raises(UnsafeRedirectDestination):
        ensure_redirect_destination_relative("https://malicious.com/invalid/path")


def test_ensure_redirect_destination_relative_backslashes_invalid():
    with pytest.raises(UnsafeRedirectDestination):
        ensure_redirect_destination_relative("https:/malicious.com")
