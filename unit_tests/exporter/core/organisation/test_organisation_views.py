import pytest
from pytest_django.asserts import assertTemplateUsed
from bs4 import BeautifulSoup
from django.test import Client
from django.urls import reverse
from exporter.core.organisation.constants import RegistrationSteps
from exporter.core.organisation.forms import (
    RegisterDetailsIndividualUKForm,
    RegistrationUKBasedForm,
    RegisterDetailsCommercialUKForm,
    RegisterAddressDetailsUKForm,
    RegisterAddressDetailsOverseasForm,
    RegistrationConfirmation,
)
from unit_tests.helpers import reload_urlconf


@pytest.fixture(autouse=True)
def setup(no_op_storage, mock_validate_registration_number, settings):
    settings.FEATURE_FLAG_DJANGO_FORMS_REGISTRATION_ENABLED = True
    reload_urlconf(["exporter.core.urls", settings.ROOT_URLCONF])


@pytest.fixture()
def registration_url():
    return reverse("core:register_an_organisation_triage")


@pytest.fixture
def post_to_step(post_to_step_factory, registration_url):
    return post_to_step_factory(registration_url)


@pytest.fixture
def goto_step(goto_step_factory, registration_url):
    return goto_step_factory(registration_url)


@pytest.fixture
def registration_data():
    return {
        "type": "commercial",
        "location": "united_kingdom",
    }


@pytest.fixture(autouse=True)
def mock_organisations_post(requests_mock):
    return requests_mock.post(url="/organisations/", json={}, status_code=201)


@pytest.fixture(autouse=True)
def mock_authenticate_user_post(requests_mock, mock_exporter_user):
    return requests_mock.post(
        url="/users/authenticate/",
        json={
            "lite_api_user_id": mock_exporter_user["user"]["lite_api_user_id"],
            "token": mock_exporter_user["user"]["token"],
        },
        status_code=200,
    )


def test_registration_type_step(goto_step, post_to_step):
    goto_step(RegistrationSteps.REGISTRATION_TYPE)
    response = post_to_step(
        RegistrationSteps.REGISTRATION_TYPE,
        {"type": "commercial"},
    )

    assert response.status_code == 200
    assert isinstance(response.context["form"], RegistrationUKBasedForm)


def test_registration_uk_based_step(goto_step, post_to_step):
    goto_step(RegistrationSteps.REGISTRATION_TYPE)
    post_to_step(
        RegistrationSteps.REGISTRATION_TYPE,
        {"type": "commercial"},
    )
    goto_step(RegistrationSteps.UK_BASED)
    response = post_to_step(
        RegistrationSteps.UK_BASED,
        {"location": "united_kingdom"},
    )

    assert response.status_code == 200
    assert isinstance(response.context["form"], RegisterDetailsCommercialUKForm)


def test_registration_individual_details_step(goto_step, post_to_step):
    goto_step(RegistrationSteps.REGISTRATION_TYPE)
    post_to_step(
        RegistrationSteps.REGISTRATION_TYPE,
        {"type": "individual"},
    )
    goto_step(RegistrationSteps.UK_BASED)
    post_to_step(
        RegistrationSteps.UK_BASED,
        {"location": "united_kingdom"},
    )

    goto_step(RegistrationSteps.REGISTRATION_DETAILS)

    response = post_to_step(
        RegistrationSteps.REGISTRATION_DETAILS,
        {"name": "joe", "eori_number": "GB205672212000", "vat_number": "GB123456789"},
    )
    assert response.status_code == 200
    assert isinstance(response.context["form"], RegisterAddressDetailsUKForm)


def test_registration_individual_end_to_end_uk_based(
    goto_step, post_to_step, mock_organisations_post, mock_authenticate_user_post
):
    goto_step(RegistrationSteps.REGISTRATION_TYPE)
    response = post_to_step(
        RegistrationSteps.REGISTRATION_TYPE,
        {"type": "individual", "location": "united_kingdom"},
    )

    assert response.status_code == 200
    assert not response.context["form"].errors
    assert isinstance(response.context["form"], RegistrationUKBasedForm)

    goto_step(RegistrationSteps.UK_BASED)
    response = post_to_step(
        RegistrationSteps.UK_BASED,
        {"type": "individual", "location": "united_kingdom"},
    )

    assert response.status_code == 200
    assert not response.context["form"].errors

    assert isinstance(response.context["form"], RegisterDetailsIndividualUKForm)

    goto_step(RegistrationSteps.REGISTRATION_DETAILS)
    response = post_to_step(
        RegistrationSteps.REGISTRATION_DETAILS,
        {"name": "joe", "eori_number": "GB205672212000", "registration_number": "GB123456"},
    )

    assert response.status_code == 200
    assert not response.context["form"].errors
    assert isinstance(response.context["form"], RegisterAddressDetailsUKForm)

    goto_step(RegistrationSteps.ADDRESS_DETAILS)
    response = post_to_step(
        RegistrationSteps.ADDRESS_DETAILS,
        {
            "name": "joe",
            "address_line_1": "xyz",
            "region": "r",
            "city": "c1",
            "postcode": "pc",
            "phone_number": "+441234567890",
            "website": "http://www.notreal.com",
        },
    )
    assert response.status_code == 200

    assert isinstance(response.context["form"], RegistrationConfirmation)

    expected_data = {
        "type": "individual",
        "location": "united_kingdom",
        "name": "joe",
        "eori_number": "GB205672212000",
        "registration_number": "GB123456",
        "site": {
            "name": "joe",
            "address": {"address_line_1": "xyz", "address_line_2": "", "city": "c1", "region": "r", "postcode": "pc"},
        },
        "phone_number": "+441234567890",
        "website": "http://www.notreal.com",
    }

    assert response.context["registration_data"] == expected_data

    assertTemplateUsed(response, "core/registration/confirmation-registration-individual-uk.html")

    soup = BeautifulSoup(response.content, "html.parser")
    name_div = soup.find("div", {"id": "name"})
    assert expected_data["name"] in name_div.text

    eori_div = soup.find("div", {"id": "eori-number"})
    assert expected_data["eori_number"] in eori_div.text

    crn_div = soup.find("div", {"id": "registration-number"})
    assert expected_data["registration_number"] in crn_div.text

    expected_data["user"] = {"email": "foo@example.com"}

    response = post_to_step(RegistrationSteps.REGISTRATION_CONFIRMATION, {})

    assert mock_organisations_post.last_request.json() == expected_data

    assert mock_authenticate_user_post.last_request.json() == {
        "email": "foo@example.com",
        "user_profile": {"first_name": "Foo", "last_name": "Bar"},
    }

    assert response.status_code == 302
    assert response.url == "/register-an-organisation/confirm/?animate=True"


def test_registration_individual_end_to_end_non_uk_based(
    goto_step, post_to_step, mock_organisations_post, mock_authenticate_user_post, mock_get_countries
):
    goto_step(RegistrationSteps.REGISTRATION_TYPE)
    post_to_step(
        RegistrationSteps.REGISTRATION_TYPE,
        {"type": "individual"},
    )
    goto_step(RegistrationSteps.UK_BASED)
    post_to_step(
        RegistrationSteps.UK_BASED,
        {"location": "abroad"},
    )
    goto_step(RegistrationSteps.REGISTRATION_DETAILS)
    post_to_step(
        RegistrationSteps.REGISTRATION_DETAILS,
        {"name": "joe", "eori_number": "GB205672212000", "registration_number": "GB123456"},
    )
    goto_step(RegistrationSteps.ADDRESS_DETAILS)
    response = post_to_step(
        RegistrationSteps.ADDRESS_DETAILS,
        {
            "name": "joe",
            "address": "xyz",
            "country": "US",
            "phone_number": "+441234567890",
            "website": "http://www.notreal.com",
        },
    )

    expected_data = {
        "type": "individual",
        "location": "abroad",
        "name": "joe",
        "eori_number": "GB205672212000",
        "registration_number": "GB123456",
        "site": {"name": "joe", "address": {"address": "xyz", "country": "US"}},
        "phone_number": "+441234567890",
        "website": "http://www.notreal.com",
    }

    assert response.context["registration_data"] == expected_data

    assertTemplateUsed(response, "core/registration/confirmation-registration-individual-abroad.html")

    soup = BeautifulSoup(response.content, "html.parser")
    name_div = soup.find("div", {"id": "name"})
    assert expected_data["name"] in name_div.text

    eori_div = soup.find("div", {"id": "eori-number"})
    assert expected_data["eori_number"] in eori_div.text

    crn_div = soup.find("div", {"id": "registration-number"})
    assert expected_data["registration_number"] in crn_div.text

    response = post_to_step(RegistrationSteps.REGISTRATION_CONFIRMATION, {})

    expected_data["user"] = {"email": "foo@example.com"}

    assert mock_organisations_post.last_request.json() == expected_data

    assert mock_authenticate_user_post.last_request.json() == {
        "email": "foo@example.com",
        "user_profile": {"first_name": "Foo", "last_name": "Bar"},
    }

    assert response.status_code == 302
    assert response.url == "/register-an-organisation/confirm/?animate=True"


def test_registration_commercial_end_to_end(
    goto_step, post_to_step, mock_organisations_post, mock_authenticate_user_post, mock_get_countries
):
    goto_step(RegistrationSteps.REGISTRATION_TYPE)
    post_to_step(
        RegistrationSteps.REGISTRATION_TYPE,
        {"type": "commercial"},
    )
    goto_step(RegistrationSteps.UK_BASED)
    post_to_step(
        RegistrationSteps.UK_BASED,
        {"location": "abroad"},
    )
    goto_step(RegistrationSteps.REGISTRATION_DETAILS)
    response = post_to_step(
        RegistrationSteps.REGISTRATION_DETAILS,
        {
            "name": "joe",
            "eori_number": "GB205672212000",
            "sic_number": "12345",
            "registration_number": "12345678",
            "vat_number": "GB123456789",
        },
    )

    assert response.status_code == 200
    assert not response.context["form"].errors
    assert isinstance(response.context["form"], RegisterAddressDetailsOverseasForm)

    goto_step(RegistrationSteps.ADDRESS_DETAILS)
    response = post_to_step(
        RegistrationSteps.ADDRESS_DETAILS,
        {
            "name": "joe",
            "address": "xyz",
            "country": "TH",
            "phone_number": "+441234567890",
            "website": "http://www.notreal.com",
        },
    )

    expected_data = {
        "type": "commercial",
        "location": "abroad",
        "name": "joe",
        "eori_number": "GB205672212000",
        "sic_number": "12345",
        "registration_number": "12345678",
        "vat_number": "GB123456789",
        "site": {"name": "joe", "address": {"address": "xyz", "country": "TH"}},
        "phone_number": "+441234567890",
        "website": "http://www.notreal.com",
    }

    assert response.context["registration_data"] == expected_data

    assertTemplateUsed(response, "core/registration/confirmation-registration-corporation-abroad.html")

    response = post_to_step(RegistrationSteps.REGISTRATION_CONFIRMATION, {})

    expected_data["user"] = {"email": "foo@example.com"}

    assert mock_organisations_post.last_request.json() == expected_data

    assert mock_authenticate_user_post.last_request.json() == {
        "email": "foo@example.com",
        "user_profile": {"first_name": "Foo", "last_name": "Bar"},
    }

    assert response.status_code == 302
    assert response.url == "/register-an-organisation/confirm/?animate=True"


def test_select_organisation_load(authorized_client, mock_exporter_user_me):
    mock_exporter_user_me["organisations"] = mock_exporter_user_me["organisations"] + [
        {"id": "9bc26604-35ee-4383-9f58-1111111", "name": "Org 2"}
    ]
    url = reverse("core:select_organisation")
    response = authorized_client.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    assert soup.title.string.strip() == "Select your organisation - LITE - GOV.UK"

    assert len(response.context["form"].fields["organisation"].choices) == 2
    assert response.context["form"].fields["organisation"].choices[1] == ("9bc26604-35ee-4383-9f58-1111111", "Org 2")
    assert response.context["back_link_url"] == "/"

    response = authorized_client.get(url + "?back_link=applications")
    assert response.context["back_link_url"] == "/applications/"
    assert response.context["back_link_text"] == "Back to applications"


def test_select_organisation_licenses(authorized_client, mock_get_organisation, mock_exporter_user_me):
    session = authorized_client.session
    session["organisation_name"] = None
    session["organisation"] = None
    session.save()

    mock_exporter_user_me["organisations"] = mock_exporter_user_me["organisations"] + [
        {"id": "9bc26604-35ee-4383-9f58-1111111", "name": "Org 2"}
    ]
    url = reverse("core:select_organisation")
    response = authorized_client.post(url, data={"organisation": mock_exporter_user_me["organisations"][0]["id"]})

    assert response.status_code == 302
    assert response.url == "/"

    response = authorized_client.post(
        url + "?back_link=applications", data={"organisation": mock_exporter_user_me["organisations"][0]["id"]}
    )
    assert response.status_code == 302
    assert response.url == "/applications/"

    assert authorized_client.session["organisation_name"] == mock_exporter_user_me["organisations"][0]["name"]

    response = authorized_client.post(
        url + "?back_link=licences", data={"organisation": mock_exporter_user_me["organisations"][0]["id"]}
    )
    assert response.status_code == 302
    assert response.url == "/licences/"
    session["organisation"] = mock_exporter_user_me["organisations"][0]["id"]
    assert authorized_client.session["organisation_name"] == mock_exporter_user_me["organisations"][0]["name"]

    response = authorized_client.post(
        url + "?back_link=applications&submitted=False",
        data={"organisation": mock_exporter_user_me["organisations"][0]["id"]},
    )
    assert response.status_code == 302
    assert response.url == "/applications/?submitted=False"
