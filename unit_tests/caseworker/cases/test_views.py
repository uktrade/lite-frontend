import pytest
import re
import uuid

from bs4 import BeautifulSoup

from pytest_django.asserts import (
    assertTemplateNotUsed,
    assertTemplateUsed,
)

from django.urls import reverse

from core import client

from unit_tests.helpers import merge_summaries

from core.exceptions import ServiceError


approve = {"key": "approve", "value": "Approve"}
proviso = {"key": "proviso", "value": "Proviso"}
refuse = {"key": "refuse", "value": "Refuse"}
conflicting = {"key": "conflicting", "value": "Conflicting"}

john_smith = {
    "email": "john.smith@example.com",
    "first_name": "John",
    "id": "63c74ddd-c119-48cc-8696-d196218ca583",
    "last_name": "Smith",
    "role_name": "Super User",
    "status": "Active",
    "team": {"id": "136cbb1f-390b-4f78-bfca-86300edec300", "name": "team1", "part_of_ecju": None},
}


@pytest.fixture(autouse=True)
def setup(
    mock_queue,
    mock_case_activity_system_user,
    mock_case,
    mock_control_list_entries,
    mock_regime_entries,
    mock_application_search,
    mock_good_on_appplication,
    mock_good_on_appplication_documents,
    mock_standard_case_activity_filters,
    mock_standard_case_activity_system_user,
    mock_standard_case_ecju_queries,
    mock_standard_case_assigned_queues,
    mock_standard_case_documents,
    mock_standard_case_additional_contacts,
):
    yield


def test_case_audit_trail_system_user(authorized_client, data_standard_case, queue_pk):
    # given the case has activity from system user
    url = reverse("cases:case", kwargs={"queue_pk": queue_pk, "pk": data_standard_case["case"]["id"]})

    # when the case is viewed
    response = authorized_client.get(url)

    # then it does not error
    assert response.status_code == 200


denials_data = [
    {
        "id": "00000000-0000-0000-0000-000000000001",
        "address": "726 example road",
        "country": "Germany",
        "end_use": 'For the needs of "example company"',
        "item_description": "example something",
        "item_list_codes": "FR3a",
        "name": "Example Name",
        "notifying_government": "Lithuania",
        "reference": "abc123/abc123",
        "regime_reg_ref": "ABC-1234",
        "entity_type": "End-user",
    }
]


def build_wizard_step_data(view_name, step_name, data):
    step_data = {f"{view_name}-current_step": step_name}
    step_data.update({f"{step_name}-{key}": value for key, value in data.items()})
    return step_data


def test_good_on_application_detail(
    authorized_client,
    queue_pk,
    standard_case_pk,
    good_on_application_pk,
    data_good_on_application,
    data_standard_case,
):
    # given I access good on application details for a good with control list entries and a part number
    url = reverse(
        "cases:good", kwargs={"queue_pk": queue_pk, "pk": standard_case_pk, "good_pk": good_on_application_pk}
    )
    response = authorized_client.get(url)

    assert response.status_code == 200

    # and the view exposes the data that the template needs
    assert response.context_data["good_on_application"] == data_good_on_application
    assert response.context_data["case"] == data_standard_case["case"]
    assert response.context_data["product_summary"] == None
    assertTemplateUsed(response, "case/product-on-case.html")
    assertTemplateNotUsed(response, "case/includes/_product-on-case-summary.html")
    assertTemplateUsed(response, "case/includes/_legacy-product-on-case-summary.html")


def test_good_on_application_firearm_detail(
    authorized_client,
    queue_pk,
    standard_case_pk,
    data_standard_case,
    mock_firearm_good_on_application,
    mock_firearm_good_on_application_documents,
    standard_firearm_expected_product_summary,
    standard_firearm_expected_product_on_application_summary,
):
    # given I access good on application details for a good with control list entries and a part number
    good = data_standard_case["case"]["data"]["goods"][0]
    url = reverse("cases:good", kwargs={"queue_pk": queue_pk, "pk": standard_case_pk, "good_pk": good["id"]})
    response = authorized_client.get(url)

    assert response.status_code == 200

    # and the view exposes the data that the template needs
    assert response.context_data["good_on_application"] == good
    assert response.context_data["case"] == data_standard_case["case"]
    expected_product_summary = merge_summaries(
        standard_firearm_expected_product_summary,
        standard_firearm_expected_product_on_application_summary,
    )
    expected_product_summary = merge_summaries(
        expected_product_summary,
        (
            (
                "product-document",
                '<a class="govuk-link govuk-link--no-visited-state" '
                f'href="/queues/00000000-0000-0000-0000-000000000001/cases/{data_standard_case["case"]["id"]}/documents/6c48a2cc-1ed9-49a5-8ca7-df8af5fc2335/" '
                'target="_blank">data_sheet.pdf</a>',
                "Upload a document that shows what your product is designed to do",
            ),
        ),
    )

    assert response.context_data["product_summary"] == expected_product_summary
    assertTemplateUsed(response, "case/product-on-case.html")
    assertTemplateUsed(response, "case/includes/_product-on-case-summary.html")
    assertTemplateNotUsed(response, "case/includes/_legacy-product-on-case-summary.html")


def test_good_on_application_firearm_detail_non_firearm_type(
    authorized_client,
    queue_pk,
    standard_case_pk,
    data_standard_case,
    mock_firearm_good_on_application,
    mock_firearm_good_on_application_documents,
    standard_firearm_expected_product_summary,
    standard_firearm_expected_product_on_application_summary,
):
    # given I access good on application details for a good with control list entries and a part number
    good = data_standard_case["case"]["data"]["goods"][0]
    good["firearm_details"] = None
    url = reverse("cases:good", kwargs={"queue_pk": queue_pk, "pk": standard_case_pk, "good_pk": good["id"]})
    response = authorized_client.get(url)

    assert response.status_code == 200

    # and the view exposes the data that the template needs
    assert response.context_data["good_on_application"] == good
    assert response.context_data["case"] == data_standard_case["case"]
    assert response.context_data["product_summary"] is None
    assertTemplateUsed(response, "case/product-on-case.html")
    assertTemplateNotUsed(response, "case/includes/_product-on-case-summary.html")
    assertTemplateUsed(response, "case/includes/_legacy-product-on-case-summary.html")


def test_good_on_application_detail_no_part_number(
    authorized_client,
    mock_application_search,
    queue_pk,
    standard_case_pk,
    good_on_application_pk,
    data_good_on_application,
):
    # given I access good on application details for a good with control list entries but no part number
    data_good_on_application["good"]["part_number"] = ""
    url = reverse(
        "cases:good", kwargs={"queue_pk": queue_pk, "pk": standard_case_pk, "good_pk": good_on_application_pk}
    )
    response = authorized_client.get(url)

    assert response.status_code == 200


def test_good_on_application_detail_no_part_number_no_control_list_entries(
    authorized_client,
    mock_application_search,
    queue_pk,
    standard_case_pk,
    good_on_application_pk,
    data_good_on_application,
):
    # given I access good on application details for a good with neither part number of control list entries
    data_good_on_application["good"]["part_number"] = ""
    data_good_on_application["control_list_entries"] = []
    data_good_on_application["good"]["control_list_entries"] = []
    url = reverse(
        "cases:good", kwargs={"queue_pk": queue_pk, "pk": standard_case_pk, "good_pk": good_on_application_pk}
    )
    response = authorized_client.get(url)

    assert response.status_code == 200


def test_good_on_application_detail_not_rated_at_application_level(
    authorized_client,
    mock_application_search,
    queue_pk,
    standard_case_pk,
    good_on_application_pk,
    data_good_on_application,
):
    # given I access good on application details for a good that has not been rated at application level
    data_good_on_application["control_list_entries"] = []
    data_good_on_application["good"]["part_number"] = ""
    data_good_on_application["good"]["control_list_entries"] = ({"rating": "ML1", "text": "Smooth-bore..."},)
    url = reverse(
        "cases:good", kwargs={"queue_pk": queue_pk, "pk": standard_case_pk, "good_pk": good_on_application_pk}
    )
    response = authorized_client.get(url)

    assert response.status_code == 200


def test_search_denials(authorized_client, data_standard_case, requests_mock, queue_pk, standard_case_pk):
    end_user_id = data_standard_case["case"]["data"]["end_user"]["id"]
    end_user_name = data_standard_case["case"]["data"]["end_user"]["name"]
    end_user_address = data_standard_case["case"]["data"]["end_user"]["address"]

    requests_mock.get(
        client._build_absolute_uri(
            f"/external-data/denial-search/?search=name:{end_user_name}&search=address:{end_user_address}"
        ),
        json={"count": "26", "total_pages": "2", "results": denials_data * 26},
    )

    url = reverse("cases:denials", kwargs={"pk": standard_case_pk, "queue_pk": queue_pk})

    response = authorized_client.get(f"{url}?end_user={end_user_id}")

    soup = BeautifulSoup(response.content, "html.parser")
    table = soup.find(id="table-denials")
    assert table
    v = {
        "id": "00000000-0000-0000-0000-000000000001",
        "address": "726 example road",
        "country": "Germany",
        "end_use": 'For the needs of "example company"',
        "item_description": "example something",
        "item_list_codes": "FR3a",
        "name": "Example Name",
        "notifying_government": "Lithuania",
        "reference": "abc123/abc123",
        "regime_reg_ref": "ABC-1234",
        "entity_type": "End-user",
    }

    # first tr is headers second onward are data
    row = table.find_all("tr")
    headers = row[0].find_all("th")

    # assert headers
    header_order = [
        "\n",
        "Reference",
        "Regime reference",
        "Name",
        "Address",
        "Country",
        "Item list codes",
        "Item description",
        "End use",
        "Entity type",
    ]
    header_values = [header.text for header in headers]
    assert header_values == header_order

    # get each column, see that it has data present
    table_body = row[1].find_all("td")[1:]
    table_body_values = [table_values.text.strip("\n") for table_values in table_body]
    # maintains order of the table values
    data_key_map = [
        "reference",
        "regime_reg_ref",
        "name",
        "address",
        "country",
        "item_list_codes",
        "item_description",
        "end_use",
        "entity_type",
    ]
    for i, value in enumerate(table_body_values):
        assert value == denials_data[0][data_key_map[i]]

    page_2 = soup.find(id="page-2")
    assert page_2.a["href"] == f"/queues/{queue_pk}/cases/{standard_case_pk}/denials/?end_user={end_user_id}&page=2"


def test_search_denials_no_matches(authorized_client, requests_mock, queue_pk, standard_case_pk):
    requests_mock.get(
        client._build_absolute_uri(f"/external-data/denial-search/"),
    )
    url = reverse("cases:denials", kwargs={"pk": standard_case_pk, "queue_pk": queue_pk})
    response = authorized_client.get(f"{url}")

    soup = BeautifulSoup(response.content, "html.parser")
    assert response.status_code == 200
    assert "No matching denials" in soup.get_text()


def test_good_on_application_detail_clc_entries(
    authorized_client,
    mock_application_search,
    queue_pk,
    standard_case_pk,
    good_on_application_pk,
    data_search,
    data_good_on_application,
    data_standard_case,
):
    """
    Test that ensures correct Control list entries are displayed in Product detail page
    Control list entries are in two places in GoodOnApplication instance and before a good
    is reviewed they could be different.
    if is_good_controlled is None, then it is not yet reviewed by the Case officer so we
    display the entries from the good.
    if is_good_controlled is not None (either Yes or No) then it means the good is reviewed
    and the Case officer applied the correct CLC entry so display from good_on_application
    """
    data_good_on_application["audit_trail"] = []
    # given I access good on application details for a good with control list entries and a part number
    url = reverse(
        "cases:good", kwargs={"queue_pk": queue_pk, "pk": standard_case_pk, "good_pk": good_on_application_pk}
    )

    response = authorized_client.get(url)
    assert response.status_code == 200
    soup = BeautifulSoup(response.content.decode("utf-8"), "html.parser")
    clc_entries = soup.find(id="control-list-entries-value").text
    clc_entries = "".join(line.strip() for line in clc_entries.split("\n"))
    assert clc_entries == "ML1,ML2"

    data_good_on_application["is_good_controlled"] = None
    data_good_on_application["control_list_entries"] = []
    # given I access good on application details for a good with control list entries and a part number
    url = reverse(
        "cases:good", kwargs={"queue_pk": queue_pk, "pk": standard_case_pk, "good_pk": good_on_application_pk}
    )

    response = authorized_client.get(url)
    assert response.status_code == 200
    soup = BeautifulSoup(response.content.decode("utf-8"), "html.parser")
    clc_entries = soup.find(id="control-list-entries-value").text
    clc_entries = "".join(line.strip() for line in clc_entries.split("\n"))
    assert clc_entries == "ML4,ML5"


def test_good_on_application_detail_security_graded_check(
    authorized_client,
    queue_pk,
    standard_case_pk,
    good_on_application_pk,
    data_good_on_application,
):
    for expected_value in ["no", "yes"]:
        data_good_on_application["good"]["is_pv_graded"] = expected_value
        # given I access good on application details for a good with control list entries and a part number
        url = reverse(
            "cases:good", kwargs={"queue_pk": queue_pk, "pk": standard_case_pk, "good_pk": good_on_application_pk}
        )
        response = authorized_client.get(url)

        assert response.status_code == 200
        soup = BeautifulSoup(response.content.decode("utf-8"), "html.parser")
        security_grading = soup.find(id="security-graded-value").text
        security_grading = "".join(line.strip() for line in security_grading.split("\n"))
        assert security_grading == expected_value.capitalize()


def test_good_on_application_good_on_application_without_document_type(
    authorized_client,
    queue_pk,
    standard_case_pk,
    good_on_application_pk,
    data_good_on_application,
    requests_mock,
):
    pk = data_good_on_application["application"]
    good_pk = data_good_on_application["good"]["id"]
    url = client._build_absolute_uri(f"/applications/{pk}/goods/{good_pk}/documents/")
    requests_mock.get(
        url=re.compile(f"{url}.*"),
        json={
            "documents": [
                {
                    "id": str(uuid.uuid4()),
                    "created_at": "2022-04-27T11:58:20.318970+01:00",
                    "name": "test-document.pdf",
                    "s3_key": "test-document.pdf",
                    "safe": True,
                    "document_type": None,
                    "good_on_application": None,
                },
            ]
        },
    )

    # given I access good on application details for a good with control list entries and a part number
    url = reverse(
        "cases:good", kwargs={"queue_pk": queue_pk, "pk": standard_case_pk, "good_pk": good_on_application_pk}
    )
    response = authorized_client.get(url)

    assert response.status_code == 200
    assert response.context["good_on_application_documents"] == {}


def test_case_worker_view_with_null_caseworker(
    authorized_client,
    requests_mock,
    queue_pk,
    standard_case_pk,
    data_standard_case,
):
    data_standard_case["case"]["case_officer"] = None

    gov_users_url = client._build_absolute_uri("/gov-users/")
    requests_mock.get(
        url=gov_users_url,
        json={
            "results": [],
        },
    )

    url = reverse(
        "cases:case_officer",
        kwargs={
            "queue_pk": queue_pk,
            "pk": standard_case_pk,
        },
    )
    response = authorized_client.get(url)
    assert response.status_code == 200
    assert response.context["data"] == {}


def test_case_worker_view_with_caseworker(
    authorized_client,
    requests_mock,
    queue_pk,
    standard_case_pk,
    data_standard_case,
):
    case_officer_id = str(uuid.uuid4())
    data_standard_case["case"]["case_officer"] = {
        "id": case_officer_id,
    }

    gov_users_url = client._build_absolute_uri("/gov-users/")
    requests_mock.get(
        url=gov_users_url,
        json={
            "results": [],
        },
    )

    url = reverse(
        "cases:case_officer",
        kwargs={
            "queue_pk": queue_pk,
            "pk": standard_case_pk,
        },
    )
    response = authorized_client.get(url)
    assert response.status_code == 200
    assert response.context["data"] == {
        "gov_user_pk": case_officer_id,
    }


@pytest.fixture
def mock_get_queries(requests_mock, standard_case_pk, data_ecju_queries_gov_serializer):
    requests_mock.get(
        client._build_absolute_uri(f"/cases/{standard_case_pk}/ecju-queries/"), json=data_ecju_queries_gov_serializer
    )


def test_close_query_view_post_success(
    authorized_client,
    requests_mock,
    queue_pk,
    standard_case_pk,
    data_ecju_queries_gov_serializer,
    data_query_closed_by_caseworker,
    mock_get_queries,
):
    # see that the query is in the open queries section
    url = reverse("cases:case", kwargs={"queue_pk": queue_pk, "pk": standard_case_pk, "tab": "ecju-queries"})
    response = authorized_client.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    open_queries = soup.find(id="open-queries")
    assert data_ecju_queries_gov_serializer["ecju_queries"][0]["question"] in str(open_queries)

    # close the query
    query_pk = data_ecju_queries_gov_serializer["ecju_queries"][0]["id"]
    requests_mock.put(client._build_absolute_uri(f"/cases/{standard_case_pk}/ecju-queries/{query_pk}/"), json={})
    cases_close_query_url = reverse(
        "cases:close_query", kwargs={"queue_pk": queue_pk, "pk": standard_case_pk, "query_pk": query_pk}
    )
    response = authorized_client.post(
        cases_close_query_url,
        data={
            f"{query_pk}-reason_for_closing_query": "Exporter clarified, closing this query",
        },
    )
    assert response.status_code == 302


def test_close_query_without_response_gives_error(
    authorized_client,
    requests_mock,
    queue_pk,
    standard_case_pk,
    data_ecju_queries_gov_serializer,
    data_query_closed_by_caseworker,
    mock_get_queries,
):
    # see that the query is in the open queries section
    url = reverse("cases:case", kwargs={"queue_pk": queue_pk, "pk": standard_case_pk, "tab": "ecju-queries"})
    response = authorized_client.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    open_queries = soup.find(id="open-queries")
    assert data_ecju_queries_gov_serializer["ecju_queries"][0]["question"] in str(open_queries)

    # close the query
    query_pk = data_ecju_queries_gov_serializer["ecju_queries"][0]["id"]
    requests_mock.put(client._build_absolute_uri(f"/cases/{standard_case_pk}/ecju-queries/{query_pk}/"), json={})
    cases_close_query_url = reverse(
        "cases:close_query", kwargs={"queue_pk": queue_pk, "pk": standard_case_pk, "query_pk": query_pk}
    )
    response = authorized_client.post(
        cases_close_query_url,
        data={
            f"{query_pk}-reason_for_closing_query": "",
        },
    )
    assert response.status_code == 200

    error_message = "Enter a reason why you are closing the query"
    assert error_message in response.content.decode("utf-8")
    assert response.context["form"].errors["reason_for_closing_query"] == [error_message]


def test_close_invalid_query_raises_error(
    authorized_client,
    queue_pk,
    standard_case_pk,
    mock_get_queries,
):
    # try to close query with invalid id
    query_pk = str(uuid.uuid4())
    url = reverse("cases:close_query", kwargs={"queue_pk": queue_pk, "pk": standard_case_pk, "query_pk": query_pk})
    response = authorized_client.post(url, data={f"{query_pk}-reason_for_closing_query": ""})
    assert response.status_code == 404


def test_close_query_view_show_closed_queries_on_page(
    authorized_client,
    requests_mock,
    queue_pk,
    standard_case_pk,
    data_ecju_queries_gov_serializer,
    data_query_closed_by_caseworker,
    mock_get_queries,
):
    # set up mock api response with closed query
    data_ecju_queries_gov_serializer["ecju_queries"][0] = data_query_closed_by_caseworker
    requests_mock.get(
        client._build_absolute_uri(f"/cases/{standard_case_pk}/ecju-queries/"), json=data_ecju_queries_gov_serializer
    )

    # see that there is no open queries section
    url = reverse("cases:case", kwargs={"queue_pk": queue_pk, "pk": standard_case_pk, "tab": "ecju-queries"})
    response = authorized_client.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    assert not soup.find("open-queries")

    # see that the query is in the closed queries section
    url = reverse("cases:case", kwargs={"queue_pk": queue_pk, "pk": standard_case_pk, "tab": "ecju-queries"})
    response = authorized_client.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    closed_queries = soup.find(id="closed-queries")
    assert data_query_closed_by_caseworker["question"] in str(closed_queries)
    assert data_query_closed_by_caseworker["response"] in str(closed_queries)
    assert data_query_closed_by_caseworker["responded_by_user_name"] in str(closed_queries)
