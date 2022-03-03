import logging

from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.functional import cached_property
from django.views.generic import TemplateView, FormView
from formtools.wizard.views import SessionWizardView
from http import HTTPStatus

from exporter.applications.forms.parties import new_party_form_group
from exporter.applications.forms.parties import (
    PartyReuseForm,
    PartySubTypeSelectForm,
    PartyNameForm,
    PartyWebsiteForm,
    PartyAddressForm,
    PartySignatoryNameForm,
    PartyDocuments,
    PartyDocumentUploadForm,
    PartyEnglishTranslationDocumentUploadForm,
    PartyCompanyLetterheadDocumentUploadForm,
)
from exporter.applications.helpers.check_your_answers import convert_party, is_application_export_type_permanent
from exporter.applications.helpers.date_fields import format_date
from exporter.applications.services import (
    get_application,
    post_party,
    post_party_document,
    validate_party,
    delete_party,
    get_party,
)
from exporter.applications.views.parties.base import AddParty, SetParty, DeleteParty, CopyParties, CopyAndSetParty
from exporter.core.constants import OPEN, AddPartyFormSteps
from exporter.core.helpers import (
    NoSaveStorage,
    is_end_user_document_available,
    is_document_in_english,
    is_document_on_letterhead,
)
from lite_content.lite_exporter_frontend.applications import EndUserForm, EndUserPage
from lite_forms.generators import error_page

from core.auth.views import LoginRequiredMixin

log = logging.getLogger(__name__)


class EndUser(LoginRequiredMixin, TemplateView):
    def get(self, request, **kwargs):
        application_id = str(kwargs["pk"])
        application = get_application(request, application_id)
        is_permanent_app = is_application_export_type_permanent(application)
        if application["end_user"]:
            kwargs = {"pk": application_id, "obj_pk": application["end_user"]["id"]}
            context = {
                "application": application,
                "title": EndUserPage.TITLE,
                "edit_url": reverse("applications:edit_end_user", kwargs=kwargs),
                "remove_url": reverse("applications:remove_end_user", kwargs=kwargs),
                "answers": convert_party(
                    party=application["end_user"],
                    application=application,
                    editable=application["status"]["value"] == "draft",
                ),
                "highlight": ["Document"]
                if (is_permanent_app and application.sub_type != OPEN and not application["end_user"]["document"])
                else {},
            }

            return render(request, "applications/end-user.html", context)
        else:
            return redirect(reverse("applications:add_end_user", kwargs={"pk": application_id}))


class AddEndUser(LoginRequiredMixin, AddParty):
    def __init__(self):
        super().__init__(new_url="applications:set_end_user", copy_url="applications:end_users_copy")

    @property
    def back_url(self):
        return reverse("applications:task_list", kwargs={"pk": self.kwargs["pk"]}) + "#end_user"


class SetEndUser(LoginRequiredMixin, SetParty):
    def __init__(self, copy_existing=False):
        super().__init__(
            url="applications:end_user_attach_document",
            party_type="end_user",
            form=new_party_form_group,
            back_url="applications:end_user",
            strings=EndUserForm,
            copy_existing=copy_existing,
            post_action=post_party,
            validate_action=validate_party,
        )

    def get_success_url(self):
        if self.application.sub_type == OPEN:
            return reverse("applications:end_user", kwargs={"pk": self.object_pk})
        else:
            return reverse(
                self.url, kwargs={"pk": self.object_pk, "obj_pk": self.get_validated_data()[self.party_type]["id"]}
            )


class RemoveEndUser(LoginRequiredMixin, DeleteParty):
    def __init__(self):
        super().__init__(
            url="applications:add_end_user",
            action=delete_party,
            error=EndUserPage.DELETE_ERROR,
        )


class CopyEndUsers(LoginRequiredMixin, CopyParties):
    def __init__(self):
        super().__init__(new_party_type="end_user")


class CopyEndUser(LoginRequiredMixin, CopyAndSetParty):
    def __init__(self):
        super().__init__(
            url="applications:end_user_attach_document",
            party_type="end_user",
            form=new_party_form_group,
            back_url="applications:end_users_copy",
            strings=EndUserForm,
            validate_action=validate_party,
            post_action=post_party,
        )

    def get_success_url(self):
        if self.application.sub_type == OPEN:
            return reverse("applications:end_user", kwargs={"pk": self.object_pk})
        else:
            return reverse(
                self.url, kwargs={"pk": self.object_pk, "obj_pk": self.get_validated_data()[self.party_type]["id"]}
            )


class EditEndUser(LoginRequiredMixin, CopyAndSetParty):
    def __init__(self):
        super().__init__(
            url="applications:end_user_attach_document",
            party_type="end_user",
            form=new_party_form_group,
            back_url="applications:end_user",
            strings=EndUserForm,
            validate_action=validate_party,
            post_action=post_party,
        )


class PartyReuseView(LoginRequiredMixin, FormView):
    form_class = PartyReuseForm

    def get_success_url(self):
        reuse_party = self.request.POST.get("reuse_party")
        if reuse_party == "yes":
            return reverse("applications:end_users_copy", kwargs=self.kwargs)
        else:
            return reverse("applications:add_end_user2", kwargs=self.kwargs)


class AddPartyView(LoginRequiredMixin, SessionWizardView):
    template_name = "core/form-wizard.html"

    file_storage = NoSaveStorage()

    form_list = [
        (AddPartyFormSteps.PARTY_SUB_TYPE, PartySubTypeSelectForm),
        (AddPartyFormSteps.PARTY_NAME, PartyNameForm),
        (AddPartyFormSteps.PARTY_WEBSITE, PartyWebsiteForm),
        (AddPartyFormSteps.PARTY_ADDRESS, PartyAddressForm),
        (AddPartyFormSteps.PARTY_SIGNATORY_NAME, PartySignatoryNameForm),
        (AddPartyFormSteps.PARTY_DOCUMENTS, PartyDocuments),
        (AddPartyFormSteps.PARTY_DOCUMENT_UPLOAD, PartyDocumentUploadForm),
        (AddPartyFormSteps.PARTY_ENGLISH_TRANSLATION_UPLOAD, PartyEnglishTranslationDocumentUploadForm),
        (AddPartyFormSteps.PARTY_COMPANY_LETTERHEAD_DOCUMENT_UPLOAD, PartyCompanyLetterheadDocumentUploadForm),
    ]

    condition_dict = {
        AddPartyFormSteps.PARTY_DOCUMENT_UPLOAD: lambda wizard: is_end_user_document_available(wizard),
        AddPartyFormSteps.PARTY_ENGLISH_TRANSLATION_UPLOAD: lambda wizard: is_end_user_document_available(wizard)
        and not is_document_in_english(wizard),
        AddPartyFormSteps.PARTY_COMPANY_LETTERHEAD_DOCUMENT_UPLOAD: lambda wizard: is_end_user_document_available(
            wizard
        )
        and is_document_on_letterhead(wizard),
    }

    @cached_property
    def application(self):
        return get_application(self.request, self.kwargs["pk"])

    def get_cleaned_data_for_step(self, step):
        cleaned_data = super().get_cleaned_data_for_step(step)
        if cleaned_data is None:
            return {}
        return cleaned_data

    def get_context_data(self, form, **kwargs):
        context = super().get_context_data(form, **kwargs)
        context["hide_step_count"] = True
        return context

    def done(self, form_list, **kwargs):
        all_data = {k: v for form in form_list for k, v in form.cleaned_data.items()}
        all_data["type"] = self.party_type
        party_document = all_data.pop("party_document", None)
        party_eng_translation_document = all_data.pop("party_eng_translation_document", None)
        party_letterhead_document = all_data.pop("party_letterhead_document", None)

        response, status_code = post_party(self.request, self.kwargs["pk"], dict(all_data))

        if status_code != HTTPStatus.CREATED:
            log.error(
                "Error creating party - response was: %s - %s",
                status_code,
                response,
                exc_info=True,
            )
            return error_page(self.request, "Unexpected error creating party")

        party_id = response[self.party_type]["id"]

        if party_document:
            data = {
                "name": getattr(party_document, "original_name", party_document.name),
                "s3_key": party_document.name,
                "size": int(party_document.size // 1024) if party_document.size else 0,  # in kilobytes
            }

            response, status_code = post_party_document(self.request, str(self.kwargs["pk"]), party_id, data)
            assert status_code == HTTPStatus.CREATED

        if party_eng_translation_document:
            data = {
                "name": getattr(party_eng_translation_document, "original_name", party_eng_translation_document.name),
                "s3_key": party_eng_translation_document.name,
                "size": int(party_eng_translation_document.size // 1024)
                if party_eng_translation_document.size
                else 0,  # in kilobytes
            }

            response, status_code = post_party_document(self.request, str(self.kwargs["pk"]), party_id, data)
            assert status_code == HTTPStatus.CREATED

        if party_letterhead_document:
            data = {
                "name": getattr(party_letterhead_document, "original_name", party_letterhead_document.name),
                "s3_key": party_letterhead_document.name,
                "size": int(party_letterhead_document.size // 1024)
                if party_letterhead_document.size
                else 0,  # in kilobytes
            }

            response, status_code = post_party_document(self.request, str(self.kwargs["pk"]), party_id, data)
            assert status_code == HTTPStatus.CREATED

        return redirect(reverse("applications:end_user_summary", kwargs={"pk": self.kwargs["pk"], "obj_pk": party_id}))


class AddEndUserView(AddPartyView):
    party_type = "end_user"


class PartyContextMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        party = get_party(self.request, kwargs["pk"], kwargs["obj_pk"])
        return {**context, "party": party[self.party_type]}

class PartySummaryView(LoginRequiredMixin, PartyContextMixin, TemplateView):
    template_name = "applications/party-summary.html"

    def get_success_url(self):
        return "#"


class EndUserSummaryView(PartySummaryView):
    party_type = "end_user"
