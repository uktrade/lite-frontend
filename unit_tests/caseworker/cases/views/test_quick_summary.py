from decimal import Decimal
import pytest
from bs4 import BeautifulSoup
from datetime import timedelta

from pytest_django.asserts import assertTemplateUsed, assertTemplateNotUsed

from copy import deepcopy
from dateutil.parser import parse
from django.test import override_settings
from django.urls import reverse
from django.utils import timezone

from core import client


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


def test_case_summary_deactivated(authorized_client, data_queue, data_standard_case):
    url = reverse("cases:case", kwargs={"queue_pk": data_queue["id"], "pk": data_standard_case["case"]["id"]})
    response = authorized_client.get(url)
    assertTemplateNotUsed(response, "case/tabs/quick-summary.html")


@override_settings(FEATURE_QUICK_SUMMARY=True)
def test_case_summary_activated(authorized_client, data_queue, data_standard_case):
    url = reverse("cases:case", kwargs={"queue_pk": data_queue["id"], "pk": data_standard_case["case"]["id"]})
    response = authorized_client.get(url)
    assertTemplateUsed(response, "case/tabs/quick-summary.html")


@override_settings(FEATURE_QUICK_SUMMARY=True)
def test_case_summary_data(authorized_client, data_queue, data_standard_case):
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
    data_standard_case["case"]["data"]["goods"][0]["report_summary_prefix"] = {"name": "casing for"}
    data_standard_case["case"]["data"]["goods"][0]["report_summary_subject"] = {"name": "nuke"}
    url = reverse("cases:case", kwargs={"queue_pk": data_queue["id"], "pk": data_standard_case["case"]["id"]})
    response = authorized_client.get(url)
    html = BeautifulSoup(response.content, "html.parser")

    status = html.find(id="status").text.strip()
    assert status == data_standard_case["case"]["data"]["status"]["value"]

    licensing_unit_case_officer = html.find(id="licensing_unit_case_officer").text.strip()
    assert licensing_unit_case_officer == f'{gov_user["first_name"]} {gov_user["last_name"]}'

    case_adviser = html.find(id="case_adviser").text.strip()
    assert case_adviser == f'{gov_user["first_name"]} {gov_user["last_name"]}'

    temporary_or_permanent = html.find(id="temporary_or_permanent").text.strip()
    assert temporary_or_permanent == data_standard_case["case"]["data"]["export_type"]["key"]

    assigned_queues = html.find(id="assigned_queues").text.strip()
    assert assigned_queues == data_standard_case["case"]["queue_details"][0]["name"]

    flags = html.find(id="flags").text.strip()
    assert flags == data_standard_case["case"]["all_flags"][0]["name"]

    open_query = html.find(id="open_query").text.strip()
    assert open_query == None if data_standard_case["case"]["has_open_queries"] else "Outstanding queries"

    latest_action = html.find(id="latest_action").text.strip()
    assert data_standard_case["case"]["latest_activity"]["text"] in latest_action

    days_on_queue_elapsed = html.find(id="days_on_queue_elapsed").text.strip()
    for queue_detail in data_standard_case["case"]["queue_details"]:
        assert str((timezone.now() - parse(queue_detail["joined_queue_at"])).days) in days_on_queue_elapsed

    total_days_elapsed = html.find(id="total_days_elapsed").text.strip()
    assert total_days_elapsed == str((timezone.now() - parse(data_standard_case["case"]["submitted_at"])).days)

    product_names = html.find(id="product_names").text.strip()
    for good in data_standard_case["case"]["data"]["goods"]:
        assert good["good"]["name"] in product_names

    total_value = html.find(id="total_value").text.strip()
    val = Decimal()
    for good in data_standard_case["case"]["data"]["goods"]:
        val += Decimal(good["value"])
    assert total_value == f"£{val}"

    control_list_entry = html.find(id="control_list_entry").text.strip()
    for good in data_standard_case["case"]["data"]["goods"]:
        for cle in good["control_list_entries"]:
            assert cle["rating"] in control_list_entry

    regime = html.find(id="regime").text.strip()
    for good in data_standard_case["case"]["data"]["goods"]:
        for regime_entry in good["regime_entries"]:
            assert regime_entry["name"] in regime

    report_summary = html.find(id="report_summary").text.strip()
    for good in data_standard_case["case"]["data"]["goods"]:
        assert f'{good["report_summary_prefix"]["name"]} {good["report_summary_subject"]["name"]}' in report_summary

    security_graded = html.find(id="security_graded").text.strip()
    assert security_graded.lower() == data_standard_case["case"]["data"]["goods"][0]["good"]["is_pv_graded"]

    security_approvals = html.find(id="security_approvals").text.strip()
    for approval in data_standard_case["case"]["data"]["security_approvals"]:
        assert approval in security_approvals

    applicant = html.find(id="applicant").text.strip()
    assert applicant == data_standard_case["case"]["data"]["submitted_by"]

    destination = html.find(id="destination").text.strip()
    all_parties = (
        data_standard_case["case"]["data"]["ultimate_end_users"] + data_standard_case["case"]["data"]["third_parties"]
    )
    all_parties.append(data_standard_case["case"]["data"]["consignee"])
    all_parties.append(data_standard_case["case"]["data"]["end_user"])
    for party in all_parties:
        assert party["country"]["name"] in destination

    denial_matches = html.find(id="denial_matches").text.strip()
    for denial_match in data_standard_case["case"]["data"]["denial_matches"]:
        assert denial_match["denial"]["reference"] in denial_matches

    sanction_matches = html.find(id="sanction_matches").text.strip()
    for sanction_match in data_standard_case["case"]["data"]["sanction_matches"]:
        assert sanction_match["list_name"] in sanction_matches

    end_use = html.find(id="end_use").text.strip()
    assert end_use == data_standard_case["case"]["data"]["intended_end_use"]

    end_user_document = html.find(id="end_user_document")
    assert end_user_document == None


@override_settings(FEATURE_QUICK_SUMMARY=True)
def test_case_summary_missing_data(authorized_client, data_queue, data_standard_case):
    data_standard_case["case"]["queue_details"] = []
    data_standard_case["case"]["flags"] = []
    data_standard_case["case"]["goods_flags"] = []
    data_standard_case["case"]["destinations_flags"] = []
    data_standard_case["case"]["has_open_queries"] = False
    data_standard_case["case"]["latest_activity"] = None
    data_standard_case["case"]["data"]["security_approvals"] = []
    data_standard_case["case"]["data"]["denial_matches"] = []
    data_standard_case["case"]["data"]["sanction_matches"] = []
    for good in data_standard_case["case"]["data"]["goods"]:
        good["control_list_entries"] = []
        good["regime_entries"] = []
        good["report_summary_prefix"] = None
        good["report_summary_subject"] = None
        good["good"]["is_pv_graded"] = "no"

    url = reverse("cases:case", kwargs={"queue_pk": data_queue["id"], "pk": data_standard_case["case"]["id"]})
    response = authorized_client.get(url)
    html = BeautifulSoup(response.content, "html.parser")

    licensing_unit_case_officer = html.find(id="licensing_unit_case_officer").text.strip()
    assert licensing_unit_case_officer == "Not assigned"

    case_adviser = html.find(id="case_adviser").text.strip()
    assert case_adviser == "Not assigned"

    assigned_queues = html.find(id="assigned_queues").text.strip()
    assert assigned_queues == "Not assigned"

    flags = html.find(id="flags").text.strip()
    assert flags == "None"

    open_query = html.find(id="open_query").text.strip()
    assert open_query == "None"

    latest_action = html.find(id="latest_action").text.strip()
    assert latest_action == "None"

    days_on_queue_elapsed = html.find(id="days_on_queue_elapsed").text.strip()
    assert days_on_queue_elapsed == "N/A"

    control_list_entry = html.find(id="control_list_entry").text.strip()
    assert control_list_entry == "None"

    regime = html.find(id="regime").text.strip()
    assert regime == "None"

    report_summary = html.find(id="report_summary").text.strip()
    assert report_summary == "None"

    security_graded = html.find(id="security_graded").text.strip()
    assert security_graded == "No"

    denial_matches = html.find(id="denial_matches").text.strip()
    assert denial_matches == "None"

    sanction_matches = html.find(id="sanction_matches").text.strip()
    assert sanction_matches == "None"

    data_standard_case["case"]["data"]["goods"][0]["report_summary_subject"] = {"name": "guns"}
    url = reverse("cases:case", kwargs={"queue_pk": data_queue["id"], "pk": data_standard_case["case"]["id"]})
    response = authorized_client.get(url)
    html = BeautifulSoup(response.content, "html.parser")

    report_summary = html.find(id="report_summary").text.strip()
    assert report_summary == "guns"
