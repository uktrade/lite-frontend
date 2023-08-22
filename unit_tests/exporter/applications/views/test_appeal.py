import pytest

from bs4 import BeautifulSoup
from pytest_django.asserts import assertContains, assertTemplateUsed

from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse

from core import client

from exporter.applications.forms.appeal import AppealForm


@pytest.fixture(autouse=True)
def feature_switch(settings):
    settings.FEATURE_FLAG_APPEALS = True


@pytest.fixture
def invalid_application_pk():
    return "82617c05-a050-428b-ae68-ed5dc985f4af"


@pytest.fixture
def application_pk(data_standard_case):
    return data_standard_case["case"]["id"]


@pytest.fixture(autouse=True)
def mock_get_application(requests_mock, application_pk, data_standard_case):
    requests_mock.get(
        client._build_absolute_uri(f"/applications/{application_pk}/"),
        json=data_standard_case["case"],
    )


@pytest.fixture(autouse=True)
def mock_get_application_invalid_pk(requests_mock, invalid_application_pk):
    requests_mock.get(
        client._build_absolute_uri(f"/applications/{invalid_application_pk}/"),
        json={},
        status_code=404,
    )


@pytest.fixture
def post_appeal_api_url(application_pk):
    return client._build_absolute_uri(f"/applications/{application_pk}/appeal/")


@pytest.fixture
def appeal_pk():
    return "c7e010b4-6c0c-4640-9a68-5bdee38c47d1"


@pytest.fixture
def mock_post_appeal(requests_mock, post_appeal_api_url, appeal_pk):
    return requests_mock.post(
        post_appeal_api_url,
        json={"id": appeal_pk},
        status_code=201,
    )


@pytest.fixture
def mock_post_appeal_failure(requests_mock, post_appeal_api_url):
    return requests_mock.post(
        post_appeal_api_url,
        json={},
        status_code=500,
    )


@pytest.fixture
def post_appeal_document_api_url(appeal_pk):
    return client._build_absolute_uri(f"/appeals/{appeal_pk}/documents/")


@pytest.fixture
def mock_post_appeal_document(requests_mock, post_appeal_document_api_url):
    return requests_mock.post(
        post_appeal_document_api_url,
        json={},
        status_code=201,
    )


@pytest.fixture
def mock_post_appeal_document_failure(requests_mock, post_appeal_document_api_url):
    return requests_mock.post(
        post_appeal_document_api_url,
        json={},
        status_code=500,
    )


@pytest.fixture
def application_url(application_pk):
    return reverse("applications:application", kwargs={"pk": application_pk})


@pytest.fixture
def appeal_url(application_pk):
    return reverse("applications:appeal", kwargs={"case_pk": application_pk})


def test_appeal_view_feature_flag_off(authorized_client, appeal_url, settings):
    settings.FEATURE_FLAG_APPEALS = False

    response = authorized_client.get(appeal_url)
    assert response.status_code == 404


def test_appeal_view_invalid_application_id(authorized_client, invalid_application_pk):
    url = reverse("applications:appeal", kwargs={"case_pk": invalid_application_pk})
    response = authorized_client.get(url)

    assert response.status_code == 404


def test_appeal_view(authorized_client, appeal_url, application_url):
    response = authorized_client.get(appeal_url)

    assert response.status_code == 200

    assert isinstance(response.context["form"], AppealForm)
    assertTemplateUsed(response, "core/form.html")

    soup = BeautifulSoup(response.content, "html.parser")
    assert soup.find("h1").string == "Appeal refusal decision"
    assert soup.title.string.strip() == "Appeal refusal decision - LITE - GOV.UK"
    assert soup.find("a", {"id": "back-link"})["href"] == application_url
    assert soup.find("input", {"id": "submit-id-submit"})["value"] == "Submit appeal request"
    assert soup.find("a", {"id": "cancel-id-cancel"})["href"] == application_url
    assert soup.find("textarea", {"name": "grounds_for_appeal"})


def test_post_appeal(authorized_client, appeal_url, application_url, mock_post_appeal):
    response = authorized_client.post(
        appeal_url,
        data={"grounds_for_appeal": "These are my grounds for appeal"},
    )

    assert response.status_code == 302
    assert response.url == application_url
    assert mock_post_appeal.called_once
    assert mock_post_appeal.last_request.json() == {"grounds_for_appeal": "These are my grounds for appeal"}


def test_post_appeal_with_files(
    authorized_client,
    appeal_url,
    application_url,
    mock_post_appeal,
    mock_post_appeal_document,
):
    response = authorized_client.post(
        appeal_url,
        data={
            "grounds_for_appeal": "These are my grounds for appeal",
            "documents": [
                SimpleUploadedFile("file 1", b"File 1 contents"),
                SimpleUploadedFile("file 2", b"File 2 contents"),
            ],
        },
    )

    assert response.status_code == 302
    assert response.url == application_url

    assert mock_post_appeal.called_once
    assert mock_post_appeal.last_request.json() == {"grounds_for_appeal": "These are my grounds for appeal"}

    assert mock_post_appeal_document.call_count == 2
    assert mock_post_appeal_document.request_history[0].json() == {"name": "file 1", "s3_key": "file 1", "size": 0}
    assert mock_post_appeal_document.request_history[1].json() == {"name": "file 2", "s3_key": "file 2", "size": 0}


def test_post_appeal_failure(authorized_client, appeal_url, mock_post_appeal_failure):
    response = authorized_client.post(
        appeal_url,
        data={"grounds_for_appeal": "These are my grounds for 4appeal"},
    )

    assertContains(response, "Unexpected error creating appeal")


def test_post_appeal_with_files_failure(
    authorized_client,
    appeal_url,
    mock_post_appeal,
    mock_post_appeal_document_failure,
):
    response = authorized_client.post(
        appeal_url,
        data={
            "grounds_for_appeal": "These are my grounds for appeal",
            "documents": [
                SimpleUploadedFile("file 1", b"File 1 contents"),
                SimpleUploadedFile("file 2", b"File 2 contents"),
            ],
        },
    )

    assertContains(response, "Unexpected error creating appeal document")
