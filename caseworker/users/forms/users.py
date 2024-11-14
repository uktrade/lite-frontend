from django.urls import reverse_lazy

from lite_content.lite_internal_frontend.users import AddUserForm
from lite_forms.components import Form, Select, TextInput, BackLink
from caseworker.queues.services import get_queues
from caseworker.teams.services import get_teams
from caseworker.users.services import get_roles


def add_user_form(request):
    return Form(
        title=AddUserForm.TITLE,
        questions=[
            TextInput(title=AddUserForm.Email.TITLE, description=AddUserForm.Email.DESCRIPTION, name="email"),
            Select(
                title=AddUserForm.Team.TITLE,
                description=AddUserForm.Team.DESCRIPTION,
                name="team",
                options=get_teams(request, True),
            ),
            Select(
                title=AddUserForm.Role.TITLE,
                description=AddUserForm.Role.DESCRIPTION,
                name="role",
                options=get_roles(request, True),
            ),
            Select(
                title=AddUserForm.DefaultQueue.TITLE,
                description=AddUserForm.DefaultQueue.DESCRIPTION,
                name="default_queue",
                options=get_queues(request, include_system=True, convert_to_options=True),
            ),
        ],
        back_link=BackLink(AddUserForm.BACK_LINK, reverse_lazy("users:users")),
        javascript_imports={"/javascripts/filter-default-queue-list.js"},
    )
