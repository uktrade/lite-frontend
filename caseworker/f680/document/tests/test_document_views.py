import pytest

from django.urls import reverse
from requests.exceptions import HTTPError

from core import client
from core.constants import CaseStatusEnum
from core.exceptions import ServiceError
from caseworker.f680.outcome.constants import OutcomeType


@pytest.fixture(autouse=True)
def setup(
    mock_queue,
    mock_case,
    settings,
    mock_f680_case_with_assigned_user,
    mock_proviso,
    mock_denial_reasons,
    mock_get_case_recommendations,
):
    settings.FEATURE_FLAG_ALLOW_F680 = True
    return


@pytest.fixture
def f680_approval_template_id():
    return "68a17258-af0f-429e-922d-25945979fa6d"


@pytest.fixture
def f680_refusal_template_id():
    return "98a37258-af0f-429e-922d-259459795a2d"


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
def document_all_url(f680_case_id, data_queue):
    return reverse("cases:f680:document:all", kwargs={"queue_pk": data_queue["id"], "pk": f680_case_id})


@pytest.fixture
def letter_templates_data(f680_approval_template_id, f680_refusal_template_id):
    return [
        {
            "id": f680_approval_template_id,
            "name": "F680 Approval",
            "decisions": [{"name": {"key": OutcomeType.APPROVE}}],
        },
        {"id": f680_refusal_template_id, "name": "F680 Refusal", "decisions": [{"name": {"key": OutcomeType.REFUSE}}]},
    ]


@pytest.fixture
def mock_letter_template_filter(requests_mock, letter_templates_data):
    url = client._build_absolute_uri(f"/caseworker/letter_templates/?case_type=f680_clearance")
    return requests_mock.get(url=url, json={"results": letter_templates_data})


@pytest.fixture
def mock_letter_template_approval_only(requests_mock, letter_templates_data):
    url = client._build_absolute_uri(f"/caseworker/letter_templates/?case_type=f680_clearance")
    return requests_mock.get(url=url, json={"results": letter_templates_data[1:]})

@pytest.fixture
def mock_letter_template_refusal_only(requests_mock, letter_templates_data):
    url = client._build_absolute_uri(f"/caseworker/letter_templates/?case_type=f680_clearance")
    return requests_mock.get(url=url, json={"results": [letter_templates_data[1]]})


class TestF680GenerateDocument:

    def test_GET_template_does_not_exist(
        self,
        authorized_client,
        generate_document_url,
        mock_preview_f680_letter_missing_template,
        mock_outcomes_approve_refuse,
        mock_letter_template_filter,
    ):
        response = authorized_client.get(generate_document_url)
        assert response.status_code == 403

    def test_GET_success(
        self,
        authorized_client,
        generate_document_url,
        mock_preview_f680_letter,
        data_preview_response,
        mock_f680_case_under_final_review,
        mock_outcomes_approve_refuse,
        mock_letter_template_filter,
    ):
        response = authorized_client.get(generate_document_url)
        assert response.status_code == 200
        assert response.context["preview"] == data_preview_response["preview"]

    def test_GET_success_approval_not_allowed(
        self,
        authorized_client,
        generate_document_url,
        mock_preview_f680_letter,
        data_preview_response,
        mock_f680_case_under_final_review,
        mock_outcomes_complete_refusal,
        mock_letter_template_refusal_only,
    ):
        response = authorized_client.get(generate_document_url)
        assert response.status_code == 404

    def test_POST_preview_success(
        self,
        authorized_client,
        generate_document_url,
        mock_preview_f680_letter_with_customisation,
        data_preview_response_with_customisation_text,
        mock_f680_case_under_final_review,
        mock_outcomes_approve_refuse,
        mock_letter_template_filter,
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
        mock_f680_case_under_final_review,
        mock_outcomes_approve_refuse,
        mock_letter_template_filter,
    ):
        response = authorized_client.post(generate_document_url, {"generate": "", "text": customisation_text})
        assert response.status_code == 302
        assert response.url == reverse(
            "cases:f680:document:all", kwargs={"queue_pk": data_queue["id"], "pk": f680_case_id}
        )
        assert mock_generate_f680_letter.call_count == 1
        assert mock_generate_f680_letter.last_request.json() == {
            "addressee": None,
            "advice_type": "approve",
            "template": f680_approval_template_id,
            "text": customisation_text,
            "visible_to_exporter": False,
        }

    def test_POST_preview_api_error(
        self,
        authorized_client,
        generate_document_url,
        data_submitted_f680_case,
        mock_preview_f680_letter_api_error,
        mock_outcomes_complete,
        customisation_text,
        mock_letter_template_filter,
    ):
        data_submitted_f680_case["case"]["data"]["status"]["key"] = CaseStatusEnum.UNDER_FINAL_REVIEW
        with pytest.raises(ServiceError):
            authorized_client.get(generate_document_url, {"preview": "", "text": customisation_text})
        assert mock_preview_f680_letter_api_error.call_count == 1

    def test_POST_generate_api_error(
        self,
        authorized_client,
        generate_document_url,
        data_submitted_f680_case,
        mock_generate_f680_letter_api_error,
        data_queue,
        f680_case_id,
        mock_outcomes_complete,
        customisation_text,
        f680_approval_template_id,
        mock_letter_template_filter,
    ):
        data_submitted_f680_case["case"]["data"]["status"]["key"] = CaseStatusEnum.UNDER_FINAL_REVIEW
        with pytest.raises(ServiceError):
            response = authorized_client.post(generate_document_url, {"generate": "", "text": customisation_text})
        assert mock_generate_f680_letter_api_error.call_count == 1


@pytest.fixture
def data_finalise_response(f680_case_id):
    return {"case": f680_case_id, "licence": ""}


@pytest.fixture
def mock_finalise_success(f680_case_id, requests_mock, data_finalise_response):
    return requests_mock.put(
        client._build_absolute_uri(f"/cases/{f680_case_id}/finalise/"),
        json=data_finalise_response,
        status_code=201,
    )


@pytest.fixture
def mock_finalise_api_error(f680_case_id, requests_mock):
    return requests_mock.put(
        client._build_absolute_uri(f"/cases/{f680_case_id}/finalise/"),
        json={"error": "error"},
        status_code=500,
    )


class TestAllDocumentsView:

    def test_GET_success(
        self,
        authorized_client,
        data_queue,
        mock_f680_case_under_final_review,
        mock_outcomes_approve_refuse,
        f680_case_id,
        f680_reference_code,
        data_submitted_f680_case,
        mock_letter_template_filter,
        letter_templates_data,
    ):
        url = reverse("cases:f680:document:all", kwargs={"queue_pk": data_queue["id"], "pk": f680_case_id})
        response = authorized_client.get(url)
        assert response.status_code == 200
        assert dict(response.context["case"]) == data_submitted_f680_case["case"]
        assert response.context["letter_templates"] == [
            {
                "id": "68a17258-af0f-429e-922d-25945979fa6d",
                "name": "F680 Approval",
                "decisions": [{"name": {"key": OutcomeType.APPROVE}}],
            },
            {
                "id": "98a37258-af0f-429e-922d-259459795a2d",
                "name": "F680 Refusal",
                "decisions": [{"name": {"key": OutcomeType.REFUSE}}],
            },
        ]

    def test_GET_no_case_404(self, authorized_client, data_queue, missing_case_id, mock_missing_case):
        url = reverse("cases:f680:document:all", kwargs={"queue_pk": data_queue["id"], "pk": missing_case_id})
        with pytest.raises(HTTPError, match="404"):
            authorized_client.get(url)

    def test_GET_letter_gen_no_allowed(
        self,
        authorized_client,
        data_queue,
        mock_f680_case_under_final_review,
        mock_outcomes_no_outcome,
        f680_case_id,
        f680_reference_code,
        data_submitted_f680_case,
        mock_letter_template_filter,
        letter_templates_data,
        document_all_url,
    ):

        response = authorized_client.get(document_all_url)
        assert response.status_code == 403

    def test_POST_finalise_success(
        self,
        authorized_client,
        data_queue,
        f680_case_id,
        mock_f680_case_under_review,
        mock_outcomes_approve_refuse,
        mock_letter_template_filter,
        letter_templates_data,
        document_all_url,
        mock_finalise_success,
    ):

        response = authorized_client.post(document_all_url)
        assert response.status_code == 302
        assert response.url == reverse(
            "cases:f680:details",
            kwargs={"queue_pk": data_queue["id"], "pk": f680_case_id},
        )
        assert mock_finalise_success.call_count == 1

    def test_POST_finalise_api_error(
        self,
        authorized_client,
        data_queue,
        f680_case_id,
        mock_f680_case_under_review,
        mock_outcomes_approve_refuse,
        mock_letter_template_filter,
        letter_templates_data,
        document_all_url,
        mock_finalise_api_error,
    ):

        with pytest.raises(ServiceError):
            response = authorized_client.post(document_all_url)
        assert mock_finalise_api_error.call_count == 1
