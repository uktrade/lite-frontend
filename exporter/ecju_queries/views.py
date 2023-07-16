from http import HTTPStatus

from django.shortcuts import redirect, render
from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView

from core.file_handler import download_document_from_s3

from exporter.applications.services import add_document_data
from exporter.ecju_queries.forms import (
    respond_to_query_form,
    ecju_query_respond_confirmation_form,
    upload_documents_form,
)
from exporter.ecju_queries.services import (
    get_ecju_query,
    put_ecju_query,
    post_ecju_query_document,
    get_ecju_query_document,
    get_ecju_query_documents,
    delete_ecju_query_document,
)
from exporter.goods.services import get_good
from lite_content.lite_exporter_frontend import strings, ecju_queries
from lite_forms.components import HiddenField, BackLink
from lite_forms.generators import form_page, error_page

from core.auth.views import LoginRequiredMixin


class RespondToQuery(LoginRequiredMixin, TemplateView):
    object_type = None
    case_id = None
    ecju_query_id = None
    ecju_query = None
    extra_id = None
    back_link = None
    response = ""

    def dispatch(self, request, *args, **kwargs):
        self.case_id = str(kwargs["case_pk"])
        self.object_type = kwargs["object_type"]
        self.ecju_query_id = str(kwargs["query_pk"])
        self.ecju_query = get_ecju_query(request, self.case_id, self.ecju_query_id)
        self.extra_id = kwargs.get("extra_pk")

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
        if "response" in request.session.keys():
            self.response = request.session["response"]

        documents = get_ecju_query_documents(request, self.case_id, self.ecju_query_id)
        context = {
            "case_id": self.case_id,
            "ecju_query": self.ecju_query,
            "object_type": self.object_type,
            "extra_id": self.extra_id,
            "back_link": self.back_link,
            "response": self.response,
            "documents": documents,
        }

        return render(request, "ecju-queries/respond_to_query.html", context)

    def post(self, request, **kwargs):
        """
        will determine what form the user is on:
        if the user is on the input form will then will determine if data is valid, and move user to confirmation form
        else will allow the user to confirm they wish to respond and post data if accepted.
        """

        request_data = request.POST
        self.response = request_data.get("response")

        # if Attach document is clicked
        if request_data.get("respond_to_query") == "add_document":
            request.session["response"] = self.response
            return redirect(
                reverse(
                    "ecju_queries:add_supporting_document",
                    kwargs={
                        "query_pk": self.ecju_query_id,
                        "object_type": self.object_type,
                        "case_pk": self.case_id,
                        "extra_pk": self.extra_id if self.extra_id else self.case_id,
                    },
                )
            )

        documents = get_ecju_query_documents(request, self.case_id, self.ecju_query_id)
        context = {
            "case_id": self.case_id,
            "ecju_query": self.ecju_query,
            "object_type": self.object_type,
            "back_link": self.back_link,
            "extra_id": self.extra_id,
            "documents": documents,
        }
        form_name = request.POST.get("form_name")

        if "respond_to_query" in request.POST:
            # Post the form data to API for validation only
            data = {"response": request.POST.get("response"), "validate_only": True}
            response, status_code = put_ecju_query(request, self.case_id, self.ecju_query_id, data)

            if status_code != HTTPStatus.OK:
                errors = response.get("errors")
                context["errors"] = {error: message[0] for error, message in errors.items()}
                return render(request, "ecju-queries/respond_to_query.html", context)
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

                if "response" in request.session.keys():
                    del request.session["response"]

                return redirect(self.back_link)
            elif request.POST.get("confirm_response") == "no":
                context["response"] = request.POST.get("response")
                return render(request, "ecju-queries/respond_to_query.html", context)
            else:
                error = {"required": ["This field is required"]}
                form = ecju_query_respond_confirmation_form(self.request.path_info)
                form.questions.append(HiddenField("response", request.POST.get("response")))
                return form_page(request, form, errors=error)
        else:
            # Submitted data does not contain an expected form field - return an error
            return error_page(request, strings.applications.AttachDocumentPage.UPLOAD_GENERIC_ERROR)


class UploadDocuments(LoginRequiredMixin, TemplateView):
    def dispatch(self, request, *args, **kwargs):
        self.case_pk = kwargs["case_pk"]
        self.query_pk = kwargs["query_pk"]
        self.object_type = kwargs["object_type"]
        self.extra_pk = kwargs["extra_pk"]

        if self.object_type == "compliance-visit":
            self.success_url = reverse(
                "ecju_queries:respond_to_query_extra",
                kwargs={
                    "query_pk": self.query_pk,
                    "object_type": self.object_type,
                    "case_pk": self.case_pk,
                    "extra_pk": self.extra_pk,
                },
            )
        else:
            self.success_url = reverse(
                "ecju_queries:respond_to_query",
                kwargs={"query_pk": self.query_pk, "object_type": self.object_type, "case_pk": self.case_pk},
            )

        return super().dispatch(request, *args, **kwargs)

    def get(self, request, **kwargs):
        self.back_link = BackLink(ecju_queries.UploadDocumentForm.BACK_FORM_LINK, self.success_url)
        form = upload_documents_form(self.back_link)
        return form_page(
            request,
            form,
            extra_data={"case_id": self.case_pk, "ecju_query_id": self.query_pk, "object_type": self.object_type},
        )

    def post(self, request, **kwargs):
        data, error = add_document_data(request)
        if error:
            return error_page(request, error)

        data, status_code = post_ecju_query_document(request, self.case_pk, self.query_pk, data)
        if status_code != HTTPStatus.CREATED:
            return error_page(request, data["errors"]["file"])

        return redirect(self.success_url)


class QueryDocument(LoginRequiredMixin, TemplateView):
    def get(self, request, **kwargs):
        self.object_type = kwargs["object_type"]
        self.case_pk = str(kwargs["case_pk"])
        self.query_pk = str(kwargs["query_pk"])
        self.doc_pk = str(kwargs["doc_pk"])

        document = get_ecju_query_document(request, self.case_pk, self.query_pk, self.doc_pk)
        return download_document_from_s3(document["s3_key"], document["name"])


class QueryDocumentDelete(LoginRequiredMixin, TemplateView):
    def dispatch(self, request, *args, **kwargs):
        self.object_type = kwargs["object_type"]
        self.case_pk = str(kwargs["case_pk"])
        self.query_pk = str(kwargs["query_pk"])
        self.extra_pk = str(kwargs["extra_pk"])
        self.doc_pk = str(kwargs["doc_pk"])

        if self.object_type == "compliance-visit":
            self.success_url = reverse(
                "ecju_queries:respond_to_query_extra",
                kwargs={
                    "query_pk": self.query_pk,
                    "object_type": self.object_type,
                    "case_pk": self.case_pk,
                    "extra_pk": self.extra_pk,
                },
            )
        else:
            self.success_url = reverse(
                "ecju_queries:respond_to_query",
                kwargs={"query_pk": self.query_pk, "object_type": self.object_type, "case_pk": self.case_pk},
            )

        return super().dispatch(request, *args, **kwargs)

    def get(self, request, **kwargs):
        document = get_ecju_query_document(request, self.case_pk, self.query_pk, self.doc_pk)
        context = {
            "object_type": self.object_type,
            "case_pk": self.case_pk,
            "query_pk": self.query_pk,
            "doc_pk": self.doc_pk,
            "extra_pk": self.extra_pk,
            "title": ecju_queries.SupportingDocumentDeletePage.TITLE,
            "document": document,
        }
        return render(request, "ecju-queries/query-document-delete.html", context)

    def post(self, request, **kwargs):
        delete_ecju_query_document(request, self.case_pk, self.query_pk, self.doc_pk)

        return redirect(self.success_url)
