from crispy_forms_gds.helper import FormHelper
from crispy_forms_gds.layout import Button, Field, Layout, Size

from django.urls import reverse
from django import forms

from lite_content.lite_internal_frontend.teams import AddTeamForm
from lite_forms.components import Form, TextInput, BackLink, Option, RadioButtons


def add_team_form():
    return Form(
        title=AddTeamForm.TITLE,
        description=AddTeamForm.DESCRIPTION,
        questions=[
            TextInput(title=AddTeamForm.Name.TITLE, description=AddTeamForm.Name.DESCRIPTION, name="name"),
            RadioButtons(
                title="Is this team part of ECJU?",
                name="part_of_ecju",
                options=[
                    Option(key=True, value="Yes"),
                    Option(key=False, value="No"),
                ],
            ),
        ],
        back_link=BackLink(AddTeamForm.BACK_LINK, reverse("teams:teams")),
    )


class EditTeamForm(forms.Form):
    name = forms.CharField(label="Name", widget=forms.TextInput(), required=True)
    part_of_ecju = forms.ChoiceField(
        choices=((False, "No"), (True, "Yes")),
        label="Is this team part of ECJU?",
        widget=forms.RadioSelect(),
        required=False,
    )
    is_ogd = forms.ChoiceField(
        choices=((False, "No"), (True, "Yes")),
        label="Is this team part of OGD?",
        widget=forms.RadioSelect(),
        required=False,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field.text("name"),
            Field.radios("part_of_ecju", legend_size=Size.MEDIUM, legend_tag="h1", inline=True),
            Field.radios("is_ogd", legend_size=Size.MEDIUM, legend_tag="h1", inline=True),
            Button("submit", "Save"),
        )
