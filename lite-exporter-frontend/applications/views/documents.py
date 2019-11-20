import logging
from inspect import signature

from django.shortcuts import redirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from s3chunkuploader.file_handler import S3FileUploadHandler

from applications.forms.end_user import attach_document_form, delete_document_confirmation_form
from applications.helpers.reverse_documents import document_switch
from applications.services import add_document_data, download_document_from_s3
from core.builtins.custom_tags import get_string
from lite_forms.generators import form_page, error_page


def get_upload_page(path, draft_id):
    paths = document_switch(path)

    if paths["has_description"]:
        description_text = get_string(paths["strings"] + ".attach_documents.description_field_title")
    else:
        description_text = None

    return attach_document_form(
        application_id=draft_id,
        title=get_string(paths["strings"] + ".attach_documents.title"),
        return_later_text=get_string(paths["strings"] + ".save_end_user"),
        description_text=description_text,
    )


def get_homepage(request, draft_id):
    return redirect(reverse(document_switch(request.path)["homepage"], kwargs={"pk": draft_id}))


def get_delete_confirmation_page(path, pk):
    paths = document_switch(path)
    return delete_document_confirmation_form(
        overview_url=reverse(paths["homepage"], kwargs={"pk": pk}),
        back_link_text=get_string(paths["strings"] + ".attach_documents.back_to_application_overview"),
    )


@method_decorator(csrf_exempt, "dispatch")
class AttachDocuments(TemplateView):
    def get(self, request, **kwargs):
        draft_id = str(kwargs["pk"])
        form = get_upload_page(request.path, draft_id)
        return form_page(request, form, extra_data={"draft_id": draft_id})

    @csrf_exempt
    def post(self, request, **kwargs):
        draft_id = str(kwargs["pk"])
        form = get_upload_page(request.path, draft_id)
        self.request.upload_handlers.insert(0, S3FileUploadHandler(request))

        if not request.FILES:
            return form_page(
                request, form, extra_data={"draft_id": draft_id}, errors={"documents": ["Select a file to upload"]}
            )

        logging.info(self.request)
        draft_id = str(kwargs["pk"])
        data, error = add_document_data(request)

        if error:
            return error_page(None, get_string("end_user.documents.attach_documents.upload_error"))

        action = document_switch(request.path)["attach"]
        if len(signature(action).parameters) == 3:
            _, status_code = action(request, draft_id, data)
        else:
            _, status_code = action(request, draft_id, kwargs["obj_pk"], data)

        if status_code == 201:
            return get_homepage(request, draft_id)
        else:
            return error_page(None, get_string("end_user.documents.attach_documents.upload_error"))


class DownloadDocument(TemplateView):
    def get(self, request, **kwargs):
        draft_id = str(kwargs["pk"])
        action = document_switch(request.path)["download"]

        if len(signature(action).parameters) == 2:
            document, _ = action(request, draft_id)
        else:
            document, _ = action(request, draft_id, kwargs["obj_pk"])

        document = document["document"]
        if document["safe"]:
            return download_document_from_s3(document["s3_key"], document["name"])
        else:
            return error_page(None, get_string("end_user.documents.attach_documents.download_error"))


class DeleteDocument(TemplateView):
    def get(self, request, **kwargs):
        return form_page(request, get_delete_confirmation_page(request.path, str(kwargs["pk"])))

    def post(self, request, **kwargs):
        draft_id = str(kwargs["pk"])
        option = request.POST.get("delete_document_confirmation")
        if option is None:
            return form_page(
                request,
                get_delete_confirmation_page(request.path, str(kwargs["pk"])),
                errors={"delete_document_confirmation": ["This field is required"]},
            )
        else:
            if option == "yes":
                action = document_switch(request.path)["delete"]

                if len(signature(action).parameters) == 2:
                    status_code = action(request, draft_id)
                else:
                    status_code = action(request, draft_id, kwargs["obj_pk"])

                if status_code == 204:
                    return get_homepage(request, draft_id)
                else:
                    return error_page(None, get_string("end_user.documents.attach_documents.delete_error"))
            else:
                return get_homepage(request, draft_id)
