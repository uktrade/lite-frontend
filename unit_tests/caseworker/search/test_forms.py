import pytest

from caseworker.search.forms import ProductSearchForm


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
