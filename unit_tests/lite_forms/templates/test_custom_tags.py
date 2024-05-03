import pytest

from lite_forms.templatetags import custom_tags


@pytest.mark.parametrize(
    "filename,expected",
    [
        ("test.pdf", "pdf"),
        ("test", "file"),
    ],
)
def test_file_type(filename, expected):
    assert expected == custom_tags.file_type(filename)


@pytest.mark.parametrize(
    "url, page, expected",
    [
        (
            "https://www.example.com/?page=1&example_param=foo&example_param=bar",
            2,
            "https://www.example.com/?page=2&example_param=foo&example_param=bar",
        ),
        (
            "https://www.example.com/?page=3&example_param=bar",
            5,
            "https://www.example.com/?page=5&example_param=bar",
        ),
        (
            "https://www.example.com/?example_param=bar",
            "10",
            "https://www.example.com/?example_param=bar&page=10",
        ),
    ],
)
def test_pagination_params(url, page, expected):
    assert custom_tags.pagination_params(url, page) == expected
