import pytest
import requests

from exporter.goods.forms.firearms import (
    FirearmCalibreForm,
    FirearmCategoryForm,
    FirearmNameForm,
    FirearmProductControlListEntryForm,
    FirearmPvGradingForm,
    FirearmPvGradingDetailsForm,
    FirearmReplicaForm,
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


@pytest.fixture
def pv_gradings(requests_mock):
    requests_mock.get(
        "/static/private-venture-gradings/v2/",
        json={"pv_gradings": [{"official": "Official"}, {"restricted": "Restricted"}]},
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
        ({}, False, {"is_pv_graded": ["Select yes if the product has a security grading or classification"]}),
        ({"is_pv_graded": True}, True, {}),
        ({"is_pv_graded": False}, True, {}),
    ),
)
def test_firearm_pv_security_gradings_form(data, is_valid, errors):
    form = FirearmPvGradingForm(data=data)
    assert form.is_valid() == is_valid
    assert form.errors == errors


@pytest.mark.parametrize(
    "data, is_valid, errors",
    (
        (
            {},
            False,
            {
                "grading": ["Select the security grading"],
                "issuing_authority": ["Enter the name and address of the issuing authority"],
                "reference": ["Enter the reference"],
                "date_of_issue": ["Enter the date of issue"],
            },
        ),
        (
            {"grading": "official", "reference": "ABC123"},
            False,
            {
                "issuing_authority": ["Enter the name and address of the issuing authority"],
                "date_of_issue": ["Enter the date of issue"],
            },
        ),
        (
            {
                "grading": "official",
                "reference": "ABC123",
                "issuing_authority": "Government entity",
                "date_of_issue_0": "20",
            },
            False,
            {
                "date_of_issue": ["Date of issue must include a month", "Date of issue must include a year"],
            },
        ),
        (
            {
                "grading": "official",
                "reference": "ABC123",
                "issuing_authority": "Government entity",
                "date_of_issue_0": "20",
                "date_of_issue_2": "2020",
            },
            False,
            {
                "date_of_issue": ["Date of issue must include a month"],
            },
        ),
        (
            {
                "grading": "official",
                "reference": "ABC123",
                "issuing_authority": "Government entity",
                "date_of_issue_0": "20",
                "date_of_issue_1": "2",
                "date_of_issue_2": "2040",
            },
            False,
            {
                "date_of_issue": ["Date of issue must be in the past"],
            },
        ),
        (
            {
                "grading": "official",
                "reference": "ABC123",
                "issuing_authority": "Government entity",
                "date_of_issue_0": "50",
                "date_of_issue_1": "2",
                "date_of_issue_2": "2020",
            },
            False,
            {
                "date_of_issue": ["day is out of range for month"],
            },
        ),
        (
            {
                "grading": "official",
                "reference": "ABC123",
                "issuing_authority": "Government entity",
                "date_of_issue_0": "20",
                "date_of_issue_1": "20",
                "date_of_issue_2": "2020",
            },
            False,
            {
                "date_of_issue": ["month must be in 1..12"],
            },
        ),
        (
            {
                "grading": "official",
                "reference": "ABC123",
                "issuing_authority": "Government entity",
                "date_of_issue_0": "20",
                "date_of_issue_1": "2",
                "date_of_issue_2": "2020",
            },
            True,
            {},
        ),
    ),
)
def test_firearm_pv_security_grading_details_form(data, is_valid, errors, request_with_session, pv_gradings):
    form = FirearmPvGradingDetailsForm(data=data, request=request_with_session)
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
