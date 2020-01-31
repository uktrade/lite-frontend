from django.shortcuts import render
from django.views.generic import TemplateView

from applications.forms.third_party import third_party_forms
from applications.services import get_application, post_third_party, delete_third_party, validate_third_party
from applications.views.parties.base import AddParty, ExistingPartiesList, SetParty, DeleteParty
from lite_content.lite_exporter_frontend.applications import ThirdPartyForm, ThirdPartyPage


class ThirdParties(TemplateView):
    def get(self, request, **kwargs):
        application_id = str(kwargs["pk"])
        application = get_application(request, application_id)

        context = {
            "application": application,
            "third_parties": application["third_parties"],
        }
        return render(request, "applications/parties/third-parties.html", context)


class AddThirdParty(AddParty):
    def __init__(self):
        super().__init__(
            new_url="applications:set_third_party", copy_url="applications:copy_third_party",
        )


class SetThirdParty(SetParty):
    def __init__(self):
        super().__init__(
            url="applications:third_party_attach_document",
            name="third_party",
            form=third_party_forms,
            back_url="applications:add_third_party",
            strings=ThirdPartyForm,
            multiple_allowed=True,
            validate_action=validate_third_party,
            post_action=post_third_party,
        )


class RemoveThirdParty(DeleteParty):
    def __init__(self, **kwargs):
        super().__init__(
            url="applications:third_parties",
            action=delete_third_party,
            error=ThirdPartyPage.DELETE_ERROR,
            multiple_allowed=True,
            **kwargs,
        )


class ExistingThirdPartiesList(ExistingPartiesList):
    def __init__(self):
        super().__init__(destination_url="applications:set_third_party", back_url="applications:add_third_party")
