import pytest

from caseworker.search.forms import ProductSearchForm, ProductSearchSuggestForm


@pytest.mark.parametrize(
    "data, is_valid, errors",
    (
        (
            {},
            True,
            {},
        ),
        (
            {"search_string": "Rifle"},
            True,
            {},
        ),
    ),
)
def test_product_search_form(data, is_valid, errors):
    form = ProductSearchForm(data=data)
    assert form.is_valid() is is_valid
    assert form.errors == errors


@pytest.mark.parametrize(
    ("data", "is_valid", "errors", "expected_cleaned_data"),
    (
        ({"q": ""}, False, {"q": ["This field is required."]}, {}),
        (
            {"q": 'end_user_country:"France"'},
            True,
            {},
            {"q": ""},
        ),
        ({"q": "some other text"}, True, {}, {"q": "some other text"}),
        ({"q": 'end_user_country:"France" some other text'}, True, {}, {"q": " some other text"}),
    ),
)
def test_product_search_suggest_form(data, is_valid, errors, expected_cleaned_data):
    form = ProductSearchSuggestForm(data=data)
    assert form.is_valid() is is_valid
    assert form.errors == errors
    assert form.cleaned_data == expected_cleaned_data
