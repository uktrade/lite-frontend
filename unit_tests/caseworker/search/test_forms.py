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
    "data, is_valid, errors",
    (
        (
            {},
            False,
            {"q": ["This field is required."]},
        ),
        (
            {"q": 'end_user_country:"France"'},
            True,
            {},
        ),
    ),
)
def test_product_search_suggest_form(data, is_valid, errors):
    form = ProductSearchSuggestForm(data=data)
    assert form.is_valid() is is_valid
    assert form.errors == errors
