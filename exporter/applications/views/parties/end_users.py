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
from exporter.applications.services import (
    copy_party,
    get_application,
    post_party,
    post_party_document,
    validate_party,
    delete_party,
    get_party,
    update_party,
)
from exporter.applications.views.parties.base import AddParty, SetParty, DeleteParty, CopyParties, CopyAndSetParty
from exporter.core.constants import OPEN, SetPartyFormSteps
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
        if application["end_user"]:
            kwargs = {"pk": application_id, "obj_pk": application["end_user"]["id"]}
            return redirect(reverse("applications:end_user_summary", kwargs=kwargs))
        else:
            return redirect(reverse("applications:add_end_user", kwargs={"pk": application_id}))


class AddEndUser(LoginRequiredMixin, AddParty):
    def __init__(self):
        super().__init__(new_url="applications:set_end_user2", copy_url="applications:end_users_copy")

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
            return reverse("applications:set_end_user2", kwargs=self.kwargs)


class SetPartyView(LoginRequiredMixin, SessionWizardView):
    template_name = "core/form-wizard.html"

    file_storage = NoSaveStorage()

    form_list = [
        (SetPartyFormSteps.PARTY_SUB_TYPE, PartySubTypeSelectForm),
        (SetPartyFormSteps.PARTY_NAME, PartyNameForm),
        (SetPartyFormSteps.PARTY_WEBSITE, PartyWebsiteForm),
        (SetPartyFormSteps.PARTY_ADDRESS, PartyAddressForm),
        (SetPartyFormSteps.PARTY_SIGNATORY_NAME, PartySignatoryNameForm),
        (SetPartyFormSteps.PARTY_DOCUMENTS, PartyDocuments),
        (SetPartyFormSteps.PARTY_DOCUMENT_UPLOAD, PartyDocumentUploadForm),
        (SetPartyFormSteps.PARTY_ENGLISH_TRANSLATION_UPLOAD, PartyEnglishTranslationDocumentUploadForm),
        (SetPartyFormSteps.PARTY_COMPANY_LETTERHEAD_DOCUMENT_UPLOAD, PartyCompanyLetterheadDocumentUploadForm),
    ]

    condition_dict = {
        SetPartyFormSteps.PARTY_DOCUMENT_UPLOAD: lambda wizard: is_end_user_document_available(wizard),
        SetPartyFormSteps.PARTY_ENGLISH_TRANSLATION_UPLOAD: lambda wizard: is_end_user_document_available(wizard)
        and not is_document_in_english(wizard),
        SetPartyFormSteps.PARTY_COMPANY_LETTERHEAD_DOCUMENT_UPLOAD: lambda wizard: is_end_user_document_available(
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
        context["title"] = form.title
        context["hide_step_count"] = True
        context["back_link_text"] = "Back"
        return context

    def get_form_kwargs(self, step=None):
        kwargs = super().get_form_kwargs(step)

        if step == SetPartyFormSteps.PARTY_ADDRESS:
            kwargs["request"] = self.request

        return kwargs

    def get_success_url(self, party_id):
        raise NotImplementedError("Subclasses must implement get_success_url()")

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
                "type": "end_user_undertaking_document",
                "name": getattr(party_document, "original_name", party_document.name),
                "s3_key": party_document.name,
                "size": int(party_document.size // 1024) if party_document.size else 0,  # in kilobytes
            }

            response, status_code = post_party_document(self.request, str(self.kwargs["pk"]), party_id, data)
            assert status_code == HTTPStatus.CREATED

        if party_eng_translation_document:
            data = {
                "type": "end_user_english_translation_document",
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
                "type": "end_user_company_letterhead_document",
                "name": getattr(party_letterhead_document, "original_name", party_letterhead_document.name),
                "s3_key": party_letterhead_document.name,
                "size": int(party_letterhead_document.size // 1024)
                if party_letterhead_document.size
                else 0,  # in kilobytes
            }

            response, status_code = post_party_document(self.request, str(self.kwargs["pk"]), party_id, data)
            assert status_code == HTTPStatus.CREATED

        return redirect(self.get_success_url(party_id))


class SetEndUserView(SetPartyView):
    party_type = "end_user"

    def get_success_url(self, party_id):
        return reverse("applications:end_user_summary", kwargs={"pk": self.kwargs["pk"], "obj_pk": party_id})


class CopyEndUserView(SetEndUserView):
    def get_form_initial(self, step):
        initial = copy_party(request=self.request, pk=str(self.kwargs["pk"]), party_pk=str(self.kwargs["obj_pk"]))
        return initial

    def get_success_url(self, party_id):
        if self.application.sub_type == OPEN:
            return reverse("applications:end_user", kwargs={"pk": self.kwargs["pk"]})

        return reverse("applications:end_user_summary", kwargs={"pk": self.kwargs["pk"], "obj_pk": party_id})


class PartyContextMixin:
    template_name = "core/form.html"

    @property
    def application_id(self):
        return str(self.kwargs["pk"])

    @property
    def party_id(self):
        return str(self.kwargs["obj_pk"])

    @property
    def party(self):
        party = get_party(self.request, self.kwargs["pk"], self.kwargs["obj_pk"])
        party_type = list(party.keys())[0]
        return party[party_type]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return {**context, "party": self.party}


class PartySummaryView(LoginRequiredMixin, PartyContextMixin, TemplateView):
    template_name = "applications/party-summary.html"

    def get_success_url(self):
        return "#"


class RemoveEndUserView(LoginRequiredMixin, PartyContextMixin, TemplateView):
    party_type = "end_user"

    def get(self, request, *args, **kwargs):
        status_code = delete_party(self.request, kwargs["pk"], kwargs["obj_pk"])
        if status_code != HTTPStatus.OK:
            return error_page(request, "Error deleting party")

        return redirect(reverse("applications:task_list", kwargs={"pk": kwargs["pk"]}))


class PartyEditMixin(LoginRequiredMixin, PartyContextMixin, FormView):
    def form_valid(self, form):
        update_party(self.request, self.application_id, self.party_id, form.cleaned_data)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("applications:end_user_summary", kwargs=self.kwargs)


class PartySubTypeEditView(PartyEditMixin):
    form_class = PartySubTypeSelectForm

    def get_initial(self):
        return {"sub_type": self.party["sub_type"]["key"], "sub_type_other": self.party["sub_type_other"]}


class PartyNameEditView(PartyEditMixin):
    form_class = PartyNameForm

    def get_initial(self):
        return {"name": self.party["name"]}


class PartyWebsiteEditView(PartyEditMixin):
    form_class = PartyWebsiteForm

    def get_initial(self):
        return {"website": self.party["website"]}


class PartyAddressEditView(PartyEditMixin):
    form_class = PartyAddressForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["request"] = self.request
        return kwargs

    def get_initial(self):
        return {"address": self.party["address"], "country": self.party["country"]["id"]}


class PartySignatoryEditView(PartyEditMixin):
    form_class = PartySignatoryNameForm

    def get_initial(self):
        return {"signatory_name_euu": self.party["signatory_name_euu"]}


class PartyDocumentEditView(LoginRequiredMixin, PartyContextMixin, FormView):
    def get_initial(self):
        return {}

    def get_form(self):
        form_kwargs = self.get_form_kwargs()
        if self.kwargs.get("document_type") == "english_translation":
            return PartyEnglishTranslationDocumentUploadForm(**form_kwargs)
        elif self.kwargs.get("document_type") == "company_letterhead":
            return PartyCompanyLetterheadDocumentUploadForm(**form_kwargs)
        else:
            raise ValueError("Invalid document type encountered")

    def form_valid(self, form):
        if self.kwargs.get("document_type") == "english_translation":
            document = form.cleaned_data["party_eng_translation_document"]
            party_document_type = "end_user_english_translation_document"
        elif self.kwargs.get("document_type") == "company_letterhead":
            document = form.cleaned_data["party_letterhead_document"]
            party_document_type = "end_user_company_letterhead_document"
        else:
            raise ValueError("Invalid document type encountered")

        data = {
            "type": party_document_type,
            "name": getattr(document, "original_name", document.name),
            "s3_key": document.name,
            "size": int(document.size // 1024) if document.size else 0,  # in kilobytes
        }

        response, status_code = post_party_document(self.request, self.application_id, self.party_id, data)
        assert status_code == HTTPStatus.CREATED
        return super().form_valid(form)

    def get_success_url(self):
        document_type = self.kwargs.pop("document_type")
        return reverse("applications:end_user_summary", kwargs=self.kwargs)
