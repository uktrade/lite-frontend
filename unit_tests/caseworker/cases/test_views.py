import pytest
import re
import uuid

from bs4 import BeautifulSoup

from django.test import override_settings
from django.urls import reverse

from core import client

from unit_tests.helpers import merge_summaries


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


good_review_parametrize_data = (
    # all field present, nothing special
    (
        {
            "comment": "Some comment",
            "control_list_entries": ["ML1a"],
            "is_good_controlled": True,
            "report_summary": "some-report-summary-id",
            "end_use_control": ["MEND", "MEND1"],
            "is_precedent": False,
        },
        {
            "comment": "Some comment",
            "control_list_entries": ["ML1a"],
            "is_good_controlled": True,
            "report_summary": "some-report-summary-id",
            "end_use_control": ["MEND", "MEND1"],
            "is_precedent": False,
        },
    ),
    # multiple control list entries
    (
        {
            "comment": "Some comment",
            "control_list_entries": ["ML1a", "ML1"],
            "is_good_controlled": True,
            "report_summary": "some-report-summary-id",
            "end_use_control": [],
            "is_precedent": False,
        },
        {
            "comment": "Some comment",
            "control_list_entries": ["ML1a", "ML1"],
            "is_good_controlled": True,
            "report_summary": "some-report-summary-id",
            "end_use_control": [],
            "is_precedent": False,
        },
    ),
    # no comment
    (
        {
            "comment": "",
            "control_list_entries": ["ML1a"],
            "is_good_controlled": True,
            "report_summary": "some-report-summary-id",
            "end_use_control": [],
            "is_precedent": False,
        },
        {
            "comment": "",
            "control_list_entries": ["ML1a"],
            "is_good_controlled": True,
            "report_summary": "some-report-summary-id",
            "end_use_control": [],
            "is_precedent": False,
        },
    ),
    # not controlled and no control list entries
    (
        {
            "comment": "Some comment",
            "control_list_entries": [],
            "does_not_have_control_list_entries": True,
            "is_good_controlled": False,
            "report_summary": "some-report-summary-id",
            "end_use_control": [],
            "is_precedent": False,
        },
        {
            "comment": "Some comment",
            "control_list_entries": [],
            "is_good_controlled": False,
            "report_summary": "some-report-summary-id",
            "end_use_control": [],
            "is_precedent": False,
        },
    ),
    # is controlled but no control list entries
    (
        {
            "comment": "Some comment",
            "control_list_entries": [],
            "does_not_have_control_list_entries": True,
            "is_good_controlled": True,
            "report_summary": "some-report-summary-id",
            "end_use_control": [],
            "is_precedent": False,
        },
        {
            "comment": "Some comment",
            "control_list_entries": [],
            "is_good_controlled": True,
            "report_summary": "some-report-summary-id",
            "end_use_control": [],
            "is_precedent": False,
        },
    ),
    # backwards compat, if API is not sending is_precedent
    (
        {
            "comment": "Some comment",
            "control_list_entries": ["ML1a"],
            "is_good_controlled": True,
            "report_summary": "some-report-summary-id",
            "end_use_control": ["MEND", "MEND1"],
        },
        {
            "comment": "Some comment",
            "control_list_entries": ["ML1a"],
            "is_good_controlled": True,
            "report_summary": "some-report-summary-id",
            "end_use_control": ["MEND", "MEND1"],
            "is_precedent": False,
        },
    ),
)


@pytest.mark.parametrize("data,expected", good_review_parametrize_data)
def test_standard_review_goods(
    authorized_client,
    requests_mock,
    standard_case_pk,
    queue_pk,
    data,
    expected,
    data_standard_case,
    mock_product_more_like_this,
):
    requests_mock_instance = requests_mock.post(f"/goods/control-list-entries/{standard_case_pk}/", json={})
    good_pk = data_standard_case["case"]["data"]["goods"][0]["good"]["id"]
    good_on_application_pk = data_standard_case["case"]["data"]["goods"][0]["id"]
    data["current_object"] = good_on_application_pk
    expected["current_object"] = good_on_application_pk

    step_data = build_wizard_step_data(
        view_name="review_standard_application_good_wizard_view",
        step_name=good_on_application_pk,
        data=data,
    )
    url = reverse("cases:review_standard_application_goods", kwargs={"queue_pk": queue_pk, "pk": standard_case_pk})

    response = authorized_client.get(f"{url}?goods={good_on_application_pk}")
    assert response.status_code == 200

    response = authorized_client.post(f"{url}?goods={good_on_application_pk}", step_data)
    assert response.status_code == 302
    assert requests_mock_instance.call_count == 1
    assert requests_mock_instance.request_history[0].json() == {**expected, "objects": [good_pk]}

    assert good_on_application_pk in mock_product_more_like_this.request_history[0].url


@pytest.mark.parametrize("data,expected", good_review_parametrize_data)
def test_open_review_goods(
    authorized_client,
    requests_mock,
    open_case_pk,
    queue_pk,
    data,
    expected,
    data_open_case,
    mock_product_more_like_this,
):
    requests_mock_instance = requests_mock.post(f"/goods/control-list-entries/{open_case_pk}/", json={})
    good_pk = data_open_case["case"]["data"]["goods_types"][0]["id"]
    step_data = build_wizard_step_data(
        view_name="review_open_application_good_wizard_view",
        step_name=good_pk,
        data=data,
    )
    url = reverse("cases:review_open_application_goods", kwargs={"queue_pk": queue_pk, "pk": open_case_pk})

    response = authorized_client.get(f"{url}?goods_types={good_pk}")

    assert response.status_code == 200

    with pytest.raises(ValueError) as e:
        response = authorized_client.post(f"{url}?goods_types={good_pk}", step_data)


def build_wizard_step_data(view_name, step_name, data):
    step_data = {f"{view_name}-current_step": step_name}
    step_data.update({f"{step_name}-{key}": value for key, value in data.items()})
    return step_data


def test_good_on_application_detail(
    authorized_client,
    mock_application_search,
    queue_pk,
    standard_case_pk,
    good_on_application_pk,
    data_search,
    data_good_on_application,
    data_standard_case,
):
    # given I access good on application details for a good with control list entries and a part number
    url = reverse(
        "cases:good", kwargs={"queue_pk": queue_pk, "pk": standard_case_pk, "good_pk": good_on_application_pk}
    )
    response = authorized_client.get(url)

    assert response.status_code == 200
    # then the search endpoint is requested for cases with goods with the same part number and control list entries
    assert mock_application_search.request_history[0].qs == {"part": ["44"], "clc_rating": ["ml1", "ml2"]}
    assert response.context_data["other_cases"] == data_search
    # and the form is pre-populated with the part number and control list entries
    assert response.context_data["form"]["search_string"].initial == 'part:"44" clc_rating:"ML1" clc_rating:"ML2"'

    # and the view exposes the data that the template needs
    assert response.context_data["good_on_application"] == data_good_on_application
    assert response.context_data["case"] == data_standard_case["case"]
    assert response.context_data["product_summary"] == None


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
    # then the search endpoint is requested for cases with goods with the same control list entries
    assert mock_application_search.request_history[0].qs == {"clc_rating": ["ml1", "ml2"]}
    # and the form is pre-populated with the part number and control list entries
    assert response.context_data["form"]["search_string"].initial == 'clc_rating:"ML1" clc_rating:"ML2"'


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
    # then the search endpoint is not requested
    assert len(mock_application_search.request_history) == 0
    # and the form is left blank
    assert response.context_data["form"]["search_string"].initial == ""


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
    # then the search endpoint is requested for cases with goods with the same control list entries as canonical good
    assert mock_application_search.request_history[0].qs == {"clc_rating": ["ml1"]}
    # and the form is pre-populated with the canonical good control list entries
    assert response.context_data["form"]["search_string"].initial == 'clc_rating:"ML1"'


def test_search_denials(authorized_client, data_standard_case, requests_mock, queue_pk, standard_case_pk):
    end_user_id = data_standard_case["case"]["data"]["end_user"]["id"]
    end_user_name = data_standard_case["case"]["data"]["end_user"]["name"]
    end_user_address = data_standard_case["case"]["data"]["end_user"]["address"]

    requests_mock.get(
        client._build_absolute_uri(f"/external-data/denial-search/?search={end_user_name}&search={end_user_address}"),
        json={"hits": {"hits": []}},
    )

    url = reverse("cases:denials", kwargs={"pk": standard_case_pk, "queue_pk": queue_pk})

    response = authorized_client.get(f"{url}?end_user={end_user_id}")

    assert response.status_code == 200


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
