import pytest
from urllib.parse import urljoin

from django.test import Client
from django.urls import reverse

from exporter.core.organisation.constants import RegistrationSteps
from exporter.core.organisation.forms import (
    RegistrationUKBasedForm,
    RegisterDetailsForm,
    RegisterAddressDetailsForm,
)


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
def mock_organisations_post(requests_mock, mock_exporter_user_me):
    return_value = {
        "id": mock_exporter_user_me["organisations"][0]["id"],
        "name": mock_exporter_user_me["organisations"][0]["name"],
    }
    return requests_mock.post(url="/organisations/", json=return_value, status_code=201)


@pytest.fixture
def mock_edit_organisation(requests_mock, mock_exporter_user_me):
    organisations_id = mock_exporter_user_me["organisations"][0]["id"]
    return requests_mock.put(url=f"/organisations/{organisations_id}/update/", json={}, status_code=200)


@pytest.fixture(autouse=True)
def mock_sso_userinfo(requests_mock, mock_exporter_user):
    return requests_mock.get(
        url="https://oidc.integration.account.gov.uk/userinfo", json={"email": "foo@example.com"}, status_code=200
    )


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
    assert isinstance(response.context["form"], RegisterDetailsForm)


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
    assert isinstance(response.context["form"], RegisterAddressDetailsForm)


def test_registration_individual_end_to_end_uk_based(
    goto_step, post_to_step, mock_organisations_post, mock_authenticate_user_post
):

    goto_step(RegistrationSteps.REGISTRATION_TYPE)
    response = post_to_step(
        RegistrationSteps.REGISTRATION_TYPE,
        {"type": "individual"},
    )

    assert response.status_code == 200
    assert not response.context["form"].errors
    assert isinstance(response.context["form"], RegistrationUKBasedForm)

    goto_step(RegistrationSteps.UK_BASED)
    response = post_to_step(
        RegistrationSteps.UK_BASED,
        {"location": "united_kingdom"},
    )

    assert response.status_code == 200
    assert not response.context["form"].errors
    assert isinstance(response.context["form"], RegisterDetailsForm)

    goto_step(RegistrationSteps.REGISTRATION_DETAILS)
    response = post_to_step(
        RegistrationSteps.REGISTRATION_DETAILS,
        {"name": "joe", "eori_number": "GB205672212000", "vat_number": "GB123456789"},
    )

    assert response.status_code == 200
    assert not response.context["form"].errors
    assert isinstance(response.context["form"], RegisterAddressDetailsForm)

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

    assert mock_organisations_post.last_request.json() == {
        "type": "individual",
        "location": "united_kingdom",
        "name": "joe",
        "eori_number": "GB205672212000",
        "vat_number": "GB123456789",
        "site": {
            "name": "joe",
            "address": {"address_line_1": "xyz", "address_line_2": "", "city": "c1", "region": "r", "postcode": "pc"},
        },
        "phone_number": "+441234567890",
        "status": "draft",
        "website": "http://www.notreal.com",
        "user": {"email": "foo@example.com"},
    }

    assert mock_authenticate_user_post.last_request.json() == {
        "email": "foo@example.com",
        "user_profile": {"first_name": "Foo", "last_name": "Bar"},
    }

    assert response.status_code == 302
    assert response.url == reverse("core:register_draft_confirm")


def test_registration_individual_end_to_end_non_uk_based(
    goto_step, post_to_step, mock_organisations_post, mock_authenticate_user_post
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
        {"name": "joe", "eori_number": "GB205672212000", "vat_number": "GB123456789"},
    )
    goto_step(RegistrationSteps.ADDRESS_DETAILS)
    response = post_to_step(
        RegistrationSteps.ADDRESS_DETAILS,
        {
            "name": "joe",
            "address": "xyz",
            "country": "usa",
            "phone_number": "+441234567890",
            "website": "http://www.notreal.com",
        },
    )

    assert mock_organisations_post.last_request.json() == {
        "type": "individual",
        "location": "abroad",
        "name": "joe",
        "eori_number": "GB205672212000",
        "vat_number": "GB123456789",
        "site": {"name": "joe", "address": {"address": "xyz", "country": "US"}},
        "phone_number": "+441234567890",
        "website": "http://www.notreal.com",
        "status": "draft",
        "user": {"email": "foo@example.com"},
    }
    assert mock_authenticate_user_post.last_request.json() == {
        "email": "foo@example.com",
        "user_profile": {"first_name": "Foo", "last_name": "Bar"},
    }

    assert response.status_code == 302
    assert response.url == reverse("core:register_draft_confirm")


def test_registration_commercial_end_to_end(
    goto_step, post_to_step, mock_organisations_post, mock_authenticate_user_post
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
    assert isinstance(response.context["form"], RegisterAddressDetailsForm)

    goto_step(RegistrationSteps.ADDRESS_DETAILS)
    response = post_to_step(
        RegistrationSteps.ADDRESS_DETAILS,
        {
            "name": "joe",
            "address": "xyz",
            "country": "usa",
            "phone_number": "+441234567890",
            "website": "http://www.notreal.com",
        },
    )

    assert mock_organisations_post.last_request.json() == {
        "type": "commercial",
        "location": "abroad",
        "name": "joe",
        "eori_number": "GB205672212000",
        "sic_number": "12345",
        "registration_number": "12345678",
        "vat_number": "GB123456789",
        "site": {"name": "joe", "address": {"address": "xyz", "country": "US"}},
        "phone_number": "+441234567890",
        "website": "http://www.notreal.com",
        "status": "draft",
        "user": {"email": "foo@example.com"},
    }
    assert mock_authenticate_user_post.last_request.json() == {
        "email": "foo@example.com",
        "user_profile": {"first_name": "Foo", "last_name": "Bar"},
    }

    assert response.status_code == 302
    assert response.url == reverse("core:register_draft_confirm")


def test_select_organisation_load(authorized_client, mock_exporter_user_me):

    mock_exporter_user_me["organisations"] = mock_exporter_user_me["organisations"] + [
        {"id": "9bc26604-35ee-4383-9f58-1111111", "name": "Org 2"}
    ]
    url = reverse("core:select_organisation")
    response = authorized_client.get(url)

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


@pytest.mark.parametrize(
    "data, field_name, post_data",
    (
        (
            {"name": "test"},
            "name",
            {"name": "test"},
        ),
        (
            {"eori_number": "GB205672212000"},
            "eori_number",
            {"eori_number": "GB205672212000"},
        ),
        (
            {"vat_number": "GB123456789"},
            "vat_number",
            {"vat_number": "GB123456789"},
        ),
        (
            {"sic_number": "12345"},
            "sic_number",
            {"sic_number": "12345"},
        ),
        (
            {"registration_number": "12345678"},
            "registration_number",
            {"registration_number": "12345678"},
        ),
        (
            {"address": "address 0"},
            "address",
            {"site": {"address": {"address": "address 0", "country": {"id": "usa"}}}},
        ),
        (
            {"address_line_1": "55 lite av"},
            "address_line_1",
            {"site": {"address": {"address_line_1": "55 lite av"}}},
        ),
        (
            {"address_line_2": ""},
            "address_line_2",
            {"site": {"address": {"address_line_2": ""}}},
        ),
        (
            {"city": "lite town"},
            "city",
            {"site": {"address": {"city": "lite town"}}},
        ),
        (
            {"region": "lite region"},
            "region",
            {"site": {"address": {"region": "lite region"}}},
        ),
        (
            {"postcode": "LR1 8GG"},
            "postcode",
            {"site": {"address": {"postcode": "LR1 8GG"}}},
        ),
        (
            {"phone_number": "+441234567890"},
            "phone_number",
            {"phone_number": "+441234567890"},
        ),
        (
            {"website": "http://www.notreal.com"},
            "website",
            {"website": "http://www.notreal.com"},
        ),
        (
            {"country": "UK"},
            "country",
            {"site": {"address": {"country": "UK"}}},
        ),
    ),
)
def test_edit_registration_views(data, field_name, post_data, authorized_client, mock_edit_organisation):
    url = reverse(f"core:register_draft_edit", kwargs={"field": field_name})
    response = authorized_client.post(url, data=data)
    assert response.status_code == 302

    assert mock_edit_organisation.last_request.json() == post_data
    assert response.url == reverse("core:register_draft_confirm")
