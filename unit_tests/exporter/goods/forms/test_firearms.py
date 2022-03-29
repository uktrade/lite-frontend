import pytest
import requests
import uuid

from exporter.goods.forms.firearms import (
    FirearmCalibreForm,
    FirearmCategoryForm,
    FirearmNameForm,
    FirearmProductControlListEntryForm,
    FirearmReplicaForm,
    FirearmRFDValidityForm,
)


@pytest.mark.parametrize(
    "data, is_valid, errors",
    (
        ({}, False, {"category": ['Select a firearm category, or select "None of the above"']}),
        (
            {"category": ["NON_AUTOMATIC_SHOTGUN", "NONE"]},
            False,
            {"category": ['Select a firearm category, or select "None of the above"']},
        ),
        ({"category": ["NON_AUTOMATIC_SHOTGUN", "NON_AUTOMATIC_RIM_FIRED_RIFLE"]}, True, {}),
        ({"category": ["NONE"]}, True, {}),
    ),
)
def test_firearm_category_form(data, is_valid, errors):
    form = FirearmCategoryForm(data=data)
    assert form.is_valid() == is_valid
    assert form.errors == errors


@pytest.mark.parametrize(
    "data, is_valid, errors",
    (
        ({}, False, {"name": ["Enter a descriptive name"]}),
        ({"name": ["TEST NAME"]}, True, {}),
    ),
)
def test_firearm_category_form(data, is_valid, errors):
    form = FirearmNameForm(data=data)
    assert form.is_valid() == is_valid
    assert form.errors == errors


@pytest.fixture
def request_with_session(rf, client):
    request = rf.get("/")
    request.session = client.session
    request.requests_session = requests.Session()

    return request


@pytest.fixture
def control_list_entries(requests_mock):
    requests_mock.get(
        "/static/control-list-entries/", json={"control_list_entries": [{"rating": "ML1"}, {"rating": "ML1a"}]}
    )


def test_firearm_product_control_list_entry_form_init_control_list_entries(request_with_session, control_list_entries):
    form = FirearmProductControlListEntryForm(request=request_with_session)
    assert form.fields["control_list_entries"].choices == [("ML1", "ML1"), ("ML1a", "ML1a")]


@pytest.mark.parametrize(
    "data, is_valid, errors",
    (
        ({}, False, {"is_good_controlled": ["Select yes if you know the products control list entry"]}),
        ({"is_good_controlled": True}, False, {"control_list_entries": ["Enter the control list entry"]}),
        ({"is_good_controlled": True, "control_list_entries": ["ML1", "ML1a"]}, True, {}),
        ({"is_good_controlled": False}, True, {}),
    ),
)
def test_firearm_product_control_list_entry_form(data, is_valid, errors, request_with_session, control_list_entries):
    form = FirearmProductControlListEntryForm(data=data, request=request_with_session)
    assert form.is_valid() == is_valid
    assert form.errors == errors


@pytest.mark.parametrize(
    "data, is_valid, errors",
    (
        ({}, False, {"calibre": ["Enter the calibre"]}),
        ({"calibre": "calibre 123"}, True, {}),
    ),
)
def test_firearm_calibre_form(data, is_valid, errors):
    form = FirearmCalibreForm(data=data)
    assert form.is_valid() == is_valid
    assert form.errors == errors


@pytest.mark.parametrize(
    "data, is_valid, errors",
    (
        ({}, False, {"is_replica": ["Select yes if the product is a replica firearm"]}),
        ({"is_replica": True}, False, {"replica_description": ["Enter a description"]}),
        ({"is_replica": True, "replica_description": "Replica description"}, True, {}),
        ({"is_replica": False}, True, {}),
    ),
)
def test_firearm_replica_form(data, is_valid, errors):
    form = FirearmReplicaForm(data=data)
    assert form.is_valid() == is_valid
    assert form.errors == errors


@pytest.mark.parametrize(
    "data, is_valid, errors",
    (
        ({}, False, {"is_rfd_valid": ["Select yes if your registered firearms dealer certificate is still valid"]}),
        ({"is_rfd_valid": True}, True, {}),
    ),
)
def test_firearm_validity_form(data, is_valid, errors):
    rfd_certificate = {
        "id": uuid.uuid4(),
        "document": {
            "name": "TEST DOCUMENT",
        },
    }

    form = FirearmRFDValidityForm(data=data, rfd_certificate=rfd_certificate)
    assert form.is_valid() == is_valid
    assert form.errors == errors
