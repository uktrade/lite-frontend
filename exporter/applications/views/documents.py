import logging
from http import HTTPStatus
from inspect import signature

from django.conf import settings
from django.shortcuts import redirect
from django.urls import reverse, NoReverseMatch
from django.views.generic import TemplateView

from caseworker.cases.services import get_document
from core.file_handler import s3_client
from exporter.applications.forms.documents import attach_document_form, delete_document_confirmation_form
from exporter.applications.helpers.check_your_answers import is_application_export_type_permanent
from exporter.applications.services import (
    add_document_data,
    download_document_from_s3,
    get_application,
    post_party_document,
    get_party_document,
    delete_party_document,
    post_additional_document,
    get_additional_document,
    delete_additional_document,
    post_goods_type_document,
    get_goods_type_document,
    delete_goods_type_document,
)
from lite_content.lite_exporter_frontend import strings
from lite_forms.generators import form_page, error_page

from core.auth.views import LoginRequiredMixin


def document_switch(path):
    if "ultimate-end-user" in path:
        return {
            "optional": True,
            "attach": post_party_document,
            "download": get_party_document,
            "delete": delete_party_document,
            "homepage": "applications:ultimate_end_users",
            "strings": strings.UltimateEndUser.Documents.AttachDocuments,
        }
    elif "end-user" in path:
        return {
            "optional": True,
            "attach": post_party_document,
            "download": get_party_document,
            "delete": delete_party_document,
            "homepage": "applications:end_user",
            "strings": strings.EndUser.Documents.AttachDocuments,
        }
    elif "consignee" in path:
        return {
            "optional": True,
            "attach": post_party_document,
            "download": get_party_document,
            "delete": delete_party_document,
            "homepage": "applications:consignee",
            "strings": strings.Consignee.Documents.AttachDocuments,
        }
    elif "third-parties" in path:
        return {
            "optional": True,
            "attach": post_party_document,
            "download": get_party_document,
            "delete": delete_party_document,
            "homepage": "applications:third_parties",
            "strings": strings.ThirdParties.Documents.AttachDocuments,
        }
    elif "additional-document" in path:
        return {
            "optional": False,
            "attach": post_additional_document,
            "download": get_additional_document,
            "delete": delete_additional_document,
            "homepage": "applications:additional_documents",
            "strings": strings.AdditionalDocuments.Documents.AttachDocuments,
        }
    elif "goods-types" in path:
        return {
            "optional": True,
            "attach": post_goods_type_document,
            "download": get_goods_type_document,
            "delete": delete_goods_type_document,
            "homepage": "applications:goods_types",
            "strings": strings.Goods.Documents.AttachDocuments,
        }
    else:
        raise NotImplementedError("document_switch doesn't support this document type")


def get_upload_page(path, draft_id, is_permanent_application=False):
    paths = document_switch(path=path)
    is_document_optional = paths["optional"]
    # For standard permanent only - upload is mandatory
    if "/end-user" in path and is_permanent_application:
        is_document_optional = False
    return attach_document_form(
        application_id=draft_id, strings=paths["strings"], back_link=paths["homepage"], is_optional=is_document_optional
    )


def get_homepage(request, draft_id, obj_pk=None):
    data = {"pk": draft_id}
    if obj_pk:
        data["obj_pk"] = obj_pk

    try:
        url = reverse(document_switch(request.path)["homepage"], kwargs=data)
    except NoReverseMatch:
        url = reverse(document_switch(request.path)["homepage"], kwargs={"pk": draft_id})
    return redirect(url)


def get_delete_confirmation_page(path, pk):
    paths = document_switch(path)
    return delete_document_confirmation_form(
        overview_url=reverse(paths["homepage"], kwargs={"pk": pk}),
        strings=paths["strings"],
    )


class AttachDocuments(LoginRequiredMixin, TemplateView):
    def get(self, request, **kwargs):
        draft_id = str(kwargs["pk"])
        form = get_upload_page(request.path, draft_id)
        return form_page(request, form, extra_data={"draft_id": draft_id})

    def post(self, request, **kwargs):
        draft_id = str(kwargs["pk"])
        application = get_application(request, draft_id)
        is_permanent_application = is_application_export_type_permanent(application)
        form = get_upload_page(request.path, draft_id, is_permanent_application=is_permanent_application)

        try:
            files = request.FILES
        except Exception:  # noqa
            return error_page(request, strings.applications.AttachDocumentPage.UPLOAD_FAILURE_ERROR)

        # Only validate documents if there are any present or are mandatory in the following cases:
        # standard permanent application end user section, additional documents section
        if (
            files
            or ("/end-user" in request.path and is_application_export_type_permanent(application))
            or "additional-document" in request.path
        ):
            logging.info(self.request)
            data, error = add_document_data(request)

            if error:
                return form_page(request, form, extra_data={"draft_id": draft_id}, errors={"documents": [error]})

            action = document_switch(request.path)["attach"]
            if len(signature(action).parameters) == 3:
                _, status_code = action(request, draft_id, data)
                if status_code == HTTPStatus.CREATED:
                    return get_homepage(request, draft_id)
            else:
                _, status_code = action(request, draft_id, kwargs["obj_pk"], data)
                if status_code == HTTPStatus.CREATED:
                    return get_homepage(request, draft_id, kwargs["obj_pk"])

            return error_page(request, strings.applications.AttachDocumentPage.UPLOAD_FAILURE_ERROR)

        return get_homepage(request, draft_id)


class DownloadDocument(LoginRequiredMixin, TemplateView):
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
            return error_page(request, strings.applications.AttachDocumentPage.DOWNLOAD_GENERIC_ERROR)


class DownloadGeneratedDocument(LoginRequiredMixin, TemplateView):
    def get(self, request, case_pk, document_pk):
        document, _ = get_document(request, pk=document_pk)
        client = s3_client()
        signed_url = client.generate_presigned_url(
            "get_object",
            Params={
                "Bucket": settings.AWS_STORAGE_BUCKET_NAME,
                "Key": document["document"]["s3_key"],
            },
            ExpiresIn=15,
        )
        return redirect(signed_url)


class DeleteDocument(LoginRequiredMixin, TemplateView):
    def get(self, request, **kwargs):
        return form_page(request, get_delete_confirmation_page(request.path, str(kwargs["pk"])))

    def post(self, request, **kwargs):
        draft_id = str(kwargs["pk"])
        option = request.POST.get("delete_document_confirmation")
        if option is None:
            return form_page(
                request,
                get_delete_confirmation_page(request.path, str(kwargs["pk"])),
                errors={"delete_document_confirmation": ["Select yes to confirm you want to delete the document"]},
            )
        else:
            if option == "yes":
                action = document_switch(request.path)["delete"]

                if len(signature(action).parameters) == 2:
                    status_code = action(request, draft_id)
                else:
                    status_code = action(request, draft_id, kwargs["obj_pk"])

                if status_code == HTTPStatus.NO_CONTENT:
                    return get_homepage(request, draft_id)
                else:
                    return error_page(request, strings.applications.DeleteDocument.DOCUMENT_DELETE_GENERIC_ERROR)
            else:
                return get_homepage(request, draft_id)
