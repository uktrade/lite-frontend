import logging

from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.functional import cached_property
from django.views.generic import TemplateView, FormView
from http import HTTPStatus

from core.common.forms import BaseForm
from core.file_handler import download_document_from_s3
from core.helpers import get_document_data

from exporter.applications.forms.parties import (
    PartyReuseForm,
    PartySubTypeSelectForm,
    PartyNameForm,
    PartyWebsiteForm,
    PartyAddressForm,
    PartySignatoryNameForm,
    PartyDocumentsForm,
    PartyDocumentUploadForm,
    PartyEnglishTranslationDocumentUploadForm,
    PartyCompanyLetterheadDocumentUploadForm,
    PartyEC3DocumentUploadForm,
)
from exporter.applications.services import (
    copy_party,
    get_application,
    post_party,
    post_party_document,
    delete_party,
    get_party,
    update_party,
    delete_party_document_by_id,
)
from exporter.applications.views.parties.base import CopyParties
from exporter.applications.helpers.parties import party_requires_ec3_document
from exporter.core.constants import (
    OPEN,
    SetPartyFormSteps,
    PartyDocumentType,
    DOCUMENT_TYPE_PARAM_ENGLISH_TRANSLATION,
    DOCUMENT_TYPE_PARAM_COMPANY_LETTERHEAD,
)
from exporter.core.helpers import (
    is_end_user_document_available,
    is_document_in_english,
    is_document_on_letterhead,
    str_to_bool,
)
from core.wizard.views import BaseSessionWizardView
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


class CopyEndUsers(LoginRequiredMixin, CopyParties):
    def __init__(self):
        super().__init__(new_party_type="end_user")


class AddEndUserView(LoginRequiredMixin, FormView):
    form_class = PartyReuseForm
    template_name = "core/form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_title"] = self.form_class.title
        return context

    def form_valid(self, form):
        reuse_party = str_to_bool(form.cleaned_data.get("reuse_party"))
        if reuse_party:
            success_url = reverse("applications:end_users_copy", kwargs=self.kwargs)
        else:
            success_url = reverse("applications:set_end_user", kwargs=self.kwargs)

        return HttpResponseRedirect(success_url)


def _post_party_document(request, application_id, party_id, document_type, document):
    data = {
        "type": document_type,
        **get_document_data(document),
    }

    response, status_code = post_party_document(request, application_id, party_id, data)
    if status_code != HTTPStatus.CREATED:
        log.error(
            "Error uploading party document of type %s - response was: %s - %s",
            data["type"],
            status_code,
            response,
            exc_info=True,
        )
    return response, status_code


class SetPartyView(LoginRequiredMixin, BaseSessionWizardView):
    form_list = [
        (SetPartyFormSteps.PARTY_SUB_TYPE, PartySubTypeSelectForm),
        (SetPartyFormSteps.PARTY_NAME, PartyNameForm),
        (SetPartyFormSteps.PARTY_WEBSITE, PartyWebsiteForm),
        (SetPartyFormSteps.PARTY_ADDRESS, PartyAddressForm),
        (SetPartyFormSteps.PARTY_SIGNATORY_NAME, PartySignatoryNameForm),
        (SetPartyFormSteps.PARTY_DOCUMENTS, PartyDocumentsForm),
        (SetPartyFormSteps.PARTY_DOCUMENT_UPLOAD, PartyDocumentUploadForm),
        (SetPartyFormSteps.PARTY_ENGLISH_TRANSLATION_UPLOAD, PartyEnglishTranslationDocumentUploadForm),
        (SetPartyFormSteps.PARTY_COMPANY_LETTERHEAD_DOCUMENT_UPLOAD, PartyCompanyLetterheadDocumentUploadForm),
    ]

    condition_dict = {
        SetPartyFormSteps.PARTY_DOCUMENT_UPLOAD: is_end_user_document_available,
        SetPartyFormSteps.PARTY_ENGLISH_TRANSLATION_UPLOAD: lambda wizard: is_end_user_document_available(wizard)
        and not is_document_in_english(wizard),
        SetPartyFormSteps.PARTY_COMPANY_LETTERHEAD_DOCUMENT_UPLOAD: lambda wizard: is_end_user_document_available(
            wizard
        )
        and not is_document_on_letterhead(wizard),
    }

    @cached_property
    def application(self):
        return get_application(self.request, self.kwargs["pk"])

    def get_context_data(self, form, **kwargs):
        context = super().get_context_data(form, **kwargs)
        if isinstance(form, BaseForm):
            context["title"] = form.Layout.TITLE
        else:
            context["title"] = form.title
        return context

    def get_form_kwargs(self, step=None):
        kwargs = super().get_form_kwargs(step)

        if step == SetPartyFormSteps.PARTY_ADDRESS:
            kwargs["request"] = self.request
        if step in (
            SetPartyFormSteps.PARTY_DOCUMENT_UPLOAD,
            SetPartyFormSteps.PARTY_ENGLISH_TRANSLATION_UPLOAD,
            SetPartyFormSteps.PARTY_COMPANY_LETTERHEAD_DOCUMENT_UPLOAD,
        ):
            kwargs["edit"] = False

        return kwargs

    def get_success_url(self, party_id):
        application = get_application(self.request, self.kwargs["pk"])
        if party_requires_ec3_document(application):
            return reverse("applications:end_user_ec3_document", kwargs={"pk": self.kwargs["pk"], "obj_pk": party_id})
        else:
            return reverse("applications:end_user_summary", kwargs={"pk": self.kwargs["pk"], "obj_pk": party_id})

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
            _, status_code = _post_party_document(
                self.request,
                self.application.id,
                party_id,
                PartyDocumentType.END_USER_UNDERTAKING_DOCUMENT,
                party_document,
            )
            if status_code != HTTPStatus.CREATED:
                return error_page(self.request, "Unexpected error uploading party document")

        if party_eng_translation_document:
            _, status_code = _post_party_document(
                self.request,
                self.application.id,
                party_id,
                PartyDocumentType.END_USER_ENGLISH_TRANSLATION_DOCUMENT,
                party_eng_translation_document,
            )
            if status_code != HTTPStatus.CREATED:
                return error_page(self.request, "Unexpected error uploading party document")

        if party_letterhead_document:
            _, status_code = _post_party_document(
                self.request,
                self.application.id,
                party_id,
                PartyDocumentType.END_USER_COMPANY_LETTERHEAD_DOCUMENT,
                party_letterhead_document,
            )
            if status_code != HTTPStatus.CREATED:
                return error_page(self.request, "Unexpected error uploading party document")

        return redirect(self.get_success_url(party_id))


class SetEndUserView(SetPartyView):
    party_type = "end_user"


class CopyEndUserView(SetEndUserView):
    def get_form_initial(self, step):
        initial = copy_party(request=self.request, pk=str(self.kwargs["pk"]), party_pk=str(self.kwargs["obj_pk"]))
        return initial

    def get_success_url(self, party_id):
        if self.application.sub_type == OPEN:
            return reverse("applications:end_user", kwargs={"pk": self.kwargs["pk"]})

        return super().get_success_url(party_id)


class PartyContextMixin:
    template_name = "core/form.html"

    @cached_property
    def application_id(self):
        return str(self.kwargs["pk"])

    @cached_property
    def party_id(self):
        return str(self.kwargs["obj_pk"])

    @cached_property
    def application(self):
        return get_application(self.request, self.kwargs["pk"])

    @property
    def party(self):
        party = get_party(self.request, self.kwargs["pk"], self.kwargs["obj_pk"])
        return party["data"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return {**context, "party": self.party}


class PartySummaryView(LoginRequiredMixin, PartyContextMixin, TemplateView):
    template_name = "applications/party-summary.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["ec3_required"] = party_requires_ec3_document(self.application)
        available_documents = {document["type"]: document for document in self.party["documents"]}
        return {**context, **available_documents}

    def get_success_url(self):
        return reverse("applications:task_list", kwargs={"pk": self.kwargs["pk"]})


class RemoveEndUserView(LoginRequiredMixin, PartyContextMixin, TemplateView):
    party_type = "end_user"

    def get(self, request, *args, **kwargs):
        status_code = delete_party(self.request, kwargs["pk"], kwargs["obj_pk"])
        if status_code != HTTPStatus.OK:
            return error_page(request, "Error deleting party")

        return redirect(reverse("applications:task_list", kwargs={"pk": kwargs["pk"]}))


class PartyEditView(LoginRequiredMixin, PartyContextMixin, FormView):
    def form_valid(self, form):
        update_party(self.request, self.application_id, self.party_id, form.cleaned_data)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("applications:end_user_summary", kwargs=self.kwargs)


class PartySubTypeEditView(PartyEditView):
    form_class = PartySubTypeSelectForm

    def get_initial(self):
        return {"sub_type": self.party["sub_type"]["key"], "sub_type_other": self.party["sub_type_other"]}


class PartyNameEditView(PartyEditView):
    form_class = PartyNameForm

    def get_initial(self):
        return {"name": self.party["name"]}


class PartyWebsiteEditView(PartyEditView):
    form_class = PartyWebsiteForm

    def get_initial(self):
        return {"website": self.party["website"]}


class PartyAddressEditView(PartyEditView):
    form_class = PartyAddressForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["request"] = self.request
        return kwargs

    def get_initial(self):
        return {"address": self.party["address"], "country": self.party["country"]["id"]}


class PartySignatoryEditView(PartyEditView):
    form_class = PartySignatoryNameForm

    def get_initial(self):
        return {"signatory_name_euu": self.party["signatory_name_euu"]}


class PartyDocumentOptionEditView(PartyEditView):
    form_class = PartyDocumentsForm

    def get_initial(self):
        return {
            "end_user_document_available": self.party["end_user_document_available"],
            "end_user_document_missing_reason": self.party["end_user_document_missing_reason"],
        }

    def form_valid(self, form):
        end_user_document_available = str_to_bool(form.cleaned_data.get("end_user_document_available"))

        # delete any existing documents except EC3 which is different from undertaking documents
        existing_documents = [
            document
            for document in self.party["documents"]
            if document["type"] != PartyDocumentType.END_USER_EC3_DOCUMENT
        ]
        if not end_user_document_available:
            for document in existing_documents:
                delete_party_document_by_id(
                    self.request,
                    self.application_id,
                    self.party_id,
                    document["id"],
                )

        return super().form_valid(form)

    def get_success_url(self):
        if self.party["end_user_document_available"]:
            return reverse("applications:end_user_edit_undertaking_document", kwargs=self.kwargs)
        else:
            return reverse("applications:end_user_summary", kwargs=self.kwargs)


class PartyUndertakingDocumentEditView(LoginRequiredMixin, PartyContextMixin, BaseSessionWizardView):
    template_name = "core/form-wizard.html"
    form_list = [
        (SetPartyFormSteps.PARTY_DOCUMENT_UPLOAD, PartyDocumentUploadForm),
        (SetPartyFormSteps.PARTY_ENGLISH_TRANSLATION_UPLOAD, PartyEnglishTranslationDocumentUploadForm),
        (SetPartyFormSteps.PARTY_COMPANY_LETTERHEAD_DOCUMENT_UPLOAD, PartyCompanyLetterheadDocumentUploadForm),
    ]

    condition_dict = {
        SetPartyFormSteps.PARTY_ENGLISH_TRANSLATION_UPLOAD: lambda wizard: is_end_user_document_available(wizard)
        and not is_document_in_english(wizard),
        SetPartyFormSteps.PARTY_COMPANY_LETTERHEAD_DOCUMENT_UPLOAD: lambda wizard: is_end_user_document_available(
            wizard
        )
        and not is_document_on_letterhead(wizard),
    }

    def get_form_kwargs(self, step=None):
        kwargs = super().get_form_kwargs(step)

        # get existing document status for the end-user
        self.existing_documents = {document["type"]: document["id"] for document in self.party["documents"]}
        self.undertaking_document_exists = PartyDocumentType.END_USER_UNDERTAKING_DOCUMENT in self.existing_documents
        self.english_translation_exists = (
            PartyDocumentType.END_USER_ENGLISH_TRANSLATION_DOCUMENT in self.existing_documents
        )
        self.company_letterhead_document_exists = (
            PartyDocumentType.END_USER_COMPANY_LETTERHEAD_DOCUMENT in self.existing_documents
        )
        if step == SetPartyFormSteps.PARTY_DOCUMENT_UPLOAD:
            kwargs["edit"] = self.undertaking_document_exists

        if step == SetPartyFormSteps.PARTY_ENGLISH_TRANSLATION_UPLOAD:
            kwargs["edit"] = self.english_translation_exists

        if step == SetPartyFormSteps.PARTY_COMPANY_LETTERHEAD_DOCUMENT_UPLOAD:
            kwargs["edit"] = self.company_letterhead_document_exists

        return kwargs

    def get_form_initial(self, step):
        if step != SetPartyFormSteps.PARTY_DOCUMENT_UPLOAD:
            return {"end_user_document_available": True}

        return {
            "end_user_document_available": True,
            "product_differences_note": self.party["product_differences_note"],
            "document_in_english": self.party["document_in_english"],
            "document_on_letterhead": self.party["document_on_letterhead"],
        }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # The back_link_url is used for the first form in the sequence. For subsequent forms,
        # the wizard automatically generates the back link to the previous form.
        context["back_link_url"] = reverse("applications:end_user_summary", kwargs=self.kwargs)
        return context

    def get_cleaned_data_for_step(self, step):
        cleaned_data = super().get_cleaned_data_for_step(step)
        if step == SetPartyFormSteps.PARTY_DOCUMENTS:
            cleaned_data = {"end_user_document_available": True}

        if cleaned_data is None:
            return {}
        return cleaned_data

    def done(self, form_list, **kwargs):
        all_data = {k: v for form in form_list for k, v in form.cleaned_data.items()}

        # get updated user choices
        party_document = all_data.pop("party_document", None)
        document_in_english = str_to_bool(all_data.pop("document_in_english", None))
        document_on_letterhead = str_to_bool(all_data.pop("document_on_letterhead", None))
        party_eng_translation_document = all_data.pop("party_eng_translation_document", None)
        party_letterhead_document = all_data.pop("party_letterhead_document", None)

        data = {
            "product_differences_note": all_data["product_differences_note"],
            "document_in_english": document_in_english,
            "document_on_letterhead": document_on_letterhead,
            "end_user_document_missing_reason": "",
        }

        response, status_code = update_party(self.request, self.application_id, self.party_id, data)
        if status_code != HTTPStatus.OK:
            log.error(
                "Error updating party - response was: %s - %s",
                status_code,
                response,
                exc_info=True,
            )
            return error_page(self.request, "Unexpected error updating party")

        # if True then user is uploading new undertaking document
        if party_document:
            _, status_code = _post_party_document(
                self.request,
                self.application_id,
                self.party_id,
                PartyDocumentType.END_USER_UNDERTAKING_DOCUMENT,
                party_document,
            )
            if status_code != HTTPStatus.CREATED:
                return error_page(self.request, "Unexpected error uploading party document")

        # if True then user choice hasn't changed and uploaded a new translation document
        if party_eng_translation_document:
            _, status_code = _post_party_document(
                self.request,
                self.application_id,
                self.party_id,
                PartyDocumentType.END_USER_ENGLISH_TRANSLATION_DOCUMENT,
                party_eng_translation_document,
            )
            if status_code != HTTPStatus.CREATED:
                return error_page(self.request, "Unexpected error uploading party document")
        elif document_in_english and self.english_translation_exists:
            # delete existing document
            delete_party_document_by_id(
                self.request,
                self.application_id,
                self.party_id,
                self.existing_documents[PartyDocumentType.END_USER_ENGLISH_TRANSLATION_DOCUMENT],
            )

        if party_letterhead_document:
            _, status_code = _post_party_document(
                self.request,
                self.application_id,
                self.party_id,
                PartyDocumentType.END_USER_COMPANY_LETTERHEAD_DOCUMENT,
                party_letterhead_document,
            )
            if status_code != HTTPStatus.CREATED:
                return error_page(self.request, "Unexpected error uploading party document")
        elif document_on_letterhead and self.company_letterhead_document_exists:
            delete_party_document_by_id(
                self.request,
                self.application_id,
                self.party_id,
                self.existing_documents[PartyDocumentType.END_USER_COMPANY_LETTERHEAD_DOCUMENT],
            )

        return redirect(reverse("applications:end_user_summary", kwargs=self.kwargs))


class PartyDocumentEditView(LoginRequiredMixin, PartyContextMixin, FormView):
    def get_form(self):
        form_kwargs = self.get_form_kwargs()
        if self.kwargs.get("document_type") == DOCUMENT_TYPE_PARAM_ENGLISH_TRANSLATION:
            return PartyEnglishTranslationDocumentUploadForm(edit=True, **form_kwargs)
        elif self.kwargs.get("document_type") == DOCUMENT_TYPE_PARAM_COMPANY_LETTERHEAD:
            return PartyCompanyLetterheadDocumentUploadForm(edit=True, **form_kwargs)
        else:
            raise ValueError("Invalid document type encountered")

    def form_valid(self, form):
        document = None
        if self.kwargs.get("document_type") == DOCUMENT_TYPE_PARAM_ENGLISH_TRANSLATION:
            document = form.cleaned_data["party_eng_translation_document"]
            party_document_type = PartyDocumentType.END_USER_ENGLISH_TRANSLATION_DOCUMENT
        elif self.kwargs.get("document_type") == DOCUMENT_TYPE_PARAM_COMPANY_LETTERHEAD:
            document = form.cleaned_data["party_letterhead_document"]
            party_document_type = PartyDocumentType.END_USER_COMPANY_LETTERHEAD_DOCUMENT
        else:
            raise ValueError("Invalid document type encountered")

        if document is None:
            return super().form_valid(form)

        data = {
            "type": party_document_type,
            "name": getattr(document, "name"),
            "s3_key": document.name,
            "size": int(document.size // 1024) if document.size else 0,  # in kilobytes
        }

        response, status_code = post_party_document(self.request, self.application_id, self.party_id, data)
        if status_code != HTTPStatus.CREATED:
            log.error(
                "Error uploading party document - response was: %s - %s",
                status_code,
                response,
                exc_info=True,
            )
            return error_page(self.request, "Unexpected error uploading party document")

        return super().form_valid(form)

    def get_success_url(self):
        self.kwargs.pop("document_type")
        return reverse("applications:end_user_summary", kwargs=self.kwargs)


class PartyDocumentDownloadView(LoginRequiredMixin, PartyContextMixin, TemplateView):
    def get(self, request, **kwargs):
        document = [doc for doc in self.party["documents"] if doc["id"] == kwargs["document_pk"]]
        if not document:
            return error_page(request, "Requested document not associated with this party")

        document = document[0]
        return download_document_from_s3(document["s3_key"], document["name"])


class PartyEC3DocumentView(LoginRequiredMixin, PartyContextMixin, FormView):
    form_class = PartyEC3DocumentUploadForm

    def get_initial(self):
        return {"ec3_missing_reason": self.party["ec3_missing_reason"]}

    def form_valid(self, form):
        party_ec3_document = form.cleaned_data.pop("party_ec3_document", None)
        ec3_missing_reason = form.cleaned_data.pop("ec3_missing_reason", None)
        if party_ec3_document and ec3_missing_reason:
            form.add_error(None, "Select an EC3 form, or enter a reason why you do not have one (optional)")
            return super().form_invalid(form)

        existing_documents = {document["type"]: document["id"] for document in self.party["documents"]}
        ec3_document_exists = PartyDocumentType.END_USER_EC3_DOCUMENT in existing_documents

        # We only want an EC3 form or missing reason, providing both is an error so
        # one of the following is true but user can edit these values from summary page.
        # If the user provides a reason then we have to delete previously uploaded document
        # if it exists and similarly if new document is uploaded then we reset the reason.
        if ec3_missing_reason and ec3_document_exists:
            delete_party_document_by_id(
                self.request,
                self.application_id,
                self.party_id,
                existing_documents[PartyDocumentType.END_USER_EC3_DOCUMENT],
            )

        if party_ec3_document:
            ec3_missing_reason = ""
            data = {
                "type": PartyDocumentType.END_USER_EC3_DOCUMENT,
                "name": getattr(party_ec3_document, "name"),
                "s3_key": party_ec3_document.name,
                "size": int(party_ec3_document.size // 1024) if party_ec3_document.size else 0,  # in kilobytes
            }
            response, status_code = post_party_document(self.request, self.application_id, self.party_id, data)
            if status_code != HTTPStatus.CREATED:
                log.error(
                    "Error uploading EC3 document - response was: %s - %s",
                    status_code,
                    response,
                    exc_info=True,
                )
                return error_page(self.request, "Unexpected error uploading EC3 document")

        data = {"ec3_missing_reason": ec3_missing_reason}
        update_party(self.request, self.application_id, self.party_id, data)

        return super().form_valid(form)

    def get_success_url(self):
        return reverse("applications:end_user_summary", kwargs=self.kwargs)
