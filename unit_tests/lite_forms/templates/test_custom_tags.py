import pytest

from lite_forms.templatetags import custom_tags


@pytest.fixture()
def dummy_choice():
    class FakeType:
        choices = (
            ("T1", "label 1"),
            ("T2", "label 2"),
        )

    return FakeType


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
    "items, expected",
    [
        ([], ""),
        (None, ""),
        (["T1"], "label 1"),
        (["T1", "T2"], "label 1, label 2"),
    ],
)
def test_list_to_choice_labels(items, expected, dummy_choice):
    assert expected == custom_tags.list_to_choice_labels(items, dummy_choice)
