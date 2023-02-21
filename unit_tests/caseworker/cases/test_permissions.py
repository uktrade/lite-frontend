import pytest
from django.urls import reverse

import rules
from bs4 import BeautifulSoup
from django.urls import reverse


mock_gov_user_id = "2a43805b-c082-47e7-9188-c8b3e1a83cb0"


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
        ["link-change-review-date", True, True],
        ["link-change-review-date", False, False],
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
    data_standard_case["case_officer"] = mock_gov_user
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
    gov_user,
    authorized_client,
    data_standard_case,
    id_element_name,
    is_user_case_advisor,
    id_element_name_visible,
):
    url = reverse("cases:case", kwargs={"queue_pk": data_queue["id"], "pk": data_standard_case["case"]["id"]})
    # We are changing rule here since mocking doesn't seem straight forward
    data_standard_case["case_officer"] = gov_user
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
