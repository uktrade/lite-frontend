import pytest

from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse

from core import client
from exporter.f680.application_sections.supporting_documents.forms import F680AttachSupportingDocument


@pytest.fixture()
def unset_f680_feature_flag(settings):
    settings.FEATURE_FLAG_ALLOW_F680 = False


@pytest.fixture(autouse=True)
def setup(mock_exporter_user_me, settings):
    settings.FEATURE_FLAG_ALLOW_F680 = True


@pytest.fixture
def missing_application_id():
    return "6bb0828c-1520-4624-b729-7f3e6e5b9f5d"


@pytest.fixture
def application_id(data_f680_case):
    return data_f680_case["id"]


@pytest.fixture
def mock_f680_application_get_404(requests_mock, missing_application_id):
    url = client._build_absolute_uri(f"/exporter/f680/application/{missing_application_id}/")
    return requests_mock.get(url=url, json={}, status_code=404)


@pytest.fixture
def mock_f680_application_get(requests_mock, data_f680_case, application_id):
    data_f680_case["application"]["sections"] = {}
    url = client._build_absolute_uri(f"/exporter/f680/application/{application_id}/")
    return requests_mock.get(url=url, json=data_f680_case)


@pytest.fixture
def document_data(application_id):
    return [
        {
            "id": "a66ebfb3-72c8-4a63-82f6-0519830729ce",  # /PS-IGNORE
            "name": "sample_doc.pdf",
            "s3_key": "sample_doc.pdf",
            "description": "my item",
            "size": 18,
            "safe": True,
            "document_type": None,
            "application": application_id,
        }
    ]


@pytest.fixture
def mock_f680_supporting_documents_get(requests_mock, data_f680_case, application_id, document_data):
    url = client._build_absolute_uri(f"/exporter/applications/{application_id}/document/")
    return requests_mock.get(url=url, json={"results": document_data})


@pytest.fixture
def f680_application_supporting_documents_add_url(data_f680_case):
    return reverse(
        "f680:supporting_documents:add",
        kwargs={"pk": data_f680_case["id"]},
    )


@pytest.fixture
def f680_application_supporting_documents_add_missing_url(missing_application_id):
    return reverse(
        "f680:supporting_documents:add",
        kwargs={"pk": missing_application_id},
    )


@pytest.fixture
def f680_application_supporting_documents_attach_url(data_f680_case):
    return reverse(
        "f680:supporting_documents:attach",
        kwargs={"pk": data_f680_case["id"]},
    )


@pytest.fixture
def f680_application_supporting_documents_attach_missing_url(missing_application_id):
    return reverse(
        "f680:supporting_documents:attach",
        kwargs={"pk": missing_application_id},
    )


class TestSupportingDocumentsView:

    def test_GET_no_application_404(
        self,
        authorized_client,
        f680_application_supporting_documents_add_missing_url,
        mock_f680_supporting_documents_get,
        mock_f680_application_get_404,
    ):
        response = authorized_client.get(f680_application_supporting_documents_add_missing_url)
        assert response.status_code == 404

    def test_GET_success(
        self,
        authorized_client,
        mock_f680_application_get,
        mock_f680_supporting_documents_get,
        f680_application_supporting_documents_add_url,
        beautiful_soup,
        application_id,
        document_data,
    ):
        response = authorized_client.get(f680_application_supporting_documents_add_url)
        document_id = document_data[0]["id"]

        assert response.status_code == 200
        assert response.context["back_link_url"] == reverse("f680:summary", kwargs={"pk": application_id})

        soup = beautiful_soup(response.content)
        header = soup.find("h1", {"class": "govuk-heading-l"})
        table = soup.find("table", {"id": "table-supporting-documents"})
        download_link = table.find("a", {"class": "govuk-link"})["href"]
        assert [th.text for th in table.find_all("th")] == ["Name", "Description", "Action"]
        assert [td.text.strip() for td in table.find_all("td")] == ["sample_doc.pdf", "my item", ""]

        assert header.text == "Supporting Documents"
        assert download_link == f"/applications/{application_id}/additional-document/{document_id}/download"

    def test_GET_no_feature_flag_forbidden(
        self,
        authorized_client,
        mock_f680_application_get,
        mock_f680_supporting_documents_get,
        f680_application_supporting_documents_add_url,
        unset_f680_feature_flag,
    ):
        response = authorized_client.get(f680_application_supporting_documents_add_url)
        assert response.status_code == 200

        assert response.context["title"] == "Forbidden"


class TestSupportingDocumentsAttachView:

    def test_GET_no_application_404(
        self,
        authorized_client,
        f680_application_supporting_documents_add_missing_url,
        mock_f680_supporting_documents_get,
        mock_f680_application_get_404,
    ):
        response = authorized_client.get(f680_application_supporting_documents_add_missing_url)
        assert response.status_code == 404

    def test_GET_success(
        self,
        authorized_client,
        mock_f680_application_get,
        mock_f680_supporting_documents_get,
        f680_application_supporting_documents_attach_url,
    ):
        response = authorized_client.get(f680_application_supporting_documents_attach_url)
        assert response.status_code == 200
        assert isinstance(response.context["form"], F680AttachSupportingDocument)

    def test_GET_no_feature_flag_forbidden(
        self,
        authorized_client,
        mock_f680_application_get,
        mock_f680_supporting_documents_get,
        f680_application_supporting_documents_attach_url,
        unset_f680_feature_flag,
    ):
        response = authorized_client.get(f680_application_supporting_documents_attach_url)
        assert response.status_code == 200
        assert response.context["title"] == "Forbidden"

    def test_POST_add_file_no_file(
        self,
        authorized_client,
        mock_f680_application_get,
        mock_f680_supporting_documents_get,
        f680_application_supporting_documents_attach_url,
        beautiful_soup,
    ):
        data = {}
        response = authorized_client.post(f680_application_supporting_documents_attach_url, data)
        assert response.status_code == 200
        soup = beautiful_soup(response.content)
        error = soup.find("ul", {"class": "govuk-list govuk-error-summary__list"}).li.text
        assert error == "Select a supporting document"

    def test_POST_add_file_success(
        self,
        authorized_client,
        mock_f680_application_get,
        mock_f680_supporting_documents_get,
        f680_application_supporting_documents_attach_url,
        requests_mock,
        application_id,
        document_data,
    ):

        post_document_url = f"/exporter/applications/{application_id}/document/"

        requests_mock.post(url=post_document_url, json={}, status_code=201)
        requests_mock.patch(f"/exporter/f680/application/{application_id}/", json={}, status_code=200)

        data = {
            "file": SimpleUploadedFile("file 1", b"File 1 contents"),
            "description": "my desc",
        }
        response = authorized_client.post(f680_application_supporting_documents_attach_url, data)
        assert response.status_code == 302
        assert response.url == reverse(
            "f680:supporting_documents:add",
            kwargs={"pk": application_id},
        )

        request_1 = requests_mock.request_history.pop()
        request_2 = requests_mock.request_history.pop()
        request_3 = requests_mock.request_history.pop()

        assert request_1.method == "PATCH"

        assert request_1.json()["application"]["sections"]["supporting_documents"] == {
            "label": "Supporting Documents",
            "items": [
                {
                    "id": document_data[0]["id"],
                    "fields": {
                        "file": {
                            "key": "file",
                            "answer": document_data[0]["name"],
                            "raw_answer": document_data[0]["name"],
                            "question": "file",
                            "datatype": "string",
                        },
                        "description": {
                            "key": "description",
                            "answer": document_data[0]["description"],
                            "raw_answer": document_data[0]["description"],
                            "question": "description",
                            "datatype": "string",
                        },
                    },
                    "fields_sequence": ["file", "description"],
                }
            ],
            "type": "multiple",
        }

        assert request_2.method == "GET"

        assert request_3.method == "POST"
        assert request_3.json() == {
            "name": "file 1",
            "s3_key": "file 1",
            "size": 0,
            "description": "my desc",
            "application": application_id,
        }

    def test_POST_add_file_success_no_previous_document_section(
        self,
        authorized_client,
        data_f680_case,
        mock_f680_supporting_documents_get,
        f680_application_supporting_documents_attach_url,
        requests_mock,
        application_id,
        document_data,
    ):

        requests_mock.get(url=f"/exporter/f680/application/{application_id}/", json=data_f680_case)

        post_document_url = f"/exporter/applications/{application_id}/document/"

        requests_mock.post(url=post_document_url, json={}, status_code=201)
        requests_mock.patch(f"/exporter/f680/application/{application_id}/", json={}, status_code=200)

        data = {
            "file": SimpleUploadedFile("file 1", b"File 1 contents"),
            "description": "my desc",
        }
        response = authorized_client.post(f680_application_supporting_documents_attach_url, data)
        assert response.status_code == 302
        assert response.url == reverse(
            "f680:supporting_documents:add",
            kwargs={"pk": application_id},
        )
