import re
from decimal import Decimal
import pytest
from bs4 import BeautifulSoup

from pytest_django.asserts import assertTemplateUsed

from django.urls import reverse

from core import client


@pytest.fixture(autouse=True)
def setup(
    settings,
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


@pytest.fixture
def mock_gov_fcdo_ogd_user(requests_mock, mock_notifications, mock_case_statuses, mock_gov_user, gov_uk_user_id):
    mock_gov_user["user"]["team"] = {
        "id": "521154de-f39e-45bf-9922-baaaaaa",
        "name": "FCDO",
        "alias": "FCO",
    }

    url = client._build_absolute_uri("/gov-users/")
    requests_mock.get(url=f"{url}me/", json=mock_gov_user)
    requests_mock.get(url=re.compile(f"{url}{gov_uk_user_id}/"), json=mock_gov_user)


@pytest.fixture
def data_ogd_queue():
    return {
        "id": "00000000-0000-0000-0000-000000000002",
        "alias": None,
        "name": "Some OGD",
        "is_system_queue": False,
        "countersigning_queue": None,
    }


@pytest.fixture
def mock_ogd_queue(requests_mock, data_ogd_queue):
    url = client._build_absolute_uri("/queues/")
    yield requests_mock.get(url=re.compile(f"{url}.*/"), json=data_ogd_queue)


def test_case_summary_activated(authorized_client, data_queue, data_standard_case, mock_queue):
    url = reverse(
        "cases:case",
        kwargs={"queue_pk": data_queue["id"], "pk": data_standard_case["case"]["id"], "tab": "quick-summary"},
    )
    response = authorized_client.get(url)
    assertTemplateUsed(response, "case/tabs/quick-summary.html")


def test_case_summary_allocate_and_approve(authorized_client, data_ogd_queue, data_standard_case, mock_ogd_queue):
    url = reverse(
        "cases:case",
        kwargs={"queue_pk": data_ogd_queue["id"], "pk": data_standard_case["case"]["id"], "tab": "quick-summary"},
    )
    response = authorized_client.get(url)
    assertTemplateUsed(response, "case/tabs/quick-summary.html")
    assert "allocate_and_approve_form" in response.context
    assert response.context["allocate_and_approve_form"].initial["return_to"] == reverse(
        "cases:approve_all", kwargs={"queue_pk": data_ogd_queue["id"], "pk": data_standard_case["case"]["id"]}
    )


def test_case_summary_allocate_and_approve_fcdo(
    authorized_client, data_ogd_queue, data_standard_case, mock_ogd_queue, mock_gov_fcdo_ogd_user
):
    url = reverse(
        "cases:case",
        kwargs={"queue_pk": data_ogd_queue["id"], "pk": data_standard_case["case"]["id"], "tab": "quick-summary"},
    )
    response = authorized_client.get(url)
    assertTemplateUsed(response, "case/tabs/quick-summary.html")
    assert "allocate_and_approve_form" in response.context
    assert response.context["allocate_and_approve_form"].initial["return_to"] == reverse(
        "cases:approve_all_legacy", kwargs={"queue_pk": data_ogd_queue["id"], "pk": data_standard_case["case"]["id"]}
    )


def test_case_summary_data(authorized_client, data_queue, data_standard_case, mock_queue):
    gov_user = {
        "id": "2a43805b-c082-47e7-9188-c8b3e1a83cb0",
        "email": "govuser@example.com",
        "first_name": "Foo",
        "last_name": "Bar",
        "status": "Active",
        "team": {"id": "00000000-0000-0000-0000-000000000001", "name": "Admin", "alias": None},
        "default_queue": {"id": "00000000-0000-0000-0000-000000000001", "name": "All cases"},
        "team": {
            "id": "521154de-f39e-45bf-9922-baaaaaa",
            "name": "Licencing Unit",
            "alias": "LICENSING_UNIT",
        },
    }
    data_standard_case["case"]["assigned_users"] = {"00000000-0000-0000-0000-000000000001": [gov_user]}
    data_standard_case["case"]["case_officer"] = gov_user
    data_standard_case["case"]["data"]["sanction_matches"] = [{"list_name": "Russia"}]
    # New style report summary
    data_standard_case["case"]["data"]["goods"][0]["report_summary_prefix"] = {"name": "casing for"}
    data_standard_case["case"]["data"]["goods"][0]["report_summary_subject"] = {"name": "nuke"}
    # Old style report summary
    data_standard_case["case"]["data"]["goods"][1]["report_summary_prefix"] = None
    data_standard_case["case"]["data"]["goods"][1]["report_summary_subject"] = None
    data_standard_case["case"]["data"]["goods"][1]["report_summary"] = "some report summary"
    url = reverse(
        "cases:case",
        kwargs={"queue_pk": data_queue["id"], "pk": data_standard_case["case"]["id"], "tab": "quick-summary"},
    )
    response = authorized_client.get(url)
    html = BeautifulSoup(response.content, "html.parser")

    table_text = html.find("table", {"class": "app-table"}).text.strip()

    expected_case_status = data_standard_case["case"]["data"]["status"]["value"]
    assert expected_case_status in table_text

    expected_lu_case_officer = f'{gov_user["first_name"]} {gov_user["last_name"]}'
    assert expected_lu_case_officer in table_text

    expected_case_adviser = f'{gov_user["first_name"]} {gov_user["last_name"]}'
    assert expected_lu_case_officer in table_text

    expected_temporary_or_permanent = data_standard_case["case"]["data"]["export_type"]["key"].capitalize()
    assert expected_temporary_or_permanent in table_text

    expected_assigned_queues = data_standard_case["case"]["queue_details"][0]["name"]
    assert expected_assigned_queues in table_text

    expected_flags = data_standard_case["case"]["all_flags"][0]["name"]
    assert expected_flags in table_text

    expected_latest_action = data_standard_case["case"]["latest_activity"]["text"]
    assert expected_latest_action in table_text

    for good in data_standard_case["case"]["data"]["goods"]:
        expected_product_name = good["good"]["name"]
        assert expected_product_name in table_text

    val = Decimal()
    expected_total_value = Decimal(0)
    for good in data_standard_case["case"]["data"]["goods"]:
        expected_total_value += Decimal(good["value"])
    assert f"£{expected_total_value}" in table_text

    for good in data_standard_case["case"]["data"]["goods"]:
        for cle in good["control_list_entries"]:
            assert cle["rating"] in table_text

    for good in data_standard_case["case"]["data"]["goods"]:
        for regime_entry in good["regime_entries"]:
            assert regime_entry["name"] in table_text

    # Check new style report summary
    good = data_standard_case["case"]["data"]["goods"][0]
    assert f'{good["report_summary_prefix"]["name"]} {good["report_summary_subject"]["name"]}' in table_text
    # Check old style report summary
    good_2 = data_standard_case["case"]["data"]["goods"][1]
    assert good_2["report_summary"] in table_text

    assert data_standard_case["case"]["data"]["goods"][0]["good"]["is_pv_graded"] in table_text.lower()

    for approval in data_standard_case["case"]["data"]["security_approvals"]:
        assert approval in table_text

    expected_applicant = data_standard_case["case"]["data"]["submitted_by"]
    assert expected_applicant in table_text

    all_parties = (
        data_standard_case["case"]["data"]["ultimate_end_users"] + data_standard_case["case"]["data"]["third_parties"]
    )
    all_parties.append(data_standard_case["case"]["data"]["consignee"])
    all_parties.append(data_standard_case["case"]["data"]["end_user"])
    for party in all_parties:
        assert party["country"]["name"] in table_text

    for denial_match in data_standard_case["case"]["data"]["denial_matches"]:
        assert denial_match["denial_entity"]["reference"] in table_text

    for sanction_match in data_standard_case["case"]["data"]["sanction_matches"]:
        assert sanction_match["list_name"] in table_text

    expected_end_use = data_standard_case["case"]["data"]["intended_end_use"]
    assert expected_end_use in table_text

    expected_end_user = data_standard_case["case"]["data"]["end_user"]["name"]
    assert expected_end_user in table_text


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
def test_case_summary_sub_status(
    data_standard_case,
    data_queue,
    mock_queue,
    authorized_client,
    value,
    expected,
):
    # Based on test_case_details_sub_status
    data_standard_case["case"]["data"]["sub_status"] = value
    case_url = reverse("cases:case", kwargs={"queue_pk": data_queue["id"], "pk": data_standard_case["case"]["id"]})
    response = authorized_client.get(case_url)

    html = BeautifulSoup(response.content, "html.parser")
    th = html.find("th", text="Sub-status")
    td = th.find_next()
    assert td.text.strip() == expected
