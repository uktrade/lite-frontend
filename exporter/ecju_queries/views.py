from http import HTTPStatus

from django.shortcuts import redirect, render
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from s3chunkuploader.file_handler import S3FileUploadHandler

from exporter.applications.services import add_document_data, download_document_from_s3
from exporter.ecju_queries.forms import (
    respond_to_query_form,
    ecju_query_respond_confirmation_form,
    document_grading_form,
    upload_documents_form,
)
from exporter.ecju_queries.services import (
    get_ecju_query,
    put_ecju_query,
    post_ecju_query_document_sensitivity,
    post_ecju_query_document,
    get_ecju_query_document,
    get_ecju_query_documents,
)
from exporter.goods.services import get_good
from lite_content.lite_exporter_frontend import strings, ecju_queries
from lite_forms.components import HiddenField, BackLink
from lite_forms.generators import form_page, error_page
from lite_forms.views import SingleFormView

from core.auth.views import LoginRequiredMixin


class RespondToQuery(LoginRequiredMixin, TemplateView):
    object_type = None
    case_id = None
    ecju_query_id = None
    ecju_query = None
    extra_id = None
    back_link = None

    def dispatch(self, request, *args, **kwargs):
        self.case_id = str(kwargs["case_pk"])
        self.object_type = kwargs["object_type"]
        self.ecju_query_id = str(kwargs["query_pk"])
        self.ecju_query = get_ecju_query(request, self.case_id, self.ecju_query_id)

        if self.object_type == "good":
            self.extra_id = kwargs["extra_pk"]
            good, _ = get_good(request, self.extra_id, full_detail=True)
            self.case_id = good["case_id"]
            self.ecju_query = get_ecju_query(request, self.case_id, self.ecju_query_id)

        if self.object_type == "application":
            self.back_link = reverse_lazy(
                "applications:application", kwargs={"pk": self.case_id, "type": "ecju-queries"}
            )
        elif self.object_type == "good":
            self.back_link = reverse_lazy("goods:good_detail", kwargs={"pk": self.extra_id, "type": "ecju-queries"})
        elif self.object_type == "end-user-advisory":
            self.back_link = reverse_lazy(
                "end_users:end_user_detail", kwargs={"pk": self.case_id, "type": "ecju-queries"}
            )
        elif self.object_type == "compliance-site":
            self.back_link = reverse_lazy(
                "compliance:compliance_site_details", kwargs={"pk": self.case_id, "tab": "ecju-queries"}
            )
        elif self.object_type == "compliance-visit":
            self.extra_id = kwargs["extra_pk"]
            self.back_link = reverse_lazy(
                "compliance:compliance_visit_details",
                kwargs={"site_case_id": self.extra_id, "pk": self.case_id, "tab": "ecju-queries"},
            )

        if self.ecju_query["response"]:
            return redirect(self.back_link)

        return super(RespondToQuery, self).dispatch(request, *args, **kwargs)

    def get(self, request, **kwargs):
        """
        Will get a text area form for the user to respond to the ecju_query
        """
        documents = get_ecju_query_documents(request, self.case_id, self.ecju_query_id)
        context = {
            "case_id": self.case_id,
            "ecju_query": self.ecju_query,
            "object_type": self.object_type,
            "back_link": self.back_link,
            "documents": documents,
        }

        return render(request, "ecju-queries/respond_to_query.html", context)

    def post(self, request, **kwargs):
        """
        will determine what form the user is on:
        if the user is on the input form will then will determine if data is valid, and move user to confirmation form
        else will allow the user to confirm they wish to respond and post data if accepted.
        """
        form_name = request.POST.get("form_name")

        if form_name == "respond_to_query":
            # Post the form data to API for validation only
            data = {"response": request.POST.get("response"), "validate_only": True}
            response, status_code = put_ecju_query(request, self.case_id, self.ecju_query_id, data)

            if status_code != HTTPStatus.OK:
                errors = response.get("errors")
                errors = {error: message for error, message in errors.items()}
                form = respond_to_query_form(self.back_link, self.ecju_query)
                data = {"response": request.POST.get("response")}
                return form_page(request, form, data=data, errors=errors)
            else:
                form = ecju_query_respond_confirmation_form(self.request.path_info)
                form.questions.append(HiddenField("response", request.POST.get("response")))
                return form_page(request, form)
        elif form_name == "ecju_query_response_confirmation":
            if request.POST.get("confirm_response") == "yes":
                data, status_code = put_ecju_query(request, self.case_id, self.ecju_query_id, request.POST)

                if "errors" in data:
                    return form_page(
                        request,
                        respond_to_query_form(self.back_link, self.ecju_query),
                        data=request.POST,
                        errors=data["errors"],
                    )

                return redirect(self.back_link)
            elif request.POST.get("confirm_response") == "no":
                return form_page(request, respond_to_query_form(self.back_link, self.ecju_query), data=request.POST)
            else:
                error = {"required": ["This field is required"]}
                form = ecju_query_respond_confirmation_form(self.request.path_info)
                form.questions.append(HiddenField("response", request.POST.get("response")))
                return form_page(request, form, errors=error)
        else:
            # Submitted data does not contain an expected form field - return an error
            return error_page(request, strings.applications.AttachDocumentPage.UPLOAD_GENERIC_ERROR)


class CheckDocumentGrading(LoginRequiredMixin, TemplateView):
    case_pk = None
    query_pk = None
    back_link = None

    def dispatch(self, request, *args, **kwargs):
        self.case_pk = kwargs["case_pk"]
        self.query_pk = kwargs["query_pk"]
        self.back_link = reverse_lazy(
            "ecju_queries:respond_to_query",
            kwargs={"query_pk": self.query_pk, "object_type": "application", "case_pk": self.case_pk},
        )
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, **kwargs):
        form = document_grading_form(request, self.back_link)
        return form_page(request, form, extra_data={"case_pk": self.case_pk, "query_pk": self.query_pk})

    def post(self, request, **kwargs):
        request_data = request.POST
        document_available = request_data.get("has_document_to_upload") == "yes"
        response, status_code = post_ecju_query_document_sensitivity(request, self.case_pk, self.query_pk, request_data)
        upload_doc_link = reverse_lazy(
            "ecju_queries:upload_document",
            kwargs={"case_pk": self.case_pk, "query_pk": self.query_pk, "object_type": "application"},
        )

        if status_code == HTTPStatus.OK:
            return redirect(upload_doc_link) if document_available else redirect(self.back_link)
        else:
            form = document_grading_form(request, self.back_link)
            return form_page(request, form, data=request_data, errors=response["errors"])


@method_decorator(csrf_exempt, "dispatch")
class UploadDocuments(LoginRequiredMixin, TemplateView):
    def get(self, request, **kwargs):
        self.case_pk = str(kwargs["case_pk"])
        self.object_type = kwargs["object_type"]
        self.query_pk = str(kwargs["query_pk"])

        self.back_link = BackLink(
            ecju_queries.UploadDocumentForm.BACK_FORM_LINK,
            reverse_lazy(
                "ecju_queries:add_supporting_document",
                kwargs={"query_pk": self.query_pk, "object_type": "application", "case_pk": self.case_pk},
            ),
        )
        form = upload_documents_form(self.back_link)
        return form_page(request, form, extra_data={"case_id": self.case_pk, "ecju_query_id": self.query_pk})

    @csrf_exempt
    def post(self, request, **kwargs):
        self.request.upload_handlers.insert(0, S3FileUploadHandler(request))

        self.case_pk = str(kwargs["case_pk"])
        self.object_type = kwargs["object_type"]
        self.query_pk = str(kwargs["query_pk"])

        data, error = add_document_data(request)
        if error:
            return error_page(request, error)

        data, status_code = post_ecju_query_document(request, self.case_pk, self.query_pk, data)
        if status_code != HTTPStatus.CREATED:
            return error_page(request, data["errors"]["file"])

        return redirect(reverse("applications:application", kwargs={"pk": self.case_pk, "type": "ecju-queries"}))


class QueryDocument(LoginRequiredMixin, TemplateView):
    def get(self, request, **kwargs):
        self.object_type = kwargs["object_type"]
        self.case_pk = str(kwargs["case_pk"])
        self.query_pk = str(kwargs["query_pk"])
        self.doc_pk = str(kwargs["doc_pk"])

        document = get_ecju_query_document(request, self.case_pk, self.query_pk, self.doc_pk)
        return download_document_from_s3(document["s3_key"], document["name"])


class QueryDocumentDelete(LoginRequiredMixin, TemplateView):
    pass
