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
    mock_f680_proviso,
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
def mock_preview_f680_letter(
    f680_case_id,
    f680_approval_template_id,
    requests_mock,
    data_preview_response,
):
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
def mock_preview_f680_letter_api_error(
    f680_case_id,
    f680_approval_template_id,
    requests_mock,
    data_preview_response,
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
def generate_approval_document_url(f680_case_id, f680_approval_template_id, data_queue):
    url = reverse(
        "cases:f680:document:generate",
        kwargs={"queue_pk": data_queue["id"], "pk": f680_case_id, "template_id": f680_approval_template_id},
    )
    return url


@pytest.fixture
def generate_refusal_document_url(f680_case_id, f680_refusal_template_id, data_queue):
    url = reverse(
        "cases:f680:document:generate",
        kwargs={"queue_pk": data_queue["id"], "pk": f680_case_id, "template_id": f680_refusal_template_id},
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
    return requests_mock.get(url=url, json=letter_templates_data)


@pytest.fixture
def mock_letter_template_approval_only(requests_mock, letter_templates_data):
    url = client._build_absolute_uri(f"/caseworker/letter_templates/?case_type=f680_clearance")
    return requests_mock.get(url=url, json=[letter_templates_data[0]])


@pytest.fixture
def mock_letter_template_refusal_only(requests_mock, letter_templates_data):
    url = client._build_absolute_uri(f"/caseworker/letter_templates/?case_type=f680_clearance")
    return requests_mock.get(url=url, json=letter_templates_data[1:])


@pytest.fixture
def outcome_documents_data(f680_approval_template_id, f680_refusal_template_id):
    return [
        {
            "id": "20cc5252-acb9-491f-9d6e-d2050f93540b",
            "template": f680_approval_template_id,
            "name": "F680-Approval.pdf",
            "visible_to_exporter": False,
        },
        {
            "id": "b2318ff0-6071-4f10-9d64-0713e7846c97",
            "template": f680_refusal_template_id,
            "name": "F680-Refusal.pdf",
            "visible_to_exporter": False,
        },
    ]


@pytest.fixture
def mock_get_outcome_documents(requests_mock, f680_case_id, outcome_documents_data):
    url = client._build_absolute_uri(f"/caseworker/f680/{f680_case_id}/outcome_document/")
    return requests_mock.get(url=url, json=outcome_documents_data)


@pytest.fixture
def mock_get_outcome_documents_approval(requests_mock, f680_case_id, outcome_documents_data):
    url = client._build_absolute_uri(f"/caseworker/f680/{f680_case_id}/outcome_document/")
    return requests_mock.get(url=url, json=outcome_documents_data[:1])


@pytest.fixture
def mock_get_outcome_refusal(requests_mock, f680_case_id, outcome_documents_data):
    url = client._build_absolute_uri(f"/caseworker/f680/{f680_case_id}/outcome_document/")
    return requests_mock.get(url=url, json=outcome_documents_data[-1])


class TestF680GenerateDocument:

    def test_GET_template_does_not_exist(
        self,
        authorized_client,
        generate_approval_document_url,
        mock_preview_f680_letter_missing_template,
        mock_outcomes_approve_refuse,
        mock_letter_template_filter,
    ):
        response = authorized_client.get(generate_approval_document_url)
        assert response.status_code == 403

    def test_GET_success(
        self,
        authorized_client,
        generate_approval_document_url,
        mock_preview_f680_letter,
        data_preview_response,
        data_queue,
        f680_case_id,
        mock_f680_case_under_final_review,
        mock_outcomes_approve_refuse,
        mock_letter_template_filter,
    ):
        response = authorized_client.get(generate_approval_document_url)
        assert response.status_code == 200
        assert response.context["preview"] == data_preview_response["preview"]

        assert response.context["form"].cancel_url == reverse(
            "cases:f680:document:all", kwargs={"queue_pk": data_queue["id"], "pk": f680_case_id}
        )

    def test_GET_success_approval_not_allowed(
        self,
        authorized_client,
        generate_approval_document_url,
        mock_preview_f680_letter,
        data_preview_response,
        mock_f680_case_under_final_review,
        mock_outcomes_complete_refusal,
        mock_letter_template_refusal_only,
    ):
        response = authorized_client.get(generate_approval_document_url)
        assert response.status_code == 404

    def test_POST_generate_approval_success(
        self,
        authorized_client,
        generate_approval_document_url,
        mock_generate_f680_letter,
        data_queue,
        f680_case_id,
        f680_approval_template_id,
        mock_f680_case_under_final_review,
        mock_outcomes_approve_refuse,
        mock_letter_template_filter,
    ):
        response = authorized_client.post(generate_approval_document_url)
        assert response.status_code == 302
        assert response.url == reverse(
            "cases:f680:document:all", kwargs={"queue_pk": data_queue["id"], "pk": f680_case_id}
        )
        assert mock_generate_f680_letter.call_count == 1
        assert mock_generate_f680_letter.last_request.json() == {
            "addressee": None,
            "advice_type": "approve",
            "template": f680_approval_template_id,
            "visible_to_exporter": False,
        }

    def test_POST_generate_refusal_success(
        self,
        authorized_client,
        generate_refusal_document_url,
        mock_generate_f680_letter,
        data_queue,
        f680_case_id,
        f680_refusal_template_id,
        mock_f680_case_under_final_review,
        mock_outcomes_approve_refuse,
        mock_letter_template_filter,
    ):
        response = authorized_client.post(generate_refusal_document_url)
        assert response.status_code == 302
        assert response.url == reverse(
            "cases:f680:document:all", kwargs={"queue_pk": data_queue["id"], "pk": f680_case_id}
        )
        assert mock_generate_f680_letter.call_count == 1
        assert mock_generate_f680_letter.last_request.json() == {
            "addressee": None,
            "advice_type": "refuse",
            "template": f680_refusal_template_id,
            "visible_to_exporter": False,
        }

    def test_POST_generate_api_error(
        self,
        authorized_client,
        generate_approval_document_url,
        data_submitted_f680_case,
        mock_generate_f680_letter_api_error,
        data_queue,
        f680_case_id,
        mock_outcomes_complete,
        f680_approval_template_id,
        mock_letter_template_filter,
    ):
        data_submitted_f680_case["case"]["data"]["status"]["key"] = CaseStatusEnum.UNDER_FINAL_REVIEW
        with pytest.raises(ServiceError):
            response = authorized_client.post(generate_approval_document_url)
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
        mock_get_outcome_documents,
    ):
        url = reverse("cases:f680:document:all", kwargs={"queue_pk": data_queue["id"], "pk": f680_case_id})
        response = authorized_client.get(url)
        assert response.status_code == 200
        assert dict(response.context["case"]) == data_submitted_f680_case["case"]
        assert response.context["required_outcome_documents"] == [
            {
                "id": "68a17258-af0f-429e-922d-25945979fa6d",
                "name": "F680 Approval",
                "decisions": [{"name": {"key": OutcomeType.APPROVE}}],
                "generated_document": {
                    "id": "20cc5252-acb9-491f-9d6e-d2050f93540b",
                    "template": "68a17258-af0f-429e-922d-25945979fa6d",
                    "name": "F680-Approval.pdf",
                    "visible_to_exporter": False,
                },
            },
            {
                "id": "98a37258-af0f-429e-922d-259459795a2d",
                "name": "F680 Refusal",
                "decisions": [{"name": {"key": OutcomeType.REFUSE}}],
                "generated_document": {
                    "id": "b2318ff0-6071-4f10-9d64-0713e7846c97",
                    "template": "98a37258-af0f-429e-922d-259459795a2d",
                    "name": "F680-Refusal.pdf",
                    "visible_to_exporter": False,
                },
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
        mock_f680_case_under_final_review,
        mock_outcomes_approve_refuse,
        mock_letter_template_filter,
        letter_templates_data,
        document_all_url,
        mock_finalise_success,
        mock_get_outcome_documents,
    ):

        response = authorized_client.post(document_all_url)
        assert response.status_code == 302
        assert response.url == reverse(
            "cases:f680:details",
            kwargs={"queue_pk": data_queue["id"], "pk": f680_case_id},
        )
        assert mock_finalise_success.call_count == 1

    def test_POST_finalise_docs_not_completed(
        self,
        authorized_client,
        data_queue,
        f680_case_id,
        mock_f680_case_under_final_review,
        mock_outcomes_approve_refuse,
        mock_letter_template_filter,
        letter_templates_data,
        document_all_url,
        mock_finalise_success,
        mock_get_outcome_documents_approval,
    ):

        response = authorized_client.post(document_all_url)
        assert response.status_code == 200
        assert response.context["form"].errors["__all__"] == [
            "Click generate for all letters. Finalise and publish to exporter can only be done once all letters have been generated."
        ]
        assert mock_finalise_success.call_count == 0

    def test_POST_finalise_api_error(
        self,
        authorized_client,
        data_queue,
        f680_case_id,
        mock_f680_case_under_final_review,
        mock_outcomes_approve_refuse,
        mock_letter_template_filter,
        letter_templates_data,
        document_all_url,
        mock_finalise_api_error,
        mock_get_outcome_documents,
    ):

        with pytest.raises(ServiceError):
            response = authorized_client.post(document_all_url)
        assert mock_finalise_api_error.call_count == 1

    @pytest.mark.parametrize(
        "update_data, expected_values, expected_hrefs",
        (
            [
                {"visible_to_exporter": False},
                ["F680 Approval", "Generated", "Regenerate"],
                [
                    "documents/20cc5252-acb9-491f-9d6e-d2050f93540b/",
                    "f680/document/68a17258-af0f-429e-922d-25945979fa6d/generate/",
                ],
            ],
            [
                {"visible_to_exporter": True},
                ["F680 Approval", "Sent", ""],
                ["documents/20cc5252-acb9-491f-9d6e-d2050f93540b/"],
            ],
            [
                {"template": "12345"},
                ["F680 Approval", "Ready", "Generate"],
                ["f680/document/68a17258-af0f-429e-922d-25945979fa6d/generate/"],
            ],
        ),
    )
    def test_GET_document_table(
        self,
        authorized_client,
        requests_mock,
        data_queue,
        mock_f680_case_under_final_review,
        mock_outcomes_approve_refuse,
        f680_case_id,
        f680_reference_code,
        data_submitted_f680_case,
        mock_letter_template_approval_only,
        beautiful_soup,
        update_data,
        expected_values,
        expected_hrefs,
        outcome_documents_data,
    ):
        post_document_url = f"/caseworker/f680/{f680_case_id}/outcome_document/"
        approval_data = outcome_documents_data[:1]
        approval_data[0].update(update_data)

        requests_mock.get(url=post_document_url, json=approval_data, status_code=200)

        url = reverse("cases:f680:document:all", kwargs={"queue_pk": data_queue["id"], "pk": f680_case_id})
        response = authorized_client.get(url)

        assert response.status_code == 200

        soup = beautiful_soup(response.content)
        table = soup.find(id="table-final-documents")
        hrefs = [a["href"].split(f"/cases/{f680_case_id}/")[1] for a in table.find_all("a")]

        assert [td.text.strip() for td in table.find_all("td")] == expected_values
        assert hrefs == expected_hrefs
