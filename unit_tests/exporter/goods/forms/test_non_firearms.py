import pytest

from exporter.goods.forms import IsFirearmForm, NonFirearmCategoryForm


@pytest.mark.parametrize(
    "data, is_valid, errors",
    (
        (
            {},
            False,
            {"is_firearm_product": ["Select yes to add a firearm product"]},
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
        ({"no_firearm_category": "PLATFORM"}, True, {}),
    ),
)
def test_non_firearm_category_form(data, is_valid, errors):
    form = NonFirearmCategoryForm(data=data)
    assert form.is_valid() == is_valid
    assert form.errors == errors


def test_non_firearm_category_form_ff_enabled(settings):
    settings.FEATURE_FLAG_NON_FIREARMS_COMPONENTS_ENABLED = True
    settings.FEATURE_FLAG_NON_FIREARMS_SOFTWARE_ENABLED = True
    form = NonFirearmCategoryForm()
    choice_values = [c.value for c in form.fields["no_firearm_category"].choices]
    assert form.NonFirearmCategoryChoices.COMPONENTS.value in choice_values
    assert form.NonFirearmCategoryChoices.SOFTWARE.value in choice_values


def test_non_firearm_category_form_ff_disabled(settings):
    settings.FEATURE_FLAG_NON_FIREARMS_COMPONENTS_ENABLED = False
    settings.FEATURE_FLAG_NON_FIREARMS_SOFTWARE_ENABLED = False
    form = NonFirearmCategoryForm()
    choice_values = [c.value for c in form.fields["no_firearm_category"].choices]
    assert form.NonFirearmCategoryChoices.COMPONENTS not in choice_values
    assert form.NonFirearmCategoryChoices.SOFTWARE not in choice_values
