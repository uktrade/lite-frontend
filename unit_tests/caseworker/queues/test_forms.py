import pytest
import requests

from caseworker.queues.forms import CaseAssignmentsCaseOfficerForm


def post_request(rf, client, data=None):
    request = rf.post("/", data if data else {})
    request.session = client.session
    request.requests_session = requests.Session()
    return request


@pytest.mark.parametrize(
    "data, valid, errors",
    (
        ({"users": "1f288b81-2c26-439f-ac32-2a43c8b1a5cb"}, True, None),  # /PS-IGNORE
        ({"users": ""}, False, {"users": ["Select a user to allocate as Licensing Unit case officer"]}),
    ),
)
def test_case_assignment_case_office_form(rf, client, mock_gov_user, mock_gov_users, data, valid, errors):
    request = post_request(rf, client)
    form = CaseAssignmentsCaseOfficerForm(data=data, request=request, team_id=mock_gov_user["user"]["team"]["id"])

    assert form.is_valid() == valid

    if not valid:
        assert form.errors == errors
