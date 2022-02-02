import pytest
from caseworker.teams.forms import EditTeamForm


@pytest.fixture
def form_team_data():
    return {
        "name": "Test",
        "part_of_ecju": True,
        "is_ogd": True,
    }


def test_edit_team_form(form_team_data):
    form = EditTeamForm(data=form_team_data)

    assert form.is_valid()
