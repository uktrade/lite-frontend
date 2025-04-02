import pytest

from django.urls import reverse
from requests.exceptions import HTTPError

from core import client
from core.exceptions import ServiceError


@pytest.fixture(autouse=True)
def setup(
    mock_queue,
    mock_case,
    settings,
    mock_f680_case_with_assigned_user,
    mock_proviso,
):
    settings.FEATURE_FLAG_ALLOW_F680 = True
    return


@pytest.fixture
def f680_approval_template_id():
    return "68a17258-af0f-429e-922d-25945979fa6d"


@pytest.fixture
def customisation_text():
    return "my customisation"


@pytest.fixture
def mock_preview_f680_letter_missing_template(f680_case_id, f680_approval_template_id, requests_mock):
    get_params = "&".join(
        [
            f"pk={f680_case_id}",
            f"template={f680_approval_template_id}",
        ]
    )
    return requests_mock.get(
        client._build_absolute_uri(f"/cases/{f680_case_id}/generated-documents/preview/?{get_params}"),
        json={"errors": {"letter_template": "Letter template not found"}},
        status_code=404,
    )


@pytest.fixture
def data_preview_response():
    return {"preview": "my big f680 preview!"}


@pytest.fixture
def data_preview_response_with_customisation_text(customisation_text):
    return {"preview": f"my big f680 preview! {customisation_text}"}


@pytest.fixture
def mock_preview_f680_letter(f680_case_id, f680_approval_template_id, requests_mock, data_preview_response):
    get_params = "&".join(
        [
            f"pk={f680_case_id}",
            f"template={f680_approval_template_id}",
        ]
    )
    return requests_mock.get(
        client._build_absolute_uri(f"/cases/{f680_case_id}/generated-documents/preview/?{get_params}"),
        json=data_preview_response,
        status_code=200,
    )


@pytest.fixture
def mock_preview_f680_letter_with_customisation(
    f680_case_id,
    f680_approval_template_id,
    requests_mock,
    data_preview_response_with_customisation_text,
    customisation_text,
):
    get_params = "&".join(
        [
            f"pk={f680_case_id}",
            f"template={f680_approval_template_id}",
            f"text={customisation_text}",
        ]
    )
    return requests_mock.get(
        client._build_absolute_uri(f"/cases/{f680_case_id}/generated-documents/preview/?{get_params}"),
        json=data_preview_response_with_customisation_text,
        status_code=200,
    )


@pytest.fixture
def mock_preview_f680_letter_api_error(
    f680_case_id,
    f680_approval_template_id,
    requests_mock,
    data_preview_response_with_customisation_text,
    customisation_text,
):
    get_params = "&".join(
        [
            f"pk={f680_case_id}",
            f"template={f680_approval_template_id}",
            f"text={customisation_text}",
        ]
    )
    return requests_mock.get(
        client._build_absolute_uri(f"/cases/{f680_case_id}/generated-documents/preview/?{get_params}"),
        json={"error": "some error"},
        status_code=500,
    )


@pytest.fixture
def mock_generate_f680_letter(f680_case_id, requests_mock, data_preview_response):
    return requests_mock.post(
        client._build_absolute_uri(f"/cases/{f680_case_id}/generated-documents/"),
        json=data_preview_response,
        status_code=201,
    )


@pytest.fixture
def mock_generate_f680_letter_api_error(f680_case_id, requests_mock, data_preview_response):
    return requests_mock.post(
        client._build_absolute_uri(f"/cases/{f680_case_id}/generated-documents/"),
        json={"error": "some error"},
        status_code=500,
    )


@pytest.fixture
def generate_document_url(f680_case_id, f680_approval_template_id, data_queue):
    url = reverse(
        "cases:f680:document:generate",
        kwargs={"queue_pk": data_queue["id"], "pk": f680_case_id, "template_id": f680_approval_template_id},
    )
    return url


@pytest.fixture
def mock_letter_template_filter(requests_mock, f680_approval_template_id):
    url = client._build_absolute_uri(f"/caseworker/letter_templates/?case_type=f680_clearance&decision=approve")
    data = {"results": [{"id": f680_approval_template_id, "name": "F680 Approval", "decisions": []}]}
    return requests_mock.get(url=url, json=data)


class TestF680GenerateDocument:

    def test_GET_template_does_not_exist(
        self, authorized_client, generate_document_url, mock_preview_f680_letter_missing_template
    ):
        response = authorized_client.get(generate_document_url)
        assert response.status_code == 404

    def test_GET_success(
        self, authorized_client, generate_document_url, mock_preview_f680_letter, data_preview_response
    ):
        response = authorized_client.get(generate_document_url)
        assert response.status_code == 200
        assert response.context["preview"] == data_preview_response["preview"]

    def test_POST_preview_success(
        self,
        authorized_client,
        generate_document_url,
        mock_preview_f680_letter_with_customisation,
        data_preview_response_with_customisation_text,
        customisation_text,
    ):
        response = authorized_client.post(generate_document_url, {"preview": "", "text": customisation_text})
        assert response.status_code == 200
        assert response.context["preview"] == data_preview_response_with_customisation_text["preview"]
        assert mock_preview_f680_letter_with_customisation.call_count == 1

    def test_POST_generate_success(
        self,
        authorized_client,
        generate_document_url,
        mock_generate_f680_letter,
        data_queue,
        f680_case_id,
        customisation_text,
        f680_approval_template_id,
    ):
        response = authorized_client.post(generate_document_url, {"generate": "", "text": customisation_text})
        assert response.status_code == 302
        assert response.url == reverse("cases:f680:details", kwargs={"queue_pk": data_queue["id"], "pk": f680_case_id})
        assert mock_generate_f680_letter.call_count == 1
        assert mock_generate_f680_letter.last_request.json() == {
            "addressee": None,
            "template": f680_approval_template_id,
            "text": customisation_text,
            "visible_to_exporter": False,
        }

    def test_POST_preview_api_error(
        self, authorized_client, generate_document_url, mock_preview_f680_letter_api_error, customisation_text
    ):
        with pytest.raises(ServiceError):
            response = authorized_client.post(generate_document_url, {"preview": "", "text": customisation_text})
        assert mock_preview_f680_letter_api_error.call_count == 1

    def test_POST_generate_api_error(
        self,
        authorized_client,
        generate_document_url,
        mock_generate_f680_letter_api_error,
        data_queue,
        f680_case_id,
        customisation_text,
        f680_approval_template_id,
    ):
        with pytest.raises(ServiceError):
            response = authorized_client.post(generate_document_url, {"generate": "", "text": customisation_text})
        assert mock_generate_f680_letter_api_error.call_count == 1


class TestAllDocumentsView:

    def test_GET_success(
        self,
        authorized_client,
        data_queue,
        mock_f680_case,
        f680_case_id,
        f680_reference_code,
        data_submitted_f680_case,
        mock_letter_template_filter,
    ):
        url = reverse("cases:f680:document:all", kwargs={"queue_pk": data_queue["id"], "pk": f680_case_id})
        response = authorized_client.get(url)
        assert response.status_code == 200
        assert dict(response.context["case"]) == data_submitted_f680_case["case"]

    def test_GET_no_case_404(self, authorized_client, data_queue, missing_case_id, mock_missing_case):
        url = reverse("cases:f680:document:all", kwargs={"queue_pk": data_queue["id"], "pk": missing_case_id})
        with pytest.raises(HTTPError, match="404"):
            authorized_client.get(url)
