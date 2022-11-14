import pytest
from exporter.goods.forms import (
    IsFirearmForm,
    NonFirearmCategoryForm,
    IsMaterialSubstanceCategoryForm,
    ProductIsComponentForm,
    ProductComponentDetailsForm,
)


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
        ({"no_firearm_category": "COMPLETE_ITEM"}, True, {}),
    ),
)
def test_non_firearm_category_form(data, is_valid, errors):
    form = NonFirearmCategoryForm(data=data)
    assert form.is_valid() == is_valid
    assert form.errors == errors


@pytest.mark.parametrize(
    "data, is_valid, errors",
    (
        ({}, False, {"is_material_substance": ["Select yes if the product is a material or substance"]}),
        ({"is_material_substance": True}, True, {}),
    ),
)
def test_is_material_form(data, is_valid, errors):
    form = IsMaterialSubstanceCategoryForm(data=data)
    assert form.is_valid() == is_valid
    assert form.errors == errors


@pytest.mark.parametrize(
    "data, is_valid, errors",
    (
        ({}, False, {"is_component": ["Select yes if the product is a component"]}),
        ({"is_component": True}, True, {}),
    ),
)
def test_is_component_form(data, is_valid, errors):
    form = ProductIsComponentForm(data=data)
    assert form.is_valid() == is_valid
    assert form.errors == errors


@pytest.mark.parametrize(
    "data, is_valid, errors",
    (
        ({}, False, {"component_type": ["Select the type of component"]}),
        ({"component_type": "yes_designed"}, False, {"designed_details": ["Enter details of the specific hardware"]}),
        (
            {"component_type": "yes_modified"},
            False,
            {"modified_details": ["Enter details of the modifications and the specific hardware"]},
        ),
        (
            {"component_type": "yes_general"},
            False,
            {"general_details": ["Enter details of the intended general-purpose use"]},
        ),
        ({"component_type": "yes_designed", "designed_details": "hardware details"}, True, {}),
        ({"component_type": "yes_modified", "modified_details": "modified hardware details"}, True, {}),
        ({"component_type": "yes_general", "general_details": "general purpose details"}, True, {}),
    ),
)
def test_component_type_form(data, is_valid, errors):
    form = ProductComponentDetailsForm(data=data)
    assert form.is_valid() == is_valid
    assert form.errors == errors
