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


def test_case_page_ecju_queries_context(authorized_client, data_standard_case, queue_pk):
    url = reverse("cases:case", kwargs={"queue_pk": queue_pk, "pk": data_standard_case["case"]["id"]})

    response = authorized_client.get(url)

    assert response.status_code == 200

    assert len(response.context["closed_ecju_queries"]) == 2
    assert len(response.context["open_ecju_queries"]) == 3


def test_case_page_renders_ecju_queries_template(authorized_client, data_standard_case, queue_pk):
    url = reverse("cases:case", kwargs={"queue_pk": queue_pk, "pk": data_standard_case["case"]["id"]})

    response = authorized_client.get(url)

    # then it does not error
    assert response.status_code == 200
    assertTemplateUsed("cases/tabs/ecju-queries.html")


def test_case_page_unallocated_user_does_not_see_add_query_button(authorized_client, data_standard_case, queue_pk):
    url = reverse("cases:case", kwargs={"queue_pk": queue_pk, "pk": data_standard_case["case"]["id"]})

    response = authorized_client.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    add_new_query_button = soup.find(id="button-new-query")
    assert add_new_query_button is None


def test_case_page_allocated_user_can_see_add_query_button(
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

    add_new_query_button = soup.find(id="button-new-query")
    assert add_new_query_button is not None
