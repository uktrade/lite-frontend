import pytest

from exporter.goods.forms.firearms import FirearmCategoryForm


@pytest.mark.parametrize(
    "data, is_valid, errors",
    (
        ({}, False, {"firearm_category": ['Select a firearm category, or select "None of the above"']}),
        (
            {"firearm_category": ["NON_AUTOMATIC_SHOTGUN", "NONE"]},
            False,
            {"firearm_category": ['Select a firearm category, or select "None of the above"']},
        ),
        ({"firearm_category": ["NON_AUTOMATIC_SHOTGUN", "NON_AUTOMATIC_RIM_FIRED_RIFLE"]}, True, {}),
        ({"firearm_category": ["NONE"]}, True, {}),
    ),
)
def test_firearm_category_form(data, is_valid, errors):
    form = FirearmCategoryForm(data=data)
    assert form.is_valid() == is_valid
    assert form.errors == errors
