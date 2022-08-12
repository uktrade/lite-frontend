import pytest

from exporter.goods.forms.common import (
    ProductNameForm,
    ProductControlListEntryForm,
    ProductPVGradingForm,
    ProductPartNumberForm,
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


@pytest.mark.parametrize(
    "data, is_valid, errors",
    (
        ({}, False, {"is_pv_graded": ["Select yes if the product has a security grading or classification"]}),
        ({"is_pv_graded": True}, True, {}),
        ({"is_pv_graded": False}, True, {}),
    ),
)
def test_product_pv_security_gradings_form(data, is_valid, errors):
    form = ProductPVGradingForm(data=data)
    assert form.is_valid() == is_valid
    assert form.errors == errors


@pytest.mark.parametrize(
    "data, is_valid, errors",
    (
        (
            {},
            False,
            {
                "part_number": ["Enter the part number or select that you do not have a part number"],
            },
        ),
        (
            {"part_number_missing": True},
            False,
            {"part_number_missing": ["Enter the part number or select that you do not have a part number"]},
        ),
        (
            {"part_number_missing": True, "part_number": "abc12345"},
            False,
            {"part_number_missing": ["Enter the part number or select that you do not have a part number"]},
        ),
        (
            {"part_number_missing": False},
            False,
            {"part_number": ["Enter the part number or select that you do not have a part number"]},
        ),
        (
            {"part_number_missing": False, "no_part_number_comments": "some comments"},
            False,
            {"part_number": ["Enter the part number or select that you do not have a part number"]},
        ),
        (
            {"part_number_missing": False, "part_number": "abc12345"},
            True,
            {},
        ),
        (
            {"part_number_missing": True, "no_part_number_comments": "some comments"},
            True,
            {},
        ),
    ),
)
def test_product_part_number_form(data, is_valid, errors):
    form = ProductPartNumberForm(data=data)
    assert form.is_valid() == is_valid
    assert form.errors == errors
