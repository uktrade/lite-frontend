import re
import uuid

from bs4 import BeautifulSoup
from copy import deepcopy

from django.test import override_settings
from django.urls import reverse
from django.conf import settings

import pytest

from core import client


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
):
    yield


def test_case_audit_trail_system_user(authorized_client, open_case_pk, queue_pk):
    # given the case has activity from system user
    url = reverse("cases:case", kwargs={"queue_pk": queue_pk, "pk": open_case_pk})

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
@override_settings(LITE_API_SEARCH_ENABLED=True)
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
@override_settings(LITE_API_SEARCH_ENABLED=True)
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


@override_settings(LITE_API_SEARCH_ENABLED=True)
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


@override_settings(LITE_API_SEARCH_ENABLED=True)
def test_good_on_application_firearm_detail(
    authorized_client,
    queue_pk,
    standard_case_pk,
    data_standard_case,
    mock_firearm_good_on_application,
    mock_firearm_good_on_application_documents,
):
    # given I access good on application details for a good with control list entries and a part number
    good = data_standard_case["case"]["data"]["goods"][0]
    url = reverse("cases:good", kwargs={"queue_pk": queue_pk, "pk": standard_case_pk, "good_pk": good["id"]})
    response = authorized_client.get(url)

    assert response.status_code == 200

    # and the view exposes the data that the template needs
    assert response.context_data["good_on_application"] == good
    assert response.context_data["case"] == data_standard_case["case"]
    assert response.context_data["product_summary"] == (
        ("firearm-type", "Firearms", "Select the type of firearm product"),
        ("firearm-category", "Non automatic shotgun, Non automatic rim-fired handgun", "Firearm category"),
        ("name", "p1", "Give the product a descriptive name"),
        ("is-good-controlled", "Yes", "Do you know the product's control list entry?"),
        ("control-list-entries", "ML1a, ML22b", "Enter the control list entry"),
        ("is-pv-graded", "Yes", "Does the product have a government security grading or classification?"),
        ("pv-grading-prefix", "NATO", "Enter a prefix (optional)"),
        ("pv-grading-grading", "Official", "What is the security grading or classification?"),
        ("pv-grading-suffix", "SUFFIX", "Enter a suffix (optional)"),
        ("pv-grading-issuing-authority", "Government entity", "Name and address of the issuing authority"),
        ("pv-grading-details-reference", "GR123", "Reference"),
        ("pv-grading-details-date-of-issue", "20 February 2020", "Date of issue"),
        ("calibre", "0.25", "What is the calibre of the product?"),
        ("is-replica", "No", "Is the product a replica firearm?"),
        ("is-registered-firearms-dealer", "No", "Are you a registered firearms dealer?"),
        (
            "is-covered-by-firearm-act-section-one-two-or-five-explanation",
            "Not covered by firearm act sections",
            "Explain",
        ),
        (
            "has-product-document",
            "Yes",
            "Do you have a document that shows what your product is and what it’s " "designed to do?",
        ),
        ("is-document-sensitive", "No", "Is the document rated above Official-sensitive?"),
        (
            "product-document",
            '<a class="govuk-link govuk-link--no-visited-state" '
            'href="/queues/00000000-0000-0000-0000-000000000001/cases/8fb76bed-fd45-4293-95b8-eda9468aa254/documents/6c48a2cc-1ed9-49a5-8ca7-df8af5fc2335/" '
            'target="_blank">data_sheet.pdf</a>',
            "Upload a document that shows what your product is designed to do",
        ),
        ("product-document-description", "product data sheet", "Description (optional)"),
        ("manufacture-year", "1990", "What year was it made?"),
        ("is-onward-exported", "No", "Will the product be onward exported to any additional countries?"),
        ("is-deactivated", "No", "Has the product been deactivated?"),
        ("number-of-items", 2, "Number of items"),
        ("total-value", "£444.00", "Total value"),
        (
            "has-serial-numbers",
            "Yes, I can add serial numbers now",
            "Will each product have a serial number or other identification marking?",
        ),
        (
            "serial-numbers",
            "\n"
            "\n"
            "\n"
            '    <details class="govuk-details govuk-!-margin-bottom-0" '
            'data-module="govuk-details">\n'
            '        <summary class="govuk-details__summary">\n'
            '            <span class="govuk-details__summary-text">\n'
            "                View serial numbers\n"
            "            </span>\n"
            "        </summary>\n"
            '        <div class="govuk-details__text">\n'
            "            \n"
            "                1. 12345  <br> \n"
            "            \n"
            "                2. ABC-123 \n"
            "            \n"
            "        </div>\n"
            "    </details>\n"
            "\n",
            "Enter serial numbers or other identification markings",
        ),
    )


@override_settings(LITE_API_SEARCH_ENABLED=True)
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


@override_settings(LITE_API_SEARCH_ENABLED=True)
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


@override_settings(LITE_API_SEARCH_ENABLED=True)
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
