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


@pytest.fixture
def mock_regimes_get(requests_mock):
    url = client._build_absolute_uri(f"/static/regimes/entries/")
    return requests_mock.get(
        url=url,
        json=[
            {
                "pk": "d73d0273-ef94-4951-9c51-c291eba949a0",
                "name": "WASSENAAR",
            },
            {
                "pk": "c760976f-fd14-4356-9f23-f6eaf084475d",
                "name": "MTCR",
            },
            {
                "pk": "af07fed6-3e27-48b3-a4f1-381c005c63d3",
                "name": "CWC",
            },
            {
                "pk": "3d7c6324-a1e0-49fc-9d9e-89f3571144bc",
                "name": "NSG",
            },
            {
                "pk": "95274b74-f644-43a1-ad9b-3a69636c8597",
                "name": "AG",
            },
        ],
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
    mock_regimes_get,
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
        "cases:tau:multiple_edit",
        kwargs={"queue_pk": data_queue["id"], "pk": data_standard_case["case"]["id"]},
    )


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
        for cle in soup.find("select", {"id": "id_form-0-control_list_entries"}).find_all("option")
        if "selected" in cle.attrs
    ]
    assert edit_good_cle == form_cle

    # Check regimes
    form_regimes = [
        regime.get_text()
        for regime in soup.find(id="id_form-0-regimes").find_all("option")
        if "selected" in regime.attrs
    ]
    assert form_regimes == ["WASSENAAR", "MTCR", "CWC", "NSG", "AG"]

    form_regimes_values = [regime.attrs["value"] for regime in soup.find(id="id_form-0-regimes").find_all("option")]

    edit_wassenaar_good_regimes = [
        entry["pk"] for entry in edit_good["regime_entries"] if entry["subsection"]["regime"]["name"] == "WASSENAAR"
    ]
    edit_mtcr_good_regimes = [
        entry["pk"] for entry in edit_good["regime_entries"] if entry["subsection"]["regime"]["name"] == "MTCR"
    ]
    edit_cwc_good_regimes = [
        entry["pk"] for entry in edit_good["regime_entries"] if entry["subsection"]["regime"]["name"] == "CWC"
    ]
    edit_nsg_good_regimes = [
        entry["pk"] for entry in edit_good["regime_entries"] if entry["subsection"]["regime"]["name"] == "NSG"
    ]
    edit_ag_good_regimes = [
        entry["pk"] for entry in edit_good["regime_entries"] if entry["subsection"]["regime"]["name"] == "AG"
    ]

    edit_regimes = (
        edit_wassenaar_good_regimes
        + edit_mtcr_good_regimes
        + edit_cwc_good_regimes
        + edit_nsg_good_regimes
        + edit_ag_good_regimes
    )

    assert edit_regimes == form_regimes_values

    # Check report summary
    assert (
        edit_good["report_summary_prefix"]["id"]
        == soup.find(id="div_id_form-0-report_summary_prefix").find("input").attrs["value"]
    )
    assert (
        edit_good["report_summary_subject"]["id"]
        == soup.find(id="div_id_form-0-report_summary_subject").find("input").attrs["value"]
    )

    # Check comments
    assert edit_good["comment"] == soup.find(id="div_id_form-0-comment").find("textarea").text.strip()

    good_id = soup.find(id="id_form-0-id").attrs["value"]
    data = {
        "form-TOTAL_FORMS": 1,
        "form-INITIAL_FORMS": 1,
        "form-MIN_NUM_FORMS": 0,
        "form-MAX_NUM_FORMS": 1000,
        "form-TOTAL_FORMS": 1,
        "form-0-id": good_id,
        "form-0-report_summary_subject": report_summary_subject["id"],
        "form-0-control_list_entries": [],
        "form-0-comment": "test",
        "form-0-refer_to_ncsc": False,
    }
    response = authorized_client.post(
        url,
        data=data,
    )

    # Check response and API payload
    assert response.status_code == 302
    assert mock_assessment_put.last_request.json() == [
        {
            "id": good_id,
            "is_good_controlled": False,
            "control_list_entries": [],
            "regime_entries": [],
            "report_summary_prefix": "",
            "report_summary_subject": "b0849a92-4611-4e5b-b076-03562b138fb5",
            "comment": "test",
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
    good["regime_entries"] = []
    edit_good = data_standard_case["case"]["data"]["goods"][1]
    edit_good["control_list_entries"] = [{"rating": "ML1"}, {"rating": "ML1a"}]
    edit_good["regime_entries"] = []

    # Get the edit form
    response = authorized_client.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    # Check if the form fields contain sane values
    edit_good = data_standard_case["case"]["data"]["goods"][1]

    # Check control list entries
    edit_good_cle = [cle["rating"] for cle in edit_good["control_list_entries"]]
    form_cle = [
        cle.attrs["value"]
        for cle in soup.find("select", {"id": "id_form-0-control_list_entries"}).find_all("option")
        if "selected" in cle.attrs
    ]
    assert edit_good_cle == form_cle

    # Check regimes
    form_regimes = [
        regime.get_text()
        for regime in soup.find(id="id_form-0-regimes").find_all("option")
        if "selected" in regime.attrs
    ]
    assert [] == form_regimes

    # Check report summary
    assert (
        edit_good["report_summary_prefix"]["id"]
        == soup.find(id="div_id_form-0-report_summary_prefix").find("input").attrs["value"]
    )
    assert (
        edit_good["report_summary_subject"]["id"]
        == soup.find(id="div_id_form-0-report_summary_subject").find("input").attrs["value"]
    )

    # Check comments
    assert edit_good["comment"] == soup.find(id="div_id_form-0-comment").find("textarea").text.strip()

    good_id = soup.find(id="id_form-0-id").attrs["value"]
    data = {
        "form-TOTAL_FORMS": 1,
        "form-INITIAL_FORMS": 1,
        "form-MIN_NUM_FORMS": 0,
        "form-MAX_NUM_FORMS": 1000,
        "form-TOTAL_FORMS": 1,
        "form-0-id": good_id,
        "form-0-report_summary_subject": report_summary_subject["id"],
        "form-0-control_list_entries": [],
        "form-0-comment": "test",
        "form-0-refer_to_ncsc": False,
    }

    response = authorized_client.post(
        url,
        data=data,
    )

    # Check response and API payload
    assert response.status_code == 302
    assert mock_assessment_put.last_request.json() == [
        {
            "id": "6daad1c3-cf97-4aad-b711-d5c9a9f4586e",
            "is_good_controlled": False,
            "control_list_entries": [],
            "regime_entries": [],
            "report_summary_prefix": "",
            "report_summary_subject": "b0849a92-4611-4e5b-b076-03562b138fb5",
            "comment": "test",
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

    data = {
        "form-TOTAL_FORMS": 1,
        "form-INITIAL_FORMS": 1,
        "form-MIN_NUM_FORMS": 0,
        "form-MAX_NUM_FORMS": 1000,
        "form-TOTAL_FORMS": 1,
        "form-0-id": good["id"],
        "form-0-report_summary_subject": report_summary_subject["id"],
        "form-0-control_list_entries": [],
        "form-0-comment": "test",
        "form-0-refer_to_ncsc": False,
        "form-0-regimes": regime_entries,
    }

    response = authorized_client.post(
        url,
        data=data,
    )

    # Check response and API payload
    assert response.status_code == 302, response.context["form"].errors

    assert mock_assessment_put.last_request.json() == [
        {
            "id": good["id"],
            "is_good_controlled": False,
            "control_list_entries": [],
            "regime_entries": regime_entries,
            "report_summary_prefix": "",
            "report_summary_subject": "b0849a92-4611-4e5b-b076-03562b138fb5",
            "comment": "test",
            "is_ncsc_military_information_security": False,
        }
    ]


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
            == soup.find(id="div_id_form-0-report_summary_subject").find("input").attrs["value"]
        )
    else:
        assert soup.find(id="div_id_form-0-report_summary_subject").find("input").attrs.get("value") is None
    if prefix:
        assert (
            edit_good["report_summary_prefix"]["id"]
            == soup.find(id="div_id_form-0-report_summary_prefix").find("input").attrs["value"]
        )
    else:
        assert soup.find(id="div_id_form-0-report_summary_prefix").find("input").attrs.get("value") is None


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


def test_multiple_edit(
    authorized_client,
    url,
    data_standard_case,
    requests_mock,
    mock_assessment_put,
    mock_control_list_entries,
    mock_precedents_api,
    report_summary_subject,
    assign_user_to_case,
    mock_gov_user,
):
    assign_user_to_case(mock_gov_user, data_standard_case)

    good_1 = data_standard_case["case"]["data"]["goods"][0]
    good_2 = data_standard_case["case"]["data"]["goods"][1]

    data = {
        "form-TOTAL_FORMS": 2,
        "form-INITIAL_FORMS": 2,
        "form-MIN_NUM_FORMS": 0,
        "form-MAX_NUM_FORMS": 1000,
        "form-TOTAL_FORMS": 2,
        "form-0-id": good_1["id"],
        "form-0-report_summary_subject": report_summary_subject["id"],
        "form-0-control_list_entries": [],
        "form-0-comment": "test_1",
        "form-0-refer_to_ncsc": False,
        "form-1-id": good_2["id"],
        "form-1-report_summary_subject": report_summary_subject["id"],
        "form-1-control_list_entries": [],
        "form-1-comment": "test_2",
        "form-1-refer_to_ncsc": False,
    }
    response = authorized_client.post(
        url,
        data=data,
    )
    # Check response and API payload
    assert response.status_code == 302
    assert mock_assessment_put.last_request.json() == [
        {
            "id": good_1["id"],
            "is_good_controlled": False,
            "control_list_entries": [],
            "regime_entries": [],
            "report_summary_prefix": "",
            "report_summary_subject": report_summary_subject["id"],
            "comment": "test_1",
            "is_ncsc_military_information_security": False,
        },
        {
            "id": good_2["id"],
            "is_good_controlled": False,
            "control_list_entries": [],
            "regime_entries": [],
            "report_summary_prefix": "",
            "report_summary_subject": report_summary_subject["id"],
            "comment": "test_2",
            "is_ncsc_military_information_security": False,
        },
    ]
