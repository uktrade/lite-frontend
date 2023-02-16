import pytest
import re

from bs4 import BeautifulSoup

from django.urls import reverse

from core import client


@pytest.fixture
def mock_report_summary(requests_mock, report_summary_subject, report_summary_prefix):
    requests_mock.get(
        "/static/report_summary/subjects/?name=scale+compelling+technologies",
        json={
            "report_summary_subjects": [report_summary_subject],
        },
    )
    requests_mock.get(
        f"/static/report_summary/subjects/{report_summary_subject['id']}/",
        json={
            "report_summary_subject": report_summary_subject,
        },
    )
    requests_mock.get(
        "/static/report_summary/prefixes/?name=components+for",
        json={
            "report_summary_prefixes": [report_summary_prefix],
        },
    )
    requests_mock.get(
        f"/static/report_summary/prefixes/{report_summary_prefix['id']}/",
        json={
            "report_summary_prefix": report_summary_prefix,
        },
    )


@pytest.fixture(autouse=True)
def setup(
    mock_queue,
    mock_case,
    mock_wassenaar_entries_get,
    mock_mtcr_entries_get,
    mock_nsg_entries_get,
    mock_cwc_entries_get,
    mock_ag_entries_get,
    mock_report_summary,
):
    yield


@pytest.fixture(autouse=True)
def default_feature_flags(settings):
    settings.FEATURE_C6_REGIMES = True


@pytest.fixture(autouse=True)
def mock_application_good_documents(data_standard_case, requests_mock):
    requests_mock.get(
        re.compile(
            rf"/applications/{data_standard_case['case']['id']}/goods/[0-9a-fA-F-]+/documents/",
        ),
        json={"documents": []},
    )


@pytest.fixture
def url(data_queue, data_standard_case):
    return reverse(
        "cases:tau:edit",
        kwargs={
            "queue_pk": data_queue["id"],
            "pk": data_standard_case["case"]["id"],
            "good_id": data_standard_case["case"]["data"]["goods"][1]["id"],
        },
    )


@pytest.fixture
def mock_cle_post(requests_mock, data_standard_case):
    yield requests_mock.post(
        client._build_absolute_uri(f"/goods/control-list-entries/{data_standard_case['case']['id']}"), json={}
    )


def get_cells(soup, table_id):
    return [td.text for td in soup.find(id=table_id).find_all("td")]


def test_tau_edit_auth(authorized_client, url, mock_control_list_entries, mock_precedents_api):
    """GET edit should return 200 with an authorised client"""
    response = authorized_client.get(url)
    assert response.status_code == 200


def test_tau_home_noauth(client, url):
    """GET edit should return 302 with an unauthorised client"""
    response = client.get(url)
    assert response.status_code == 302


def test_form(
    authorized_client,
    url,
    data_standard_case,
    requests_mock,
    mock_cle_post,
    mock_control_list_entries,
    mock_precedents_api,
    report_summary_prefix,
    report_summary_subject,
):
    """
    Tests the submission of a valid form only. More tests on the form itself are in test_forms.py
    """
    # Remove assessment from a good
    good = data_standard_case["case"]["data"]["goods"][0]
    good["is_good_controlled"] = None
    good["control_list_entries"] = []
    edit_good = data_standard_case["case"]["data"]["goods"][1]
    edit_good["control_list_entries"] = [{"rating": "ML1"}, {"rating": "ML1a"}]
    # Get the edit form
    response = authorized_client.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    # Check if the form fields contain sane values
    edit_good = data_standard_case["case"]["data"]["goods"][1]

    # Check control list entries
    edit_good_cle = [cle["rating"] for cle in edit_good["control_list_entries"]]
    form_cle = [
        cle.attrs["value"]
        for cle in soup.find("select", {"id": "control_list_entries"}).find_all("option")
        if "selected" in cle.attrs
    ]
    assert edit_good_cle == form_cle

    # Check regimes
    form_regimes = [
        regime.attrs["value"] for regime in soup.find_all("input", {"name": "regimes"}) if "checked" in regime.attrs
    ]
    assert form_regimes == ["WASSENAAR", "MTCR", "CWC", "NSG", "AG"]

    edit_mtcr_good_regimes = [
        entry["pk"] for entry in edit_good["regime_entries"] if entry["subsection"]["regime"]["name"] == "MTCR"
    ]
    form_mtcr_entries = [
        regime_entry.attrs["value"]
        for regime_entry in soup.find("select", {"id": "mtcr_entries"}).find_all("option")
        if "selected" in regime_entry.attrs
    ]
    assert edit_mtcr_good_regimes == form_mtcr_entries

    edit_wassenaar_good_regimes = [
        entry["pk"] for entry in edit_good["regime_entries"] if entry["subsection"]["regime"]["name"] == "WASSENAAR"
    ]
    form_wassenaar_entries = [
        regime_entry.attrs["value"]
        for regime_entry in soup.find_all("input", {"name": "wassenaar_entries"})
        if "checked" in regime_entry.attrs
    ]
    assert edit_wassenaar_good_regimes == form_wassenaar_entries

    edit_nsg_good_regimes = [
        entry["pk"] for entry in edit_good["regime_entries"] if entry["subsection"]["regime"]["name"] == "NSG"
    ]
    form_nsg_entries = [
        regime_entry.attrs["value"]
        for regime_entry in soup.find("select", {"id": "nsg_entries"}).find_all("option")
        if "selected" in regime_entry.attrs
    ]
    assert edit_nsg_good_regimes == form_nsg_entries

    edit_cwc_good_regimes = [
        entry["pk"] for entry in edit_good["regime_entries"] if entry["subsection"]["regime"]["name"] == "CWC"
    ]
    form_cwc_entries = [
        regime_entry.attrs["value"]
        for regime_entry in soup.find_all("input", {"name": "cwc_entries"})
        if "checked" in regime_entry.attrs
    ]
    assert edit_cwc_good_regimes == form_cwc_entries

    edit_ag_good_regimes = [
        entry["pk"] for entry in edit_good["regime_entries"] if entry["subsection"]["regime"]["name"] == "AG"
    ]
    form_ag_entries = [
        regime_entry.attrs["value"]
        for regime_entry in soup.find_all("input", {"name": "ag_entries"})
        if "checked" in regime_entry.attrs
    ]
    assert edit_ag_good_regimes == form_ag_entries

    # Check report summary TODO: - uncomment once work to load report_summaries is done
    # assert edit_good["report_summary_subject"] == soup.find("form").find(id="report_summary_subject").attrs["value"]
    # assert edit_good["report_summary_prefix"] == soup.find("form").find(id="report_summary_prefix").attrs["value"]

    # Check comments
    assert edit_good["comment"] == soup.find("form").find(id="id_comment").text.strip()

    response = authorized_client.post(
        url,
        data={
            "report_summary_subject": report_summary_subject["id"],
            "does_not_have_control_list_entries": True,
            "comment": "test",
            "regimes": ["NONE"],
        },
    )

    # Check response and API payload
    assert response.status_code == 302
    assert requests_mock.last_request.json() == {
        "control_list_entries": [],
        "report_summary_subject": report_summary_subject["id"],
        "report_summary_prefix": "",
        "comment": "test",
        "current_object": "6daad1c3-cf97-4aad-b711-d5c9a9f4586e",
        "objects": ["6a7fc61f-698b-46b6-9876-6ac0fddfb1a2"],
        "is_good_controlled": False,
        "regime_entries": [],
    }


def test_form_no_regime_entries(
    authorized_client,
    url,
    data_standard_case,
    requests_mock,
    mock_cle_post,
    mock_control_list_entries,
    mock_precedents_api,
    report_summary_subject,
):
    """
    Tests the submission of a valid form only. More tests on the form itself are in test_forms.py
    """
    # Remove assessment from a good
    good = data_standard_case["case"]["data"]["goods"][0]
    good["is_good_controlled"] = None
    good["control_list_entries"] = []
    del good["regime_entries"]
    edit_good = data_standard_case["case"]["data"]["goods"][1]
    edit_good["control_list_entries"] = [{"rating": "ML1"}, {"rating": "ML1a"}]
    del edit_good["regime_entries"]
    # Get the edit form
    response = authorized_client.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    # Check if the form fields contain sane values
    edit_good = data_standard_case["case"]["data"]["goods"][1]

    # Check control list entries
    edit_good_cle = [cle["rating"] for cle in edit_good["control_list_entries"]]
    form_cle = [
        cle.attrs["value"]
        for cle in soup.find("select", {"id": "control_list_entries"}).find_all("option")
        if "selected" in cle.attrs
    ]
    assert edit_good_cle == form_cle

    # Check regimes
    form_mtcr_entries = [
        cle.attrs["value"]
        for cle in soup.find("select", {"id": "mtcr_entries"}).find_all("option")
        if "selected" in cle.attrs
    ]
    assert [] == form_mtcr_entries

    # Check report summary
    # assert edit_good["report_summary"] == soup.find("form").find(id="report_summary").attrs["value"]

    # Check comments
    assert edit_good["comment"] == soup.find("form").find(id="id_comment").text.strip()

    response = authorized_client.post(
        url,
        data={
            "report_summary_subject": report_summary_subject["id"],
            "does_not_have_control_list_entries": True,
            "comment": "test",
            "regimes": ["NONE"],
        },
    )

    # Check response and API payload
    assert response.status_code == 302
    assert requests_mock.last_request.json() == {
        "control_list_entries": [],
        "report_summary_subject": report_summary_subject["id"],
        "report_summary_prefix": "",
        "comment": "test",
        "current_object": "6daad1c3-cf97-4aad-b711-d5c9a9f4586e",
        "objects": ["6a7fc61f-698b-46b6-9876-6ac0fddfb1a2"],
        "is_good_controlled": False,
        "regime_entries": [],
    }


@pytest.mark.parametrize(
    "regimes_form_data, regime_entries",
    (
        (
            {"regimes": ["NONE"]},
            [],
        ),
        (
            {"regimes": ["MTCR"], "mtcr_entries": ["c760976f-fd14-4356-9f23-f6eaf084475d"]},
            ["c760976f-fd14-4356-9f23-f6eaf084475d"],
        ),
        (
            {"regimes": ["WASSENAAR"], "wassenaar_entries": ["d73d0273-ef94-4951-9c51-c291eba949a0"]},
            ["d73d0273-ef94-4951-9c51-c291eba949a0"],
        ),
        (
            {"regimes": ["NSG"], "nsg_entries": ["3d7c6324-a1e0-49fc-9d9e-89f3571144bc"]},
            ["3d7c6324-a1e0-49fc-9d9e-89f3571144bc"],
        ),
        (
            {"regimes": ["CWC"], "cwc_entries": ["af07fed6-3e27-48b3-a4f1-381c005c63d3"]},
            ["af07fed6-3e27-48b3-a4f1-381c005c63d3"],
        ),
        (
            {"regimes": ["AG"], "ag_entries": ["95274b74-f644-43a1-ad9b-3a69636c8597"]},
            ["95274b74-f644-43a1-ad9b-3a69636c8597"],
        ),
        (
            {
                "regimes": ["WASSENAAR", "MTCR", "NSG", "CWC", "AG"],
                "mtcr_entries": ["c760976f-fd14-4356-9f23-f6eaf084475d"],
                "wassenaar_entries": ["d73d0273-ef94-4951-9c51-c291eba949a0"],
                "nsg_entries": ["3d7c6324-a1e0-49fc-9d9e-89f3571144bc"],
                "cwc_entries": ["af07fed6-3e27-48b3-a4f1-381c005c63d3"],
                "ag_entries": ["95274b74-f644-43a1-ad9b-3a69636c8597"],
            },
            [
                "c760976f-fd14-4356-9f23-f6eaf084475d",
                "d73d0273-ef94-4951-9c51-c291eba949a0",
                "3d7c6324-a1e0-49fc-9d9e-89f3571144bc",
                "af07fed6-3e27-48b3-a4f1-381c005c63d3",
                "95274b74-f644-43a1-ad9b-3a69636c8597",
            ],
        ),
    ),
)
def test_form_regime_entries(
    authorized_client,
    url,
    data_standard_case,
    requests_mock,
    mock_cle_post,
    mock_control_list_entries,
    mock_precedents_api,
    regimes_form_data,
    regime_entries,
    report_summary_subject,
):
    # Remove assessment from a good
    good = data_standard_case["case"]["data"]["goods"][0]
    good["is_good_controlled"] = None
    good["control_list_entries"] = []
    edit_good = data_standard_case["case"]["data"]["goods"][1]
    edit_good["control_list_entries"] = [{"rating": "ML1"}, {"rating": "ML1a"}]

    response = authorized_client.post(
        url,
        data={
            "report_summary_subject": report_summary_subject["id"],
            "does_not_have_control_list_entries": True,
            "comment": "test",
            **regimes_form_data,
        },
    )

    # Check response and API payload
    assert response.status_code == 302, response.context["form"].errors
    assert requests_mock.last_request.json() == {
        "control_list_entries": [],
        "report_summary_subject": report_summary_subject["id"],
        "report_summary_prefix": "",
        "comment": "test",
        "current_object": "6daad1c3-cf97-4aad-b711-d5c9a9f4586e",
        "objects": ["6a7fc61f-698b-46b6-9876-6ac0fddfb1a2"],
        "is_good_controlled": False,
        "regime_entries": regime_entries,
    }


def test_control_list_suggestions_json(
    authorized_client,
    url,
    requests_mock,
    mock_control_list_entries,
    mock_precedents_api,
    mocker,
    data_standard_case,
):
    good = data_standard_case["case"]["data"]["goods"][0]
    good["is_good_controlled"] = None
    good["control_list_entries"] = []
    good["firearm_details"]["year_of_manufacture"] = "1930"

    mock_get_cle_suggestions_json = mocker.patch("caseworker.tau.views.get_cle_suggestions_json")
    mock_get_cle_suggestions_json.return_value = {"mock": "suggestion"}

    response = authorized_client.get(url)
    assert response.context["cle_suggestions_json"] == {"mock": "suggestion"}
