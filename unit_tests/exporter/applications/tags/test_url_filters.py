import pytest

from exporter.applications.templatetags.url_filters import has_param


@pytest.mark.parametrize(
    "url, param, expected_result",
    [
        ("http://example.com/applications/?param1=value1", "param1=value1", True),
        ("http://example.com/applications/?param1=value1", "param1=value2", False),
        ("http://example.com/applications/?param1=value1&param2=value2", "param2=value2", True),
        ("http://example.com/applications/", "param1=value1", False),  # Testing with no query params
        (
            "http://example.com/applications/?param1=value1&param1=value2",
            "param1=value2",
            True,
        ),  # Multiple same-name params
    ],
)
def test_has_param(url, param, expected_result):
    assert has_param(url, param) == expected_result
