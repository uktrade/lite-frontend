import pytest
import uuid
import re

from bs4 import BeautifulSoup
from urllib import parse

from django.urls import reverse

from core import client

from caseworker.queues.forms import CaseAssignmentUsersForm, CaseAssignmentQueueForm
from caseworker.queues.views.case_assignments import CaseAssignmentsCaseAssigneeSteps

queue_pk = "59ef49f4-cf0c-4085-87b1-9ac6817b4ba6"

gov_user_id = "1f288b81-2c26-439f-ac32-2a43c8b1a5cb"  # /PS-IGNORE

example_return_to_url = "/example/endpoint"


@pytest.fixture(autouse=True)
def setup(
    mock_cases_search,
    mock_cases_search_head,
    authorized_client,
    queue_pk,
    mock_queue,
    mock_countries,
    mock_queues_list,
    mock_control_list_entries,
    mock_regime_entries,
    mock_empty_bookmarks,
):
    yield


@pytest.fixture
def mock_team_queue(requests_mock, data_queue):
    data_queue["is_system_queue"] = False
    url = client._build_absolute_uri("/queues/")
    yield requests_mock.get(url=re.compile(f"{url}.*/"), json=data_queue)


@pytest.fixture
def mock_cases_search_head(requests_mock):
    url = client._build_absolute_uri(f"/cases/")
    yield requests_mock.head(url=re.compile(f"{url}.*"), headers={"resource-count": "350"})


def test_case_assignment_case_office_no_user_selected(authorized_client, mock_gov_users):
    url = (
        reverse("queues:case_assignments_case_officer", kwargs={"pk": queue_pk})
        + f"?cases={str(uuid.uuid4())}&cases={str(uuid.uuid4())}"
    )
    data = {}
    response = authorized_client.post(url, data)

    assert response.status_code == 200
    assert response.context_data["form"].errors == {
        "users": ["Select a user to allocate as Licensing Unit case officer"]
    }


@pytest.fixture
def post_to_step_user_assignment_with_return_to(post_to_step_factory, user_assignment_url):
    user_assignment_url = user_assignment_url + f"&return_to={example_return_to_url}"
    return post_to_step_factory(user_assignment_url)


@pytest.fixture
def post_to_step_user_assignment_with_invalid_return_to(post_to_step_factory, user_assignment_url):
    user_assignment_url = user_assignment_url + "&return_to=http://www.evil.com"
    return post_to_step_factory(user_assignment_url)


def test_case_assignment_case_adviser_with_return_to(
    mock_gov_users,
    mock_team_queue,
    mock_put_assignments,
    post_to_step_user_assignment_with_return_to,
):
    data = {"users": [gov_user_id]}
    response = post_to_step_user_assignment_with_return_to(
        CaseAssignmentsCaseAssigneeSteps.SELECT_USERS,
        data,
    )
    assert response.status_code == 302
    assert response.url == example_return_to_url


def test_case_assignment_case_adviser_with_invalid_return_to(
    post_to_step_user_assignment_with_invalid_return_to,
):
    data = {"users": [gov_user_id]}
    response = post_to_step_user_assignment_with_invalid_return_to(
        CaseAssignmentsCaseAssigneeSteps.SELECT_USERS,
        data,
    )
    assert response.status_code == 403
    assert b"Invalid return_to parameter" in response.content


@pytest.fixture
def mock_put_case_case_officer(requests_mock):
    case_officer_put_url = client._build_absolute_uri("/cases/cases-update-case-officer/")
    return requests_mock.put(url=case_officer_put_url, json={})


def test_case_assignment_case_officer(authorized_client, requests_mock, mock_gov_users, mock_put_case_case_officer):
    cases_ids = [str(uuid.uuid4()), str(uuid.uuid4())]
    url = (
        reverse("queues:case_assignments_case_officer", kwargs={"pk": queue_pk})
        + f"?cases={cases_ids[0]}&cases={cases_ids[1]}"
    )

    data = {"users": gov_user_id}
    response = authorized_client.post(url, data)
    assert response.status_code == 302
    assert response.url == reverse("queues:cases", kwargs={"queue_pk": queue_pk})
    assert mock_put_case_case_officer.last_request.json() == {
        "gov_user_pk": gov_user_id,
        "case_ids": cases_ids,
    }


def test_case_assignment_case_officer_with_return_to(
    authorized_client, requests_mock, mock_gov_users, mock_put_case_case_officer
):
    cases_ids = [str(uuid.uuid4()), str(uuid.uuid4())]
    url = (
        reverse("queues:case_assignments_case_officer", kwargs={"pk": queue_pk})
        + f"?cases={cases_ids[0]}&cases={cases_ids[1]}&return_to={example_return_to_url}"
    )
    data = {"users": gov_user_id}
    response = authorized_client.post(url, data)
    assert response.status_code == 302
    assert response.url == example_return_to_url


def test_case_assignment_case_officer_with_invalid_return_to(authorized_client):
    cases_ids = [str(uuid.uuid4()), str(uuid.uuid4())]
    url = (
        reverse("queues:case_assignments_case_officer", kwargs={"pk": queue_pk})
        + f"?cases={cases_ids[0]}&cases={cases_ids[1]}&return_to=http://www.evil.com"
    )
    data = {"users": gov_user_id}
    response = authorized_client.post(url, data)
    assert response.status_code == 403
    assert b"Invalid return_to parameter" in response.content


@pytest.mark.parametrize(
    "user_role_assigned, expected_url_name",
    (
        ("CASE_ADVISOR", "case_assignments_assign_user"),
        ("LU_CASE_OFFICER", "case_assignments_case_officer"),
    ),
)
def test_case_assignment_select_role(authorized_client, mock_gov_user, user_role_assigned, expected_url_name):
    url_params = (
        f"?cases={str(uuid.uuid4())}&cases={str(uuid.uuid4())}&return_to={parse.quote(example_return_to_url, safe='')}"
    )

    url = reverse("queues:case_assignment_select_role", kwargs={"pk": queue_pk}) + url_params
    response = authorized_client.get(url)
    assert response.status_code == 200

    response = authorized_client.post(url, {"role": user_role_assigned})
    assert response.status_code == 302
    assert response.url == reverse(f"queues:{expected_url_name}", kwargs={"pk": queue_pk}) + url_params


def test_case_assignments_add_user_system_queue(
    authorized_client,
    data_queue,
    data_standard_case,
    data_assignment,
    mock_standard_case_with_assignments,
    mock_queue,
    mock_gov_users,
):

    case = data_standard_case
    url_base = reverse(
        "queues:case_assignments_assign_user",
        kwargs={
            "pk": data_queue["id"],
        },
    )
    url = f"{url_base}?cases={case['case']['id']}"
    response = authorized_client.get(url)
    assert response.status_code == 200
    context = response.context
    assert isinstance(context["form"], CaseAssignmentUsersForm)
    # Flow initiated from a system queue, so expect the SELECT_QUEUE step next
    assert context["wizard"]["steps"].next == CaseAssignmentsCaseAssigneeSteps.SELECT_QUEUE

    html = BeautifulSoup(response.content, "html.parser")
    assert "Who do you want to allocate as case adviser?" in html.find("h1").get_text()


@pytest.fixture
def mock_users_team_queues_list(requests_mock, gov_uk_user_id, data_queue):
    url = client._build_absolute_uri(f"/users/{gov_uk_user_id}/team-queues/")
    return requests_mock.get(url=url, json={"queues": [[data_queue["id"], "Some Queue"]]})


@pytest.fixture
def user_assignment_url(data_standard_case, data_queue):
    case = data_standard_case
    url_base = reverse("queues:case_assignments_assign_user", kwargs={"pk": data_queue["id"]})
    url = f"{url_base}?cases={case['case']['id']}"
    return url


@pytest.fixture
def post_to_step_user_assignment(post_to_step_factory, user_assignment_url):
    return post_to_step_factory(user_assignment_url)


def test_case_assignments_add_user_system_queue_submit_success(
    authorized_client,
    data_queue,
    data_standard_case,
    data_assignment,
    mock_standard_case_with_assignments,
    mock_queue,
    mock_gov_users,
    mock_put_assignments,
    mock_users_team_queues_list,
    mock_standard_case_ecju_queries,
    mock_standard_case_assigned_queues,
    mock_standard_case_documents,
    mock_standard_case_additional_contacts,
    mock_standard_case_activity_filters,
    post_to_step_user_assignment,
):
    data = {
        "users": [gov_user_id],
        "note": "foobar",
    }
    # POST step 1
    response = post_to_step_user_assignment(
        CaseAssignmentsCaseAssigneeSteps.SELECT_USERS,
        data,
    )
    assert response.status_code == 200
    context = response.context
    assert isinstance(context["form"], CaseAssignmentQueueForm)
    assert context["wizard"]["steps"].current == CaseAssignmentsCaseAssigneeSteps.SELECT_QUEUE

    html = BeautifulSoup(response.content, "html.parser")
    assert "Select a team queue to add the case to" in html.find("h1").get_text()

    data = {
        "queue": data_queue["id"],
    }
    # POST step 2
    response = post_to_step_user_assignment(
        CaseAssignmentsCaseAssigneeSteps.SELECT_QUEUE,
        data,
        follow=True,
    )
    assert response.status_code == 200
    assert response.redirect_chain[-1][0] == f"/queues/{data_queue['id']}/"
    messages = [str(msg) for msg in response.context["messages"]]
    expected_message = "Case adviser was added successfully"
    assert messages == [expected_message]
    assert mock_put_assignments.called
    assert mock_put_assignments.last_request.json() == {
        "case_assignments": [
            {
                "case_id": data_standard_case["case"]["id"],
                "users": [gov_user_id],
            }
        ],
        "note": "foobar",
        "remove_existing_assignments": False,
    }

    html = BeautifulSoup(response.content, "html.parser")
    assert expected_message in html.select("div.app-snackbar__content")[0].get_text()


def test_case_assignments_add_user_system_queue_submit_validation_error(
    authorized_client,
    data_queue,
    data_standard_case,
    data_assignment,
    mock_standard_case_with_assignments,
    mock_queue,
    mock_gov_users,
    mock_put_assignments,
    mock_users_team_queues_list,
    mock_standard_case_ecju_queries,
    mock_standard_case_assigned_queues,
    mock_standard_case_documents,
    mock_standard_case_additional_contacts,
    mock_standard_case_activity_filters,
    post_to_step_user_assignment,
):
    data = {
        "note": "foobar",
    }
    # POST step 1 - validation error
    response = post_to_step_user_assignment(
        CaseAssignmentsCaseAssigneeSteps.SELECT_USERS,
        data,
    )
    assert response.status_code == 200
    assert response.context["form"]["users"].errors == ["Select a user to allocate"]

    data = {
        "users": [gov_user_id],
        "note": "foobar",
    }
    # POST step 1 - valid
    response = post_to_step_user_assignment(
        CaseAssignmentsCaseAssigneeSteps.SELECT_USERS,
        data,
    )
    assert response.status_code == 200
    assert isinstance(response.context["form"], CaseAssignmentQueueForm)
    assert response.context["wizard"]["steps"].current == CaseAssignmentsCaseAssigneeSteps.SELECT_QUEUE

    html = BeautifulSoup(response.content, "html.parser")
    assert "Select a team queue to add the case to" in html.find("h1").get_text()

    data = {}
    # POST step 2
    response = post_to_step_user_assignment(
        CaseAssignmentsCaseAssigneeSteps.SELECT_QUEUE,
        data,
    )
    assert response.status_code == 200
    assert response.context["form"]["queue"].errors == ["Select a queue to add the case to"]


@pytest.fixture
def mock_put_assignments(requests_mock, data_queue, data_assignment):
    url = client._build_absolute_uri(f"/queues/{data_queue['id']}/case-assignments/")
    return requests_mock.put(url=url, json=data_assignment)


def test_case_assignments_add_user_team_queue(
    authorized_client,
    data_queue,
    data_standard_case,
    data_assignment,
    mock_standard_case_with_assignments,
    mock_team_queue,
    mock_gov_users,
):

    case = data_standard_case
    url_base = reverse("queues:case_assignments_assign_user", kwargs={"pk": data_queue["id"]})
    url = f"{url_base}?cases={case['case']['id']}"
    response = authorized_client.get(url)
    assert response.status_code == 200
    context = response.context
    assert isinstance(context["form"], CaseAssignmentUsersForm)
    # Flow initiated from a team queue, so expect no followup step
    assert context["wizard"]["steps"].next == None

    html = BeautifulSoup(response.content, "html.parser")
    assert "Who do you want to allocate as case adviser?" in html.find("h1").get_text()


def test_case_assignments_add_user_team_queue_submit_success(
    authorized_client,
    data_queue,
    data_standard_case,
    data_assignment,
    mock_team_queue,
    mock_gov_users,
    mock_put_assignments,
    mock_standard_case_with_assignments,
    mock_standard_case_ecju_queries,
    mock_standard_case_assigned_queues,
    mock_standard_case_documents,
    mock_standard_case_additional_contacts,
    mock_standard_case_activity_filters,
    post_to_step_user_assignment,
):
    data = {
        "users": [gov_user_id],
        "note": "foobar",
    }
    response = post_to_step_user_assignment(
        CaseAssignmentsCaseAssigneeSteps.SELECT_USERS,
        data,
        follow=True,
    )
    assert response.status_code == 200
    assert response.redirect_chain[-1][0] == f"/queues/{data_queue['id']}/"
    messages = [str(msg) for msg in response.context["messages"]]
    expected_message = "Case adviser was added successfully"
    assert messages == [expected_message]
    assert mock_put_assignments.called
    assert mock_put_assignments.last_request.json() == {
        "case_assignments": [
            {
                "case_id": data_standard_case["case"]["id"],
                "users": [gov_user_id],
            }
        ],
        "note": "foobar",
        "remove_existing_assignments": False,
    }

    html = BeautifulSoup(response.content, "html.parser")
    assert expected_message in html.select("div.app-snackbar__content")[0].get_text()


def test_case_assignments_add_user_team_queue_submit_validation_error(
    authorized_client,
    data_queue,
    data_standard_case,
    data_assignment,
    mock_team_queue,
    mock_gov_users,
    mock_put_assignments,
    mock_standard_case_with_assignments,
    mock_standard_case_ecju_queries,
    mock_standard_case_assigned_queues,
    mock_standard_case_documents,
    mock_standard_case_additional_contacts,
    mock_standard_case_activity_filters,
    post_to_step_user_assignment,
):

    data = {
        "users": [],
        "note": "foobar",
    }
    response = post_to_step_user_assignment(
        CaseAssignmentsCaseAssigneeSteps.SELECT_USERS,
        data,
    )
    assert response.status_code == 200
    assert response.context["form"]["users"].errors == ["Select a user to allocate"]
