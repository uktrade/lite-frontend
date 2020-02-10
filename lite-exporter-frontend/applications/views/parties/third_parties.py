from django.shortcuts import render
from django.views.generic import TemplateView

from applications.forms.third_party import third_party_forms
from applications.services import get_application, post_party, delete_party, validate_party
from applications.views.parties.base import AddParty, CopyParties, SetParty, DeleteParty, CopyAndSetParty
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
            new_url="applications:set_third_party", copy_url="applications:third_parties_copy",
        )


class SetThirdParty(SetParty):
    def __init__(self):
        super().__init__(
            url="applications:third_party_attach_document",
            party_type="third_party",
            form=third_party_forms,
            back_url="applications:add_third_party",
            strings=ThirdPartyForm,
            validate_action=validate_party,
            post_action=post_party,
        )


class RemoveThirdParty(DeleteParty):
    def __init__(self, **kwargs):
        super().__init__(
            url="applications:third_parties", action=delete_party, error=ThirdPartyPage.DELETE_ERROR, **kwargs,
        )


class CopyThirdParties(CopyParties):
    def __init__(self):
        super().__init__(new_party_type="third_party")


class CopyThirdParty(CopyAndSetParty):
    def __init__(self):
        super().__init__(
            url="applications:third_party_attach_document",
            party_type="third_party",
            form=third_party_forms,
            back_url="applications:add_third_party",
            strings=ThirdPartyForm,
            validate_action=validate_party,
            post_action=post_party,
        )
