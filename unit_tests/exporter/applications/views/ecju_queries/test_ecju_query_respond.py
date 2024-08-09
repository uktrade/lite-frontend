import pytest

from django.urls import reverse
from bs4 import BeautifulSoup

from core import client
from exporter.ecju_queries.ecju_forms import ECJUQueryRespondForm


@pytest.fixture
def data_standard_case_pk(data_standard_case):
    return data_standard_case["case"]["id"]


@pytest.fixture
def data_ecju_query_pk(data_ecju_queries):
    return data_ecju_queries["ecju_queries"][0]["id"]


@pytest.fixture
def url(data_standard_case_pk, data_ecju_query_pk):
    return reverse(
        "ecju_queries:respond_to_application_query",
        kwargs={
            "case_pk": data_standard_case_pk,
            "query_pk": data_ecju_query_pk,
        },
    )


@pytest.fixture
def confirm_url(data_standard_case_pk, data_ecju_query_pk):
    return reverse(
        "ecju_queries:respond_to_application_query_confirm",
        kwargs={
            "case_pk": data_standard_case_pk,
            "query_pk": data_ecju_query_pk,
        },
    )


@pytest.fixture(autouse=True)
def mock_ecju_query(data_standard_case, data_ecju_queries, requests_mock):

    data = {"ecju_query": data_ecju_queries["ecju_queries"][0]}
    requests_mock.get(
        url=f"/cases/{data_standard_case['case']['id']}/ecju-queries/{data_ecju_queries['ecju_queries'][0]['id']}/",
        json=data,
    )
    yield data


@pytest.fixture
def mock_put_ecju_query(requests_mock, data_standard_case, data_ecju_queries):
    url = client._build_absolute_uri(
        f"/cases/{data_standard_case['case']['id']}/ecju-queries/{data_ecju_queries['ecju_queries'][0]['id']}/"
    )
    yield requests_mock.put(url=url, json={})


@pytest.fixture(autouse=True)
def mock_ecju_query_get_document(data_standard_case, data_ecju_queries, requests_mock):
    data = {
        "documents": [
            {
                "id": "fa7fe703-a976-4b8f-8683-8676c1f5fe0a",  # /PS-IGNORE
                "name": "sample.pdf",
                "user": {"first_name": "Joe", "last_name": "bloggs"},
                "description": "test sample",
            }
        ]
    }
    requests_mock.get(
        url=f"/cases/{data_standard_case['case']['id']}/ecju-queries/{data_ecju_queries['ecju_queries'][0]['id']}/document/",
        json=data,
    )
    yield data


def test_ecju_form(data_standard_case, data_ecju_queries):

    ecju_respond_form = ECJUQueryRespondForm(
        ecju_query=data_ecju_queries["ecju_queries"][0],
        case_id=data_standard_case["case"]["id"],
        ecju_response="Test Response",
        documents={},
        data={},
        edit_url=None,
    )

    assert ecju_respond_form.fields["response"].initial is "Test Response"
    assert ecju_respond_form.is_valid() == True


def test_ecju_respond_query_view_not_editable(authorized_client, mock_application_get, data_standard_case, url):
    response = authorized_client.get(url)
    assert response.status_code == 200

    assert response.context["form"]["response"].initial is None
    assert response.context["back_link_url"] == f'/applications/{data_standard_case["case"]["id"]}/ecju-queries/'
    assert response.context["back_link_text"] == "back to ecju queries"

    soup = BeautifulSoup(response.content, "html.parser")
    document_details = soup.find(class_="app-documents__item-details")
    assert document_details.find(class_="govuk-link--no-visited-state").text == "sample.pdf"
    assert "Uploaded by Joe bloggs" in document_details.find(class_="govuk-hint").text
    edit_link = soup.find(class_="application-edit-link")
    assert edit_link == None


def test_ecju_respond_query_view_editable(
    authorized_client, mock_application_get, mock_status_properties_can_invoke_major_editable, data_standard_case, url
):
    response = authorized_client.get(url)
    assert response.status_code == 200

    soup = BeautifulSoup(response.content, "html.parser")
    edit_link = soup.find(class_="application-edit-link")
    assert edit_link.text == "Edit and submit your application"
    assert reverse(f"applications:edit_type", kwargs={"pk": data_standard_case["case"]["id"]}) == edit_link["href"]


# TODO: After amend by copy is switched on, ensure this test is merged with the above
def test_ecju_respond_query_view_editable_amend_by_copy_feature(
    settings,
    authorized_client,
    mock_application_get,
    mock_status_properties_can_invoke_major_editable,
    data_organisation,
    data_standard_case,
    url,
):
    settings.FEATURE_AMENDMENT_BY_COPY_EXPORTER_IDS = [data_organisation["id"]]
    response = authorized_client.get(url)
    assert response.status_code == 200

    soup = BeautifulSoup(response.content, "html.parser")
    edit_link = soup.find(class_="application-edit-link")
    assert edit_link.text == "Edit and submit your application"
    assert (
        reverse(f"applications:major_edit_confirm", kwargs={"pk": data_standard_case["case"]["id"]})
        == edit_link["href"]
    )


def test_ecju_respond_query_view_add_document(
    authorized_client, mock_application_get, data_standard_case_pk, data_ecju_query_pk, url
):
    data = {"response": "session response", "add_document": ""}
    response_session_key = f"{data_ecju_query_pk}_response"
    response = authorized_client.post(url, data)

    assert authorized_client.session[response_session_key] == "session response"
    assert response.status_code == 302
    assert (
        response.url
        == f"/ecju-queries/{data_ecju_query_pk}/application/{data_standard_case_pk}/case/{data_standard_case_pk}/add-document/"
    )

    # Check form response is retained from session
    response = authorized_client.get(url)
    assert response.context["form"]["response"].initial == "session response"
    assert response_session_key in authorized_client.session.keys()


def test_ecju_respond_query_view_post_sucess(
    authorized_client, mock_application_get, data_standard_case_pk, data_ecju_query_pk, confirm_url, url
):
    data = {"response": "session response"}
    response_session_key = f"{data_ecju_query_pk}_response"

    response = authorized_client.post(url, data)
    assert authorized_client.session[response_session_key] == "session response"
    assert response.status_code == 302
    assert response.url == confirm_url

    # Check form response is retained from session
    response = authorized_client.get(url)
    assert response.context["form"]["response"].initial == "session response"
    assert response_session_key in authorized_client.session.keys()


def test_ecju_respond_query_view_delete_document(
    authorized_client,
    mock_application_get,
    data_standard_case_pk,
    data_ecju_query_pk,
    mock_ecju_query_get_document,
    url,
):
    document_id = mock_ecju_query_get_document["documents"][0]["id"]
    response_session_key = f"{data_ecju_query_pk}_response"

    data = {"response": "session response", "delete_document": document_id}
    response = authorized_client.post(url, data)
    assert authorized_client.session[response_session_key] == "session response"

    assert response.status_code == 302

    assert (
        response.url
        == f"/ecju-queries/{data_ecju_query_pk}/application/{data_standard_case_pk}/case/{data_standard_case_pk}/document/{document_id}/delete/"
    )
    # Check form response is retained from session

    response = authorized_client.get(url)
    assert response.context["form"]["response"].initial == "session response"
    assert response_session_key in authorized_client.session.keys()


def test_ecju_respond_query_view_cancel(
    authorized_client, mock_application_get, data_standard_case_pk, data_ecju_query_pk, url
):

    data = {"response": "session response", "cancel": ""}
    response_session_key = f"{data_ecju_query_pk}_response"

    session = authorized_client.session
    session[response_session_key] = "session response"
    session.save()

    response = authorized_client.post(url, data)

    assert response.status_code == 302

    assert response.url == f"/applications/{data_standard_case_pk}/ecju-queries/"
    # Check form response has been removed from session

    response = authorized_client.get(url)
    assert response.context["form"]["response"].initial is None
    assert response_session_key not in authorized_client.session.keys()


def test_ecju_respond_query_confirm_view(authorized_client, confirm_url, url):
    response = authorized_client.get(confirm_url)

    assert response.status_code == 200

    assert response.context["back_link_url"] == url
    assert response.context["back_link_text"] == "back to edit response"


def test_ecju_respond_query_confirm_view_cancel(
    authorized_client, mock_application_get, data_standard_case_pk, confirm_url, data_ecju_query_pk, url
):

    data = {"cancel": ""}
    response_session_key = f"{data_ecju_query_pk}_response"

    session = authorized_client.session
    session[response_session_key] = "session response"
    session.save()

    response = authorized_client.post(confirm_url, data)
    assert response.status_code == 302
    assert response.url == f"/applications/{data_standard_case_pk}/ecju-queries/"

    # Check form response has been removed from session

    response = authorized_client.get(url)
    assert response.context["form"]["response"].initial is None
    assert response_session_key not in authorized_client.session.keys()


def test_ecju_respond_query_confirm_view_save_response(
    authorized_client, mock_application_get, data_standard_case_pk, confirm_url, data_ecju_query_pk, mock_put_ecju_query
):
    response_session_key = f"{data_ecju_query_pk}_response"

    session = authorized_client.session
    session[response_session_key] = "session response"
    session.save()
    response = authorized_client.post(confirm_url, {})

    assert response.status_code == 302
    assert response.url == f"/applications/{data_standard_case_pk}/ecju-queries/"
    assert response_session_key not in authorized_client.session.keys()
    assert mock_put_ecju_query.called

    assert mock_put_ecju_query.last_request.json() == {"response": "session response"}


def test_ecju_respond_query_confirm_view_save_with_no_response(
    authorized_client, mock_application_get, data_standard_case_pk, confirm_url, mock_put_ecju_query
):

    response = authorized_client.post(confirm_url, {})

    assert response.status_code == 302
    assert response.url == f"/applications/{data_standard_case_pk}/ecju-queries/"
    assert mock_put_ecju_query.called
    assert mock_put_ecju_query.last_request.json() == {}
