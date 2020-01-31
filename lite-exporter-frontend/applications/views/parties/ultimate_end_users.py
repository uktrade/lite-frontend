from django.shortcuts import render
from django.views.generic import TemplateView

from applications.forms.parties import new_party_form_group
from applications.helpers.validate_status import check_all_parties_have_a_document
from applications.services import (
    get_application,
    get_ultimate_end_users,
    post_ultimate_end_user,
    delete_ultimate_end_user,
    validate_ultimate_end_user,
)
from applications.views.parties.base import AddParty, ExistingPartiesList, SetParty, DeleteParty
from lite_content.lite_exporter_frontend.applications import UltimateEndUserForm, UltimateEndUserPage


class UltimateEndUsers(TemplateView):
    def get(self, request, **kwargs):
        application_id = str(kwargs["pk"])
        application = get_application(request, application_id)
        ultimate_end_users = get_ultimate_end_users(request, application_id)

        context = {
            "application": application,
            "ultimate_end_users": ultimate_end_users,
            "show_warning": check_all_parties_have_a_document(ultimate_end_users) == "in_progress",
        }
        return render(request, "applications/parties/ultimate-end-users.html", context)


class AddUltimateEndUser(AddParty):
    def __init__(self):
        super().__init__(
            new_url="applications:set_ultimate_end_user", copy_url="applications:copy_ultimate_end_user",
        )


class SetUltimateEndUser(SetParty):
    def __init__(self):
        super().__init__(
            url="applications:ultimate_end_user_attach_document",
            name="ultimate_end_user",
            action=post_ultimate_end_user,
            form=new_party_form_group,
            back_url="applications:add_ultimate_end_user",
            strings=UltimateEndUserForm,
            multiple_allowed=True,
            post_action=post_ultimate_end_user,
            validate_action=validate_ultimate_end_user,
        )


class RemoveUltimateEndUser(DeleteParty):
    def __init__(self, **kwargs):
        super().__init__(
            url="applications:ultimate_end_users",
            action=delete_ultimate_end_user,
            error=UltimateEndUserPage.DELETE_ERROR,
            multiple_allowed=True,
            **kwargs,
        )


class ExistingUltimateEndUser(ExistingPartiesList):
    def __init__(self):
        super().__init__(
            destination_url="applications:set_ultimate_end_user", back_url="applications:add_ultimate_end_user"
        )
