from caseworker.users.manage.forms import EditCaseworkerUser
import pytest
from core import client


@pytest.fixture(autouse=True)
def user_form_data():
    roles = [{"id": 1, "name": "Role A"}, {"id": 2, "name": "Role B"}]
    teams = [{"id": 1, "name": "Team A"}, {"id": 2, "name": "Team A"}]
    queues = [
        {"id": 1, "name": "Queue A", "team": {"id": "1"}},
        {"id": 2, "name": "Queue B", "team": {"id": "2"}},
        {"id": 3, "name": "Queue C", "team": None},
    ]
    return {"roles": roles, "teams": teams, "queues": queues}


@pytest.mark.parametrize(
    "can_caseworker_edit_user",
    ([False, True]),
)
def test_edit_user_form(can_caseworker_edit_user, user_form_data, mock_request):
    roles = user_form_data["roles"]
    teams = user_form_data["teams"]
    queues = user_form_data["queues"]

    form = EditCaseworkerUser(mock_request, roles, teams, queues, can_caseworker_edit_user)

    assert len(form.fields["role"].choices) == len(roles)
    assert len(form.fields["team"].choices) == len(teams)
    assert len(form.fields["default_queue"].choices) == len(queues) + 1

    assert form.fields["email"].widget.attrs.get("disabled", False) is not can_caseworker_edit_user
    assert form.fields["role"].widget.attrs.get("disabled", False) is not can_caseworker_edit_user
    assert form.fields["team"].widget.attrs.get("disabled", False) is not can_caseworker_edit_user
    assert form.fields["default_queue"].widget.attrs.get("disabled") is None

    for i, t in enumerate(teams):
        assert form.fields["role"].choices[i].value == t["id"]
        assert form.fields["role"].choices[i].label == t["name"]

    for i, r in enumerate(roles):
        assert form.fields["team"].choices[i].value == r["id"]
        assert form.fields["team"].choices[i].label == r["name"]

    assert form.fields["default_queue"].choices[0].value == None
    assert form.fields["default_queue"].choices[0].label == "Select"

    assert form.fields["default_queue"].choices[1].value == 1
    assert form.fields["default_queue"].choices[1].label == "Queue A"
    assert form.fields["default_queue"].choices[1].attrs == {"data-attribute": "1"}

    assert form.fields["default_queue"].choices[3].value == 3
    assert form.fields["default_queue"].choices[3].label == "Queue C"
    assert form.fields["default_queue"].choices[3].attrs == {"data-attribute": None}


@pytest.mark.parametrize(
    "data, valid, cleaned_data, errors",
    (
        (
            {},
            False,
            {},
            {
                "email": ["Enter an email address in the correct format, like name@example.com"],
                "role": ["This field is required."],
                "team": ["This field is required."],
                "default_queue": ["This field is required."],
            },
        ),
        (
            {"email": "test@123.com", "role": 1, "team": 2},
            False,
            {"email": "test@123.com", "role": "1", "team": "2"},
            {
                "default_queue": ["This field is required."],
            },
        ),
        (
            {"email": "test@123.com", "role": 1, "team": 2, "default_queue": None},
            False,
            {"email": "test@123.com", "role": "1", "team": "2"},
            {
                "default_queue": ["This field is required."],
            },
        ),
        (
            {"email": "test@123.com", "role": 1, "team": 2, "default_queue": 3},
            True,
            {"email": "test@123.com", "role": "1", "team": "2", "default_queue": "3"},
            {},
        ),
    ),
)
def test_edit_user_form_post(data, valid, cleaned_data, errors, user_form_data, mock_request):

    roles = user_form_data["roles"]
    teams = user_form_data["teams"]
    queues = user_form_data["queues"]

    form = EditCaseworkerUser(
        request=mock_request, data=data, roles=roles, teams=teams, queues=queues, can_caseworker_edit_user=True
    )
    form.initial = {"email": data.get("email")}

    assert form.is_valid() == valid

    assert form.cleaned_data == cleaned_data
    assert form.errors == errors


def test_edit_user_form_post_caseworker_no_edit_permission(user_form_data, mock_request):

    data = {"email": "", "default_queue": 1}

    roles = user_form_data["roles"]
    teams = user_form_data["teams"]
    queues = user_form_data["queues"]

    form = EditCaseworkerUser(
        request=mock_request, data=data, roles=roles, teams=teams, queues=queues, can_caseworker_edit_user=False
    )
    form.initial = {"email": "test@test123.com"}

    assert form.is_valid() == True
    assert form.cleaned_data == {"default_queue": "1"}
    assert form.errors == {}


@pytest.mark.parametrize(
    "new_email, old_email, valid, duplicate_count, errors",
    (
        ["test@123.com", "testchange@123.com", False, 1, {"email": ["This email has already been registered"]}],
        ["test@123.com", "testchange@123.com", True, 0, {}],
        ["test@123.com", "test@123.com", True, 1, {}],
        ["test@123.com", "test@123.com", True, 0, {}],
    ),
)
def test_edit_user_form_post_update_email(
    new_email, old_email, valid, duplicate_count, errors, user_form_data, mock_request, requests_mock
):

    form_data = {"role": "1", "team": "2", "default_queue": "3", "email": new_email}
    roles = user_form_data["roles"]
    teams = user_form_data["teams"]
    queues = user_form_data["queues"]

    requests_mock.get(
        client._build_absolute_uri("/caseworker/gov_users/gov_users_list/?email=test@123.com"),
        json={"count": duplicate_count},
    )

    form = EditCaseworkerUser(
        request=mock_request, data=form_data, roles=roles, teams=teams, queues=queues, can_caseworker_edit_user=True
    )
    form.initial = {"email": old_email}

    assert form.is_valid() == valid
    assert form.errors == errors
