import pytest

from exporter.goods.forms.common import (
    ProductNameForm,
    ProductControlListEntryForm,
)


@pytest.mark.parametrize(
    "data, is_valid, errors",
    (
        ({}, False, {"name": ["Enter a descriptive name"]}),
        ({"name": ["TEST NAME"]}, True, {}),
    ),
)
def test_product_form(data, is_valid, errors):
    form = ProductNameForm(data=data)
    assert form.is_valid() == is_valid
    assert form.errors == errors


@pytest.fixture
def control_list_entries(requests_mock):
    requests_mock.get(
        "/static/control-list-entries/", json={"control_list_entries": [{"rating": "ML1"}, {"rating": "ML1a"}]}
    )


def test_product_control_list_entry_form_init_control_list_entries(request_with_session, control_list_entries):
    form = ProductControlListEntryForm(request=request_with_session)
    assert form.fields["control_list_entries"].choices == [("ML1", "ML1"), ("ML1a", "ML1a")]


@pytest.mark.parametrize(
    "data, is_valid, errors",
    (
        ({}, False, {"is_good_controlled": ["Select yes if you know the product's control list entry"]}),
        ({"is_good_controlled": True}, False, {"control_list_entries": ["Enter the control list entry"]}),
        ({"is_good_controlled": True, "control_list_entries": ["ML1", "ML1a"]}, True, {}),
        ({"is_good_controlled": False}, True, {}),
    ),
)
def test_product_control_list_entry_form(data, is_valid, errors, request_with_session, control_list_entries):
    form = ProductControlListEntryForm(data=data, request=request_with_session)
    assert form.is_valid() == is_valid
    assert form.errors == errors
