import re
import pytest
from uuid import uuid4

from django.urls import reverse
from pytest_django.asserts import assertTemplateUsed
from bs4 import BeautifulSoup

from core import client


@pytest.fixture
def data_assignment(data_standard_case, data_queue):
    assignment_id = "4ccc09d8-04e1-426d-a69d-eda2d3854788"
    user_id = "9ac96323-d519-4781-8424-84b9c7cc3186"
    return {
        "case": data_standard_case["case"]["id"],
        "id": assignment_id,
        "queue": data_queue["id"],
        "user": {
            "email": "example@example.net",
            "first_name": "some",
            "id": user_id,
            "last_name": "user",
            "team": "The A Team",
        },
    }


@pytest.fixture
def mock_standard_case_with_assignments(requests_mock, data_standard_case, data_assignment, data_queue):
    url = client._build_absolute_uri(f"/cases/{data_standard_case['case']['id']}/")
    data_standard_case["case"]["assigned_users"] = {
        data_queue["name"]: [
            {
                "id": data_assignment["user"]["id"],
                "first_name": data_assignment["user"]["first_name"],
                "last_name": data_assignment["user"]["last_name"],
                "email": data_assignment["user"]["email"],
                "assignment_id": data_assignment["id"],
            }
        ]
    }
    return requests_mock.get(url=url, json=data_standard_case)


@pytest.fixture
def mock_remove_assignment(requests_mock, data_standard_case, data_assignment):
    url = client._build_absolute_uri(
        f"/cases/{data_standard_case['case']['id']}/case-assignments/{data_assignment['id']}"
    )
    return requests_mock.delete(url=url, json=data_assignment)


@pytest.fixture
def mock_remove_assignment_error(requests_mock, data_standard_case, data_assignment):
    url = client._build_absolute_uri(
        f"/cases/{data_standard_case['case']['id']}/case-assignments/{data_assignment['id']}"
    )
    return requests_mock.delete(url=url, json={}, status_code=500)


def test_case_assignments_remove_user_GET(
    authorized_client, data_queue, data_standard_case, data_assignment, mock_standard_case_with_assignments, mock_queue
):

    case = data_standard_case
    url_params = f"?assignment_id={data_assignment['id']}"
    url = (
        reverse("cases:remove-case-assignment", kwargs={"queue_pk": data_queue["id"], "pk": case["case"]["id"]})
        + url_params
    )
    response = authorized_client.get(url)
    assert response.status_code == 200
    assertTemplateUsed(response, "layouts/case.html")
    context = response.context
    assert context["adviser_identifier"] == "some user"

    html = BeautifulSoup(response.content, "html.parser")
    assert "Are you sure you want to remove some user as case adviser?" in html.find("h2").get_text()


def test_case_assignments_remove_user_GET_404(authorized_client, data_queue, data_standard_case, mock_queue, mock_case):

    url = reverse(
        "cases:remove-case-assignment", kwargs={"queue_pk": data_queue["id"], "pk": data_standard_case["case"]["id"]}
    )
    response = authorized_client.get(url)
    assert response.status_code == 404


def test_case_assignments_POST_remove_user_success(
    authorized_client,
    data_queue,
    data_standard_case,
    data_assignment,
    mock_standard_case_with_assignments,
    mock_standard_case_ecju_queries,
    mock_standard_case_assigned_queues,
    mock_standard_case_documents,
    mock_standard_case_additional_contacts,
    mock_standard_case_activity_filters,
    mock_remove_assignment,
    mock_queue,
):

    case = data_standard_case
    url = reverse("cases:remove-case-assignment", kwargs={"queue_pk": data_queue["id"], "pk": case["case"]["id"]})
    response = authorized_client.post(url, data={"assignment_id": str(data_assignment["id"])}, follow=True)
    assert response.status_code == 200
    assert response.redirect_chain[-1][0] == f"/queues/{data_queue['id']}/cases/{data_standard_case['case']['id']}/"
    messages = [str(msg) for msg in response.context["messages"]]
    expected_message = "some user was successfully removed as case adviser"
    assert messages == [expected_message]
    assert mock_remove_assignment.called
    assert (
        mock_remove_assignment.last_request.path
        == f"/cases/{data_standard_case['case']['id']}/case-assignments/{data_assignment['id']}/"
    )
    assert mock_remove_assignment.last_request.json() == {}

    html = BeautifulSoup(response.content, "html.parser")
    assert expected_message in html.select("div.app-snackbar__content")[0].get_text()


def test_case_assignments_remove_user_POST_error(
    authorized_client,
    data_queue,
    data_standard_case,
    data_assignment,
    mock_standard_case_with_assignments,
    mock_standard_case_ecju_queries,
    mock_standard_case_assigned_queues,
    mock_standard_case_documents,
    mock_standard_case_additional_contacts,
    mock_standard_case_activity_filters,
    mock_remove_assignment_error,
    mock_queue,
):

    case = data_standard_case
    url = reverse("cases:remove-case-assignment", kwargs={"queue_pk": data_queue["id"], "pk": case["case"]["id"]})
    response = authorized_client.post(url, data={"assignment_id": str(data_assignment["id"])}, follow=True)
    assert response.status_code == 200
    assert response.redirect_chain[-1][0] == f"/queues/{data_queue['id']}/cases/{data_standard_case['case']['id']}/"
    messages = [str(msg) for msg in response.context["messages"]]
    expected_message = "An error occurred when removing some user as case adviser. Please try again later"
    assert messages == [expected_message]
    assert mock_remove_assignment_error.called
    assert (
        mock_remove_assignment_error.last_request.path
        == f"/cases/{data_standard_case['case']['id']}/case-assignments/{data_assignment['id']}/"
    )

    html = BeautifulSoup(response.content, "html.parser")
    assert expected_message in html.select("div.app-snackbar__content")[0].get_text()


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
    url = reverse("cases:add-case-assignment", kwargs={"queue_pk": data_queue["id"], "pk": case["case"]["id"]})
    response = authorized_client.get(url)
    assert response.status_code == 200
    context = response.context
    assert context["form"]
    # Flow initiated from a system queue, so expect the SELECT_QUEUE step next
    assert context["wizard"]["steps"].next == "SELECT_QUEUE"

    html = BeautifulSoup(response.content, "html.parser")
    assert "Which users do you want to assign to this case?" in html.find("h1").get_text()


@pytest.fixture
def mock_users_team_queues_list(requests_mock, gov_uk_user_id, data_queue):
    url = client._build_absolute_uri(f"/users/{gov_uk_user_id}/team-queues/")
    return requests_mock.get(url=url, json={"queues": [[data_queue["id"], "Some Queue"]]})


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
):
    user_id = "1f288b81-2c26-439f-ac32-2a43c8b1a5cb"
    case = data_standard_case
    url = reverse("cases:add-case-assignment", kwargs={"queue_pk": data_queue["id"], "pk": case["case"]["id"]})
    data = {
        "case_assignment_add_user-current_step": "SELECT_USERS",
        "SELECT_USERS-users": [user_id],
        "SELECT_USERS-note": "foobar",
    }
    # POST step 1
    response = authorized_client.post(url, data)
    assert response.status_code == 200
    context = response.context
    assert context["form"]
    assert context["wizard"]["steps"].current == "SELECT_QUEUE"

    html = BeautifulSoup(response.content, "html.parser")
    assert "Select a team queue to add the case to" in html.find("h1").get_text()

    data = {
        "case_assignment_add_user-current_step": "SELECT_QUEUE",
        "SELECT_QUEUE-queue": data_queue["id"],
    }
    # POST step 2
    response = authorized_client.post(url, data, follow=True)
    assert response.status_code == 200
    assert response.redirect_chain[-1][0] == f"/queues/{data_queue['id']}/cases/{data_standard_case['case']['id']}/"
    messages = [str(msg) for msg in response.context["messages"]]
    expected_message = "Case adviser was added successfully"
    assert messages == [expected_message]
    assert mock_put_assignments.called
    assert mock_put_assignments.last_request.json() == {
        "case_assignments": [
            {
                "case_id": data_standard_case["case"]["id"],
                "users": [user_id],
            }
        ],
        "note": "foobar",
        "remove_existing_assignments": False,
    }

    html = BeautifulSoup(response.content, "html.parser")
    assert expected_message in html.select("div.app-snackbar__content")[0].get_text()


@pytest.fixture
def mock_team_queue(requests_mock, data_queue):
    data_queue["is_system_queue"] = False
    url = client._build_absolute_uri("/queues/")
    yield requests_mock.get(url=re.compile(f"{url}.*/"), json=data_queue)


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
    url = reverse("cases:add-case-assignment", kwargs={"queue_pk": data_queue["id"], "pk": case["case"]["id"]})
    response = authorized_client.get(url)
    assert response.status_code == 200
    context = response.context
    assert context["form"]
    # Flow initiated from a team queue, so expect no followup step
    assert context["wizard"]["steps"].next == None

    html = BeautifulSoup(response.content, "html.parser")
    assert "Which users do you want to assign to this case?" in html.find("h1").get_text()


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
):

    user_id = "1f288b81-2c26-439f-ac32-2a43c8b1a5cb"
    case = data_standard_case
    url = reverse("cases:add-case-assignment", kwargs={"queue_pk": data_queue["id"], "pk": case["case"]["id"]})
    data = {
        "case_assignment_add_user-current_step": "SELECT_USERS",
        "SELECT_USERS-users": [user_id],
        "SELECT_USERS-note": "foobar",
    }
    response = authorized_client.post(url, data, follow=True)
    assert response.status_code == 200
    assert response.redirect_chain[-1][0] == f"/queues/{data_queue['id']}/cases/{data_standard_case['case']['id']}/"
    messages = [str(msg) for msg in response.context["messages"]]
    expected_message = "Case adviser was added successfully"
    assert messages == [expected_message]
    assert mock_put_assignments.called
    assert mock_put_assignments.last_request.json() == {
        "case_assignments": [
            {
                "case_id": data_standard_case["case"]["id"],
                "users": [user_id],
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
    mock_remove_assignment_error,
):

    user_id = "1f288b81-2c26-439f-ac32-2a43c8b1a5cb"
    case = data_standard_case
    url = reverse("cases:add-case-assignment", kwargs={"queue_pk": data_queue["id"], "pk": case["case"]["id"]})
    data = {
        "case_assignment_add_user-current_step": "SELECT_USERS",
        "SELECT_USERS-users": [],
        "SELECT_USERS-note": "foobar",
    }
    response = authorized_client.post(url, data)
    assert response.status_code == 200
    assert response.context["form"]["users"].errors == ["Select a user to allocate"]
