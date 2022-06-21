import pytest
from exporter.organisation.members.users.constants import AddUserSteps
from exporter.organisation.members.users import forms
from django.urls import reverse
from exporter.core.enums import Roles


@pytest.fixture()
def add_member_url():
    return reverse("organisation:members:add_new")


@pytest.fixture
def post_to_step(post_to_step_factory, add_member_url):
    return post_to_step_factory(add_member_url)


@pytest.fixture
def goto_step(goto_step_factory, add_member_url):
    return goto_step_factory(add_member_url)


@pytest.fixture
def mock_post_users(requests_mock):
    return requests_mock.post(url="/users/", json={}, status_code=201)


def test_select_role_add_non_agent(goto_step, post_to_step, mock_exporter_user_me, mock_post_users, mock_sites):
    goto_step(AddUserSteps.SELECT_ROLE)

    response = post_to_step(
        AddUserSteps.SELECT_ROLE,
        {"role": Roles.administrator.id},
    )

    assert response.status_code == 200
    assert isinstance(response.context["form"], forms.AddUserForm)

    goto_step(AddUserSteps.ADD_MEMBER)
    site_id = mock_sites["sites"][0]["id"]
    response = post_to_step(
        AddUserSteps.ADD_MEMBER,
        {"email": "test@test.com", "sites": [site_id]},
    )
    assert response.status_code == 302
    assert mock_post_users.last_request.json() == {
        "email": "test@test.com",
        "role": Roles.administrator.id,
        "sites": [site_id],
    }
    assert response.url == "/organisation/members/"


def test_select_role_add_agent(goto_step, post_to_step, mock_exporter_user_me, mock_post_users, mock_sites):
    goto_step(AddUserSteps.SELECT_ROLE)

    response = post_to_step(
        AddUserSteps.SELECT_ROLE,
        {"role": Roles.agent.id},
    )

    assert response.status_code == 200
    assert isinstance(response.context["form"], forms.AddUserForm)

    goto_step(AddUserSteps.ADD_MEMBER)
    site_id = mock_sites["sites"][0]["id"]
    response = post_to_step(
        AddUserSteps.ADD_MEMBER,
        {"email": "test@test.com", "sites": [site_id]},
    )

    assert response.status_code == 200
    assert isinstance(response.context["form"], forms.AgentDeclarationForm)

    goto_step(AddUserSteps.AGENT_DECLARATION)

    response = post_to_step(
        AddUserSteps.AGENT_DECLARATION,
        {},
    )
    assert response.status_code == 302
    assert mock_post_users.last_request.json() == {
        "email": "test@test.com",
        "role": Roles.agent.id,
        "sites": [site_id],
    }

    assert response.url == "/organisation/members/"
