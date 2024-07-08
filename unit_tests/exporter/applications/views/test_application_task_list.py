import pytest

from pytest_django.asserts import assertTemplateUsed

from django.urls import reverse

from exporter.applications.constants import ApplicationStatus


@pytest.fixture
def application(data_standard_case):
    return data_standard_case["case"]


@pytest.fixture
def draft_application(data_standard_case):
    data_standard_case["case"]["data"]["status"] = {
        "key": ApplicationStatus.DRAFT,
        "value": ApplicationStatus.DRAFT.title(),
    }
    return data_standard_case["case"]


@pytest.fixture
def task_list_url(draft_application):
    return reverse(
        "applications:task_list",
        kwargs={
            "pk": draft_application["id"],
        },
    )


@pytest.fixture
def mock_application_documents_get(application, requests_mock):
    return requests_mock.get(
        f"/applications/{application['id']}/documents/",
        json={"documents": []},
    )


@pytest.fixture
def mock_case_notes_get(application, requests_mock):
    return requests_mock.get(
        f"/cases/{application['id']}/case-notes/",
        json={"case_notes": []},
    )


@pytest.fixture
def mock_goods_get(application, requests_mock):
    return requests_mock.get(
        f"/applications/{application['id']}/goods/",
        json={"goods": []},
    )


@pytest.fixture
def mock_application_submit(application, requests_mock):
    return requests_mock.put(
        f"/applications/{application['id']}/submit/",
        json={},
    )


def test_application_task_list_status_code(
    authorized_client,
    task_list_url,
    mock_application_get,
    mock_application_documents_get,
    mock_case_notes_get,
    mock_goods_get,
):
    response = authorized_client.get(task_list_url)
    assert response.status_code == 200


def test_application_task_list_template_rendered(
    authorized_client,
    task_list_url,
    mock_application_get,
    mock_application_documents_get,
    mock_case_notes_get,
    mock_goods_get,
):
    response = authorized_client.get(task_list_url)
    assertTemplateUsed(response, "applications/task-list.html")


@pytest.mark.parametrize(
    "goods, ultimate_end_users_required",
    (
        ([], False),
        (
            [{"is_good_incorporated": False}],
            False,
        ),
        (
            [{"is_good_incorporated": True}],
            True,
        ),
        (
            [
                {"is_good_incorporated": True},
                {"is_good_incorporated": False},
            ],
            True,
        ),
        (
            [{"is_onward_exported": False}],
            False,
        ),
        (
            [{"is_onward_exported": True}],
            True,
        ),
        (
            [
                {"is_onward_exported": True},
                {"is_onward_exported": False},
            ],
            True,
        ),
        (
            [
                {"is_onward_exported": True, "is_good_incorporated": False},
            ],
            True,
        ),
        (
            [
                {"is_onward_exported": False, "is_good_incorporated": True},
            ],
            True,
        ),
    ),
)
def test_application_task_list_ultimate_end_users_required(
    goods,
    ultimate_end_users_required,
    authorized_client,
    task_list_url,
    draft_application,
    mock_application_get,
    mock_application_documents_get,
    mock_case_notes_get,
    requests_mock,
):
    requests_mock.get(
        f"/applications/{draft_application['id']}/goods/",
        json={"goods": goods},
    )
    response = authorized_client.get(task_list_url)
    assert response.context["ultimate_end_users_required"] == ultimate_end_users_required


def test_application_task_list_post_f680_security_approvals(
    authorized_client,
    task_list_url,
    mock_application_get,
    mock_application_submit,
):
    authorized_client.post(task_list_url)

    assert mock_application_submit.called_once
    assert mock_application_submit.last_request.json() == {}
