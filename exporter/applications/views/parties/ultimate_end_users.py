from django.shortcuts import render
from django.views.generic import TemplateView

from exporter.applications.forms.parties import new_party_form_group
from exporter.applications.services import (
    get_application,
    get_ultimate_end_users,
    post_party,
    delete_party,
    validate_party,
)
from exporter.applications.views.parties.base import AddParty, CopyParties, SetParty, DeleteParty, CopyAndSetParty
from lite_content.lite_exporter_frontend.applications import UltimateEndUserForm, UltimateEndUserPage

from core.auth.views import LoginRequiredMixin


class UltimateEndUsers(LoginRequiredMixin, TemplateView):
    def get(self, request, **kwargs):
        application_id = str(kwargs["pk"])
        application = get_application(request, application_id)
        ultimate_end_users = get_ultimate_end_users(request, application_id)

        context = {
            "application": application,
            "ultimate_end_users": ultimate_end_users,
        }
        return render(request, "applications/parties/ultimate-end-users.html", context)


class AddUltimateEndUser(LoginRequiredMixin, AddParty):
    def __init__(self):
        super().__init__(
            new_url="applications:set_ultimate_end_user",
            copy_url="applications:ultimate_end_users_copy",
        )


class SetUltimateEndUser(LoginRequiredMixin, SetParty):
    def __init__(self):
        super().__init__(
            url="applications:ultimate_end_user_attach_document",
            party_type="ultimate_end_user",
            action=post_party,
            form=new_party_form_group,
            back_url="applications:add_ultimate_end_user",
            strings=UltimateEndUserForm,
            post_action=post_party,
            validate_action=validate_party,
        )


class RemoveUltimateEndUser(LoginRequiredMixin, DeleteParty):
    def __init__(self, **kwargs):
        super().__init__(
            url="applications:ultimate_end_users",
            action=delete_party,
            error=UltimateEndUserPage.DELETE_ERROR,
            **kwargs,
        )


class CopyUltimateEndUsers(LoginRequiredMixin, CopyParties):
    def __init__(self):
        super().__init__(new_party_type="ultimate_end_user")


class CopyUltimateEndUser(LoginRequiredMixin, CopyAndSetParty):
    def __init__(self):
        super().__init__(
            url="applications:ultimate_end_user_attach_document",
            party_type="ultimate_end_user",
            form=new_party_form_group,
            back_url="applications:ultimate_end_users_copy",
            strings=UltimateEndUserForm,
            validate_action=validate_party,
            post_action=post_party,
        )
