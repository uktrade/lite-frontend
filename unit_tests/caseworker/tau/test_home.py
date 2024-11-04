import pytest

from bs4 import BeautifulSoup

from django.urls import reverse

from core import client
from caseworker.tau import views


@pytest.fixture
def mock_report_summary_subject(requests_mock, report_summary_subject):
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


@pytest.fixture(autouse=True)
def setup(
    mock_queue,
    mock_case,
    mock_mtcr_entries_get,
    mock_wassenaar_entries_get,
    mock_nsg_entries_get,
    mock_cwc_entries_get,
    mock_ag_entries_get,
    mock_application_good_documents,
    mock_report_summary_subject,
):
    yield


@pytest.fixture
def url(data_standard_case):
    return reverse(
        "cases:tau:home",
        kwargs={"queue_pk": "1b926457-5c9e-4916-8497-51886e51863a", "pk": data_standard_case["case"]["id"]},
    )


@pytest.fixture()
def gov_user():
    return {
        "user": {
            "id": "2a43805b-c082-47e7-9188-c8b3e1a83cb0",
            "team": {
                "id": "211111b-c111-11e1-1111-1111111111a",
                "name": "Test",
                "alias": "TEST_1",
            },
        }
    }


def get_cells(soup, table_id):
    return ["\n".join([t.strip() for t in td.text.strip().split("\n")]) for td in soup.find(id=table_id).find_all("td")]


def test_tau_home_auth(authorized_client, url, mock_control_list_entries, mock_precedents_api):
    """GET /tau should return 200 with an authorised client"""
    response = authorized_client.get(url)
    assert response.status_code == 200


def test_home_unassessessed_goods_with_precedents(
    authorized_client,
    settings,
    url,
    data_queue,
    data_standard_case,
    mock_control_list_entries,
    mock_precedents_api,
    mock_gov_user,
    assign_user_to_case,
):
    # Remove assessment from a good
    good = data_standard_case["case"]["data"]["goods"][0]
    good["is_good_controlled"] = None
    good["control_list_entries"] = []
    good["firearm_details"]["year_of_manufacture"] = "1930"

    assign_user_to_case(mock_gov_user, data_standard_case)
    response = authorized_client.get(url)
    assert response.status_code == 200
    assert response.context["unassessed_goods_with_precedents"] == True


def test_home_unassessessed_goods_without_precedents(
    authorized_client,
    settings,
    url,
    data_queue,
    data_standard_case,
    mock_control_list_entries,
    mock_good_precedent_endpoint_empty,
    mock_gov_user,
    assign_user_to_case,
):
    # Remove assessment from a good
    good = data_standard_case["case"]["data"]["goods"][0]
    good["is_good_controlled"] = None
    good["control_list_entries"] = []
    good["firearm_details"]["year_of_manufacture"] = "1930"

    assign_user_to_case(mock_gov_user, data_standard_case)
    response = authorized_client.get(url)
    assert response.status_code == 200
    assert response.context["unassessed_goods_with_precedents"] == False


def test_home_content(
    authorized_client,
    settings,
    url,
    data_queue,
    data_standard_case,
    mock_control_list_entries,
    mock_precedents_api,
    mock_gov_user,
    assign_user_to_case,
):
    """GET /tau would return a case info panel"""
    assign_user_to_case(mock_gov_user, data_standard_case)

    # Remove assessment from a good
    good = data_standard_case["case"]["data"]["goods"][0]
    good["is_good_controlled"] = None
    good["control_list_entries"] = []
    good["firearm_details"]["year_of_manufacture"] = "1930"

    response = authorized_client.get(url)
    assert response.status_code == 200

    # Test elements of case info panel
    soup = BeautifulSoup(response.content, "html.parser")
    element = soup.find("p", class_="govuk-notification-banner__heading")
    assert element.get_text() == "1 product going from Great Britain to Abu Dhabi and United Kingdom."

    good_2_id = data_standard_case["case"]["data"]["goods"][1]["id"]
    assert get_cells(soup, f"good-{good_2_id}") == [
        "Selected",
        "2.",
        "p2",
        "ML8a,ML9a",
        "No",
        "w-1\n\nmtcr-1\n\nnsg-1\n\ncwc-1\n\nag-1",
        "",
        "No",
        "test assesment note",
    ]

    # "current_user" passed in from caseworker context processor
    # used to test rule "can_user_change_case"
    assert response.context["current_user"] == mock_gov_user["user"]


def test_home_content_without_allocated_user_hides_clear_assessment_button(
    authorized_client,
    url,
    data_queue,
    data_standard_case,
    mock_control_list_entries,
    mock_precedents_api,
    mock_gov_user,
):
    # Remove assessment from a good
    good = data_standard_case["case"]["data"]["goods"][0]
    good["is_good_controlled"] = None
    good["control_list_entries"] = []
    good["firearm_details"]["year_of_manufacture"] = "1930"

    response = authorized_client.get(url)
    assert response.status_code == 200

    # Test elements of case info panel
    soup = BeautifulSoup(response.content, "html.parser")
    assert soup.find(id="clear-assessments-button") is None


def test_assessed_products_form(
    authorized_client,
    settings,
    url,
    data_queue,
    data_standard_case,
    mock_control_list_entries,
    mock_precedents_api,
    mock_gov_user,
    assign_user_to_case,
):
    assign_user_to_case(mock_gov_user, data_standard_case)

    good = data_standard_case["case"]["data"]["goods"][0]
    good["is_good_controlled"] = {"key": "True", "value": "Yes"}
    good["is_ncsc_military_information_security"] = False

    good = data_standard_case["case"]["data"]["goods"][1]
    good["is_good_controlled"] = {"key": "False", "value": "No"}
    good["is_ncsc_military_information_security"] = True

    response = authorized_client.get(url)
    assert response.status_code == 200
    # Test elements of case info panel
    soup = BeautifulSoup(response.content, "html.parser")
    assessed_products_form = soup.find("form", {"class": "assessment-formset"})
    choose_multiple_edit_url = reverse(
        "cases:tau:choose_multiple_edit",
        kwargs={
            "queue_pk": "1b926457-5c9e-4916-8497-51886e51863a",
            "pk": data_standard_case["case"]["id"],
        },
    )
    assert assessed_products_form.attrs["action"] == choose_multiple_edit_url
    good = data_standard_case["case"]["data"]["goods"][0]
    all_td_elems = assessed_products_form.find("tbody").find_all("td")
    all_td_text = [td_elem.text.strip().strip().replace("\n", "") for td_elem in all_td_elems]
    assert all_td_text == [
        "Selected",
        "1.",
        "p1",
        "ML8a,ML9a",
        "Yes",
        "w-1    mtcr-1    nsg-1    cwc-1    ag-1    T1",
        "firearms (2)",
        "No",
        "test comment",
        "Selected",
        "2.",
        "p2",
        "ML8a,ML9a",
        "No",
        "w-1    mtcr-1    nsg-1    cwc-1    ag-1",
        "",
        "Yes",
        "test assesment note",
    ]

    all_a_elems = assessed_products_form.find("tbody").find_all("a", href=True)
    expected_good_urls = [
        reverse(
            "cases:good",
            kwargs={
                "queue_pk": "00000000-0000-0000-0000-000000000001",
                "pk": data_standard_case["case"]["id"],
                "good_pk": good["id"],
            },
        )
        for good in data_standard_case["case"]["data"]["goods"]
    ]
    actual_good_urls = [a_elem.attrs["href"] for a_elem in all_a_elems]
    assert expected_good_urls == actual_good_urls

    assert soup.find(id="clear-assessments-button") is not None


def test_tau_home_noauth(client, url):
    """GET /tau should return 302 with an unauthorised client"""
    response = client.get(url)
    assert response.status_code == 302


def test_form_without_allocated_user_hides_submit_button(
    authorized_client,
    url,
    data_standard_case,
    mock_control_list_entries,
    mock_precedents_api,
    report_summary_subject,
    assign_user_to_case,
    mock_gov_user,
):
    # Remove assessment from a good
    good = data_standard_case["case"]["data"]["goods"][0]
    good["is_good_controlled"] = None
    good["control_list_entries"] = []
    # unassessed products should have 1 entry
    response = authorized_client.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    unassessed_products = soup.find(id="unassessed-products").find_all("input")
    assert len(unassessed_products) == 1
    assert unassessed_products[0].attrs["value"] == good["id"]

    assert soup.find(id="submit-id-submit") is None


def test_form(
    authorized_client,
    url,
    data_standard_case,
    requests_mock,
    mock_control_list_entries,
    mock_precedents_api,
    report_summary_subject,
    assign_user_to_case,
    mock_gov_user,
    mock_assessment_put,
):
    """
    Tests the submission of a valid form only. More tests on the form itself are in test_forms.py
    """
    assign_user_to_case(mock_gov_user, data_standard_case)

    # Remove assessment from a good
    good = data_standard_case["case"]["data"]["goods"][0]
    good["is_good_controlled"] = None
    good["control_list_entries"] = []
    response = authorized_client.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    unassessed_products = soup.find(id="unassessed-products").find_all("input")
    assert len(unassessed_products) == 1
    assert unassessed_products[0].attrs["value"] == good["id"]

    assert soup.find(id="submit-id-submit") is not None

    data = {
        "report_summary_subject": report_summary_subject["id"],
        "goods": [good["id"]],
        "does_not_have_control_list_entries": True,
        "regimes": ["NONE"],
    }

    response = authorized_client.post(url, data=data)
    assert response.status_code == 302

    assert mock_assessment_put.last_request.json() == [
        {
            "control_list_entries": [],
            "report_summary_subject": report_summary_subject["id"],
            "report_summary_prefix": "",
            "comment": "",
            "id": "0bedd1c3-cf97-4aad-b711-d5c9a9f4586e",
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
    mock_control_list_entries,
    mock_precedents_api,
    regimes_form_data,
    regime_entries,
    report_summary_subject,
    mock_assessment_put,
):
    # Remove assessment from a good
    good = data_standard_case["case"]["data"]["goods"][0]
    good["is_good_controlled"] = None
    good["control_list_entries"] = []

    data = {
        "report_summary_subject": report_summary_subject["id"],
        "goods": [good["id"]],
        "does_not_have_control_list_entries": True,
        **regimes_form_data,
    }

    response = authorized_client.post(url, data=data)
    assert response.status_code == 302
    assert mock_assessment_put.last_request.json() == [
        {
            "control_list_entries": [],
            "report_summary_subject": report_summary_subject["id"],
            "report_summary_prefix": "",
            "comment": "",
            "id": "0bedd1c3-cf97-4aad-b711-d5c9a9f4586e",
            "is_good_controlled": False,
            "regime_entries": regime_entries,
            "is_ncsc_military_information_security": False,
        }
    ]


@pytest.mark.parametrize(
    "team_alias, team_name",
    (
        (views.TAU_ALIAS, "TAU"),
        ("Not TAU", "Some other team"),
    ),
)
def test_move_case_forward(
    requests_mock,
    authorized_client,
    url,
    data_standard_case,
    mock_control_list_entries,
    mock_precedents_api,
    gov_user,
    team_alias,
    team_name,
):
    """
    When all products has been assessed, we will get a move-case-forward form.
    """
    gov_user["user"]["team"]["name"] = team_name
    gov_user["user"]["team"]["alias"] = team_alias
    data_standard_case["case"]["case_officer"] = gov_user["user"]

    requests_mock.get(
        client._build_absolute_uri("/gov-users/2a43805b-c082-47e7-9188-c8b3e1a83cb0"),
        json=gov_user,
    )

    response = authorized_client.get(url)
    assert response.context["unassessed_goods"] == []

    soup = BeautifulSoup(response.content, "html.parser")
    forms = soup.find_all("form", {"class": "move-case-forward-form"})
    if team_alias == views.TAU_ALIAS:
        assert len(forms) == 1
        assert forms[0].attrs["action"] == reverse(
            "cases:tau:move_case_forward",
            kwargs={"queue_pk": "1b926457-5c9e-4916-8497-51886e51863a", "pk": data_standard_case["case"]["id"]},
        )
    else:
        assert len(forms) == 0


def test_control_list_suggestions_json(
    authorized_client,
    url,
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
    "is_user_case_advisor",
    [True, False],
)
def test_permission_move_case_forward_button(
    requests_mock,
    authorized_client,
    url,
    data_standard_case,
    mock_control_list_entries,
    mock_precedents_api,
    gov_user,
    is_user_case_advisor,
):
    gov_user["user"]["team"]["name"] = "TAU"
    gov_user["user"]["team"]["alias"] = views.TAU_ALIAS
    requests_mock.get(
        client._build_absolute_uri("/gov-users/2a43805b-c082-47e7-9188-c8b3e1a83cb0"),
        json=gov_user,
    )
    if is_user_case_advisor:
        data_standard_case["case"]["case_officer"] = gov_user["user"]
    response = authorized_client.get(url)

    soup = BeautifulSoup(response.content, "html.parser")
    forms = soup.find_all("form", {"class": "move-case-forward-form"})
    if is_user_case_advisor:
        assert len(forms) == 1
        assert forms[0].attrs["action"] == reverse(
            "cases:tau:move_case_forward",
            kwargs={"queue_pk": "1b926457-5c9e-4916-8497-51886e51863a", "pk": data_standard_case["case"]["id"]},
        )
    else:
        assert len(forms) == 0


def test_form_rendered_once(
    authorized_client,
    url,
    data_queue,
    data_standard_case,
    mock_control_list_entries,
    mock_precedents_api,
    mock_gov_user,
    assign_user_to_case,
):
    # This is to ensure that we only render our own form and suppress crispy
    # forms from rendering its own.
    assign_user_to_case(mock_gov_user, data_standard_case)

    # Remove assessment from a good
    good = data_standard_case["case"]["data"]["goods"][0]
    good["is_good_controlled"] = None
    good["control_list_entries"] = []
    good["firearm_details"]["year_of_manufacture"] = "1930"

    response = authorized_client.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    tau_form = soup.find(id="tau-form")
    assert tau_form is not None
    assert not tau_form.select("form")


def test_notification_banner_not_there_when_all_goods_assesed(
    authorized_client,
    url,
    data_queue,
    data_standard_case,
    mock_control_list_entries,
    mock_precedents_api,
    mock_gov_user,
    assign_user_to_case,
):
    """GET /tau would return a case info panel"""
    assign_user_to_case(mock_gov_user, data_standard_case)

    response = authorized_client.get(url)
    assert response.status_code == 200

    soup = BeautifulSoup(response.content, "html.parser")
    banner = soup.find("div", class_="tau-notification-banner")
    assert banner is None


def test_previous_assessments_anchors(
    authorized_client,
    url,
    data_queue,
    data_standard_case,
    mock_control_list_entries,
    mock_precedents_api,
    mock_gov_user,
):
    # Verify that assessment table has anchors for each good.

    # Remove assessment from a good
    good = data_standard_case["case"]["data"]["goods"][0]
    good["is_good_controlled"] = None
    good["control_list_entries"] = []
    good["firearm_details"]["year_of_manufacture"] = "1930"

    response = authorized_client.get(url)

    assert response.status_code == 200
    case_anchor_ids = {"good-" + good["id"] for good in data_standard_case["case"]["data"]["goods"]}

    soup = BeautifulSoup(response.content, "html.parser")
    # Elements with anchors (ids) in the format good-{{ goodonapplication_id }}
    anchor_ids = {
        element.attrs["id"] for element in soup.findAll("tr", id=lambda value: (value or "").startswith("good-"))
    }

    assert anchor_ids.issubset(case_anchor_ids)
