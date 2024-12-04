import pytest
from django.core.exceptions import SuspiciousOperation
from lite_forms.views import ensure_redirect_destination_relative


def test_ensure_redirect_destination_relative_valid():
    try:
        ensure_redirect_destination_relative("/valid/path")
    except SuspiciousOperation:
        pytest.fail("UnsafeRedirectDestination was raised unexpectedly!")


def test_ensure_redirect_destination_relative_backslashes_valid():
    try:
        ensure_redirect_destination_relative("\\valid\path")
    except SuspiciousOperation:
        pytest.fail("UnsafeRedirectDestination was raised unexpectedly!")


def test_ensure_redirect_destination_relative_invalid():
    with pytest.raises(SuspiciousOperation):
        ensure_redirect_destination_relative("https://malicious.com/invalid/path")


def test_ensure_redirect_destination_relative_backslashes_invalid():
    with pytest.raises(SuspiciousOperation):
        ensure_redirect_destination_relative("https:/malicious.com")
