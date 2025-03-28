import pytest
from bs4 import BeautifulSoup
from django.urls import reverse
from pytest_django.asserts import assertTemplateUsed

from core import client
from core.exceptions import ServiceError


@pytest.fixture
def mock_add_assignment(requests_mock, data_standard_case, mock_gov_user, data_queue):
    queue_id = data_queue["id"]
    url = client._build_absolute_uri(f"/queues/{queue_id}/case-assignments/")
    return requests_mock.put(url=url, json={})


@pytest.fixture
def mock_add_assignment_error(requests_mock, data_standard_case, mock_gov_user, data_queue):
    queue_id = data_queue["id"]
    url = client._build_absolute_uri(f"/queues/{queue_id}/case-assignments/")
    return requests_mock.put(url=url, json={}, status_code=500)


@pytest.fixture
def mock_remove_assignment(requests_mock, data_standard_case, data_assignment):
    url = client._build_absolute_uri(
        f"/cases/{data_standard_case['case']['id']}/case-assignments/{data_assignment['id']}"
    )
    return requests_mock.delete(url=url, json=data_assignment)


@pytest.fixture
def mock_remove_f680_assignment(requests_mock, data_submitted_f680_case, data_f680_assignment):
    url = client._build_absolute_uri(
        f"/cases/{data_submitted_f680_case['case']['id']}/case-assignments/{data_f680_assignment['id']}"
    )
    return requests_mock.delete(url=url, json=data_f680_assignment)


@pytest.fixture
def mock_remove_assignment_error(requests_mock, data_standard_case, data_assignment):
    url = client._build_absolute_uri(
        f"/cases/{data_standard_case['case']['id']}/case-assignments/{data_assignment['id']}"
    )
    return requests_mock.delete(url=url, json={}, status_code=500)


@pytest.fixture
def mock_remove_case_officer(requests_mock, data_standard_case):
    url = client._build_absolute_uri(f"/cases/{data_standard_case['case']['id']}/case-officer/")
    return requests_mock.delete(url=url, json={}, status_code=200)


@pytest.fixture
def mock_remove_case_officer_error(requests_mock, data_standard_case):
    url = client._build_absolute_uri(f"/cases/{data_standard_case['case']['id']}/case-officer/")
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


def test_f680_case_assignments_POST_remove_user_success(
    authorized_client,
    data_queue,
    data_submitted_f680_case,
    mock_f680_case,
    data_f680_assignment,
    mock_f680_case_with_assignments,
    mock_remove_f680_assignment,
    mock_queue,
    settings,
):
    settings.FEATURE_FLAG_ALLOW_F680 = True
    case = data_submitted_f680_case
    url = reverse("cases:remove-case-assignment", kwargs={"queue_pk": data_queue["id"], "pk": case["case"]["id"]})
    response = authorized_client.post(url, data={"assignment_id": str(data_f680_assignment["id"])}, follow=True)
    assert response.status_code == 200
    assert response.redirect_chain[-1][0] == reverse(
        "cases:f680:details", kwargs={"queue_pk": data_queue["id"], "pk": data_submitted_f680_case["case"]["id"]}
    )
    messages = [str(msg) for msg in response.context["messages"]]
    expected_message = "some user was successfully removed as case adviser"
    assert messages == [expected_message]

    assert mock_remove_f680_assignment.called
    assert (
        mock_remove_f680_assignment.last_request.path
        == f"/cases/{data_submitted_f680_case['case']['id']}/case-assignments/{data_f680_assignment['id']}/"
    )
    assert mock_remove_f680_assignment.last_request.json() == {}

    html = BeautifulSoup(response.content, "html.parser")
    assert expected_message in html.select("div.app-snackbar__content")[0].get_text()


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
    assert (
        response.redirect_chain[-1][0]
        == f"/queues/{data_queue['id']}/cases/{data_standard_case['case']['id']}/details/"
    )
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
    assert (
        response.redirect_chain[-1][0]
        == f"/queues/{data_queue['id']}/cases/{data_standard_case['case']['id']}/details/"
    )
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


@pytest.mark.parametrize(
    "first_name, last_name, expected_case_officer_name",
    (
        ("some", "user", "some user"),
        ("", "", "example@example.net"),  # /PS-IGNORE
    ),
)
def test_case_remove_case_officer_GET(
    first_name,
    last_name,
    expected_case_officer_name,
    authorized_client,
    data_queue,
    data_standard_case,
    mock_queue,
    data_assignment,
    requests_mock,
):

    case_url = client._build_absolute_uri(f"/cases/{data_standard_case['case']['id']}/")
    data_standard_case["case"]["case_officer"] = {
        "id": data_assignment["user"]["id"],
        "first_name": first_name,
        "last_name": last_name,
        "email": data_assignment["user"]["email"],
    }
    requests_mock.get(url=case_url, json=data_standard_case)

    case = data_standard_case
    url = reverse("cases:remove-case-officer", kwargs={"queue_pk": data_queue["id"], "pk": case["case"]["id"]})
    response = authorized_client.get(url)
    assert response.status_code == 200
    assertTemplateUsed(response, "layouts/case.html")
    context = response.context
    assert context["case_officer_name"] == expected_case_officer_name

    html = BeautifulSoup(response.content, "html.parser")
    assert (
        f"Are you sure you want to remove {expected_case_officer_name} as Licensing Unit case officer?"
        in html.find("h2").get_text()
    )


def test_case_POST_remove_case_officer_success(
    authorized_client,
    data_queue,
    data_standard_case,
    mock_standard_case_with_case_officer,
    mock_standard_case_ecju_queries,
    mock_standard_case_assigned_queues,
    mock_standard_case_documents,
    mock_standard_case_additional_contacts,
    mock_standard_case_activity_filters,
    mock_remove_case_officer,
    mock_queue,
):

    case = data_standard_case
    url = reverse("cases:remove-case-officer", kwargs={"queue_pk": data_queue["id"], "pk": case["case"]["id"]})
    response = authorized_client.post(url, follow=True)
    assert response.status_code == 200
    assert (
        response.redirect_chain[-1][0]
        == f"/queues/{data_queue['id']}/cases/{data_standard_case['case']['id']}/details/"
    )
    messages = [str(msg) for msg in response.context["messages"]]
    expected_message = "some user was successfully removed as Licensing Unit case officer"
    assert messages == [expected_message]
    assert mock_remove_case_officer.called
    assert mock_remove_case_officer.last_request.path == f"/cases/{data_standard_case['case']['id']}/case-officer/"
    assert mock_remove_case_officer.last_request.json() == {}

    html = BeautifulSoup(response.content, "html.parser")
    assert expected_message in html.select("div.app-snackbar__content")[0].get_text()


def test_case_remove_officer_POST_error(
    authorized_client,
    data_queue,
    data_standard_case,
    data_assignment,
    mock_standard_case_with_case_officer,
    mock_standard_case_ecju_queries,
    mock_standard_case_assigned_queues,
    mock_standard_case_documents,
    mock_standard_case_additional_contacts,
    mock_standard_case_activity_filters,
    mock_remove_case_officer_error,
    mock_queue,
):

    case = data_standard_case
    url = reverse("cases:remove-case-officer", kwargs={"queue_pk": data_queue["id"], "pk": case["case"]["id"]})
    response = authorized_client.post(url, follow=True)
    assert response.status_code == 200
    assert (
        response.redirect_chain[-1][0]
        == f"/queues/{data_queue['id']}/cases/{data_standard_case['case']['id']}/details/"
    )
    messages = [str(msg) for msg in response.context["messages"]]
    expected_message = (
        "An error occurred when removing some user as Licensing Unit case officer. Please try again later"
    )
    assert messages == [expected_message]
    assert mock_remove_case_officer_error.called
    assert (
        mock_remove_case_officer_error.last_request.path == f"/cases/{data_standard_case['case']['id']}/case-officer/"
    )

    html = BeautifulSoup(response.content, "html.parser")
    assert expected_message in html.select("div.app-snackbar__content")[0].get_text()


def test_case_remove_officer_POST_404(authorized_client, data_queue, data_standard_case, mock_queue, mock_case):

    url = reverse(
        "cases:remove-case-officer", kwargs={"queue_pk": data_queue["id"], "pk": data_standard_case["case"]["id"]}
    )
    response = authorized_client.get(url)
    assert response.status_code == 404


def test_case_assign_me(
    authorized_client,
    data_queue,
    data_standard_case,
    data_assignment,
    mock_gov_user,
    mock_add_assignment,
    mock_standard_case,
    mock_standard_case_ecju_queries,
    mock_standard_case_documents,
    mock_standard_case_additional_contacts,
    mock_standard_case_activity_filters,
    mock_queue,
    mock_standard_case_assigned_queues,
):
    case = data_standard_case
    url = reverse("queues:case_assignment_assign_to_me", kwargs={"pk": data_queue["id"]})
    case_url = reverse("cases:case", kwargs={"queue_pk": data_queue["id"], "pk": data_standard_case["case"]["id"]})
    data = {
        "queue_id": data_queue["id"],
        "user_id": mock_gov_user["user"]["id"],
        "case_id": case["case"]["id"],
        "return_to": case_url,
    }

    response = authorized_client.post(url, data=data, follow=True)
    assert response.status_code == 200
    assert (
        response.wsgi_request.path
        == "/queues/00000000-0000-0000-0000-000000000001/cases/8fb76bed-fd45-4293-95b8-eda9468aa254/"  # /PS-IGNORE
    )

    html = BeautifulSoup(response.content, "html.parser")
    success_message = html.find(class_="app-snackbar__content")
    assert "You have been successfully added as case adviser" in success_message.text


def test_f680_case_assign_me(
    authorized_client,
    data_queue,
    data_submitted_f680_case,
    data_f680_assignment,
    mock_gov_user,
    mock_add_assignment,
    mock_f680_case,
    mock_queue,
    settings,
):
    settings.FEATURE_FLAG_ALLOW_F680 = True
    url = reverse("queues:case_assignment_assign_to_me", kwargs={"pk": data_queue["id"]})
    case_url = reverse(
        "cases:f680:details", kwargs={"queue_pk": data_queue["id"], "pk": data_submitted_f680_case["case"]["id"]}
    )
    data = {
        "queue_id": data_queue["id"],
        "user_id": mock_gov_user["user"]["id"],
        "case_id": data_submitted_f680_case["case"]["id"],
        "return_to": case_url,
    }

    response = authorized_client.post(url, data=data, follow=True)

    assert response.status_code == 200
    assert response.wsgi_request.path == reverse(
        "cases:f680:details",
        kwargs={"queue_pk": "00000000-0000-0000-0000-000000000001", "pk": data_submitted_f680_case["case"]["id"]},
    )

    html = BeautifulSoup(response.content, "html.parser")
    success_message = html.find(class_="app-snackbar__content")
    assert "You have been successfully added as case adviser" in success_message.text


def test_case_assign_me_api_failure(
    authorized_client,
    data_queue,
    data_standard_case,
    data_assignment,
    mock_gov_user,
    mock_add_assignment_error,
    mock_standard_case,
    mock_standard_case_ecju_queries,
    mock_standard_case_documents,
    mock_standard_case_additional_contacts,
    mock_standard_case_activity_filters,
    mock_queue,
    mock_standard_case_assigned_queues,
):
    case = data_standard_case
    url = reverse("queues:case_assignment_assign_to_me", kwargs={"pk": data_queue["id"]})
    case_url = reverse("cases:case", kwargs={"queue_pk": data_queue["id"], "pk": data_standard_case["case"]["id"]})
    data = {
        "queue_id": data_queue["id"],
        "user_id": mock_gov_user["user"]["id"],
        "case_id": case["case"]["id"],
        "return_to": case_url,
    }

    with pytest.raises(ServiceError) as ex:
        authorized_client.post(url, data=data, follow=True)

    assert ex.value.status_code == 500
    assert ex.value.user_message == "Unexpected error allocating you as case advisor"
