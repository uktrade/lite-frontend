import pytest
from caseworker.teams.forms import EditTeamForm


def test_edit_team_form(form_team_data):
    form = EditTeamForm(data=form_team_data)

    assert form.is_valid()
