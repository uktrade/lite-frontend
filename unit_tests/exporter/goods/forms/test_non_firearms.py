import pytest
from exporter.goods.forms import IsFirearmForm, NonFirearmCategoryForm


@pytest.mark.parametrize(
    "data, is_valid, errors",
    (
        (
            {},
            False,
            {
                "is_firearm_product": [
                    "Select whether it’s a complete product, forms part of a product or helps operate a product"
                ]
            },
        ),
        ({"is_firearm_product": True}, True, {}),
    ),
)
def test_is_firearm_form(data, is_valid, errors):
    form = IsFirearmForm(data=data)
    assert form.is_valid() == is_valid
    assert form.errors == errors


@pytest.mark.parametrize(
    "data, is_valid, errors",
    (
        ({}, False, {"no_firearm_category": ["Select the product category"]}),
        ({"no_firearm_category": "COMPLETE_PRODUCT"}, True, {}),
    ),
)
def test_non_firearm_category_form(data, is_valid, errors):
    form = NonFirearmCategoryForm(data=data)
    assert form.is_valid() == is_valid
    assert form.errors == errors
