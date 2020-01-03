from http import HTTPStatus

from django.http import Http404
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from s3chunkuploader.file_handler import S3FileUploadHandler

from applications.services import (
    get_application_ecju_queries,
    get_case_notes,
    post_application_case_notes,
    get_ecju_query,
    put_ecju_query,
    add_document_data,
    download_document_from_s3,
    get_status_properties,
)
from core.helpers import convert_dict_to_query_params
from goods import forms
from goods.forms import (
    edit_form,
    attach_documents_form,
    respond_to_query_form,
    ecju_query_respond_confirmation_form,
    delete_good_form,
    add_goods_questions,
    document_grading_form,
)
from goods.services import (
    get_goods,
    post_goods,
    get_good,
    update_good,
    delete_good,
    get_good_documents,
    get_good_document,
    delete_good_document,
    post_good_documents,
    raise_clc_query,
    post_good_document_sensitivity,
)
from lite_content.lite_exporter_frontend import strings
from lite_forms.components import HiddenField
from lite_forms.generators import error_page, form_page
from lite_forms.views import SingleFormView


class Goods(TemplateView):
    def get(self, request, **kwargs):
        description = request.GET.get("description", "").strip()
        part_number = request.GET.get("part_number", "").strip()
        control_rating = request.GET.get("control_rating", "").strip()

        filtered = True if (description or part_number or control_rating) else False

        params = {
            "page": int(request.GET.get("page", 1)),
            "description": description,
            "part_number": part_number,
            "control_rating": control_rating,
        }

        goods = get_goods(request, **params)

        context = {
            "goods": goods,
            "description": description,
            "part_number": part_number,
            "control_code": control_rating,
            "filtered": filtered,
            "params": params,
            "page": params.pop("page"),
            "params_str": convert_dict_to_query_params(params),
        }
        return render(request, "goods/goods.html", context)


class GoodsDetailEmpty(TemplateView):
    def get(self, request, **kwargs):
        return redirect(reverse_lazy("goods:good_detail", kwargs={"pk": kwargs["pk"], "type": "case-notes"}))


class GoodsDetail(TemplateView):
    good_id = None
    good = None
    view_type = None

    def dispatch(self, request, *args, **kwargs):
        self.good_id = str(kwargs["pk"])
        self.good = get_good(request, self.good_id)[0]
        self.view_type = kwargs["type"]

        if self.view_type != "case-notes" and self.view_type != "ecju-queries":
            return Http404

        return super(GoodsDetail, self).dispatch(request, *args, **kwargs)

    def get(self, request, **kwargs):
        documents = get_good_documents(request, str(self.good_id))

        context = {
            "good": self.good,
            "documents": documents,
            "type": self.view_type,
        }

        if self.good["query"]:
            status_props, _ = get_status_properties(request, self.good["case_status"]["key"])
            context["status_is_read_only"] = status_props["is_read_only"]
            context["status_is_terminal"] = status_props["is_terminal"]

        if self.view_type == "case-notes":
            if self.good.get("case_id"):
                case_notes = get_case_notes(request, self.good["case_id"])["case_notes"]
                context["notes"] = filter(lambda note: note["is_visible_to_exporter"], case_notes)

        if self.view_type == "ecju-queries":
            context["open_queries"], context["closed_queries"] = get_application_ecju_queries(
                request, self.good["case_id"]
            )

        return render(request, "goods/good.html", context)

    def post(self, request, **kwargs):
        if self.view_type != "case-notes":
            return Http404

        good_id = kwargs["pk"]
        data, _ = get_good(request, str(good_id))

        response, _ = post_application_case_notes(request, data["case_id"], request.POST)

        if "errors" in response:
            errors = response.get("errors")
            if errors.get("text"):
                error = errors.get("text")[0]
                error = error.replace("This field", "Case note")
                error = error.replace("this field", "the case note")  # TODO: Move to API

            else:
                error_list = []
                for key in errors:
                    error_list.append("{field}: {error}".format(field=key, error=errors[key][0]))
                error = "\n".join(error_list)
            return error_page(request, error)

        return redirect(reverse_lazy("goods:good_detail", kwargs={"pk": good_id, "type": "case-notes"}))


class AddGood(SingleFormView):
    def init(self, request, **kwargs):
        self.form = add_goods_questions()
        self.action = post_goods

    def get_success_url(self):
        return reverse_lazy("goods:add_document", kwargs={"pk": self.get_validated_data()["good"]["id"]})


class RaiseCLCQuery(TemplateView):
    def get(self, request, **kwargs):
        return form_page(request, forms.raise_a_clc_query(str(kwargs["pk"])))

    def post(self, request, **kwargs):
        good_id = str(kwargs["pk"])
        request_data = request.POST.copy()
        request_data["good_id"] = good_id

        data, _ = raise_clc_query(request, request_data)

        if "errors" in data:
            return form_page(
                request, forms.raise_a_clc_query(str(kwargs["pk"])), data=request_data, errors=data["errors"]
            )

        return redirect(reverse("goods:goods"))


class DraftAddGood(TemplateView):
    def get(self, request, **kwargs):
        return form_page(request, forms.form)

    def post(self, request, **kwargs):
        data, status_code = post_goods(request, request.POST)

        if status_code == HTTPStatus.BAD_REQUEST:
            return form_page(request, forms.form, request.POST, errors=data["errors"])

        return redirect(reverse_lazy("applications:task_list"), kwargs["pk"])


class EditGood(TemplateView):
    good_id = None
    form = None

    def dispatch(self, request, *args, **kwargs):
        self.good_id = str(kwargs["pk"])
        self.form = edit_form(self.good_id)
        return super(EditGood, self).dispatch(request, *args, **kwargs)

    def get(self, request, **kwargs):
        data, _ = get_good(request, self.good_id)
        return form_page(request, self.form, data)

    def post(self, request, **kwargs):
        data, status_code = update_good(request, self.good_id, request.POST)

        if status_code == 400:
            return form_page(request, self.form, request.POST, errors=data["errors"])

        return redirect(reverse_lazy("goods:good", kwargs={"pk": self.good_id}))


class DeleteGood(TemplateView):
    def get(self, request, **kwargs):
        data, _ = get_good(request, str(kwargs["pk"]))
        return form_page(request, delete_good_form(data))

    def post(self, request, **kwargs):
        delete_good(request, str(kwargs["pk"]))
        return redirect(reverse_lazy("goods:goods"))


class CheckDocumentGrading(SingleFormView):
    def init(self, request, **kwargs):
        self.object_pk = kwargs["pk"]
        self.form = document_grading_form(request)
        self.action = post_good_document_sensitivity

    def get_success_url(self):
        good = self.get_validated_data()["good"]
        if good["missing_document_reason"]:
            url = "goods:good"
        else:
            url = "goods:attach_documents"
        return reverse_lazy(url, kwargs={"pk": self.object_pk})


@method_decorator(csrf_exempt, "dispatch")
class AttachDocuments(TemplateView):
    def get(self, request, **kwargs):
        good_id = str(kwargs["pk"])
        # get_good(request, good_id)

        form = attach_documents_form(reverse("goods:good", kwargs={"pk": good_id}))

        return form_page(request, form, extra_data={"good_id": good_id})

    @csrf_exempt
    def post(self, request, **kwargs):
        self.request.upload_handlers.insert(0, S3FileUploadHandler(request))

        good_id = str(kwargs["pk"])
        good, _ = get_good(request, good_id)

        data, error = add_document_data(request)

        if error:
            return error_page(request, error)

        if "description" not in data:
            data["description"] = ""
        data = [data]

        # Send LITE API the file information
        good_documents, _ = post_good_documents(request, good_id, data)

        if "errors" in good_documents:
            return error_page(request, strings.goods.AttachDocumentPage.UPLOAD_FAILURE_ERROR)

        if good["is_good_controlled"] == "unsure":
            return redirect(reverse("goods:raise_clc_query", kwargs={"pk": good_id}))

        return redirect(reverse("goods:good", kwargs={"pk": good_id}))


class Document(TemplateView):
    def get(self, request, **kwargs):
        good_id = str(kwargs["pk"])
        file_pk = str(kwargs["file_pk"])

        document = get_good_document(request, good_id, file_pk)
        return download_document_from_s3(document["s3_key"], document["name"])


class DeleteDocument(TemplateView):
    def get(self, request, **kwargs):
        good_id = str(kwargs["pk"])
        file_pk = str(kwargs["file_pk"])

        good, _ = get_good(request, good_id)
        document = get_good_document(request, good_id, file_pk)
        original_file_name = document["name"]

        context = {
            "title": "Are you sure you want to delete this file?",
            "description": original_file_name,
            "good": good,
            "document": document,
        }
        return render(request, "goods/delete-document.html", context)

    def post(self, request, **kwargs):
        good_id = str(kwargs["pk"])
        file_pk = str(kwargs["file_pk"])

        _, _ = get_good(request, good_id)
        _ = get_good_document(request, good_id, file_pk)  # noqa
        # Delete the file on the API
        delete_good_document(request, good_id, file_pk)

        return redirect(reverse("goods:good", kwargs={"pk": good_id}))


class RespondToQuery(TemplateView):
    good_id = None
    ecju_query_id = None
    ecju_query = None
    clc_query_case_id = None

    def dispatch(self, request, *args, **kwargs):
        self.good_id = str(kwargs["pk"])
        self.ecju_query_id = str(kwargs["query_pk"])

        good, _ = get_good(request, self.good_id)
        self.clc_query_case_id = good["case_id"]
        self.ecju_query = get_ecju_query(request, self.clc_query_case_id, self.ecju_query_id)

        if self.ecju_query["response"]:
            return redirect(reverse_lazy("goods:good_detail", kwargs={"pk": self.good_id, "type": "ecju-queries"}))

        return super(RespondToQuery, self).dispatch(request, *args, **kwargs)

    def get(self, request, **kwargs):
        """
        Will get a text area form for the user to respond to the ecju_query
        """

        return form_page(request, respond_to_query_form(self.good_id, self.ecju_query))

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
            response, status_code = put_ecju_query(request, self.clc_query_case_id, self.ecju_query_id, data)

            if status_code != 200:
                errors = response.get("errors")
                errors = {error: message for error, message in errors.items()}
                form = respond_to_query_form(self.clc_query_case_id, self.ecju_query)
                data = {"response": request.POST.get("response")}
                return form_page(request, form, data=data, errors=errors)
            else:
                form = ecju_query_respond_confirmation_form(
                    reverse_lazy("goods:respond_to_query", kwargs={"pk": self.good_id, "query_pk": self.ecju_query_id})
                )
                form.questions.append(HiddenField("response", request.POST.get("response")))
                return form_page(request, form)
        elif form_name == "ecju_query_response_confirmation":
            if request.POST.get("confirm_response") == "yes":
                data, status_code = put_ecju_query(request, self.clc_query_case_id, self.ecju_query_id, request.POST)
                if "errors" in data:
                    return form_page(
                        request,
                        respond_to_query_form(self.good_id, self.ecju_query),
                        data=request.POST,
                        errors=data["errors"],
                    )

                return redirect(reverse_lazy("goods:good_detail", kwargs={"pk": self.good_id, "type": "ecju-queries"}))

            elif request.POST.get("confirm_response") == "no":
                return form_page(
                    request, respond_to_query_form(self.clc_query_case_id, self.ecju_query), data=request.POST
                )
            else:
                error = {"required": ["This field is required"]}
                form = ecju_query_respond_confirmation_form(
                    reverse_lazy("goods:respond_to_query", kwargs={"pk": self.good_id, "query_pk": self.ecju_query_id})
                )
                form.questions.append(HiddenField("response", request.POST.get("response")))
                return form_page(request, form, errors=error)
        else:
            # Submitted data does not contain an expected form field - return an error
            return error_page(request, strings.goods.AttachDocumentPage.UPLOAD_GENERIC_ERROR)
