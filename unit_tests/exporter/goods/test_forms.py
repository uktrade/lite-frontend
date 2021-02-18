import pytest
import requests
from django.test import override_settings

from lite_forms.components import HelpSection

from exporter.core.services import get_pv_gradings
from exporter.applications.services import serialize_good_on_app_data
from exporter.goods import forms


@pytest.fixture(autouse=True)
def setup(
    mock_control_list_entries, mock_pv_gradings,
):
    yield


def post_request(rf, client, data=None):
    request = rf.post("/", data if data else {})
    request.session = client.session
    request.requests_session = requests.Session()
    return request


def test_add_goods_questions_feature_flag_on(settings):
    settings.FEATURE_FLAG_ONLY_ALLOW_SIEL = True

    form = forms.add_goods_questions(control_list_entries=[])

    assert form.questions[3].options[-1].components[0].__class__ == HelpSection
    assert form.questions[4].options[-1].components[0].__class__ == HelpSection


def test_add_goods_questions_feature_flag_off(settings):
    settings.FEATURE_FLAG_ONLY_ALLOW_SIEL = False

    form = forms.add_goods_questions(control_list_entries=[])

    assert form.questions[3].options[-1].components == []
    assert form.questions[4].options[-1].components == []


@pytest.mark.parametrize(
    "value, serialized",
    [
        ("2,300.00", "2300.00"),
        ("2,3,,,,,00.00", "2300.00"),
        ("23,444200", "23444200"),
        ("foo", "foo"),  # this will be caught by serializer on the api and return an error
        ("84.34.111", "84.34.111"),  # this too
    ],
)
def test_serialize_good_on_app_data(value, serialized):
    data = {
        "good_id": "some-uuid",
        "value": value,
        "quantity": value,
    }
    expected = {
        "good_id": "some-uuid",
        "value": serialized,
        "quantity": serialized,
    }
    assert serialize_good_on_app_data(data) == expected


@pytest.mark.parametrize(
    "value, serialized",
    [
        ("2,300.00", "2300.00"),
        ("2,3,,,,,00.00", "2300.00"),
        ("23,444200", "23444200"),
        ("foo", "foo"),  # this will be caught by serializer on the api and return an error
        ("84.34.111", "84.34.111"),  # this too
    ],
)
def test_serialize_good_on_app_data_no_value_key(value, serialized):

    data = {
        "good_id": "some-uuid",
        "quantity": value,
    }
    expected = {
        "good_id": "some-uuid",
        "quantity": serialized,
    }
    assert serialize_good_on_app_data(data) == expected


@pytest.fixture
def pv_gradings(mock_pv_gradings, rf, client):
    request = rf.get("/")
    request.session = client.session
    request.requests_session = requests.Session()
    data = get_pv_gradings(request, convert_to_options=True)
    return data


@pytest.mark.parametrize(
    "params, num_forms, question_checks",
    [
        (
            {"is_firearms_core": True},
            5,
            [
                {"qindex": 1, "name": "type"},
                {"qindex": 2, "name": "is_sporting_shotgun"},
                {"qindex": 0, "name": "name"},
                {"qindex": 0, "name": "firearm_calibre_step"},
                {"qindex": 0, "name": "is_registered_firearm_dealer"},
            ],
        ),
        (
            {"is_firearms_core": True, "draft_pk": "123", "is_firearm": True},
            9,
            [
                {"qindex": 1, "name": "type"},
                {"qindex": 1, "name": "has_identification_markings"},
                {"qindex": 2, "name": "is_sporting_shotgun"},
                {"qindex": 0, "name": "name"},
                {"qindex": 1, "name": "year_of_manufacture"},
                {"qindex": 2, "name": "is_replica"},
                {"qindex": 0, "name": "firearm_calibre_step"},
                {"qindex": 0, "name": "is_registered_firearm_dealer"},
                {"qindex": 2, "name": "is_covered_by_firearm_act_section_one_two_or_five"},
            ],
        ),
        (
            {"is_firearms_accessory": True},
            5,
            [
                {"qindex": 1, "name": "type"},
                {"qindex": 0, "name": "name"},
                {"qindex": 1, "name": "is_military_use"},
                {"qindex": 1, "name": "is_component"},
                {"qindex": 1, "name": "uses_information_security"},
            ],
        ),
        (
            {"is_firearms_software_tech": True},
            5,
            [
                {"qindex": 1, "name": "type"},
                {"qindex": 0, "name": "name"},
                {"qindex": 1, "name": "software_or_technology_details"},
                {"qindex": 1, "name": "is_military_use"},
                {"qindex": 1, "name": "uses_information_security"},
            ],
        ),
    ],
)
@override_settings(FEATURE_FLAG_ONLY_ALLOW_FIREARMS_PRODUCTS=True)
def test_core_firearm_product_form_group(rf, client, params, num_forms, question_checks):
    """ Test to ensure correct set of questions are asked in adding a firearm product journey depending on the firearm_type."""
    data = {"product_type_step": True, "type": "firearms"}
    kwargs = {"is_pv_graded": False, **params}
    request = post_request(rf, client, data=data)
    form_parts = forms.add_good_form_group(request, **kwargs).forms
    assert len(form_parts) == int(num_forms)

    for i, q in enumerate(question_checks):
        assert form_parts[i].questions[q["qindex"]].name == q["name"]


def test_has_valid_rfd_certificate_is_expired():
    actual = forms.has_valid_rfd_certificate(
        {"organisation": {"documents": [{"document_type": "rfd-certificate", "is_expired": True}]}}
    )

    assert actual is False


def test_has_valid_rfd_certificate_not_expired():
    actual = forms.has_valid_rfd_certificate(
        {"organisation": {"documents": [{"document_type": "rfd-certificate", "is_expired": False}]}}
    )

    assert actual is True


def test_has_valid_rfd_certificate_empty():
    actual = forms.has_valid_rfd_certificate({"organisation": {"documents": []}})

    assert actual is False


def test_has_valid_section_five_certificate_is_expired():
    actual = forms.has_valid_section_five_certificate(
        {"organisation": {"documents": [{"document_type": "section-five-certificate", "is_expired": True}]}}
    )

    assert actual is False


def test_has_valid_section_five_certificate_not_expired():
    actual = forms.has_valid_section_five_certificate(
        {"organisation": {"documents": [{"document_type": "section-five-certificate", "is_expired": False}]}}
    )

    assert actual is True


def test_has_valid_section_five_certificate_empty():
    actual = forms.has_valid_section_five_certificate({"organisation": {"documents": []}})

    assert actual is False


def test_goods_check_document_available_form():
    form = forms.check_document_available_form("back")
    assert len(form.questions) == 1
    assert form.title == "Do you have a document that shows what your product is and what it’s designed to do?"
    assert form.questions[0].name == "is_document_available"
    assert len(form.buttons) == 1
    assert form.buttons[0].value == "Save and continue"


def test_goods_check_document_sensitivity_form():
    form = forms.document_grading_form("back")
    assert len(form.questions) == 1
    assert form.title == "Is the document rated above OFFICIAL-SENSITIVE?"
    assert form.questions[0].name == "is_document_sensitive"
    assert len(form.buttons) == 1
    assert form.buttons[0].value == "Save and continue"
