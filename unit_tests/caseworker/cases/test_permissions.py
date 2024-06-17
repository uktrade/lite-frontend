import pytest
import re
from core import client

from bs4 import BeautifulSoup
from django.urls import reverse


mock_gov_user_id = "2a43805b-c082-47e7-9188-c8b3e1a83cb0"  # /PS-IGNORE


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


@pytest.mark.parametrize(
    "id_element_name, is_user_case_advisor, id_element_name_visible",
    (
        ["link-change-status", True, True],
        ["link-change-status", False, False],
        ["link-change-queues", True, True],
        ["link-change-queues", False, False],
    ),
)
def test_permission_summary_change_links(
    authorized_client,
    data_queue,
    mock_gov_user,
    data_standard_case,
    id_element_name,
    is_user_case_advisor,
    id_element_name_visible,
):
    url = reverse("cases:case", kwargs={"queue_pk": data_queue["id"], "pk": data_standard_case["case"]["id"]})
    if is_user_case_advisor:
        data_standard_case["case"]["case_officer"] = mock_gov_user["user"]
    response = authorized_client.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    id_html_find_result = soup.find(id=id_element_name)
    if id_element_name_visible:
        assert id_html_find_result
    else:
        assert id_html_find_result is None


@pytest.mark.parametrize(
    "id_element_name, is_user_case_advisor, id_element_name_visible",
    (
        ["button-done", True, True],
        ["button-done", False, False],
    ),
)
def test_permission_move_case_forward_done_button(
    mock_status_properties,
    mock_queue,
    data_queue,
    mock_gov_user,
    authorized_client,
    data_standard_case,
    id_element_name,
    is_user_case_advisor,
    id_element_name_visible,
):
    url = reverse("cases:case", kwargs={"queue_pk": data_queue["id"], "pk": data_standard_case["case"]["id"]})
    if is_user_case_advisor:
        data_standard_case["case"]["case_officer"] = mock_gov_user["user"]
    mock_status_properties["is_terminal"] = True
    data_queue["is_system_queue"] = False
    mock_queue.return_value = data_queue
    response = authorized_client.get(url)

    soup = BeautifulSoup(response.content, "html.parser")
    id_html_find_result = soup.find(id=id_element_name)
    if id_element_name_visible:
        assert id_html_find_result
    else:
        assert id_html_find_result is None


@pytest.fixture
def mock_regime_entries_get(requests_mock, wassenaar_regime_entry):
    regime_entries_url = client._build_absolute_uri("/static/regimes/entries/")
    requests_mock.get(
        re.compile(f"{regime_entries_url}ag|cwc|mtcr|nsg|wassenaar"),
        json=[wassenaar_regime_entry],
    )


@pytest.mark.parametrize(
    "view_name, is_user_case_officer, is_user_assigned",
    (
        ["cases:case", False, False],
        ["cases:activities:notes-and-timeline", False, False],
        ["cases:advice_view", False, False],
        ["cases:tau:home", False, False],
        ["cases:case", True, False],
        ["cases:activities:notes-and-timeline", True, False],
        ["cases:advice_view", True, False],
        ["cases:tau:home", True, False],
        ["cases:case", False, True],
        ["cases:activities:notes-and-timeline", False, True],
        ["cases:advice_view", False, True],
        ["cases:tau:home", False, True],
    ),
)
def test_warning_renders_when_expected(
    authorized_client,
    data_queue,
    mock_gov_user,
    mock_denial_reasons,
    mock_control_list_entries_get,
    mock_regime_entries_get,
    mock_precedents_api,
    data_standard_case,
    view_name,
    is_user_case_officer,
    is_user_assigned,
    requests_mock,
    mock_gov_users,
):
    if is_user_case_officer:
        data_standard_case["case"]["case_officer"] = mock_gov_user["user"]
    elif is_user_assigned:
        data_standard_case["case"]["assigned_users"] = {data_queue["name"]: [mock_gov_user["user"]]}
    else:
        data_standard_case["case"]["case_officer"] = None
        data_standard_case["case"]["assigned_users"] = {}
    requests_mock.get(
        client._build_absolute_uri(f"/gov-users/"),
        json={
            "results": mock_gov_users,
        },
    )
    url = reverse(view_name, kwargs={"queue_pk": data_queue["id"], "pk": data_standard_case["case"]["id"]})
    response = authorized_client.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    if is_user_case_officer or is_user_assigned:
        assert not soup.find(id="allocation-warning")
    else:
        assert soup.find(id="allocation-warning")
