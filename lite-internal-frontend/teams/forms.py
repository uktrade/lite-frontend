from django.urls import reverse

from lite_content.lite_internal_frontend.teams import AddTeamForm, EditTeamForm
from lite_forms.components import Form, TextInput, BackLink


def add_team_form():
    return Form(
        title=AddTeamForm.TITLE,
        description=AddTeamForm.DESCRIPTION,
        questions=[TextInput(title=AddTeamForm.Name.TITLE, description=AddTeamForm.Name.DESCRIPTION, name="name"),],
        back_link=BackLink(AddTeamForm.BACK_LINK, reverse("teams:teams")),
    )


def edit_team_form():
    return Form(
        title=EditTeamForm.TITLE,
        description=EditTeamForm.DESCRIPTION,
        questions=[TextInput(title=EditTeamForm.Name.TITLE, description=EditTeamForm.Name.DESCRIPTION, name="name"),],
        back_link=BackLink(EditTeamForm.BACK_LINK, reverse("teams:teams")),
    )
