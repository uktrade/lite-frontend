import pytest

from exporter.goods.forms.common import ProductNameForm


@pytest.mark.parametrize(
    "data, is_valid, errors",
    (
        ({}, False, {"name": ["Enter a descriptive name"]}),
        ({"name": ["TEST NAME"]}, True, {}),
    ),
)
def test_firearm_category_form(data, is_valid, errors):
    form = ProductNameForm(data=data)
    assert form.is_valid() == is_valid
    assert form.errors == errors
