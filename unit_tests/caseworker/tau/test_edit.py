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


def test_form_without_allocated_user_hides_submit_button(
    authorized_client,
    url,
    data_standard_case,
    requests_mock,
    mock_assessment_put,
    mock_control_list_entries,
    mock_precedents_api,
    report_summary_prefix,
    report_summary_subject,
):
    # Remove assessment from a good
    good = data_standard_case["case"]["data"]["goods"][0]
    good["is_good_controlled"] = None
    good["control_list_entries"] = []
    edit_good = data_standard_case["case"]["data"]["goods"][1]
    edit_good["control_list_entries"] = [{"rating": "ML1"}, {"rating": "ML1a"}]
    # Get the edit form
    response = authorized_client.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    assert soup.find(id="submit-id-submit") is None


def test_form(
    authorized_client,
    url,
    data_standard_case,
    requests_mock,
    mock_assessment_put,
    mock_control_list_entries,
    mock_precedents_api,
    report_summary_prefix,
    report_summary_subject,
    assign_user_to_case,
    mock_gov_user,
):
    """
    Tests the submission of a valid form only. More tests on the form itself are in test_forms.py
    """
    # Remove assessment from a good
    assign_user_to_case(mock_gov_user, data_standard_case)

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
        for cle in soup.find("select", {"name": "control_list_entries"}).find_all("option")
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

    assert edit_good["report_summary_prefix"]["id"] == soup.find("form").find(id="report_summary_prefix").attrs["value"]
    assert (
        edit_good["report_summary_subject"]["id"] == soup.find("form").find(id="report_summary_subject").attrs["value"]
    )

    # Check comments
    assert edit_good["comment"] == soup.find("form").find(id="id_comment").text.strip()

    assert soup.find(id="submit-id-submit") is not None

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
    assert mock_assessment_put.last_request.json() == [
        {
            "control_list_entries": [],
            "report_summary_subject": report_summary_subject["id"],
            "report_summary_prefix": "",
            "comment": "test",
            "id": "6daad1c3-cf97-4aad-b711-d5c9a9f4586e",
            "is_good_controlled": False,
            "regime_entries": [],
            "is_ncsc_military_information_security": False,
        }
    ]


def test_form_no_regime_entries(
    authorized_client,
    url,
    data_standard_case,
    requests_mock,
    mock_assessment_put,
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
        for cle in soup.find("select", {"name": "control_list_entries"}).find_all("option")
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
    assert mock_assessment_put.last_request.json() == [
        {
            "control_list_entries": [],
            "report_summary_subject": report_summary_subject["id"],
            "report_summary_prefix": "",
            "comment": "test",
            "id": "6daad1c3-cf97-4aad-b711-d5c9a9f4586e",
            "is_good_controlled": False,
            "regime_entries": [],
            "is_ncsc_military_information_security": False,
        }
    ]


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
    mock_assessment_put,
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
    assert mock_assessment_put.last_request.json() == [
        {
            "control_list_entries": [],
            "report_summary_subject": report_summary_subject["id"],
            "report_summary_prefix": "",
            "comment": "test",
            "id": "6daad1c3-cf97-4aad-b711-d5c9a9f4586e",
            "is_good_controlled": False,
            "regime_entries": regime_entries,
            "is_ncsc_military_information_security": False,
        }
    ]


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


@pytest.mark.parametrize(
    "name, prefix, subject",
    (
        ("Both present", True, True),
        ("Prefix missing", False, True),
        ("Subject missing", True, False),
        ("Both missing", False, False),
    ),
)
def test_form_report_summary_conditions(
    name,
    authorized_client,
    url,
    data_standard_case,
    mock_assessment_put,
    mock_control_list_entries,
    mock_precedents_api,
    prefix,
    subject,
):
    """
    Tests the display of the report_summary prefix and subject in the Edit page
    """
    # Remove assessment from a good
    good = data_standard_case["case"]["data"]["goods"][0]
    good["is_good_controlled"] = None
    good["control_list_entries"] = []
    edit_good = data_standard_case["case"]["data"]["goods"][1]
    edit_good["control_list_entries"] = [{"rating": "ML1"}, {"rating": "ML1a"}]
    if not prefix:
        edit_good["report_summary_prefix"] = None
    if not subject:
        edit_good["report_summary_subject"] = None

    # Get the edit form
    response = authorized_client.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    if subject:
        assert (
            edit_good["report_summary_subject"]["id"]
            == soup.find("form").find(id="report_summary_subject").attrs["value"]
        )
    else:
        assert soup.find("form").find(id="report_summary_subject").attrs.get("value") is None
    if prefix:
        assert (
            edit_good["report_summary_prefix"]["id"]
            == soup.find("form").find(id="report_summary_prefix").attrs["value"]
        )
    else:
        assert soup.find("form").find(id="report_summary_prefix").attrs.get("value") is None


def test_form_only_rendered_once(
    authorized_client,
    url,
    data_standard_case,
    requests_mock,
    mock_assessment_put,
    mock_control_list_entries,
    mock_precedents_api,
    report_summary_prefix,
    report_summary_subject,
    assign_user_to_case,
    mock_gov_user,
):
    # This is to test a bug where we were rendering the form tag in the
    # template but not suppressing it when crispy forms was rendering the form
    # itself.
    # This caused malformed HTML to be rendered by the browser and resulted in
    # the submit button being rendered in the wrong place.

    assign_user_to_case(mock_gov_user, data_standard_case)

    good = data_standard_case["case"]["data"]["goods"][0]
    good["is_good_controlled"] = None
    good["control_list_entries"] = []
    edit_good = data_standard_case["case"]["data"]["goods"][1]
    edit_good["control_list_entries"] = [{"rating": "ML1"}, {"rating": "ML1a"}]
    # Get the edit form
    response = authorized_client.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    tau_form = soup.find(id="tau-form")
    assert tau_form is not None
    assert not tau_form.select("form")
