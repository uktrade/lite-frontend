import pytest

from django.urls import reverse

from bs4 import BeautifulSoup
from pytest_django.asserts import assertTemplateUsed


@pytest.fixture(autouse=True)
def setup(
    mock_case,
    mock_queue,
    mock_standard_case_ecju_queries,
    mock_standard_case_assigned_queues,
    mock_standard_case_documents,
    mock_standard_case_additional_contacts,
    mock_standard_case_activity_filters,
):
    yield


def test_case_page_renders_documents_template(authorized_client, data_standard_case, queue_pk):
    url = reverse("cases:case", kwargs={"queue_pk": queue_pk, "pk": data_standard_case["case"]["id"]})

    response = authorized_client.get(url)

    # then it does not error
    assert response.status_code == 200
    assertTemplateUsed("cases/tabs/documents.html")


def test_case_page_unallocated_user_does_not_see_document_actions(authorized_client, data_standard_case, queue_pk):
    url = reverse("cases:case", kwargs={"queue_pk": queue_pk, "pk": data_standard_case["case"]["id"]})

    response = authorized_client.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    attach_document_button = soup.find(id="button-attach-document")
    assert attach_document_button is None

    generate_document_button = soup.find(id="button-generate-document")
    assert generate_document_button is None


def test_case_page_allocated_user_can_see_document_actions(
    authorized_client,
    data_standard_case,
    queue_pk,
    mock_gov_user,
    assign_user_to_case,
):
    assign_user_to_case(mock_gov_user, data_standard_case)

    url = reverse("cases:case", kwargs={"queue_pk": queue_pk, "pk": data_standard_case["case"]["id"]})

    response = authorized_client.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    attach_document_button = soup.find(id="button-attach-document")
    assert attach_document_button is not None

    generate_document_button = soup.find(id="button-generate-document")
    assert generate_document_button is not None
