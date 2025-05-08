import pytest
import uuid

from http import HTTPStatus

from django.urls import reverse

from exporter.applications.constants import ExportLicenceSteps
from exporter.applications.forms.common import (
    ApplicationNameForm,
    LicenceTypeForm,
    ToldByAnOfficialForm,
)


@pytest.fixture(autouse=True)
def default_settings(settings):
    settings.FEATURE_FLAG_INDETERMINATE_EXPORT_LICENCE_TYPE_ALLOWED_ORGANISATIONS = []


@pytest.fixture()
def apply_for_a_licence_start_url():
    return reverse("apply_for_a_licence:start")


@pytest.fixture()
def apply_for_an_export_licence_url():
    return reverse("applications:apply")


@pytest.fixture()
def post_to_step(post_to_step_factory, apply_for_an_export_licence_url):
    return post_to_step_factory(apply_for_an_export_licence_url)


@pytest.fixture()
def application_id():
    return str(uuid.uuid4())


@pytest.fixture()
def mock_post_export_licence_application(requests_mock, api_url, application_id):
    return requests_mock.post(
        api_url("/exporter/export-licences/application/"),
        json={"id": application_id},
        status_code=HTTPStatus.CREATED,
    )


@pytest.fixture()
def mock_post_export_licence_application_error(requests_mock, api_url, application_id):
    return requests_mock.post(
        api_url("/exporter/export-licences/application/"),
        json={"id": application_id},
        status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
    )


def test_POST_apply_for_a_licence_redirects(
    authorized_client,
    apply_for_a_licence_start_url,
):
    response = authorized_client.post(apply_for_a_licence_start_url, data={"licence_type": "export_licence"})
    assert response.status_code == 302
    assert response.url == reverse("applications:apply")


def test_create_application_success(
    authorized_client,
    apply_for_an_export_licence_url,
    post_to_step,
    mock_post_export_licence_application,
    application_id,
):
    response = authorized_client.get(apply_for_an_export_licence_url)
    assert response.status_code == 200
    assert isinstance(response.context["form"], LicenceTypeForm)

    response = post_to_step(
        ExportLicenceSteps.LICENCE_TYPE,
        {
            "licence_type": "siel",
        },
    )
    assert response.status_code == 200
    assert isinstance(response.context["form"], ApplicationNameForm)

    response = post_to_step(
        ExportLicenceSteps.APPLICATION_NAME,
        {
            "name": "Application Name",
        },
    )
    assert response.status_code == 200
    assert isinstance(response.context["form"], ToldByAnOfficialForm)

    response = post_to_step(
        ExportLicenceSteps.TOLD_BY_AN_OFFICIAL,
        {
            "have_you_been_informed": "yes",
            "reference_number_on_information_form": "CRE/2020/1234567",
        },
    )
    assert response.status_code == 302
    assert response.url == reverse("applications:task_list", kwargs={"pk": application_id})
    assert mock_post_export_licence_application.last_request.json() == {
        "licence_type": "siel",
        "export_type": "permanent",
        "have_you_been_informed": "yes",
        "name": "Application Name",
        "reference_number_on_information_form": "CRE/2020/1234567",
    }


def test_create_application_failure(
    authorized_client,
    apply_for_an_export_licence_url,
    post_to_step,
    beautiful_soup,
    mock_post_export_licence_application_error,
):
    response = authorized_client.get(apply_for_an_export_licence_url)
    assert response.status_code == 200
    assert isinstance(response.context["form"], LicenceTypeForm)

    response = post_to_step(
        ExportLicenceSteps.LICENCE_TYPE,
        {
            "licence_type": "siel",
        },
    )
    assert response.status_code == 200
    assert isinstance(response.context["form"], ApplicationNameForm)

    response = post_to_step(
        ExportLicenceSteps.APPLICATION_NAME,
        {
            "name": "Application Name",
        },
    )
    assert response.status_code == 200
    assert isinstance(response.context["form"], ToldByAnOfficialForm)

    response = post_to_step(
        ExportLicenceSteps.TOLD_BY_AN_OFFICIAL,
        {
            "have_you_been_informed": "yes",
            "reference_number_on_information_form": "CRE/2020/1234567",
        },
    )
    assert response.status_code == 200
    soup = beautiful_soup(response.content)
    assert "Unexpected error creating export licence application" in soup.text


def test_create_application_success_with_indeterminate_export_licence_type(
    authorized_client,
    apply_for_an_export_licence_url,
    post_to_step,
    mock_post_export_licence_application,
    application_id,
    settings,
    user_organisation_id,
):
    settings.FEATURE_FLAG_INDETERMINATE_EXPORT_LICENCE_TYPE_ALLOWED_ORGANISATIONS = [user_organisation_id]

    response = authorized_client.get(apply_for_an_export_licence_url)
    assert response.status_code == 200
    assert isinstance(response.context["form"], ApplicationNameForm)

    response = post_to_step(
        ExportLicenceSteps.APPLICATION_NAME,
        {
            "name": "Application Name",
        },
    )
    assert response.status_code == 200
    assert isinstance(response.context["form"], ToldByAnOfficialForm)

    response = post_to_step(
        ExportLicenceSteps.TOLD_BY_AN_OFFICIAL,
        {
            "have_you_been_informed": "yes",
            "reference_number_on_information_form": "CRE/2020/1234567",
        },
    )
    assert response.status_code == 302
    assert response.url == reverse("applications:task_list", kwargs={"pk": application_id})
    assert mock_post_export_licence_application.last_request.json() == {
        "export_type": "permanent",
        "have_you_been_informed": "yes",
        "name": "Application Name",
        "reference_number_on_information_form": "CRE/2020/1234567",
    }
