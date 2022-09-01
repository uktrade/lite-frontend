import pytest
from exporter.goods.forms import IsFirearmForm, NonFirearmCategoryForm, IsMaterialSubstanceCategoryForm


@pytest.fixture(autouse=True)
def setup(settings):
    settings.FEATURE_FLAG_NON_FIREARMS_ENABLED = True
    settings.FEATURE_FLAG_NON_FIREARMS_COMPONENTS_ENABLED = True
    settings.FEATURE_FLAG_NON_FIREARMS_SOFTWARE_ENABLED = True
    settings.FEATURE_FLAG_NON_FIREARMS_MATERIAL_ENABLED = True
    settings.FEATURE_FLAG_NON_FIREARMS_PLATFORM_ENABLED = True


@pytest.fixture
def disable_non_firearms(settings):
    settings.FEATURE_FLAG_NON_FIREARMS_ENABLED = False
    settings.FEATURE_FLAG_NON_FIREARMS_COMPONENTS_ENABLED = False
    settings.FEATURE_FLAG_NON_FIREARMS_SOFTWARE_ENABLED = False
    settings.FEATURE_FLAG_NON_FIREARMS_MATERIAL_ENABLED = False
    settings.FEATURE_FLAG_NON_FIREARMS_PLATFORM_ENABLED = False


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


@pytest.mark.parametrize(
    "feature, choice",
    (
        ("FEATURE_FLAG_NON_FIREARMS_PLATFORM_ENABLED", "PLATFORM"),
        ("FEATURE_FLAG_NON_FIREARMS_COMPONENTS_ENABLED", "MATERIAL_CATEGORY"),
        ("FEATURE_FLAG_NON_FIREARMS_MATERIAL_ENABLED", "MATERIAL_CATEGORY"),
        ("FEATURE_FLAG_NON_FIREARMS_SOFTWARE_ENABLED", "SOFTWARE"),
    ),
)
def test_non_firearm_category_form_ff_enabled(settings, disable_non_firearms, feature, choice):
    setattr(settings, feature, True)
    form = NonFirearmCategoryForm()
    choice_values = [c.value for c in form.fields["no_firearm_category"].choices]
    assert len(choice_values) == 1
    assert choice_values == [choice]


@pytest.mark.parametrize(
    "feature, choice",
    (
        ("FEATURE_FLAG_NON_FIREARMS_MATERIAL_ENABLED", True),
        ("FEATURE_FLAG_NON_FIREARMS_COMPONENTS_ENABLED", False),
    ),
)
def test_is_material_form_feaature_ff_enabled(settings, disable_non_firearms, feature, choice):
    setattr(settings, feature, True)
    form = IsMaterialSubstanceCategoryForm()
    choice_values = [c[0] for c in form.fields["is_material_substance"].choices]
    assert len(choice_values) == 1
    assert choice_values[0] == choice


@pytest.mark.parametrize(
    "data, is_valid, errors",
    (
        ({}, False, {"is_material_substance": ["Select yes if material or substance category"]}),
        ({"is_material_substance": True}, True, {}),
    ),
)
def test_is_material_form(data, is_valid, errors):
    form = IsMaterialSubstanceCategoryForm(data=data)
    assert form.is_valid() == is_valid
    assert form.errors == errors
