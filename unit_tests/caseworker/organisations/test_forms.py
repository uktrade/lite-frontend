import pytest
import requests

from caseworker.core.services import get_countries
from caseworker.organisations import forms
from lite_forms import common


@pytest.fixture(autouse=True)
def setup(
    mock_get_countries,
):
    yield


def post_request(rf, client, data=None):
    request = rf.post("/", data if data else {})
    request.session = client.session
    request.requests_session = requests.Session()
    return request


@pytest.fixture
def countries(mock_get_countries, rf, client):
    request = rf.get("/")
    request.session = client.session
    request.requests_session = requests.Session()
    data = get_countries(request, True, ["GB"])
    return data


@pytest.mark.parametrize(
    "type, location, num_forms",
    [
        ("commercial", "united_kingdom", 5),
        ("individual", "united_kingdom", 4),
    ],
)
def test_register_organisation_form(rf, client, type, location, num_forms):
    data = {"type": type, "location": location}
    request = post_request(rf, client, data=data)
    registration_forms = forms.register_organisation_forms(request)
    assert len(registration_forms.forms) == num_forms


@pytest.mark.parametrize(
    "is_individual, in_uk, num_questions",
    [
        (False, False, 6),
        (False, True, 10),
        (True, False, 6),
        (True, True, 10),
    ],
)
def test_create_default_site_form(rf, client, is_individual, in_uk, num_questions):
    request = rf.get("/")
    request.session = client.session
    request.requests_session = requests.Session()
    form = forms.create_default_site_form(request, is_individual, in_uk)
    assert len(form.questions) == num_questions

    ph_no_q = form.questions[7] if in_uk else form.questions[3]
    assert ph_no_q.title == "Phone number" if is_individual else "Organisation phone number"
    assert ph_no_q.name == "phone_number"
    assert ph_no_q.description == "For international numbers include the country code"

    website_q = form.questions[8] if in_uk else form.questions[4]
    assert website_q.title == "Website"
    assert website_q.name == "website"


def test_create_admin_user_form():
    form = forms.create_admin_user_form()
    assert len(form.questions) == 2
    assert form.questions[1].title == "Contact phone number"
    assert form.questions[1].optional == True


@pytest.mark.parametrize(
    "is_commercial, in_uk, num_questions",
    [
        (False, False, 6),
        (False, True, 10),
        (True, False, 6),
        (True, True, 10),
    ],
)
def test_edit_address_questions_form(countries, is_commercial, in_uk, num_questions):
    form = common.edit_address_questions_form(is_commercial, in_uk, countries)
    assert form.title == "Edit default site for this exporter"
    assert len(form.questions) == num_questions

    ph_no_q = form.questions[7] if in_uk else form.questions[3]
    assert ph_no_q.title == "Organisation phone number" if is_commercial else "Phone number"
    assert ph_no_q.name == "phone_number"
    assert ph_no_q.description == "For international numbers include the country code"

    website_q = form.questions[8] if in_uk else form.questions[4]
    assert website_q.title == "Website"
    assert website_q.name == "website"
