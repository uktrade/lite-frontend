import pytest
import re
import uuid

from bs4 import BeautifulSoup

from pytest_django.asserts import (
    assertTemplateNotUsed,
    assertTemplateUsed,
)

from copy import deepcopy
from dateutil.parser import parse
from django.urls import reverse
from django.utils import timezone

from core import client
from caseworker.cases.helpers.case import LU_POST_CIRC_FINALISE_QUEUE_ALIAS
from core.constants import SecurityClassifiedApprovalsType


@pytest.fixture(autouse=True)
def setup(
    settings,
    mock_queue,
    mock_gov_lu_user,
    mock_case,
    mock_standard_case_activity_filters,
    mock_standard_case_activity_system_user,
    mock_standard_case_ecju_queries,
    mock_standard_case_assigned_queues,
    mock_standard_case_documents,
    mock_standard_case_additional_contacts,
    mock_standard_case_on_post_circulation_queue,
):
    pass


def test_case_details_latest_activity(authorized_client, data_queue, data_standard_case):
    url = reverse("cases:case", kwargs={"queue_pk": data_queue["id"], "pk": data_standard_case["case"]["id"]})
    response = authorized_client.get(url)
    assertTemplateUsed(response, "layouts/case.html")
    context = response.context
    assert context["case"]["latest_activity"]
    assert context["case"]["latest_activity"]["text"] == "Flag added"


def test_case_details_latest_activity(authorized_client, data_queue, data_standard_case):
    url = reverse("cases:case", kwargs={"queue_pk": data_queue["id"], "pk": data_standard_case["case"]["id"]})
    response = authorized_client.get(url)
    assertTemplateUsed(response, "layouts/case.html")
    context = response.context
    assert context["case"]["total_days_elapsed"] == (timezone.now() - parse(context["case"]["submitted_at"])).days


def test_case_details_im_done_lu_user(authorized_client, data_queue, data_standard_case):
    url = reverse("cases:case", kwargs={"queue_pk": data_queue["id"], "pk": data_standard_case["case"]["id"]})
    response = authorized_client.get(url)
    assertTemplateUsed(response, "layouts/case.html")
    context = response.context
    assert context["hide_im_done"] == True
    assert context["current_user"]["team"]["alias"] == "LICENSING_UNIT"
    assert len(context["case"]["queue_details"]) == 1
    assert context["case"]["queue_details"][0]["alias"] == LU_POST_CIRC_FINALISE_QUEUE_ALIAS
    assert context["case"]["queue_details"][0]["days_on_queue_elapsed"] == 2


def test_case_details_im_done_fcdo_user(
    authorized_client,
    data_queue,
    data_standard_case,
    mock_standard_case_on_fcdo_countersigning_queue,
    mock_gov_fcdo_user,
):
    url = reverse("cases:case", kwargs={"queue_pk": data_queue["id"], "pk": data_standard_case["case"]["id"]})
    response = authorized_client.get(url)
    assertTemplateUsed(response, "layouts/case.html")
    context = response.context
    assert context["hide_im_done"] == False
    assert context["current_user"]["team"]["alias"] == "FCDO"
    assert len(context["case"]["queue_details"]) == 1
    assert context["case"]["queue_details"][0]["alias"] == "FCDO_COUNTER_SIGNING"
    assert context["case"]["queue_details"][0]["days_on_queue_elapsed"] == 3


def test_case_details_im_done_tau_user(
    authorized_client,
    data_queue,
    data_standard_case,
    mock_gov_tau_user,
):
    url = reverse("cases:case", kwargs={"queue_pk": data_queue["id"], "pk": data_standard_case["case"]["id"]})
    response = authorized_client.get(url)
    assertTemplateUsed(response, "layouts/case.html")
    context = response.context
    assert context["hide_im_done"] == True
    assert context["current_user"]["team"]["alias"] == "TAU"
    assert context["is_tau_user"] == True


def test_case_details_has_end_user_destination(
    authorized_client,
    data_queue,
    data_standard_case,
):
    url = reverse("cases:case", kwargs={"queue_pk": data_queue["id"], "pk": data_standard_case["case"]["id"]})
    response = authorized_client.get(url)
    assertTemplateUsed(response, "layouts/case.html")
    destination = response.context["case"]["data"]["destinations"]
    assert destination["type"] == "end_user"
    assert destination["data"]["name"] == "End User"


def test_case_details_with_no_destinations(
    authorized_client,
    requests_mock,
    data_queue,
    data_standard_case,
):
    url = reverse("cases:case", kwargs={"queue_pk": data_queue["id"], "pk": data_standard_case["case"]["id"]})
    case_no_destinations = deepcopy(data_standard_case)
    del case_no_destinations["case"]["data"]["destinations"]
    case_id = data_standard_case["case"]["id"]
    requests_mock.get(client._build_absolute_uri(f"/cases/{case_id}"), json=case_no_destinations)
    response = authorized_client.get(url)
    assertTemplateUsed(response, "layouts/case.html")
    destinations = response.context["destinations"]
    assert len(destinations) == 1
    assert destinations[0]["type"] == "end_user"
    assert destinations[0]["name"] == "End User"


@pytest.mark.parametrize(
    "is_system_queue",
    (
        True,
        False,
    ),
)
def test_case_assign_me_button_when_user_is_already_assigned(
    is_system_queue,
    authorized_client,
    data_queue,
    data_standard_case,
    mock_gov_user,
    assign_user_to_case,
):
    data_queue["is_system_queue"] = is_system_queue
    assign_user_to_case(
        mock_gov_user,
        data_standard_case,
    )

    case_url = reverse("cases:case", kwargs={"queue_pk": data_queue["id"], "pk": data_standard_case["case"]["id"]})
    response = authorized_client.get(case_url)

    html = BeautifulSoup(response.content, "html.parser")
    needs_allocation = html.find(id="allocation-warning")

    assert not needs_allocation


@pytest.mark.parametrize(
    "is_system_queue",
    (
        True,
        False,
    ),
)
def test_case_assign_me_button_when_user_is_not_assigned(
    is_system_queue,
    authorized_client,
    data_queue,
    data_standard_case,
    mock_gov_user,
):
    data_queue["is_system_queue"] = is_system_queue
    case_url = reverse("cases:case", kwargs={"queue_pk": data_queue["id"], "pk": data_standard_case["case"]["id"]})
    response = authorized_client.get(case_url)

    html = BeautifulSoup(response.content, "html.parser")
    needs_allocation = html.find(id="allocation-warning")
    banner_form = html.find("form", attrs={"class": "app-case-warning-banner__action-form"})

    assert "You need to allocate yourself or someone else to this case to work on it" in needs_allocation.text
    assert needs_allocation.find(id="allocate-case-link").text == "Allocate case"
    if not is_system_queue:
        assert needs_allocation.find(id="allocate-to-me-button").text == "Allocate to me"
        assert banner_form.find(id="id_return_to").get("value") == f"http://testserver{case_url}"
        assert banner_form.find(id="id_case_id").get("value") == data_standard_case["case"]["id"]
        assert banner_form.find(id="id_user_id").get("value") == mock_gov_user["user"]["id"]


def test_case_details_appeal_details(
    data_standard_case,
    data_queue,
    authorized_client,
):
    data_standard_case["case"]["data"]["appeal"] = {
        "grounds_for_appeal": "This is my reason for appeal",
    }
    case_url = reverse("cases:case", kwargs={"queue_pk": data_queue["id"], "pk": data_standard_case["case"]["id"]})
    response = authorized_client.get(case_url)

    assertTemplateUsed(response, "case/slices/appeal-details.html")

    html = BeautifulSoup(response.content, "html.parser")
    dt = html.find("dt", string=re.compile("Grounds for appeal"))
    assert dt
    assert dt.find_next().find("p").string == "This is my reason for appeal"


def test_case_details_appeal_details_no_appeal(
    data_standard_case,
    data_queue,
    authorized_client,
):
    case_url = reverse("cases:case", kwargs={"queue_pk": data_queue["id"], "pk": data_standard_case["case"]["id"]})
    response = authorized_client.get(case_url)

    assertTemplateNotUsed(response, "case/slices/appeal-details.html")


@pytest.mark.parametrize(
    "value, expected",
    (
        (None, "No sub-status set"),
        (
            {
                "id": "status-1",
                "name": "Status 1",
            },
            "Status 1",
        ),
    ),
)
def test_case_details_sub_status(
    data_standard_case,
    data_queue,
    authorized_client,
    value,
    expected,
):
    data_standard_case["case"]["data"]["sub_status"] = value
    case_url = reverse("cases:case", kwargs={"queue_pk": data_queue["id"], "pk": data_standard_case["case"]["id"]})
    response = authorized_client.get(case_url)

    html = BeautifulSoup(response.content, "html.parser")
    dt = html.find("dt", string=re.compile("Sub-status"))
    assert dt
    dd = dt.find_next()
    assert dd.get_text().replace("\n", "").replace("\t", "") == expected


@pytest.mark.parametrize(
    "value, expected",
    (
        ([], 0),
        (
            [
                {
                    "id": "status-1",
                    "name": "Status 1",
                }
            ],
            1,
        ),
    ),
)
def test_case_details_sub_status_change_displayed(
    data_standard_case,
    requests_mock,
    data_queue,
    authorized_client,
    mock_gov_user,
    value,
    expected,
):
    data_standard_case["case"]["case_officer"] = mock_gov_user["user"]
    case_id = data_standard_case["case"]["id"]
    requests_mock.get(
        client._build_absolute_uri(f"/applications/{case_id}/sub-statuses/"),
        json=value,
    )
    case_url = reverse("cases:case", kwargs={"queue_pk": data_queue["id"], "pk": data_standard_case["case"]["id"]})
    response = authorized_client.get(case_url)

    html = BeautifulSoup(response.content, "html.parser")

    assert len(html.find_all(id="link-case-sub-status-change")) == expected


@pytest.mark.parametrize(
    "licence_data, expected_status, expected_text",
    (
        ([], None, "No licence status set"),
        ([{"created_at": "2023-08-08", "status": "Issued"}], "Issued", "Issued"),
        (
            [{"created_at": "2023-08-11", "status": "Cancelled"}, {"created_at": "2023-08-09", "status": "Revoked"}],
            "Cancelled",
            "Cancelled",
        ),
    ),
)
def test_case_details_licence_status_displayed(
    data_standard_case,
    requests_mock,
    data_queue,
    authorized_client,
    mock_gov_user,
    licence_data,
    expected_status,
    expected_text,
):

    data_standard_case["case"]["licences"] = licence_data
    case_url = reverse("cases:case", kwargs={"queue_pk": data_queue["id"], "pk": data_standard_case["case"]["id"]})
    response = authorized_client.get(case_url)
    assert response.context["licence_status"] == expected_status
    html = BeautifulSoup(response.content, "html.parser")

    assert html.find(id="case-licence-status").span.text.strip() == expected_text


@pytest.mark.parametrize(
    "reference_code,expected_banner_msg",
    (
        (
            "GBSIEL/2024/0000010/P",
            "The exporter edited this application and the case has been superseded by GBSIEL/2024/0000010/P.",
        ),
        (
            None,
            "The exporter is editing their application. A new case will be created when they resubmit.",
        ),
    ),
)
def test_case_superseded_warning(
    reference_code,
    expected_banner_msg,
    authorized_client,
    data_queue,
    data_standard_case,
    mock_gov_user,
):
    synthetic_amendment_id = str(uuid.uuid4())
    data_standard_case["case"]["superseded_by"] = {"id": synthetic_amendment_id, "reference_code": reference_code}
    case_url = reverse("cases:case", kwargs={"queue_pk": data_queue["id"], "pk": data_standard_case["case"]["id"]})
    response = authorized_client.get(case_url)

    html = BeautifulSoup(response.content, "html.parser")
    superseded_banner = html.find(id="superseded-warning")
    superseded_message = superseded_banner.find("span", attrs={"class": "app-case-warning-banner__text"})

    assert expected_banner_msg in superseded_message.text


def test_case_amendment_warning(
    authorized_client,
    data_queue,
    data_standard_case,
    mock_gov_user,
):
    synthetic_superseded_id = str(uuid.uuid4())
    data_standard_case["case"]["amendment_of"] = {
        "id": synthetic_superseded_id,
        "reference_code": "GBSIEL/2024/0000002/P",
    }
    case_url = reverse("cases:case", kwargs={"queue_pk": data_queue["id"], "pk": data_standard_case["case"]["id"]})
    response = authorized_client.get(case_url)

    html = BeautifulSoup(response.content, "html.parser")
    amendment_banner = html.find(id="amendment-warning")
    amendment_message = amendment_banner.find("span", attrs={"class": "app-case-warning-banner__text"})

    assert (
        "This case was created when the exporter edited the original application at GBSIEL/2024/0000002/P."
        in amendment_message.text
    )


@pytest.mark.parametrize(
    "itar_controls_status,expected",
    (
        (False, "No"),
        (True, "Yes"),
    ),
)
def test_case_details_security_approvals(
    data_standard_case, data_queue, authorized_client, itar_controls_status, expected
):
    data_standard_case["case"]["data"]["is_mod_security_approved"] = True
    data_standard_case["case"]["data"]["security_approvals"] = [SecurityClassifiedApprovalsType.F680]
    data_standard_case["case"]["data"]["subject_to_itar_controls"] = itar_controls_status

    case_url = reverse("cases:case", kwargs={"queue_pk": data_queue["id"], "pk": data_standard_case["case"]["id"]})
    response = authorized_client.get(case_url)

    assertTemplateUsed(response, "components/security-approvals.html")

    html = BeautifulSoup(response.content, "html.parser")
    dt = html.find("dt", string=re.compile("Do you have an MOD security approval, such as F680 or F1686?"))
    assert dt
    assert dt.find_next().string == "Yes"

    dt = html.find("dt", string=re.compile("What type of approval do you have?"))
    assert dt
    assert dt.find_next().string == "F680"

    dt = html.find("dt", string=re.compile("Are any products on this application subject to ITAR controls?"))
    assert dt
    assert dt.find_next().string == expected
